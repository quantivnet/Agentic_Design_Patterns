# Plan: <title>

- **ID:** `YYYY-MM-<slug>`  ·  **Author:** <session/person>  ·  **Date:** <YYYY-MM-DD>
- **Status:** DRAFT | APPROVED | IN PROGRESS | DONE | ABANDONED
- **Gate check:** list every entry from `handoff/OPEN-QUESTIONS.md` this plan
  touches. If any is OPEN, the plan's status cannot pass DRAFT
  (`gated-scope` rule 1). Write "Gates: none" only after checking the file.
- **Executes under:** `executing-plans` skill — the executor STOPs on any
  mismatch and closes steps only with pasted verification output.

## Goal

One paragraph. What is true about the repo after this plan that isn't now.

## Non-goals

Explicit list of adjacent work this plan deliberately does not do, each with
the reason (usually: gated on Q-NNN, or belongs to a later phase). This
section is what keeps a hasty executor from "helpfully" widening scope.

## Preconditions

Each precondition = check command + expected output, verbatim. The executor
runs all of them before step 1; any deviation is a STOP.

```
$ <command>
<expected output>
```

## Steps

Repeat this block per step. No step may omit any field.

### Step N — <title>

- **Intent:** one sentence.
- **Files:** exact paths created/modified. "Various" is not a path.
- **Change:** the complete code, file content, or exact commands — no
  "implement X appropriately". If the executor has to design anything, the
  plan is not finished.
- **Verify:**
  ```
  $ <command>
  ```
- **Expected output:** verbatim (mark genuinely variable fragments like
  hashes/timestamps explicitly). Deviation = STOP.
- **Hasty-model trap:** the specific shortcut a capable-but-rushed executor
  will be tempted to take at this step, and why it's wrong here. Write the
  temptation, not a platitude — "you will want to also fix the typo in the
  filename; don't, renames are gated on Q-002."
- **STOP conditions:** anything beyond output-mismatch that must halt the
  step.

## Rollback

Exact commands to return to the pre-plan state at any step boundary.

## Definition of done

Checklist. Must include: every step reported with pasted verification output;
PR opened with the evidence appendix; no file outside the plan's file list
changed (`git diff --stat` pasted to prove it — fact-discipline absence rule).

## Evidence appendix (filled during execution)

Step-by-step verbatim verification outputs, in order.
