# Session Onboarding Protocol

For any agent session (or new human contributor) starting work in this repo.
Total cost if followed: ~5 minutes and a few thousand tokens. Total cost of
skipping it, historically: failures F1–F6.

## Read order (before the first edit)

1. `handoff/README.md` — the map (1 min).
2. `handoff/FAILURE-LOG.md` — skim all entries. This is *why* the rules
   exist; rules read without their failures get rationalized away.
3. The four skills in `handoff/skills/` (or `.claude/skills/` once
   installed): `executing-plans`, `spec-fidelity`, `gated-scope`,
   `fact-discipline`. These are binding, not advisory.
4. `handoff/OPEN-QUESTIONS.md` — know the live gates before scoping anything.
5. `handoff/docs/MODEL-ROUTING.md` — check whether today's task runs solo or
   queues for a human, *before* starting it.
6. If executing a plan: the plan file, in full, including every trap callout.

## Tool routing for context economy

This repo has two context bombs and one shape trap:

- **`Agentic_Design_Patterns.pdf` is 20 MB / 400+ pages. Never read it
  wholesale.** Use `Read` with the `pages` parameter for specific pages only,
  and only when a task genuinely needs book text. Repo work almost never does.
- **Notebook files are single-line JSON.** `cat`/`Read` on one dumps escaped
  JSON and wastes tokens. Extract code instead:
  ```
  python3 -c "import json,sys; [print(''.join(c.get('source',[]))) for c in json.load(open(sys.argv[1]))['cells']]" 'notebooks/<file>'
  ```
- **Start from `notebooks/INDEX.md`** (once Phase 1 lands) to locate the
  right notebook — don't open files to find out what they are.
- Sweeping questions ("which files use ADK?") → `Grep` over `notebooks/`, or
  an Explore agent for multi-angle sweeps. Never a file-by-file Read loop.
- Facts about repo state → run the counting command (`fact-discipline`),
  don't eyeball directory listings.

## After a context compaction

Assume the summary is lossy in exactly the dangerous places. Before
continuing:

1. Re-read this file and the four skill files (cheap, they're short).
2. Re-read the *current step* of the active plan — the whole step block,
   including its trap.
3. **Re-run the last verification command yourself** and compare to the
   plan's expected output. Never trust a summary's claim that "step N passed"
   without the pasted output in front of you — a summarized pass is
   tier-nothing evidence (`fact-discipline` rule 2).
4. Re-check `handoff/OPEN-QUESTIONS.md`: a gate you remember as answered may
   be a gate the summary invented an answer for.

## Session end

- Work pushed to the session branch; PR carries the evidence appendix.
- Any new failure observed → append to `FAILURE-LOG.md` (with verification
  command) in the same PR.
- Any new external question raised → append to `OPEN-QUESTIONS.md` as OPEN.
- Anything half-done → say so in the PR description, precisely. "Steps 1–2
  done with evidence; step 3 BLOCKED on missing GOOGLE_API_KEY" — never
  "mostly done."
