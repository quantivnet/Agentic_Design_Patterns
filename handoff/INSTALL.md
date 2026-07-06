# Install / Activation

The handoff is staged, not active: nothing in `handoff/` binds a session
until these steps run. They are deliberately manual — activating the rules is
a human decision. Total time: ~3 minutes.

## 1. Promote the skills

From the repo root:

```
mkdir -p .claude/skills
cp -r handoff/skills/executing-plans .claude/skills/
cp -r handoff/skills/spec-fidelity   .claude/skills/
cp -r handoff/skills/gated-scope     .claude/skills/
cp -r handoff/skills/fact-discipline .claude/skills/
```

**Verify:**
```
$ ls .claude/skills
executing-plans  fact-discipline  gated-scope  spec-fidelity
$ head -3 .claude/skills/executing-plans/SKILL.md
---
name: executing-plans
description: Use whenever executing a multi-step plan in this repo (anything in handoff/plans/, or any user-approved step list). Enforces STOP-on-mismatch and evidence-based step completion — a step is done only when its verification output is pasted.
```

The originals stay in `handoff/skills/` as the reviewed source of truth;
per `docs/MAINTENANCE.md`, skill edits happen there (with a FAILURE-LOG
justification) and are re-copied.

## 2. Create the repo `CLAUDE.md`

Write exactly this content to `CLAUDE.md` at the repo root (the repo has none
today — verify with `ls CLAUDE.md` → `No such file or directory` before
writing; if one exists, merge instead of overwriting):

```markdown
# Agentic Design Patterns — working rules

Code companion to the book by Antonio Gulli. The `notebooks/` files are
Jupyter JSON (some still missing `.ipynb` until the restoration plan lands).

Before any work, follow `handoff/docs/ONBOARDING.md` (read order, tool
routing, post-compaction protocol). Binding rules live in `.claude/skills/`:
executing-plans, spec-fidelity, gated-scope, fact-discipline — each justified
in `handoff/FAILURE-LOG.md`.

Hard constraints:
- Check `handoff/docs/MODEL-ROUTING.md` before starting a task; some tasks
  queue for a human, some are never done (the PDF is untouchable).
- Check `handoff/OPEN-QUESTIONS.md`; work gated on an OPEN question is
  refused, not flagged.
- Never Read `Agentic_Design_Patterns.pdf` wholesale (20 MB); never `cat` a
  notebook — extract cell source via the one-liner in ONBOARDING.md.
- `notebooks/INDEX.md` is generated; edit only via `tools/build_index.py`.
```

**Verify:**
```
$ wc -l CLAUDE.md
# expected: 20 ± 2
```

## 3. Commit the activation

```
git checkout -b activate-handoff
git add .claude/ CLAUDE.md
git commit -m "Activate handoff: install four project skills and CLAUDE.md

Skills sourced from handoff/skills/ (see handoff/FAILURE-LOG.md for the
documented failures each one answers)."
git push -u origin activate-handoff
```

Open a PR; a human merges (per `docs/MODEL-ROUTING.md`).

## 4. First real work

Execute `handoff/plans/2026-07-notebook-restoration-phase-1.md` in a fresh
session, under the now-active `executing-plans` skill. If its preconditions
no longer reproduce (the repo moved since 2026-07-06), the plan's own rules
say: STOP, re-baseline, human re-approves — see `docs/MAINTENANCE.md`, row
"plans (APPROVED)".
