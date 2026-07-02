# Barton Command Center — Lesson Cartridge Schema (v2)

A **cartridge** is one JSON lesson file. The interface ("the rail") reads it and
presents the deliverer with exactly one focal action at a time. This document is
the contract between *you* (the author filling cartridges with your own curriculum
content) and *the engine* (which renders them).

Design law: **the author declares a beat; the engine just displays it.** No runtime
regrouping, no string-sniffing. What you write is what the deliverer sees.

---

## Top level

```jsonc
{
  "schemaVersion": 2,
  "meta": { ... },          // identity + pre-flight info
  "materials": [ ... ],     // physical things to have ready before "Go"
  "objectives": [ ... ],    // plain-language goals, deliverer-facing
  "beats": [ ... ]          // THE RAIL — ordered, the whole lesson
}
```

### `meta`
```jsonc
{
  "level": 3,
  "lesson": 1,
  "title": "Short Vowel Blending",   // your title
  "estMinutes": 35,                  // optional, shown on pre-flight
  "author": "you",                   // optional bookkeeping
  "videoSpeedDefault": 1.5           // optional; 1 | 1.5 | 2  (default 1.5)
}
```

### `materials` (array of strings)
Shown on the pre-flight screen *before* the deliverer presses Go, so nothing is
discovered mid-lesson.
```jsonc
["Letter tile set (level 3)", "Whiteboard + marker", "Student reading page 4"]
```

### `objectives` (array of strings)
Plain language. What the student will be able to do. Not jargon.
```jsonc
["Blend three sounds into a spoken word", "Read 6 new short-a words"]
```

---

## The beat (the atom)

Every beat shares ONE envelope so the UI is perfectly predictable. Every field
except `id` is optional — a beat includes only the parts that moment needs.

```jsonc
{
  "id": "L3.1.warmup.01",     // REQUIRED. Stable, unique. Used for resume + reteach jumps.
  "phase": "Warm-up",         // groups beats into named sections on the progress map
  "label": "Review letter sounds",  // optional short human title for the progress map

  "say":     { ... },         // tutor script line + audio
  "listen":  { ... },         // what a correct response sounds like
  "do":      "string",        // a physical/procedural instruction
  "board":   { ... },         // declarative student-board state (sticky)
  "note":    "string",        // why-this-matters / teacher note
  "media":   { ... },         // embedded video segment
  "recovery":{ ... }          // the struggle branch
}
```

### `say`
```jsonc
{
  "text": "Your scripted line here.",
  "audio": true               // optional; show a 🔊 TTS button. default false
}
```
`text` may also be an array of strings for multi-line script; each renders as its
own SAY line within the same beat.

### `listen`
```jsonc
{
  "expect": ["/k/ /a/ /t/", "cat"],   // one or more acceptable responses
  "hint": "Sounds, then the blended word."  // optional clarifier for the deliverer
}
```

### `do`
A plain string. A procedural instruction to the *deliverer* (not script to read
aloud). e.g. `"Point to each tile as the student says its sound."`

### `board` — declarative, STICKY
The board shows whatever a beat last set, and **holds that until another beat
changes it.** Omit `board` on a beat and the student screen does not change — which
is correct, because most consecutive beats discuss the same board.

To deliberately empty the board, use mode `"clear"`.

```jsonc
{ "mode": "tiles", "level": 2, "openDrawer": "consonants" }
```

The `tiles` mode drives the full Barton tile engine (the manipulative surface with
the six color drawers, grouping/seam-physics, and tap-to-speak). A beat configures
that surface; it does not replace it.

#### `tiles` mode fields

| field | type | meaning |
|---|---|---|
| `level` | int 2–10 | which cumulative tile set to load (Book N stacks all tiles through N). Matches the engine's drawers: blue consonants, yellow vowels, red units, green endings, orange prefixes, purple roots. |
| `openDrawer` | string | which drawer opens by default: `consonants`, `vowels`, `units`, `endings`, `prefixes`, `roots`. Guides the deliverer to the right tiles without searching. |
| `prePlace` | array | OPTIONAL. Words/segments to build on the board automatically (modeling beats). See below. **Omit the key entirely** for hands-off practice beats (board stays sticky). An explicit `prePlace: []` is NOT the same as omitting it — see semantics below. |
| `lock` | bool | On a board-bearing beat, defaults to **false**. If true, the board is display-only for this beat (student watches the model). See lock semantics below. |

**`prePlace` semantics (absent vs empty):**
- **Key absent** → leave existing board tiles untouched (sticky). Use this for practice beats that carry over a model.
- **`prePlace: []`** (explicit empty array) → clear the board and place nothing. Use this to deliberately empty the tile area while staying in `tiles` mode.
- **`prePlace: [{...}]`** → clear the board, then build the listed words.

**`lock` semantics (explicit on board beats, sticky on no-board beats):**
- A beat **with** a `board` field sets lock explicitly: `lock: true` locks, and **absent/`false` unlocks** — so any board-bearing beat that doesn't say `lock:true` is interactive. This removes the surprise of a drawer-only beat silently inheriting a lock.
- A beat **without** a `board` field changes nothing, including lock — the prior lock state persists (sticky). This is what keeps a teacher model locked across an intervening no-board beat.

**Pre-place vs hands-off (the Mix model).** This is the pedagogical fork:

- *Modeling beat* — the deliverer is showing the student something. Use `prePlace`
  so the word is already built when the beat opens; optionally `lock: true` so it
  stays put while modeled.
  ```jsonc
  { "mode": "tiles", "level": 2, "prePlace": [{ "word": "cat", "row": 0 }], "lock": true }
  ```
- *Practice beat* — the student builds it themselves. Omit `prePlace`; the board
  carries over whatever tiles are there, drawers ready.
  ```jsonc
  { "mode": "tiles", "level": 2, "openDrawer": "vowels" }
  ```

A `prePlace` entry is `{ "word": "cat", "row": 0 }` — the engine spells it from the
loaded tile set, placing the segments flush as one group on the given row (row 0 =
top). Multiple entries stack on successive rows. The engine colors each segment by
its Barton category automatically; you write the spelling, not the colors.

Because the board is **sticky**, a practice beat following a model beat keeps the
modeled word on screen unless you `clear` it or declare new `prePlace`.

#### Other board modes

| mode | payload | notes |
|---|---|---|
| `clear` | — | empties the student board |
| `word_frame` | `{ "words": ["cat","map","sun"] }` | grid; engine spotlights one word at a time, deliverer steps through |
| `phrase_builder` | `{ "columns": { "article":["the","a"], "noun":["cat","dog"], "verb":["ran","sat"] } }` | tap columns to build a sentence into a tray |
| `fill_blanks` | `{ "bank": ["a","i","o"], "rows": ["c___t", "m___p"] }` | blanks written inline as `___`; drag bank chips in |
| `sentences` | `{ "items": ["The cat sat.", "A map is flat."] }` | display sentences for marking |
| `story` | `{ "title": "...", "text": "...", "images": [{ "src": "assets/worksheets/level4/lesson1_extra_practice_1.png", "label": "Lesson 1 Extra Practice #1", "alt": "Lesson 1 Student Page 13 Extra Practice 1" }] }` | connected text display; optional `pageType: "worksheet"` or `"reference_page"` displays rendered real page images without persistence |
| `matching` | `{ "pairs": [["cat","🐱"], ["dog","🐕"]] }` | pairs, not parallel arrays — prevents misalignment |
| `sight_words` | `{ "words": ["the","said","was"] }` | sight-word pills |

For source reference pages, use the same real-image display pattern as worksheets.
Do not synthesize student reference or rule pages from typed fields when the manual
provides a page. The student writes on the physical paper copy; the app only displays
the rendered source page.

```jsonc
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

Authoring principle (yours): **the payload describes presence; the rules govern
attachment.** Feedback is always "not here," never "you can't use this."

### `media` — timestamped video segment
No video re-cutting required. Point at the source file and declare in/out points.
```jsonc
{
  "source": "level3_module1.mp4",  // file in your /videos folder
  "start": 124,                    // seconds (or "2:04")
  "end": 188,                      // seconds (or "3:08")
  "caption": "Model: blending three sounds"   // optional
}
```
The player carries a persistent speed toggle (1× / 1.5× / 2×), defaulting to
`meta.videoSpeedDefault`. For a pre-cut standalone clip, set `start: 0` and omit
`end`.

### `recovery` — the struggle branch (the novice lifeline)
Structured, always one tap away on its own beat — never buried.
```jsonc
{
  "trigger": "Student can't isolate the middle vowel sound.",
  "prompts": [
    "Say the word slowly with me.",
    "What sound does your mouth make in the middle?"
  ],
  "reteach": "L3.1.warmup.03"   // optional: jump back and replay this beat id
}
```

---

## Architecture (decided)

**Unified surface.** The Barton tile engine *is* the board — not a guest inside a
weaker frame. The rail (left, the script) and the tile engine (right, the
manipulative) live on one screen. A beat's `board` field configures the tile
engine; it never replaces it. This keeps the deliverer on a single surface so they
never have to track whether two windows agree.

**Pop-out escape hatch.** For second-screen / tablet rooms, the board detaches into
its own window. Same engine, same state — just relocated. No second system to
author or maintain.

**One tile engine, retire the rest.** The pointer-based tile engine (touch-aware:
`pointerdown`, capture, touch drag-thresholds) is the single source of truth for
tiles. The older mouse-only `spawnTiles` stub is retired.

---

## Engine guarantees (so the deliverer never wonders)

1. **One focal beat.** The active beat is fully present; all others are peripheral.
2. **Board follows the rail.** Advancing onto a beat with a `board` field configures
   the student surface automatically. No separate "spawn" button to remember.
3. **Passive board readout.** A small always-visible line confirms current
   student-surface state (e.g. "Tiles: Book 2 · vowels open") without being a control.
4. **Resume.** `beat.id` lets the rail reopen exactly where it was left.
5. **Recovery is first-class.** Every beat's `recovery` is reachable in one tap.
6. **Model vs practice is explicit.** `prePlace`/`lock` make modeling beats build
   themselves; their absence makes practice beats hands-off.

---

## Minimum valid cartridge

```jsonc
{
  "schemaVersion": 2,
  "meta": { "level": 1, "lesson": 1, "title": "Sample" },
  "beats": [
    { "id": "b1", "say": { "text": "Let's begin." } }
  ]
}
```
`schemaVersion`, `meta.title`, and a non-empty `beats[]` with unique `id`s are the
only hard requirements. Everything else is optional and degrades gracefully.
