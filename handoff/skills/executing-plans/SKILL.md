---
name: executing-plans
description: Use when executing any multi-step plan (handoff/plans/ or a user-approved step list). STOP on any plan-vs-reality mismatch; a step is done only when its verification output is pasted — "it should pass" never closes a step.
---

# Executing Plans

Justified by `handoff/FAILURE-LOG.md` F2, F3, F4: code shipped because the
end looked plausible while individual steps went unverified, hedge comments
stood in for verification runs, and a bulk import landed with no step-level
check at all.

## Hard rules

1. **STOP on any plan-vs-reality mismatch.** Before each step, check its
   stated preconditions against the actual repo. Any difference — counts,
   branch state, outputs, unexpected files — halt, report the exact
   mismatch, wait. No improvised workarounds, no "adapting the plan as
   intended," no continuing with later steps. A plan you had to reinterpret
   is no longer approved.

2. **A step is done only when its verification output is pasted** and
   compared to the plan's expected output. Never closes a step: "should
   pass", "trivial change", "verified locally" without the output, "same
   command worked earlier", reading the code and concluding it's correct.

3. **Output deviation = mismatch = STOP.** Includes unexpected *passes*: if
   the plan says a check must fail with 50 errors and it passes, the
   baseline is wrong — halt.

4. **No reordering, merging, or skipping steps.** Order is part of what was
   approved.

5. **Unverifiable step = BLOCKED, not done.** Missing key/tool/network:
   report what was missing. Never substitute a weaker check and call it
   equivalent.

6. **Read the step's hasty-model trap before executing.** Feeling the pull
   of exactly that shortcut confirms the trap is live, not that you're the
   exception.

## Reporting format (per step)

```
Step N: <title> — DONE | BLOCKED | STOPPED
$ <verification command>
<verbatim output>
Matches expected: yes / NO (diff: ...)
```
