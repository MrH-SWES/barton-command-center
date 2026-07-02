Known recovery context:
- The original GitHub main clone was stale/static.
- The recovered Drive copy contained the real v2 app.
- The recovered copy’s .git database was corrupt, so files were salvaged into a clean clone.
- The rescued state is now pushed to GitHub as branch recovered-drive-copy.
- This working directory is ~/Projects/barton-command-center-salvage.
- Work from recovered-drive-copy / fable-phase0, not main.
- app.html, AUTHORING_GUIDE.md, SCHEMA.md, schema_pressure.md, validate_cartridge.py, lessons/, assets/, and _raw_data/ are present.
- Do not merge or rewrite main during this task.

Title: Barton Command Center — Recovered Repo Triage + Level 4 v2 Cartridge Factory

You are the senior curriculum architect and implementation engineer for Barton Command Center.

You have the full mission below. Read all phases now so you understand the destination, but execute only the current phase.

At the end of each phase:
- STOP.
- Report using the required phase report format.
- Do not proceed until I reply exactly: y
- If I reply anything other than exactly y, treat it as feedback/correction, not authorization to proceed.

Core mission:
Recover the authoritative Barton Command Center working state after migration from a work laptop, determine the true runtime/schema contract, stabilize the repo, then build a Level 4 Lesson 1 gold cartridge and repeatable Level 4 conversion/validation pipeline.

Highest risks:
- The GitHub repo may be stale.
- The Drive recovery folder may contain the true working copy.
- The current app may be old/static v1 rather than the remembered schemaVersion 2 app.
- Docs may be stale.
- Existing validators or authoring guides may contradict the runtime.
- Missing Barton source/story text must be treated as a blocker, not invented.

Do not assume v2 exists. Prove it from source.

────────────────────────────────
PHASE 0A — RECOVERY / AUTHORITY INVENTORY ONLY
────────────────────────────────

Read-only. Do not modify files.

Goal:
Determine whether this working directory is the authoritative recovered project, a stale GitHub clone, a Drive-export copy, or a partial/mixed migration artifact.

Inspect:
- Current directory structure
- .git status
- git branches/remotes/log
- GitHub remote relationship, if any
- presence of app files such as index.html, app.html, package.json, assets/, lessons/, _raw_data/, .claude/, AUTHORING_GUIDE.md
- whether there are copied/migrated artifacts from Google Drive
- whether there are untracked or ignored files that matter
- whether the repo history indicates work not pushed to GitHub

Report:
1. What directory/repo you are examining
2. Whether it appears authoritative, stale, partial, or uncertain
3. What evidence supports that conclusion
4. Whether GitHub main appears behind this copy
5. Whether this copy has a usable .git history
6. What files/directories are likely important
7. What files/directories should not be touched
8. Recommended safest next step:
   - continue here
   - switch repos/directories
   - push a rescue branch
   - create a new repo
   - compare against GitHub clone
9. Exact commands you ran
10. Any blockers or uncertainties

STOP after Phase 0A.
Do not proceed until I reply exactly: y

────────────────────────────────
PHASE 0B — RUNTIME / SCHEMA INVENTORY ONLY
────────────────────────────────

Read-only. Do not modify files.

Goal:
Derive the actual current cartridge/runtime contract from source code and working lesson files.

Do not trust docs first. Trust runtime code first, working lesson files second, docs third.

Inspect for:
- schemaVersion
- say
- listen
- do
- board
- recovery
- applyBoardState
- prePlace
- lock
- dialogue
- board_action
- student_page
- sight_word_tracker
- spawn_tiles
- any parser/loader/normalizer/validator
- cartridge rendering logic
- lesson selection/loading logic

Report:
1. Current runtime contract
2. Supported lesson/cartridge fields
3. Supported step/beat types
4. Whether this is v1, v2, hybrid, or uncertain
5. Evidence from exact source files/line references
6. Existing validator/parser/schema-check inventory
7. Whether each validator/parser appears current or stale
8. Contradictions between runtime, lessons, docs, and prior assumptions
9. Which source should be trusted for each contradiction
10. Whether the original v2 cartridge-factory plan is valid, invalid, or needs revision

If this repo is clearly not the expected v2 app, say so plainly and recommend a recovery/migration plan. Do not start migrating yet.

STOP after Phase 0B.
Do not proceed until I reply exactly: y

────────────────────────────────
PHASE 1 — REPO STABILIZATION / RESCUE PLAN
────────────────────────────────

Only proceed after I reply exactly y.

Goal:
Make the current project safe to work on before curriculum/schema changes.

Allowed actions depend on Phase 0A/0B findings.

Possible actions:
- create a rescue branch
- add notes documenting current repo state
- add a recovery inventory document
- add or update README setup notes
- compare recovered copy against GitHub clone
- preserve important Drive-only files
- prepare a branch that can be pushed to GitHub safely

Do not:
- delete recovered files
- overwrite GitHub main
- rewrite history
- perform broad migration
- change schema/runtime yet
- edit lessons except for documentation/inventory if needed

Report:
1. Files changed
2. Branch status
3. Git status
4. Recovery/stabilization decisions made
5. Remaining risks
6. Exact commands run
7. Recommended next phase

STOP after Phase 1.
Do not proceed until I reply exactly: y

────────────────────────────────
PHASE 2 — GOLD LEVEL 4 LESSON 1 PLAN
────────────────────────────────

Only proceed after I reply exactly y.

Goal:
Create an implementation plan for Level 4 Lesson 1 based on the actual runtime contract.

Before editing the cartridge, inspect required source materials:
- Current Level 4 Lesson 1 cartridge
- Any sample/gold cartridge
- AUTHORING_GUIDE.md
- schema_pressure.md if present
- Level 4 OCR/manual source text
- Level 4 Lesson 1 story-page text
- relevant student pages
- existing Level 4/Level 3 lesson examples

Report:
1. Source materials present
2. Source materials missing
3. What can be authored safely
4. What must be blocked because source text is missing
5. The exact target cartridge format
6. A section-by-section conversion plan
7. Any schema limitations discovered
8. Whether to proceed with authoring or stop for missing sources

Do not invent missing Barton copyrighted/story text.

STOP after Phase 2.
Do not proceed until I reply exactly: y

────────────────────────────────
PHASE 3 — LEVEL 4 LESSON 1 GOLD CARTRIDGE
────────────────────────────────

Only proceed after I reply exactly y.

Goal:
Complete and correct Level 4 Lesson 1 as the gold-standard cartridge for the actual current runtime.

Requirements:
- Use the runtime-derived schema, not stale assumptions.
- Preserve Barton instructional intent.
- Keep instruction executable by a tutor/delivery engine.
- Distinguish teacher speech, teacher action, student response, board/tile state, and error recovery in whatever form the runtime supports.
- Use v2 fields only if the runtime supports them or Phase 1 explicitly authorized a migration.
- Use v1 fields only if this is truly the active runtime contract.
- Replace placeholder story text only if real source text is present.
- If story/student text is missing, mark the exact blocker clearly and do not invent it.

Do not mark complete unless:
- The cartridge is valid for the current app.
- It loads or can reasonably be loaded by the current runtime.
- No unsupported fields are introduced.
- No stale assumptions are smuggled in.
- Missing source content is clearly blocked rather than invented.

Report:
1. Files changed
2. Cartridge structure
3. Source text used
4. Missing-source blockers
5. Runtime compatibility
6. Manual checks performed
7. Any issues added to schema_pressure.md or equivalent
8. PASS/FAIL

STOP after Phase 3.
Do not proceed until I reply exactly: y

────────────────────────────────
PHASE 4 — VALIDATION / SCHEMA CHECKING
────────────────────────────────

Only proceed after I reply exactly y.

Goal:
Repair or create practical validation for the actual cartridge/runtime contract.

If a validator already exists:
- Reconcile it against the runtime.
- Update it only as needed.
- Do not replace it blindly.

If no validator exists:
- Create the smallest useful validator appropriate for this project shape.

Validator should catch, where applicable:
- unsupported fields
- missing required fields
- invalid lesson structure
- stale field usage
- placeholder text
- malformed board/tile actions
- missing required student/teacher text
- impossible references to missing lesson assets
- v1/v2 mismatch, if relevant

Do not overbuild a theoretical validator.

Report:
1. Validator/parser status before
2. Files changed
3. What validation now enforces
4. What it intentionally does not enforce
5. Commands/tests run
6. PASS/FAIL

STOP after Phase 4.
Do not proceed until I reply exactly: y

────────────────────────────────
PHASE 5 — LESSON 2 PIPELINE TEST
────────────────────────────────

Only proceed after I reply exactly y.

Goal:
Create or update a repeatable authoring guide/prompt for converting Level 4 Lessons 2+ and test it on Lesson 2 if source text is present.

The guide must explain:
- How to map manual text into the current runtime format
- How to distinguish scripted speech, procedure, board/tile actions, student response, and recovery
- How to handle missing source/student/story text
- What fields are allowed
- What fields are forbidden
- When to log schema pressure
- What not to invent
- How to validate the result

If Level 4 Lesson 2 source text is present:
- Convert Lesson 2 using the guide.
- Validate/check it.
- Critique it against the guide.
- Fix issues found.

If source text is missing:
- Do not invent.
- Create the pipeline guide and document Lesson 2 as blocked.

Report:
1. Files changed
2. Guide/prompt status
3. Lesson 2 status
4. Validation/check results
5. Missing blockers
6. Recommended next lesson workflow
7. PASS/FAIL

STOP after Phase 5.
Do not proceed until I reply exactly: y

────────────────────────────────
FINAL PHASE — FINAL REPORT
────────────────────────────────

Only proceed after I reply exactly y.

Produce final report:

1. Executive summary
2. Authoritative repo status
3. Runtime/schema status
4. Lesson 1 status
5. Validator status
6. Lesson 2/pipeline status
7. Remaining blockers
8. Recommended next 5 tasks
9. Commands/tests run
10. Files changed
11. What should be pushed to GitHub
12. What should not be pushed
13. PASS/FAIL

Do not mark PASS unless:
- The authoritative repo state is identified
- The runtime/schema contract is known
- Repo has been stabilized or a safe stabilization plan exists
- Lesson 1 work is complete or explicitly blocked by missing source
- Validation exists or its absence is explicitly justified
- Lesson 2 pipeline has been tested or explicitly blocked by missing source
