# Handoff — Departing Architect → Successor Sessions

Staged infrastructure that converts one architect's judgment about this repo
into rules, plans, and tooling that make any capable successor — human or
model — perform near that level here. Produced 2026-07-06 against commit
`41e082a`, in a read-only session: **nothing outside `handoff/` was
modified.** Activation is a deliberate human step — see `INSTALL.md`.

## The one lesson everything here encodes

This repo's entire failure history is a single class: **unverified
mirroring.** Code mirrored an external API from memory (`gpt4omini`, Weaviate
v3, un-awaited `create_session`). Filenames mirrored intentions, not contents
(`Copy of ...` that isn't a copy; "code snippets" that aren't runnable).
Claims mirrored what was once true, undated (`gemini-2.0-flash-exp` in 10+
files). And a bulk import mirrored a folder without anyone checking that a
single file would render (50 of 61 extensionless). Every artifact below
exists to force a verification step between a mirror and a merge. The full
evidence, with re-runnable commands: `FAILURE-LOG.md`.

## Map

| Path | What it is |
|---|---|
| `FAILURE-LOG.md` | Documented failures F1–F7, each with a verification command. The root justification for every rule here. |
| `OPEN-QUESTIONS.md` | Live gates (Q-001…Q-003). Work behind an OPEN gate is refused, not flagged. |
| `skills/executing-plans/` | STOP on plan-vs-reality mismatch; steps close only with pasted verification output. |
| `skills/spec-fidelity/` | API-mirroring code comes only from captured specs; failing contract tests are never fixed at the assertion. |
| `skills/gated-scope/` | Unanswered external question ⇒ dependent work refused outright. |
| `skills/fact-discipline/` | Statistics carry source + as-of date; tier-X claims need tier-X evidence; expected outputs captured, never predicted; absence claims need a documented search. |
| `skills/context-economy/` | Tool routing around this repo's context bombs: the 20 MB PDF, single-line-JSON notebooks (line-based tools lie), file-by-file reading where an index or sweep is cheaper. |
| `plans/PLAN-TEMPLATE.md` | Required shape for all future plans (complete code, per-step verify + expected output + hasty-model trap). |
| `plans/2026-07-notebook-restoration-phase-1.md` | The flagship plan: the next real piece of work, fully designed and ready to execute. All expected outputs were actually captured, not predicted. |
| `docs/ONBOARDING.md` | Session start protocol: read order, tool routing for context economy, post-compaction re-verification. |
| `docs/MODEL-ROUTING.md` | What runs solo, what needs a spec capture, what queues for a human, what is never done. |
| `docs/MAINTENANCE.md` | Per-artifact refresh triggers; append-only and no-hand-editing invariants. |
| `tools-staging/` | The validator and index generator the flagship plan installs into `tools/`. Already exercised against this repo (outputs captured in the plan). |
| `INSTALL.md` | Exact activation steps, with their own verification. |

## First session after activation

Follow `docs/ONBOARDING.md`, then execute
`plans/2026-07-notebook-restoration-phase-1.md` under the `executing-plans`
skill. That plan is deliberately the first task: it is mechanical, fully
specified, needs no API keys, and its traps exercise every skill at
least once — a calibration run for the whole system.
