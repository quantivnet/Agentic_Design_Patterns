---
name: fact-discipline
description: Use when stating any fact in a doc, index, PR, commit message, or report — statistics, claims about behavior or content, existence/absence claims. Source + as-of date on every statistic; tier-matched evidence; expected outputs captured by running, never predicted; absence claims need a documented search.
---

# Fact Discipline

Justified by `handoff/FAILURE-LOG.md` F5 (undated model IDs, retired alias
in 10+ files), F6 (a "Copy of" that isn't a copy; "code snippets" secretly
non-runnable), F4 (landed under the message "agentic design added"), and F7
(a *verification expectation* in this very handoff was predicted instead of
run, and was wrong). Unverified statements here have a track record.

## Hard rules

1. **Every statistic carries a source and an as-of date.** "50 of 61 files
   lack the extension (per `ls notebooks | grep -vc '\.ipynb$'`,
   2026-07-06)" — never a bare "most files are broken."

2. **Claims require tier-matched evidence:**
   - **Runtime tier** ("it runs", "it retrieves the document") — executed
     output, pasted. Reading code is not runtime evidence (F2: the code read
     fine; the corpus was HTML).
   - **Spec tier** ("this model ID / signature is valid") — a dated capture
     per `spec-fidelity`. Recall is not spec evidence (F1).
   - **Repo tier** ("this file contains / N of X") — command + output. A
     filename is not evidence about content (F6).
   - Downgrades are explicit: "*appears* to do X (not executed)."

3. **Expected outputs are captured, not predicted.** Any command + expected
   output published anywhere (plan, log, doc) must be pasted from an actual
   run against the current repo state. Predicting output from understanding
   is how F7 happened — to the author of these rules, in the file defining
   them.

4. **Absence claims require a documented search** — the exact command and
   its (empty or counted) output, in the same document as the claim. An
   absence claim without a search is a confession you didn't look.

5. **Names and labels are claims** — filenames, index Status columns, commit
   messages, PR titles. A commit renaming 50 files says "rename 50 files:
   append .ipynb", never "updated".

6. **Freshness is part of the fact.** External-service statements (models,
   API shapes, pricing) are valid only with their as-of date, and expire per
   the capture's re-verify date. Repeating a dated fact without its date
   strips the safety off it.
