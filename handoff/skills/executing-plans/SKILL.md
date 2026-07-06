---
name: executing-plans
description: Use whenever executing a multi-step plan in this repo (anything in handoff/plans/, or any user-approved step list). Enforces STOP-on-mismatch and evidence-based step completion — a step is done only when its verification output is pasted.
---

# Executing Plans

## Why this skill exists (documented failure)

`handoff/FAILURE-LOG.md` **F2**: the Chapter 14 RAG example builds its vector
store from a GitHub HTML page because the download step was never checked —
only the final print. **F3**: the Chapter 2 ADK example ships the comment
*"might trigger warning"* where a verification run should have been; the
session-creation call is an un-awaited coroutine. Both shipped because "the
end looked plausible" substituted for "each step was verified."
**F4**: 50 unrenderable files landed in one bulk commit no step-level check
ever touched.

## Hard rules

1. **STOP on any plan-vs-reality mismatch.** Before each step, check the
   step's stated preconditions against the actual repo. If *anything* differs
   — file counts, branch state, command output, a file that exists when the
   plan says it shouldn't — halt, report the exact mismatch, and wait. Do not
   improvise a workaround, do not "adapt the plan as intended," do not
   continue with later steps. A plan you had to reinterpret is a plan that is
   no longer approved.

2. **A step is done only when its verification output is pasted.** Every step
   report must contain the verification command *and its verbatim output*,
   compared against the plan's expected output. The following never close a
   step: "it should pass", "this is a trivial change", "verified locally"
   (without the output), "the same command worked in step 2", reading the
   code and concluding it's correct.

3. **Expected-output deviation is a mismatch.** If the output differs from
   the plan's expected output in any way you cannot mechanically account for
   (a timestamp, a hash the plan marks as variable), that is rule 1 — STOP.
   In particular: an unexpected *pass* is as suspicious as an unexpected
   fail. If the plan says a validator must fail with 50 errors and it passes,
   the baseline is wrong — halt.

4. **No reordering, merging, or skipping steps**, even when a later step
   "obviously" subsumes an earlier one. Order is part of what was approved.

5. **A step whose verification cannot be run is BLOCKED, not done.** Missing
   API key, unreachable network, absent tool — report it as blocked with what
   was missing. Never substitute a weaker check and call it equivalent.

6. **Read the step's hasty-model trap before executing it.** Plans in this
   repo annotate each step with the specific shortcut a capable-but-rushed
   model will want to take. If you feel the pull of exactly that shortcut,
   that is confirmation the trap is live, not license to take it.

## Reporting format

Per step, in the PR description or session report:

```
Step N: <title> — DONE | BLOCKED | STOPPED
$ <verification command>
<verbatim output>
Matches expected: yes / NO (diff: ...)
```

A plan is complete only when every step shows DONE with pasted output.
