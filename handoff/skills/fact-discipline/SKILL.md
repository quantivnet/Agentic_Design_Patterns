---
name: fact-discipline
description: Use whenever writing any document, index, PR description, commit message, or report in this repo that states a fact — a statistic, a claim about what code does, a claim that something exists or is absent, or a claim about an external service. Every statistic carries a source and as-of date; tier-X claims require tier-X evidence; absence claims require a documented search.
---

# Fact Discipline

## Why this skill exists (documented failure)

`handoff/FAILURE-LOG.md` **F5**: 17 model-ID strings drift across the corpus
— including a retired experimental alias in 10+ files — with no as-of dates,
so nobody can tell stale from current. **F6**: a file named `Copy of ...`
contains *different* content than the file it claims to copy; a "code
snippets" file is secretly non-runnable ("Conceptual … not runnable code" in
cell 1) with nothing in its name or any index saying so. **F4** reached
`main` under the commit message "agentic design added" — a description
carrying zero verifiable facts. In this repo, unverified statements have a
track record of being wrong.

## Hard rules

1. **Every statistic carries a source and an as-of date.** "50 of 61 files
   lack the extension (per `ls notebooks | grep -vc '\.ipynb$'`, 2026-07-06)"
   — never a bare "most files are broken." Numbers without provenance are
   treated as rumors by successors, and should be.

2. **Claims about tier X require tier-X evidence.** The tiers, strongest
   claim each tier can support:
   - **Runtime tier** — "this notebook runs / this pipeline retrieves the
     document": requires *executed output*, pasted. Reading the code is not
     runtime evidence (F2: the code read fine; the corpus was HTML).
   - **Spec tier** — "this model ID / signature / import path is valid":
     requires a capture per `spec-fidelity`, with date. Recalling the API is
     not spec evidence (F1).
   - **Repo tier** — "this file contains / the repo has N of X": requires a
     command plus output. A filename is not repo evidence about content
     (F6: `Copy of` isn't a copy; "code snippets" isn't runnable code).
   - Downgrades must be explicit: if you only have repo-tier evidence, say
     "the code *appears* to do X (not executed)."

3. **Absence claims require a documented search.** "There are no tests",
   "nothing references this filename", "no other file uses gpt4omini" — each
   needs the exact search command and its (empty or counted) output, in the
   same document as the claim. An absence claim without a search is a
   confession that you didn't look.

4. **Names and labels are claims.** Filenames, index Status columns, commit
   messages, PR titles — all assert facts and all fall under rules 1–3. If a
   file is conceptual/non-runnable, its index row must say so; if a commit
   renames 50 files, its message says "rename 50 files: append .ipynb", not
   "updated".

5. **Freshness is part of the fact.** Any statement about an external service
   (available models, current API shape, pricing, deprecations) is only valid
   with its as-of date attached, and goes stale per the capture's re-verify
   date (`spec-fidelity` template, default 90 days). Repeating a dated fact
   without its date strips the safety off it.
