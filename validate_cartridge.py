#!/usr/bin/env python3
"""Validate a Barton Command Center v2 cartridge.
Usage: python3 validate_cartridge.py path/to/lesson.json
Exits 0 if valid, 1 if errors found. Warnings don't fail the build.
"""
import json, os, re, sys

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

# Payload types the runtime consumes (initModeState in app.html).
LIST_PAYLOADS = {   # mode -> fields that must be arrays
    "word_frame": ["words"],
    "sight_words": ["words"],
    "fill_blanks": ["bank", "rows"],
    "sentences": ["items"],
    "matching": ["pairs"],
}

TOP_KEYS = {"schemaVersion", "meta", "materials", "objectives", "beats"}
BEAT_KEYS = {"id", "phase", "label", "say", "listen", "do", "board", "note",
             "media", "recovery"}
V1_BEAT_KEYS = {"type", "command", "payload", "steps", "mode"}  # dead v1 shape

PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|XXX|PLACEHOLDER|LOREM IPSUM)\b",
                         re.IGNORECASE)


def scan_placeholders(value, path, warnings):
    """Walk any JSON value and warn on placeholder markers in strings."""
    if isinstance(value, str):
        m = PLACEHOLDER.search(value)
        if m:
            warnings.append(f"{path} contains placeholder text {m.group(0)!r}.")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            scan_placeholders(v, f"{path}[{i}]", warnings)
    elif isinstance(value, dict):
        for k, v in value.items():
            scan_placeholders(v, f"{path}.{k}", warnings)

def validate(data):
    errors, warnings = [], []

    # v1/v2 mismatch: the runtime rejects anything without schemaVersion 2,
    # and the old v1 shape ({level, lesson, title, sections}) is unloadable.
    if isinstance(data, dict) and ("sections" in data or "steps" in data):
        errors.append("This is a v1 cartridge (has 'sections'/'steps'); "
                      "the runtime only loads v2 ({schemaVersion:2, meta, beats}).")
        return errors, warnings

    if data.get("schemaVersion") != 2:
        warnings.append("schemaVersion is not 2 (engine targets v2).")

    for k in sorted(set(data) - TOP_KEYS):
        warnings.append(f"Unknown top-level field {k!r} (runtime ignores it).")

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

        stale = V1_BEAT_KEYS & set(b)
        if stale:
            errors.append(f"{loc} ({bid}) has stale v1 field(s) {sorted(stale)} — "
                          "the v2 runtime does not read them.")
        for k in sorted(set(b) - BEAT_KEYS - V1_BEAT_KEYS):
            warnings.append(f"{loc} ({bid}) unknown field {k!r} (runtime ignores it).")

        say = b.get("say")
        if say is not None:
            if not isinstance(say, dict) or "text" not in say:
                errors.append(f"{loc} ({bid}) say must be an object with 'text'.")
            else:
                t = say["text"]
                ok = isinstance(t, str) or (
                    isinstance(t, list) and t and all(isinstance(x, str) for x in t))
                if not ok:
                    errors.append(f"{loc} ({bid}) say.text must be a string or "
                                  "non-empty array of strings.")

        listen = b.get("listen")
        if listen is not None:
            if not isinstance(listen, dict):
                errors.append(f"{loc} ({bid}) listen must be an object.")
            elif "expect" in listen and not isinstance(listen["expect"], list):
                errors.append(f"{loc} ({bid}) listen.expect must be an array.")

        for field in ("do", "note"):
            if field in b and not isinstance(b[field], str):
                errors.append(f"{loc} ({bid}) {field!r} must be a string.")

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
                                elif "row" in entry and not isinstance(entry["row"], int):
                                    errors.append(f"{loc} ({bid}) prePlace[{k}].row must be an int.")
                else:
                    for field in LIST_PAYLOADS.get(mode, []):
                        val = board.get(field)
                        if val is not None and not isinstance(val, list):
                            errors.append(f"{loc} ({bid}) board.{field} must be an array.")
                        elif isinstance(val, list) and not val:
                            warnings.append(f"{loc} ({bid}) board.{field} is empty — "
                                            "the student page will render blank.")
                    if mode == "phrase_builder":
                        cols = board.get("columns")
                        if cols is not None and (not isinstance(cols, dict) or
                                not all(isinstance(v, list) for v in cols.values())):
                            errors.append(f"{loc} ({bid}) phrase_builder.columns must be "
                                          "an object of arrays.")
                    if mode == "fill_blanks":
                        for k, row in enumerate(board.get("rows") or []):
                            if isinstance(row, str) and "___" not in row:
                                warnings.append(f"{loc} ({bid}) fill_blanks rows[{k}] "
                                                "has no '___' blank.")
                    if mode == "matching":
                        for k, pair in enumerate(board.get("pairs") or []):
                            if not (isinstance(pair, list) and len(pair) >= 2):
                                warnings.append(f"{loc} ({bid}) matching pairs[{k}] is not "
                                                "a [left, right] pair — runtime drops it.")
                    if mode == "story" and not (board.get("text") or "").strip():
                        errors.append(f"{loc} ({bid}) story.text is empty.")

        media = b.get("media")
        if isinstance(media, dict) and not media.get("source"):
            errors.append(f"{loc} ({bid}) media missing 'source'.")
        elif isinstance(media, dict) and not os.path.exists(media["source"]):
            warnings.append(f"{loc} ({bid}) media source {media['source']!r} not found "
                            "on disk (videos are gitignored; verify it ships with the app).")

        rec = b.get("recovery")
        if isinstance(rec, dict):
            rt = rec.get("reteach")
            if rt and rt not in all_ids:
                errors.append(f"{loc} ({bid}) recovery.reteach {rt!r} points to no existing beat id.")
            if not rec.get("prompts"):
                warnings.append(f"{loc} ({bid}) recovery has no prompts.")

    scan_placeholders(data, "cartridge", warnings)

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
