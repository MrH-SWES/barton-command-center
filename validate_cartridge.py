#!/usr/bin/env python3
"""Validate a Barton Command Center v2 cartridge.
Usage: python3 validate_cartridge.py path/to/lesson.json
Exits 0 if valid, 1 if errors found. Warnings don't fail the build.
"""
import json, sys

BOARD_MODES = {
    "clear": [],
    "tiles": [],   # all tiles fields optional; validated specially below
    "word_frame": ["words"],
    "phrase_builder": ["columns"],
    "fill_blanks": ["bank", "rows"],
    "sentences": ["items"],
    "story": ["title", "text"],
    "matching": ["pairs"],
    "sight_words": ["words"],
}

def validate(data):
    errors, warnings = [], []

    if data.get("schemaVersion") != 2:
        warnings.append("schemaVersion is not 2 (engine targets v2).")

    meta = data.get("meta")
    if not isinstance(meta, dict):
        errors.append("meta is required and must be an object.")
    else:
        if not meta.get("title"):
            errors.append("meta.title is required.")
        spd = meta.get("videoSpeedDefault", 1.5)
        if spd not in (1, 1.5, 2):
            warnings.append(f"meta.videoSpeedDefault {spd!r} is unusual (expected 1, 1.5, or 2).")

    beats = data.get("beats")
    if not isinstance(beats, list) or not beats:
        errors.append("beats must be a non-empty array.")
        return errors, warnings

    seen_ids, all_ids = set(), set()
    for b in beats:
        if isinstance(b, dict) and b.get("id"):
            all_ids.add(b["id"])

    for i, b in enumerate(beats):
        loc = f"beats[{i}]"
        if not isinstance(b, dict):
            errors.append(f"{loc} must be an object."); continue

        bid = b.get("id")
        if not bid:
            errors.append(f"{loc} missing required 'id'.")
        elif bid in seen_ids:
            errors.append(f"{loc} duplicate id {bid!r}.")
        else:
            seen_ids.add(bid)

        if not any(k in b for k in ("say", "do", "board", "note", "media", "listen")):
            warnings.append(f"{loc} ({bid}) is empty — no say/do/board/note/media/listen.")

        if "phase" not in b:
            warnings.append(f"{loc} ({bid}) has no 'phase' — it will show an unlabeled pill on the progress map.")

        board = b.get("board")
        if board is not None:
            mode = board.get("mode") if isinstance(board, dict) else None
            if mode not in BOARD_MODES:
                errors.append(f"{loc} ({bid}) board.mode {mode!r} is not a known mode.")
            else:
                for req in BOARD_MODES[mode]:
                    if req not in board:
                        errors.append(f"{loc} ({bid}) board mode {mode!r} missing field {req!r}.")
                if mode == "tiles":
                    lvl = board.get("level")
                    if lvl is not None and (not isinstance(lvl, int) or not (2 <= lvl <= 10)):
                        errors.append(f"{loc} ({bid}) tiles.level {lvl!r} must be an int 2-10.")
                    dr = board.get("openDrawer")
                    drawers = {"consonants","vowels","units","endings","prefixes","roots"}
                    if dr is not None and dr not in drawers:
                        errors.append(f"{loc} ({bid}) tiles.openDrawer {dr!r} not one of {sorted(drawers)}.")
                    pp = board.get("prePlace")
                    if pp is not None:
                        if not isinstance(pp, list):
                            errors.append(f"{loc} ({bid}) tiles.prePlace must be an array.")
                        else:
                            for k, entry in enumerate(pp):
                                if not isinstance(entry, dict) or not entry.get("word"):
                                    errors.append(f"{loc} ({bid}) prePlace[{k}] needs a 'word'.")

        media = b.get("media")
        if isinstance(media, dict) and not media.get("source"):
            errors.append(f"{loc} ({bid}) media missing 'source'.")

        rec = b.get("recovery")
        if isinstance(rec, dict):
            rt = rec.get("reteach")
            if rt and rt not in all_ids:
                errors.append(f"{loc} ({bid}) recovery.reteach {rt!r} points to no existing beat id.")
            if not rec.get("prompts"):
                warnings.append(f"{loc} ({bid}) recovery has no prompts.")

    return errors, warnings


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 validate_cartridge.py path/to/lesson.json"); sys.exit(2)
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}"); sys.exit(1)

    errors, warnings = validate(data)
    for w in warnings: print(f"⚠️  {w}")
    if errors:
        for e in errors: print(f"❌ {e}")
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s). INVALID.")
        sys.exit(1)
    print(f"✅ Valid cartridge. {len(warnings)} warning(s).")
    sys.exit(0)


if __name__ == "__main__":
    main()
