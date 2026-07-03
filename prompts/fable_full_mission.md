Title: Barton Command Center — Fable Controlled Mission

Known recovery context:
- GitHub main was stale/static.
- The real recovered v2 app came from the Drive/work-laptop migration.
- The recovered .git database was corrupt, so files were salvaged into a clean clone.
- The rescued state is pushed as branch: recovered-drive-copy.
- This working branch is: fable-phase0.
- Base branch is: recovered-drive-copy.
- Do not touch, merge, rewrite, or target main.
- Important files/directories include app.html, AUTHORING_GUIDE.md, SCHEMA.md, schema_pressure.md, validate_cartridge.py, lessons/, assets/, _raw_data/, and .claude/.

Control rule:
Execute only one phase at a time.

At the end of each phase:
1. Commit allowed changes to fable-phase0 if any changes were made.
2. Update the PR.
3. Post the phase report as a PR comment.
4. STOP.
5. Do not continue until I comment exactly: y

If I comment anything other than exactly y, treat it as feedback, correction, or redirection.

Core mission:
Recover and stabilize the authoritative Barton Command Center working state, derive the actual runtime/schema contract from source, then build toward a Level 4 Lesson 1 gold cartridge and repeatable Level 4 conversion/validation pipeline.

Hard rules:
- Runtime code is more authoritative than docs.
- Working lesson files are more authoritative than stale notes.
- Do not invent missing Barton source/story/student-page text.
- Do not migrate schemas blindly.
- Do not build new architecture unless explicitly authorized.
- Do not mark PASS unless checks actually pass.

PHASE 0A — Recovery / Authority Inventory Only

Read-only. Do not modify project files.

Inspect:
- current repo, branch, remotes, status
- relationship between fable-phase0, recovered-drive-copy, and main
- app.html, index.html, AUTHORING_GUIDE.md, SCHEMA.md, validate_cartridge.py, schema_pressure.md
- lessons/, assets/, _raw_data/, .claude/
- evidence that this is the recovered v2 project rather than stale main
- files/directories that should not be touched

Report:
1. repo/branch examined
2. whether this appears authoritative, stale, partial, or uncertain
3. evidence
4. whether main appears behind this copy
5. important files/directories
6. files/directories not to touch
7. safest next step
8. exact commands run
9. blockers/uncertainties

STOP after Phase 0A. Wait for my exact comment: y

PHASE 0B — Runtime / Schema Inventory Only

Read-only. Do not modify project files.

Derive the actual cartridge/runtime contract from source.

Inspect for:
- schemaVersion
- beats
- say
- listen
- do
- board
- note
- media
- recovery
- applyBoardState
- prePlace
- lock
- dialogue
- board_action
- student_page
- sight_word_tracker
- spawn_tiles
- parser/loader/normalizer/validator
- lesson selection/loading logic
- cartridge rendering logic

Report:
1. current runtime contract
2. supported cartridge fields
3. supported beat/step types
4. whether this is v1, v2, hybrid, or uncertain
5. source file/line evidence
6. validator/parser/schema-check inventory
7. whether each validator appears current or stale
8. contradictions between runtime, lessons, docs, and assumptions
9. trusted source for each contradiction
10. whether the v2 cartridge-factory plan remains valid

STOP after Phase 0B. Wait for my exact comment: y

PHASE 1 — Repo Stabilization / Rescue Plan

Only proceed after exact y.

Goal:
Make the recovered project safe for continued work.

Allowed:
- add recovery notes
- add/update setup notes
- document branch strategy
- document large-file/_raw_data recommendation
- recommend LFS or external storage strategy

Do not:
- delete recovered files
- rewrite history
- touch main
- broadly migrate schemas
- edit lessons except for inventory documentation

Report:
1. files changed
2. branch status
3. git status
4. stabilization decisions
5. remaining risks
6. commands run
7. recommended next phase

STOP after Phase 1. Wait for exact y.

PHASE 2 — Level 4 Lesson 1 Gold Plan

Only proceed after exact y.

Inspect:
- Level 4 Lesson 1 cartridge
- Level 4 Lesson 2 cartridge if relevant
- sample/gold cartridge
- AUTHORING_GUIDE.md
- SCHEMA.md
- schema_pressure.md
- Level 4 OCR/manual source text
- story/student-page text
- existing Level 3 and Level 4 examples

Report:
1. source materials present
2. source materials missing
3. what can be authored safely
4. what is blocked by missing source
5. exact target cartridge format
6. section-by-section conversion plan
7. schema limitations
8. proceed or stop recommendation

Do not invent missing source text.

STOP after Phase 2. Wait for exact y.

PHASE 3 — Level 4 Lesson 1 Gold Cartridge

Only proceed after exact y.

Goal:
Complete/correct Level 4 Lesson 1 as the gold cartridge for the actual runtime.

Requirements:
- use runtime-derived schema
- preserve Barton instructional intent
- distinguish teacher speech, teacher action, student response, board/tile state, and recovery using supported fields
- do not introduce unsupported fields
- do not invent missing story/student text
- document blockers clearly

Report:
1. files changed
2. cartridge structure
3. source text used
4. missing-source blockers
5. runtime compatibility
6. checks performed
7. schema_pressure updates
8. PASS/FAIL

STOP after Phase 3. Wait for exact y.

PHASE 4 — Validation / Schema Checking

Only proceed after exact y.

Goal:
Repair or create practical validation for the actual cartridge/runtime contract.

If validator exists:
- reconcile it against runtime
- update only as needed

If no validator exists:
- create the smallest useful validator

Validator should catch:
- unsupported fields
- missing required fields
- invalid lesson structure
- stale field usage
- placeholder text
- malformed board/tile actions
- missing required student/teacher text
- missing asset references
- v1/v2 mismatch where relevant

Report:
1. validator status before
2. files changed
3. what validation enforces
4. what it intentionally does not enforce
5. commands/tests run
6. PASS/FAIL

STOP after Phase 4. Wait for exact y.

PHASE 5 — Lesson 2 Pipeline Test

Only proceed after exact y.

Goal:
Create/update a repeatable authoring guide/prompt for Level 4 Lessons 2+ and test on Lesson 2 if source text is present.

Guide must explain:
- mapping source text into runtime format
- scripted speech vs procedure vs board/tile actions vs student response vs recovery
- missing source handling
- allowed fields
- forbidden fields
- when to log schema pressure
- what not to invent
- how to validate

If Lesson 2 source is present:
- convert/check Lesson 2
- critique against guide
- fix issues

If missing:
- document as blocked

Report:
1. files changed
2. guide status
3. Lesson 2 status
4. validation results
5. blockers
6. recommended next workflow
7. PASS/FAIL

STOP after Phase 5. Wait for exact y.

FINAL PHASE — Final Report

Only proceed after exact y.

Report:
1. executive summary
2. authoritative repo status
3. runtime/schema status
4. Lesson 1 status
5. validator status
6. Lesson 2/pipeline status
7. blockers
8. recommended next 5 tasks
9. commands/tests run
10. files changed
11. what should be pushed/merged
12. what should not be pushed/merged
13. PASS/FAIL
