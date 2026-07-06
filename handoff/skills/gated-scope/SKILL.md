---
name: gated-scope
description: Use whenever a task depends on an unanswered external question — author intent, which duplicate file is canonical, target framework version, licensing, anything only a human outside the session can answer. Work behind an open gate is refused outright; a "pending confirmation" flag is not a gate.
---

# Gated Scope

## Why this skill exists (documented failure)

`handoff/FAILURE-LOG.md` **F6, part 2**: the two Chapter 18 Guardrails files
began as one. "Which is canonical?" was never answered, work proceeded on
both anyway, and they diverged in provider, imports, and logging. Today
*neither* can be deleted safely, and reconciling them costs far more than the
question would have. The failure was not the open question — it was doing the
work anyway with a mental asterisk. Asterisks don't survive context
compaction, session handoffs, or merges. Only refusals do.

## Hard rules

1. **An open external question blocks its dependent work outright.** If a
   task's correctness depends on an answer only a human can give (the author,
   the repo owner, a licensor), the task is reported as **BLOCKED: gated on
   Q-NNN** and *no part of the gated work is performed*. Not a draft, not a
   "provisional" version, not "I'll do both variants." Provisional work
   becomes permanent the moment anyone else builds on it — that is exactly
   how F6 happened.

2. **A "pending confirmation" flag is not a gate.** Writing "TODO: confirm
   with author" above the code, opening the PR as draft, or noting the
   assumption in the description does not unblock anything. The test is
   mechanical: *if the answer came back the other way, would finished work
   have to be reverted?* If yes, the work is gated, and gated work is not
   started.

3. **Questions live in `handoff/OPEN-QUESTIONS.md`**, one entry each:

   ```
   ## Q-NNN — <one-line question>
   Raised: <date> by <session/PR>. Blocks: <task/plan step>.
   Answer: OPEN | "<verbatim answer>" — <who>, <date>, <where (link/quote)>
   ```

   A question is answered only by a quoted reply with source and date. "I'm
   fairly sure the author would want X" is not an answer; it is the question
   restated as a guess.

4. **Separable ungated work may proceed** — but only if it does not touch,
   reference, or foreclose the gated part. When splitting, state the split
   explicitly: "Steps 1–3 proceed; step 4 is gated on Q-002." If the split
   requires judgment about the gated content, the split itself is gated.

5. **Deletion and merging of user-authored content is always gated.** No
   session deletes, merges, or "reconciles" the Guardrails pair, the
   `Copy of` files, or any notebook without a written answer from the author
   naming what survives. This rule has no exceptions for obviousness — F6's
   files also looked obviously redundant, and weren't (the "Copy" is
   different content).

## Currently open gates (seed list, as of 2026-07-06)

- **Q-001** — Which Chapter 18 Guardrails file is canonical, and should the
  other be deleted or renamed as a variant? Blocks: any dedup/deletion.
- **Q-002** — May files be renamed beyond adding `.ipynb` (fix the
  `Chapter 21_ Chapter 21_` stutter, trailing spaces, `Copy of` prefix)?
  Book/site links may reference exact names. Blocks: any cosmetic renaming.
- **Q-003** — Which framework versions does the published book target?
  (Determines whether code should be fixed forward to current APIs or pinned
  to book-era versions.) Blocks: any behavioral code change in `notebooks/`.

Copy these into `handoff/OPEN-QUESTIONS.md` when that file is first created.
