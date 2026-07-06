---
name: gated-scope
description: Use when a task depends on an unanswered external question — author intent, canonical file among duplicates, target framework versions, licensing. Gated work is refused outright until the answer is in handoff/OPEN-QUESTIONS.md; a "pending confirmation" flag is not a gate.
---

# Gated Scope

Justified by `handoff/FAILURE-LOG.md` F6: the two Chapter 18 Guardrails
files began as one; "which is canonical?" was never answered, both were
edited anyway, and now neither can be deleted safely. The failure wasn't the
open question — it was working with a mental asterisk. Asterisks don't
survive compaction, handoffs, or merges. Refusals do.

## Hard rules

1. **An open external question blocks its dependent work outright.** Report
   `BLOCKED: gated on Q-NNN` and perform *no part* of the gated work — no
   draft, no provisional version, no "both variants." Provisional becomes
   permanent the moment anyone builds on it; that is exactly F6.

2. **A "pending confirmation" flag is not a gate.** TODO comments, draft-PR
   status, and noted assumptions unblock nothing. Mechanical test: *if the
   answer came back the other way, would finished work have to be reverted?*
   Yes = gated = not started.

3. **Gates live only in `handoff/OPEN-QUESTIONS.md`** — the single source of
   truth for what is open and what was answered (never duplicate its content
   elsewhere). A question is answered only by a verbatim quote with who,
   date, and where. "The author would probably want X" is the question
   restated as a guess.

4. **Separable ungated work may proceed** — only if it doesn't touch,
   reference, or foreclose the gated part. State the split explicitly
   ("steps 1–3 proceed; step 4 gated on Q-002"). If the split itself
   requires judgment about the gated content, the split is gated.

5. **Deleting or merging user-authored content is always gated** — no
   exception for obviousness. F6's files also looked obviously redundant and
   weren't (the "Copy" is different content).
