# Model Routing Table

What an agent session may do solo, what it may do solo only with specific
evidence in hand, and what queues for a human. "Human" here means the repo
owner (or the book's author, where noted). When a task doesn't match any row,
route it to the nearest *more restrictive* row and note the gap — then add
the row (see MAINTENANCE.md).

| Task | Route | Condition / reason |
|---|---|---|
| Regenerate `notebooks/INDEX.md` | **Solo** | Deterministic generator; verify by re-run + empty diff. |
| Execute an APPROVED plan in `handoff/plans/` | **Solo** | Under `executing-plans`; any STOP condition converts the remainder to *human*. |
| Edit prose in `handoff/` docs (typos, clarity) | **Solo** | Except skill files — see below. |
| Append to `FAILURE-LOG.md` / `OPEN-QUESTIONS.md` | **Solo** | Append-only; entries need verification commands. |
| Draft a new plan (status DRAFT) | **Solo** | Approval to APPROVED is human. |
| Extension-only renames per the flagship plan | **Solo** | Pure R100 renames, validator-verified. |
| Edit notebook code to track an API change | **Solo + spec** | Only with a `specs/` capture (per `spec-fidelity`) *and* Q-003 answered. Missing either → human queue. |
| Change a model ID anywhere | **Solo + spec** | Requires captured provider model list with as-of date; never in passing. |
| Add dependency manifests, CI workflows, pre-commit hooks | **Human review** | Infrastructure choices outlive sessions; propose as draft PR, human merges. |
| Edit a skill file in `handoff/skills/` | **Human review** | And only with a FAILURE-LOG entry justifying the change (MAINTENANCE.md). |
| Delete or merge any notebook (duplicates included) | **Human (author)** | Gated on Q-001; `gated-scope` rule 5 — no exceptions for "obvious" redundancy. |
| Rename files beyond appending `.ipynb` | **Human (author)** | Gated on Q-002; external links may use exact names. |
| Anything touching `Agentic_Design_Patterns.pdf` | **Never** | The book is the author's artifact; the repo mirrors it, not vice versa. |
| Merge any PR to `main` | **Human** | Sessions open draft PRs with evidence; humans merge. |
| Force-push, history rewrite, branch deletion on `main` | **Never solo** | No current task needs it; a request for it is itself a STOP. |

## Escalation rule

Two consecutive failed solo attempts at the same task ⇒ the task reclassifies
to **Human review** for this repo until a FAILURE-LOG entry explains what was
missing and the row above is amended. Do not take a third run at it with a
"better idea" — that is how hedge-guards (F3) get written.
