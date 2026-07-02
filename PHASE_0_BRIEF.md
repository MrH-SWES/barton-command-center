# Build Brief — Phase 0: Scaffold & Salvage

**Project:** Barton Command Center (in-classroom delivery shell for an owned, licensed reading curriculum)
**You are:** the coding agent. Build exactly Phase 0. Do NOT build the rail logic, responsive states, or polish yet — those are later phases. Stop when the Definition of Done is met and report.

---

## Context you need

This app lets a non-pedagogy-trained adult (sub, para, parent volunteer) deliver scripted reading lessons in one classroom. The guiding law: **the deliverer never wonders what to do next.** Everything serves that.

The final app is a **single, self-contained HTML file** that runs by double-click — **no server, no `fetch`, no build step.** This is a hard constraint (classroom Chromebooks, locked-down network). Cartridge lesson data is embedded in the file, not fetched.

The screen is a **rail (left, the script for the deliverer)** beside a **board (right, the interactive tile manipulative the students use).** Phase 0 builds the skeleton and wires in the real tile engine. Later phases build the rail.

## Repo files — salvage map (READ BEFORE CODING)

- **`tiles-app.html`** — SALVAGE THE ENGINE INTACT. This is a working, touch-aware, pointer-based Barton tile manipulative. Do not rewrite its logic. Preserve these exactly: the `B_LEVELS` data object; the state vars (`tiles`, `baseTiles`, `activeDrawer`, `draggedTile`, `draggedGroup`, `gesture`, etc.); and the functions `dragThresholdFor`, `getFontSize`, `getUniqueSorted`, `sameRowY`, `areFlush`, `recomputeGroupsAround`, `getGroupChain`, `createTile`, `renderTray`, `renderActiveDrawer`, `renderAlphabet`, `renderWordPane`, `findSeamNear`, `findNearbyTiles`, `calculateDropTarget`, `updateGhostVisual`, `clearGhostVisual`, `speakText`, `speakGroup`, `speakAllBoard`, `onPointerStart`, `beginDrag`, `handleMove`, `handleEnd`, `insertAtSeam`, `updateDragVisual`, `switchDrawer`. The grouping/seam physics and the `pointerdown`+`setPointerCapture` model are the crown jewel — keep them.
- **`cockpit.html`** — REFERENCE FOR INTENT ONLY, then supersede. Its three-zone layout (`#rail` / `#timeline` / `#workspace`) and card-activation feel are the right direction, but it uses an OLD data shape (`data.level`, `getBadge`, `getStepText`, typed steps) and it `fetch`es a lesson — both rejected. Do not carry its data model or its fetch forward.
- **`index.html`, `index.broken-annotated*`** — RETIRE. Do not use. The mouse-only `spawnTiles` tile code in `index.html` is explicitly replaced by the `tiles-app.html` engine.
- **`SCHEMA.md`** — the FROZEN cartridge contract. The data model below is authoritative; follow it, not cockpit's shape.
- **`sample_lesson.json`** — a valid sample cartridge. Use its CONTENTS as the embedded Phase 0 cartridge.
- **`validate_cartridge.py`** — run cartridges through this; they must pass.

## Cartridge schema (authoritative — see SCHEMA.md for full detail)

A cartridge is `{ schemaVersion:2, meta, materials?, objectives?, beats[] }`. A **beat** is the atom, envelope: `{ id (required, unique), phase?, label?, say?, listen?, do?, board?, note?, media?, recovery? }`. The `board` field is **declarative and sticky** — it configures the tile engine (mode `tiles` with `level`, `openDrawer`, optional `prePlace`/`lock`), or other modes (`clear`, `word_frame`, etc.). Board persists across beats until a beat changes it. Phase 0 does NOT need to act on beats yet — just load and hold the data.

---

## Phase 0 scope — build exactly this

1. **Create `app.html`** (new file; do not edit the legacy files). Single self-contained HTML file, no external build deps. The Lexend webfont link is fine to keep.

2. **Embed the cartridge.** Take the contents of `sample_lesson.json` and embed it as a JS object literal inside `app.html` (e.g. `const CARTRIDGE = { ... };`). NO `fetch`. Verify it would pass `validate_cartridge.py`.

3. **Two-zone shell.** A flex layout: left zone `#rail` (~38% width) and right zone `#board` (~62%). Left zone for Phase 0 is just a placeholder reading "Rail — built in Phase 1" plus a readout of `CARTRIDGE.meta.title` and `CARTRIDGE.beats.length` (proof the data loaded). Right zone hosts the tile engine.

4. **Import the tile engine into `#board`.** Bring the entire working engine from `tiles-app.html` into `app.html`, scoped so its DOM lives inside `#board` (not full-window as it currently is). The engine must keep working: tray drawers switch, tiles drag from tray to board, groups form/split, seam-insert works, double-tap speaks, "Speak"/"Reset" work, touch and mouse both work. Re-scope its CSS so `#wordPane`, `#alphabetSection`, `#bottomDock` are positioned relative to `#board`, not the viewport.

5. **No regressions.** The engine must behave identically to `tiles-app.html` — just inside a panel. If anything in the engine breaks during re-scoping, fix the positioning/containment, never the physics logic.

6. **Leave hooks, build nothing else.** Add empty stub functions `applyBoardState(board)` and `renderRail()` with `// Phase 2` / `// Phase 1` comments. Do not implement them.

## Hard constraints (do not violate)

- No `fetch`, no server dependency, no build tooling. Double-click `app.html` → it runs.
- Do not modify `tiles-app.html`, `cockpit.html`, `index.html`, or any legacy file. Only create `app.html`.
- Do not alter the tile engine's grouping/seam/pointer logic. Re-scope its container/CSS only.
- Do not invent a new data shape. The schema is frozen.

## Definition of Done (self-check before reporting)

- [ ] `app.html` opens by double-click (file://) with zero console errors.
- [ ] Left zone shows the placeholder + correct embedded title and beat count.
- [ ] Right zone shows the full tile board: drawers, alphabet rail, tray.
- [ ] Drag tile from tray → board works (mouse AND touch/pointer).
- [ ] Two flush tiles form a group; directional drag splits the group; seam-insert pushes neighbors over.
- [ ] Double-tap a word speaks it; "Speak" reads the board; "Reset" clears.
- [ ] No `fetch` anywhere in `app.html`.
- [ ] `applyBoardState` and `renderRail` exist as untouched stubs.

When done, report: what you salvaged verbatim, what you re-scoped, and any place the engine fought the containment so I know where the seams are.
