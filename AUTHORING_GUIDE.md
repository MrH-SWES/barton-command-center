# Barton Command Center v2 Cartridge Authoring Guide

This guide documents the current authoring style for Barton Command Center v2 cartridges, using `lessons/Level 4/level4_lesson1.json` and `lessons/Level 4/level4_lesson2.json` as the gold examples.

The core rule is simple: author the lesson as ordered, meaningful beats. The app renders the beat; it does not infer pedagogy from loose text.

## Required File Shape

A v2 lesson cartridge is one JSON file with this top-level shape:

```json
{
  "schemaVersion": 2,
  "meta": {
    "level": 4,
    "lesson": 3,
    "title": "Lesson Title",
    "estMinutes": 50,
    "author": "Barton Command Center",
    "videoSpeedDefault": 1.5
  },
  "materials": [],
  "objectives": [],
  "beats": []
}
```

Required in practice:

- `schemaVersion`: must be `2`.
- `meta`: lesson identity and preflight data.
- `materials`: physical items the tutor needs before starting.
- `objectives`: plain-language goals for the lesson.
- `beats`: the full ordered lesson.

Do not use v1 fields such as `sections`, legacy beat `type`, `type: "dialogue"`, `type: "action"`, `type: "board_action"`, or imperative `spawn_tiles`.

## Beat Envelope

Every beat uses the same envelope. Include only the fields that moment needs.

```json
{
  "id": "L4.3.teach.01",
  "phase": "New Teaching",
  "label": "Short display title",
  "say": { "text": "Tutor script." },
  "listen": { "expect": ["Expected student response"], "hint": "Optional tutor cue." },
  "do": "Tutor procedure.",
  "note": "Tutor note, caution, or why-it-matters content.",
  "recovery": {
    "trigger": "What struggle this supports.",
    "prompts": ["Prompt one.", "Prompt two."],
    "reteach": "L4.3.teach.01"
  },
  "board": { "mode": "tiles", "level": 4 },
  "media": {
    "source": "optional-video.mp4",
    "start": 0,
    "end": 30,
    "caption": "Optional caption"
  }
}
```

Stable beat IDs matter. Follow the Level 4 pattern: `L4.2.words.01`, `L4.2.stories.03`, etc. Use `phase` for the progress map and `label` for the human-readable step title.

## Granularity Rule

Use grouped beats.

- One beat per activity, drill segment, or meaningful instructional move.
- Do not create one beat per word unless the tutor script truly changes word by word.
- A word list, phrase list, sentence list, or tile drill usually belongs in one beat.
- Split a sequence when the teaching purpose changes.

Examples:

- Lesson 1 groups the real tile spelling sequence into `L4.1.spelltiles.03` instead of making separate beats for `NOD`, `NO`, `SPIT`, `SPY`, etc.
- Lesson 2 groups the word-frame page into `L4.2.words.01` with one `word_frame` list instead of one beat per word.
- Lesson 2 splits `COPY` into its own "other way" teaching beat because the script introduces a new decision rule.

## Mapping Manual Content To Fields

Use this mapping consistently:

- Manual script to be spoken aloud -> `say`
- Expected student response -> `listen`
- Tutor procedure or physical action -> `do`
- Tutor notes, cautions, rule rationale, why it matters -> `note`
- Struggle guidance, prompts, reteach jumps -> `recovery`
- Student-facing surface state -> `board`
- Video or timed media -> `media`

Keep `say` student-facing. Do not bury procedure in `say` unless the tutor should actually say it.

## Board Conventions

Board state is declarative and sticky.

- If a beat omits `board`, the previous board remains.
- Use `board.mode: "clear"` when the student board should intentionally empty.
- Use `board.mode: "tiles"` for tile-engine work.
- Use `prePlace` for tutor modeling or when the manual begins with a built word.
- Use `prePlace` plus `lock: true` for display-only modeling.
- For student practice, use hands-off/unlocked board state: omit `prePlace` or set `lock: false` as appropriate.
- Do not encode imperative commands such as spawn/remove/move tile. Describe the desired state.

Tile examples:

```json
{
  "mode": "tiles",
  "level": 4,
  "openDrawer": "units",
  "prePlace": [],
  "lock": true
}
```

Lesson 1 uses this for Unit review: an empty tile board, Units drawer open, locked for review.

```json
{
  "mode": "tiles",
  "level": 4,
  "openDrawer": "vowels",
  "prePlace": [{ "word": "bonus", "row": 0 }],
  "lock": true
}
```

Lesson 2 uses this style for modeling a built word before syllable division.

```json
{
  "mode": "tiles",
  "level": 4,
  "openDrawer": "vowels",
  "lock": false
}
```

Use this style when the student manipulates or continues working with tiles.

## Student And Teacher Surface Conventions

The current app behavior has different expectations for Teacher View and Student View.

- Teacher View can show full lists, controls, notes, and rail context.
- Student View should show one active word, phrase, sentence, sight word, or story surface at a time.
- Do not author around teacher chrome. Put the right board payload in the cartridge and let the app present it cleanly.

Use these board modes for student pages:

- `word_frame`: word reading lists. Student View shows one active word at a time. Lesson 1 `L4.1.words.01` and Lesson 2 `L4.2.words.01` are the model.
- `sentences`: read-only phrase and sentence lists. Student View shows one active item at a time. Use this for Barton phrase groups and sentence pages; do not force read-only phrase pages into `phrase_builder`.
- `sight_words`: current-session sight word list work when the source provides a list. Teacher can mark words and build a session reading deck. Lesson 1 `L4.1.sightread.01` is the model.
- Physical sight word decks: if the source only reviews an existing physical Reading Deck and gives no word list, use `do`/`listen`/`note` without a `sight_words` board. Lesson 2 `L4.2.sightread.01` is the model.
- `story`: connected text, story reading, reference pages, and non-persistent worksheet/reference displays.
- Student reference and rule pages: encode as a `story` board with `pageType: "reference_page"`, `purpose: "reference"`, and an `images` array pointing to a rendered real source page. If the manual says to bring out or update a student reference page, display the real page image. Do not synthesize the page with typed headings, blank lines, or reconstructed rule text. The app is only a display/reference surface; the student writes on the physical paper page.
- Extra practice: encode as a `story` board with `pageType: "worksheet"` and an `images` array of rendered real manual pages. Do not create synthetic worksheet placeholders and do not require persistence.
- Extra practice page location: Lesson N extra-practice pages are usually found immediately before the Lesson N+1 divider/overview in the manual. At the start of a new level, the opening review may pull from the final lesson of the previous level.

Example reference-page display:

```json
{
  "mode": "story",
  "pageType": "reference_page",
  "purpose": "reference",
  "title": "Student Page #48: Spelling Rules - Book 4",
  "text": "Use the student's physical spelling rules page.",
  "images": [
    {
      "src": "assets/reference/level4/book4_spelling_rules_student_page_48.png",
      "label": "Student Page #48: Spelling Rules - Book 4",
      "alt": "Book 4 Spelling Rules student page 48"
    }
  ]
}
```

Example worksheet reference:

```json
{
  "mode": "story",
  "pageType": "worksheet",
  "title": "Lesson 2 Extra Practice",
  "subtitle": "Rendered from the real Book 4 manual pages before Lesson 3",
  "text": "Show Lesson 2 Extra Practice #1 or #2. The student completes the selected paper copy outside the app.",
  "images": [
    {
      "src": "assets/worksheets/level4/lesson2_extra_practice_1.png",
      "label": "Lesson 2 Extra Practice #1",
      "alt": "Lesson 2 Student Page 23 Extra Practice 1"
    }
  ]
}
```

## Source Fidelity Rules

Work from the actual manual source.

- Prefer the cleanest OCR available, but do not trust OCR blindly.
- Verify OCR-damaged rule text, word lists, stories, and board-critical items against PDF page images.
- For worksheets and reference pages, render the real PDF page as an image asset and point the cartridge at that asset.
- Do not invent words, stories, examples, rules, or repeat-lesson content.
- If the lesson source cannot be confidently identified, stop and report.
- If a word or rule remains uncertain after OCR and PDF checks, do not silently guess. Record the uncertainty in the report and, if it exposes a schema limitation, log it in `schema_pressure.md`.

Lesson 2 source checks are a useful model: PDF images were used to confirm `SNE`, remove a stray OCR artifact from the nonsense-reading list, correct `LA-TOP`, and restore `rodent` to the word-frame list.

## Schema Pressure Policy

Do not redesign the schema midstream while authoring a cartridge.

- If content fits the current fields, encode it with the existing schema.
- If content only partly fits, use the least misleading existing field and document the limitation.
- Add pressure to `schema_pressure.md` only when the issue is a reusable schema concern, not a one-off authoring choice.
- Keep authoring moving; schema pressure is evidence for later design, not permission to fork the format.

Current known pressure examples include phrase-list specificity, reference-page fidelity, story variants, and student tile-bank intent for unlocked manipulation beats.

## Validation Procedure

After authoring or editing a cartridge, run:

```powershell
python validate_cartridge.py "lessons/Level 4/level4_lesson3.json"
```

Also rerun validation on previous gold lessons:

```powershell
python validate_cartridge.py "lessons/Level 4/level4_lesson1.json"
python validate_cartridge.py "lessons/Level 4/level4_lesson2.json"
```

Before reporting success, confirm:

- New cartridge validates with 0 errors.
- Prior gold lessons still validate.
- New cartridge uses `schemaVersion: 2`.
- No v1 fields remain: `sections`, legacy `type`, `spawn_tiles`.
- Beat IDs are unique.
- Lesson covers the source end to end.

## Runtime Smoke-Test Procedure

When app-shell edits are allowed and the cartridge is exposed in the loader:

1. Start a local server from the repo root.
2. Open `http://127.0.0.1:5500/app.html`.
3. Confirm the new cartridge appears in the selector.
4. Select it and confirm the beat count displays.
5. Click Begin Lesson.
6. Confirm the first beat renders.
7. Jump through representative board modes used by the lesson:
   - a locked modeling `tiles` beat
   - an unlocked practice `tiles` beat
   - `word_frame`
   - `sentences`
   - `sight_words`, if present
   - `story`
   - worksheet/reference display, if present
8. Confirm Student View shows one active item at a time for word, phrase, sentence, and sight-word surfaces.
9. Confirm Teacher View still shows the fuller rail/list context.

When app-shell edits are not allowed and the selector does not yet expose the new cartridge, report that limitation. Do not edit `app.html` just to complete a cartridge-authoring task.

## Checklist For Future Lesson-Authoring Agents

Use this checklist before replacing a lesson file:

- Read `SCHEMA.md`, `sample_lesson.json`, `schema_pressure.md`, Lesson 1, Lesson 2, and the target lesson.
- Locate the exact manual pages for the target lesson.
- Back up any old-schema lesson file before overwriting.
- Build the top-level v2 shape: `schemaVersion`, `meta`, `materials`, `objectives`, `beats`.
- Author grouped beats by activity, drill segment, or teaching move.
- Map script/procedure/response/note/recovery/board into the correct fields.
- Use declarative board state only.
- Use `prePlace` + `lock: true` for modeling.
- Use unlocked hands-off tile state for student practice.
- Use `word_frame` for word-reading pages.
- Use `sentences` for read-only Barton phrases and sentence pages.
- Use `sight_words` only when the source provides sight words for the app surface.
- Use `story` for connected text, reference pages, and non-persistent worksheets.
- When a lesson uses a student reference/rule page, render the real manual/student page into `assets/reference/...` and reference it with `board.images`.
- Locate extra-practice pages immediately before the next lesson divider, render those real pages into `assets/worksheets/...`, and reference them with `board.images`.
- At a new level boundary, use the final lesson's extra practice from the previous level for the opening review when the manual calls for it.
- Do not create synthetic worksheet or reference-page placeholders.
- Verify OCR-damaged words, rules, stories, and tile-critical details against PDF images.
- Do not invent missing source content.
- Log reusable schema pressure; do not redesign the schema during authoring.
- Validate the new cartridge.
- Revalidate Lesson 1 and Lesson 2.
- Smoke-test in the app if the cartridge is exposed by the shell.
- Report source pages, backup path, beat count, phases, board modes, validation results, schema pressure, uncertainties, and smoke-test result.

## Concrete Examples From Lessons 1 And 2

### Modeling Beat

Lesson 1 `L4.1.teach.02` models `bu` as an Open syllable. It uses `prePlace` and `lock: true` because the tutor is showing the student the concept.

```json
"board": {
  "mode": "tiles",
  "level": 4,
  "openDrawer": "vowels",
  "prePlace": [{ "word": "bu", "row": 0 }],
  "lock": true
}
```

### Practice Beat

Lesson 2 `L4.2.realtiles.01` starts tile spelling practice with an empty interactive board.

```json
"board": {
  "mode": "tiles",
  "level": 4,
  "openDrawer": "consonants",
  "prePlace": [],
  "lock": false
}
```

The words are listed in `do` because the tutor dictates them as a grouped drill.

### Word Frame

Lesson 2 `L4.2.words.01` uses one beat for the whole student word page:

```json
"board": {
  "mode": "word_frame",
  "words": ["navy", "predict", "wipid", "refund", "pony"]
}
```

The real cartridge contains the full list. Student View shows one active word at a time; Teacher View can show more context.

### Read-Only Phrase Groups

Lesson 1 `L4.1.phrases.01` and Lesson 2 `L4.2.phrases.01` use `sentences` mode for phrase groups:

```json
"board": {
  "mode": "sentences",
  "items": [
    "Who: The Spanish lady",
    "Did What: began a trip",
    "Where: in Reno",
    "Add-On: in the spring."
  ]
}
```

These are read-only phrase lists. Do not convert them to `phrase_builder` unless the source activity actually asks the student to build phrases in the app.

### Sight Word Decks

Lesson 1 has a source sight-word list, so it uses `sight_words`:

```json
"board": {
  "mode": "sight_words",
  "words": ["put", "pull", "how", "now"]
}
```

Lesson 2 reviews an existing physical Reading Deck, so it does not invent a `sight_words` board.

### Stories

Lessons 1 and 2 put each story in its own beat because the story title, task, and reading mode change:

```json
"board": {
  "mode": "story",
  "title": "Navy Pilot",
  "text": "Jason has chosen to be a Navy pilot..."
}
```

Use separate beats for basic and advanced story options.

### Recovery

Recovery should be specific and usable in the moment:

```json
"recovery": {
  "trigger": "Student is unsure or reads a word inaccurately.",
  "prompts": [
    "Put a dot below each vowel.",
    "How many letters are between the dots?",
    "Draw the dividing line the most common way.",
    "Say each syllable exactly as divided.",
    "Is that a real word? If not, move the line the other way."
  ]
}
```

This Lesson 2 pattern keeps the tutor from having to improvise the correction path.
