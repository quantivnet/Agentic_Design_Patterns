# Plan: Notebook Restoration — Phase 1 (visibility & validation)

- **ID:** `2026-07-notebook-restoration-phase-1`  ·  **Author:** departing-architect session  ·  **Date:** 2026-07-06
- **Status:** APPROVED (ready to execute in a fresh session)
- **Gate check:** touches none of Q-001/Q-002/Q-003 (`handoff/OPEN-QUESTIONS.md`).
  This plan adds extensions and generated/tooling files only — no deletions,
  no cosmetic renames, no content edits. Gates: none open for this scope.
- **Executes under:** `executing-plans` skill.

## Goal

Every file in `notebooks/` renders on GitHub and opens as a notebook (all 61
gain/keep the `.ipynb` extension), a validation script exists that fails CI-style
on any future regression, and a generated `INDEX.md` states per notebook: cell
count, frameworks, model IDs referenced, and runnable-vs-conceptual status.
This is failure F4 (and the visibility half of F6) fixed at the root — see
`handoff/FAILURE-LOG.md`.

## Non-goals

- **No deletion or merging of duplicates** (`Copy of ...`, Guardrails `(1)`)
  — gated on Q-001. They get extensions like everything else.
- **No renaming beyond appending `.ipynb`** — the `Chapter 21_ Chapter 21_`
  stutter, trailing spaces, and `Copy of` prefixes stay — gated on Q-002.
- **No edits to notebook content** — not the `gpt4omini` typo (F1), not the
  blob-URL bug (F2), not model IDs (F5) — all gated on Q-003 (fix-forward vs
  pin-to-book-era is the author's call). Phase 2 material.
- **No dependency manifests, no CI wiring** — Phase 2, needs human review per
  `handoff/docs/MODEL-ROUTING.md`.

## Preconditions

```
$ git status --porcelain | wc -l
0
$ ls notebooks | wc -l
61
$ ls notebooks | grep -vc '\.ipynb$'
50
$ ls handoff/tools-staging
build_index.py
validate_notebooks.py
```

Any deviation (e.g. 62 files because someone added one since 2026-07-06):
STOP and re-baseline — do not proceed on drifted preconditions.

## Steps

### Step 1 — Install the validator and capture the failing baseline

- **Intent:** put the validation tooling in `tools/` and prove it detects the
  current breakage *before* anything is fixed.
- **Files:** `tools/validate_notebooks.py`, `tools/build_index.py` (new).
- **Change:**
  ```
  mkdir -p tools
  cp handoff/tools-staging/validate_notebooks.py tools/
  cp handoff/tools-staging/build_index.py tools/
  ```
- **Verify:**
  ```
  $ python3 tools/validate_notebooks.py | head -1; echo "exit=${PIPESTATUS[0]}"
  $ python3 tools/validate_notebooks.py | grep -c 'FAIL MISSING'
  ```
- **Expected output** (captured against commit `41e082a`, 2026-07-06):
  ```
  files=61 json_ok=61 nbformat4_ok=61 has_cells=61 ext_ok=11 dupe_groups=0
  exit=1
  50
  ```
- **Hasty-model trap:** the validator exits 1 and prints 50 FAIL lines — a
  rushed executor reads that as "the tool is broken" and either patches the
  validator to pass or skips straight to renaming. The failing run IS the
  deliverable of this step: it is the baseline that proves step 2 did
  something. Do not modify the copied scripts; do not reorder steps 1 and 2.
- **STOP conditions:** `dupe_groups` ≠ 0 (means notebook content changed
  since this plan was written); `json_ok` < 61 (a file is corrupt — that is a
  new FAILURE-LOG entry, not a thing to quietly fix).

### Step 2 — Append `.ipynb` to the 50 extensionless files

- **Intent:** make every notebook render on GitHub and open in Jupyter.
- **Files:** the 50 files listed in Appendix A — renamed in place, content
  untouched.
- **Change** (from repo root; rename derives from `git ls-files`, Appendix A
  is the cross-check):
  ```
  git ls-files -z notebooks | while IFS= read -r -d '' f; do
    case "$f" in *.ipynb) ;; *) git mv "$f" "$f.ipynb" ;; esac
  done
  ```
- **Verify:**
  ```
  $ python3 tools/validate_notebooks.py; echo "exit=$?"
  $ git status --porcelain | grep -c '^R '
  ```
- **Expected output:**
  ```
  files=61 json_ok=61 nbformat4_ok=61 has_cells=61 ext_ok=61 dupe_groups=0
  exit=0
  50
  ```
- **Hasty-model trap:** with the filenames in hand you will notice
  `Chapter 21_ Chapter 21_ ...` (stuttered), `...(LangChain Code Example ).ipynb`
  (trailing space), and `Copy of ...` — and want to clean them up "while
  you're in there." Don't. The published book and any external links
  reference these exact names; cosmetic renames are gated on Q-002
  (`gated-scope`). Extension append only — the diff must show 50 renames
  where old name + `.ipynb` = new name, byte-identical content (pure R100).
- **STOP conditions:** any rename where content changed (git shows `R0xx`
  instead of `R100` at commit time); rename count ≠ 50.

### Step 3 — Generate `notebooks/INDEX.md`

- **Intent:** one generated page stating what each notebook is, which
  framework it teaches, which model IDs it references (F5 made visible), and
  whether it is runnable or conceptual (F6 part 3 made visible).
- **Files:** `notebooks/INDEX.md` (new, generated).
- **Change:**
  ```
  python3 tools/build_index.py
  ```
- **Verify:**
  ```
  $ python3 tools/build_index.py
  $ grep -c CONCEPTUAL notebooks/INDEX.md
  $ python3 tools/validate_notebooks.py | head -1
  ```
- **Expected output:**
  ```
  wrote INDEX.md rows=61
  2
  files=61 json_ok=61 nbformat4_ok=61 has_cells=61 ext_ok=61 dupe_groups=0
  ```
  (The 2 CONCEPTUAL rows are the Chapter 16 "code snippets" and Chapter 8
  "ADK Conceptual Example" files, whose own first cells say they are not
  runnable.)
- **Hasty-model trap:** the index will display `gemini-2.0-flash-exp`,
  `gpt4omini`, and other stale/broken model IDs, and you will want to
  "correct" them — either by hand-editing index rows or by editing the
  notebooks so the index looks better. The index reports what IS
  (`fact-discipline` rule 5, names and labels are claims); fixing the
  underlying IDs is Phase 2, gated on
  Q-003. If the index is embarrassing, it is working.
- **STOP conditions:** rows ≠ 61; re-running `build_index.py` twice produces
  a diff (generator must be deterministic).

### Step 4 — Commit, push, open PR with evidence appendix

- **Intent:** land the change with its proof attached.
- **Files:** none beyond steps 1–3.
- **Change:**
  ```
  git checkout -b notebook-restoration-phase-1   # if not already on a work branch
  git add tools/ notebooks/INDEX.md
  git commit -m "Restore notebook visibility: append .ipynb to 50 files, add validator and generated index

  Fixes FAILURE-LOG F4. Content untouched (all renames R100).
  Duplicates and content bugs deliberately excluded: gated on Q-001/Q-003."
  git push -u origin notebook-restoration-phase-1
  ```
  Open a draft PR whose description contains the full Evidence appendix.
- **Verify:**
  ```
  $ git status --porcelain | wc -l
  $ git show --pretty=format: --name-status | cut -f1 | sort | uniq -c
  ```
- **Expected output:**
  ```
  0
        3 A
       50 R100
  ```
- **Hasty-model trap:** writing the commit message as "updated" or "fixed
  notebooks" (the F4 commit was literally "agentic design added"). The
  message above states the countable facts; use it. Also: do not merge the
  PR yourself — Phase 1 is solo-executable but the merge is a human action
  per `handoff/docs/MODEL-ROUTING.md`.
- **STOP conditions:** any `R0xx` (non-identical rename) or any `M` line in
  the name-status output — both mean content changed, which this plan
  forbids.

## Rollback

At any step boundary before the commit: `git checkout -- . && git clean -fd tools/`
(renames are staged by `git mv`; `git reset --hard` from the work branch also
works). After push: delete the branch; nothing touches `main` until PR merge.

## Definition of done

- [ ] All four steps reported with pasted verification output matching expected.
- [ ] Draft PR open; description carries the full evidence appendix.
- [ ] `git show --pretty=format: --name-status | cut -f1 | sort | uniq -c`
      output pasted, showing exactly `3 A` + `50 R100` (proves nothing outside
      the file list changed — fact-discipline absence rule).
- [ ] `handoff/docs/MAINTENANCE.md` trigger honored: INDEX.md regenerated in
      the same PR as the renames it reflects.

## Evidence appendix (filled during execution)

*(empty — executor pastes verbatim outputs here, per step, in order)*

## Appendix A — the 50 files to rename (cross-check list, as of 2026-07-06)

Derived via `ls notebooks | grep -v '\.ipynb$'`. If `git ls-files` in step 2
renames a different count than 50, or touches a file not on this list, STOP.

```
Appendix C_
Appendix_ Pydantic
Chapter 10_ Model Context Protocol (ADK Agent Consuming FastMCP Server)
Chapter 10_ Model Context Protocol (FastMCP Server Example)
Chapter 10_ Model Context Protocol (__init__.py for FastMCP Client Agent)
Chapter 10_ Model Context Protocol (__init__.py for MCP Filesystem Example)
Chapter 10_ Model Context Protocol (agent.py for MCP Filesystem Example)
Chapter 12_ Exception Handling and Recovery (Agent with Fallback)
Chapter 13_ Human-in-the-Loop (Customer Support Agent with Personalization and Escalation)
Chapter 14_ Knowledge Retrieval (RAG  LangChain)
Chapter 14_ Knowledge Retrieval (RAG Google Search)
Chapter 14_ Knowledge Retrieval (RAG VertexAI)
Chapter 15_ Inter-Agent Communication (A2A AgentCard for an Agent acting as a WeatherBot)
Chapter 15_ Inter-Agent Communication (A2A)
Chapter 15_ Inter-Agent Communication (Synchronous and Streaming Requests)
Chapter 16_ Resource-Aware Optimization (OI and Google search)
Chapter 16_ Resource-Aware Optimization (code snippets)
Chapter 17_ Reasoning Techniques (Executing code)
Chapter 17_ Reasoning Techniques (Google DeepSearch)
Chapter 17_ Reasoning Techniques (Prompt with CoT for Agent)
Chapter 17_ Reasoning Techniques (Prompt with Self-correction with Agents)
Chapter 18_ Guardrails_Safety Patterns (ADK validate tool)
Chapter 18_ Guardrails_Safety Patterns (LLM as a Guardrail)
Chapter 18_ Guardrails_Safety Patterns (Practical Code Examples for Guardrails)
Chapter 18_ Guardrails_Safety Patterns (Practical Code Examples for Guardrails)(1)
Chapter 19_ Evaluation and Monitoring (Basic Agent Response Evaluation (Correctness_Relevance))
Chapter 19_ Evaluation and Monitoring (LLM as a Judge)
Chapter 1_ Prompt Chaining (Code Example)
Chapter 1_ Prompt Chaining (JSON example)
Chapter 20_ Prioritization (SuperSimplePM)
Chapter 21_ Chapter 21_ Exploration and Discovery(Agent Laboratory)
Chapter 2_ Routing (Google ADK Code Example)
Chapter 2_ Routing (LangGraph Code Example)
Chapter 2_ Routing (Openrouter example)
Chapter 3_ Parallelization (LangChain Code Example)
Chapter 4_ Reflection (ADK Code Example)
Chapter 4_ Reflection (Iterative Loop reflection)
Chapter 4_ Reflection (LangChain Code Example)
Chapter 5_ Tool Use (CrewAI Function Calling Example)
Chapter 5_ Tool Use (LangChain Code Example )
Chapter 6_ Planning - Code Example
Chapter 6_ Planning - Deep Research API  Example
Chapter 7_ Multi-Agent Collaboration - Code Example (CrewAI + Gemini)
Chapter 8_ Memory Management - Code Example (ADK Conceptual Example_ Explicit State Update via EventActions)
Chapter 8_ Memory Management - Code Example (ADK LlmAgent output_key Example)
Chapter 8_ Memory Management - Code Example (ADK MemoryService InMemory Example)
Chapter 8_ Memory Management - Code Example (ADK SessionService InMemory and Database)
Chapter 8_ Memory Management - Code Example (LangChain and LangGraph)
Chapter 9_ Adaptation - Code Example (OpenEvolve)
Copy of Chapter 8_ Memory Management - Code Example (LangChain and LangGraph)
```
