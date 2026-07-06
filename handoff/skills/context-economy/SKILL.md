---
name: context-economy
description: Use before any exploration, file inspection, or counting in this repo. Routes around its two context bombs and one shape trap — the 20 MB PDF, single-line-JSON notebooks (line-based tools lie; cat wastes tokens), and file-by-file reading where an index or sweep is cheaper.
---

# Context Economy

Justified by `handoff/FAILURE-LOG.md` F7: a wrong verification expectation
shipped into the handoff because `grep -c` counts lines and every notebook
is one line. The repo's file shapes actively mislead default tooling, and
wasted context degrades every judgment made after the waste.

## The three hazards

1. **`Agentic_Design_Patterns.pdf` — 20 MB, 400+ pages. Never read
   wholesale.** Specific pages via `Read` with the `pages` parameter, only
   when a task genuinely needs book text. Repo work almost never does.

2. **Every notebook is single-line JSON.** Consequences:
   - `cat`/`Read` dumps escaped JSON — never do it. Extract code instead:
     ```
     python3 -c "import json,sys; [print(''.join(c.get('source',[]))) for c in json.load(open(sys.argv[1]))['cells']]" 'notebooks/<file>'
     ```
   - Line-based counts lie: `grep -c` returns at most 1 per file. Count
     occurrences with `grep -o <pat> <file> | wc -l`. Anything built on
     "lines" (`awk NR`, `wc -l`, `sed -n`) needs a second look before you
     trust it here.

3. **Don't open files to learn what they are.** Route by cost:
   - What exists / what is X → `notebooks/INDEX.md` (once Phase 1 lands),
     else `ls` + the extraction one-liner on the single candidate.
   - "Which files use/say X" → `Grep` over `notebooks/` (`-l` or `-o`,
     never `-c`).
   - Multi-angle sweeps ("map everything touching ADK sessions") → delegate
     to an Explore agent; keep the conclusion, not the file dumps.
   - Facts about repo state → run the counting command (`fact-discipline`),
     don't eyeball listings.

## Session hygiene

- Prefer one command that prints a decisive number over three that print
  scenery; every wasted screen of output is context the actual work no
  longer has.
- After a context compaction, treat remembered file contents as stale:
  re-extract before editing (see `handoff/docs/ONBOARDING.md`).
