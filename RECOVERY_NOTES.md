# Recovery Notes — Barton Command Center

Status notes for the salvaged v2 working state. Written during the gated Fable
mission (see `prompts/fable_full_mission.md`), Phase 1. Facts below were derived
from the runtime and git history, not from memory.

## 1. Provenance

- GitHub `main` went stale; the real v2 app continued on a work laptop and was
  migrated via Drive.
- The recovered `.git` database was corrupt, so files were salvaged into a clean
  clone and pushed as branch **`recovered-drive-copy`**
  (commit `f068197 Recover v2 Barton Command Center from Drive migration`).
- `main` is an ancestor of `recovered-drive-copy` and is exactly **1 commit
  behind** it. Until a deliberate merge is authorized, `main` is stale —
  do not target it.

## 2. Branch strategy

| branch | role |
| --- | --- |
| `recovered-drive-copy` | authoritative salvaged base — do not rebase or rewrite |
| `phase-0a-fable-clean` | active working branch for the gated mission (this branch) |
| `main` | stale (pre-salvage); merge only when explicitly authorized |
| `copilot-fable-phase0-quarantine`, `fable-phase0`, `phase-0a-copilot-snapshot` | untrusted prior-attempt drafts — reference only, never merge |

## 3. Running the app

- `app.html` is the single-file v2 runtime. Opened via `file://` (double-click),
  only the **embedded sample cartridge** works.
- Level 4 lessons are **fetched** from `lessons/Level 4/` (`app.html`
  `CARTRIDGE_SOURCES`), so they require a local server:
  `serve-local.ps1` (Windows) or `python3 -m http.server` from the repo root,
  then open `http://localhost:8000/app.html`.
- `index.html` is only a redirect to `app.html`. `tiles-app.html`,
  `cockpit.html`, and `index.broken-annotated-teleprompter.html` are legacy
  references — keep, but do not build on them.
- Validate any cartridge with: `python3 validate_cartridge.py path/to/lesson.json`

## 4. Data inventory (as of Phase 0B)

- **Runtime contract is v2** (`schemaVersion: 2`, `beats[]`); no v1 step types
  survive in `app.html`. `SCHEMA.md` and `validate_cartridge.py` match the
  runtime one-for-one.
- **Level 4 lessons 1–10** are valid v2 cartridges (all pass the validator).
  The runtime dropdown currently lists only lessons 1–7.
- **Levels 1–3 lessons** (and `level4_lesson1.v1-backup.json`) are legacy v1
  `sections` format — the current runtime cannot load them. They are inventory,
  not dead weight: they hold converted Barton content awaiting v2 migration.
- Duplicate files: `lessons/level3_lesson1..7.json` at the `lessons/` root
  duplicate `lessons/Level 3/` — likely salvage duplication. Left in place
  (Phase 1 deletes nothing); resolve in a later authorized cleanup.
- **Stale docs — do not author against these:**
  - `MASTER_PROMPT.txt` targets the dead v1 schema (`steps`, `dialogue`,
    `board_action`, `sentence_marking`, `story_reading`).
  - `PHASE_0_BRIEF.md`'s "no fetch" hard constraint predates the current
    loader; the runtime deliberately fetches the lesson library.

## 5. Large files / `_raw_data`

- `.gitignore` ignores `_raw_data/` and `*.mp4`, **but** 34 `_raw_data` files
  (~500 MB of Barton manual PDFs plus their OCR `.txt` extracts) were already
  tracked in the salvage commit — gitignore does not untrack them. They live in
  git history, which is why `.git` is ~530 MB and every clone/push carries it.
- The OCR `.txt` files are small and are the working source for lesson
  conversion — keeping them tracked is fine.
- **Recommendation (not yet executed):** move the manual **PDFs** out of git —
  either external storage (Drive) with a pointer file, or `git lfs migrate`.
  Both require history rewriting or re-push coordination, so this must be its
  own explicitly authorized step, done after any pending branches are merged.
  Until then: do not commit new PDFs/videos; the ignore rules now catch them.

## 6. Do not touch

- `main` (until merge is authorized)
- `_raw_data/` contents (irreplaceable licensed source; read-only)
- `assets/` media
- Legacy HTML references (`tiles-app.html`, `cockpit.html`,
  `index.broken-annotated-teleprompter.html`)
- Quarantine/prior-attempt branches (reference only)
