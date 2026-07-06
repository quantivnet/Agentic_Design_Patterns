# Failure Log

Append-only register of documented failures in this repository. Every rule in
`handoff/skills/` exists because of an entry here; a skill may not be edited
without citing (or adding) an entry. Each entry carries a verification command
so a successor can re-confirm the evidence instead of trusting this file.

All evidence gathered **as of 2026-07-06** against commit `41e082a`
(`Update README.md`, tip of `main`). If `main` has moved, re-run the
verification commands before citing an entry.

---

## F1 — Invalid model ID typed from memory

**What happened:** `notebooks/Chapter 21_ Chapter 21_ Exploration and
Discovery(Agent Laboratory)` references the model `"gpt4omini"` (twice). That
string is not, and never was, a valid OpenAI model ID (`gpt-4o-mini` is). Any
run of that example fails at the first API call. It was written from memory of
the spec, not from the spec.

**Verify** (note: notebook files are single-line JSON, so count occurrences
with `grep -o`, never lines with `grep -c`):
```
grep -o 'gpt4omini' 'notebooks/Chapter 21_ Chapter 21_ Exploration and Discovery(Agent Laboratory)' | wc -l
# expected: 2
```

**Motivates:** `spec-fidelity`.

---

## F2 — RAG example ingests an HTML page and calls it a corpus

**What happened:** `notebooks/Chapter 14_ Knowledge Retrieval (RAG  LangChain)`
downloads its corpus from
`https://github.com/langchain-ai/langchain/blob/master/docs/docs/how_to/state_of_the_union.txt`
— the GitHub **web page** (HTML), not the raw file
(`raw.githubusercontent.com/...`). The vector store is therefore built over
GitHub's page markup. The example "works" in the sense that it prints output,
which is exactly why nobody caught it: the first step of the pipeline was
never verified, only the last.

The same file also uses `weaviate.Client(...)` and
`langchain_community.embeddings.OpenAIEmbeddings` — the Weaviate v3 client API
(removed in `weaviate-client` v4, released March 2024) and an import path
LangChain deprecated in favor of `langchain_openai`. As of 2026-07-06 a fresh
`pip install` of these libraries cannot run this cell.

**Verify:**
```
grep -c 'github.com/langchain-ai/langchain/blob' 'notebooks/Chapter 14_ Knowledge Retrieval (RAG  LangChain)'
# expected: 1  (a raw.githubusercontent.com URL would be correct)
grep -c 'weaviate.Client' 'notebooks/Chapter 14_ Knowledge Retrieval (RAG  LangChain)'
# expected: 1
```

**Motivates:** `executing-plans` (verify each step's actual output, not the
pipeline's willingness to print something), `spec-fidelity`.

---

## F3 — Hedge comments instead of verification

**What happened:** `notebooks/Chapter 2_ Routing (Google ADK Code Example)`
calls `runner.session_service.create_session(...)` synchronously (an async
coroutine in ADK ≥ 1.0 — as of 2026-07-06 this returns an un-awaited
coroutine, so no session is created) and probes `event.content.text` behind
`hasattr`, with the literal comment *"might trigger warning"*. The author was
unsure whether the attribute exists and shipped the uncertainty as a runtime
guard plus a hedge comment, instead of running the code once and finding out.
"It should work" made it into print.

**Verify:**
```
grep -c 'might trigger warning' 'notebooks/Chapter 2_ Routing (Google ADK Code Example)'
# expected: 1
grep -c 'await.*create_session' 'notebooks/Chapter 2_ Routing (Google ADK Code Example)'
# expected: 0, with grep exit code 1  (the call is never awaited)
```

**Motivates:** `executing-plans` ("should pass" is banned), `spec-fidelity`.

---

## F4 — 50 of 61 notebooks are invisible

**What happened:** every file in `notebooks/` is valid Jupyter notebook JSON
(nbformat 4), but 50 of 61 lack the `.ipynb` extension. GitHub renders none of
them; editors don't open them as notebooks; `jupyter` won't list them. The
repo's entire code payload is effectively unbrowsable, and this shipped in a
bulk commit (`653ba6a agentic design added`) that nobody could have reviewed
file-by-file. A one-command check (`python3 -m json.tool` per file, or the
validator in `handoff/tools-staging/`) would have surfaced it.

**Verify:**
```
ls notebooks | grep -vc '\.ipynb$'
# expected: 50   (before the restoration plan runs; 0 after — plus INDEX.md once generated)
```

**Motivates:** `executing-plans`; also the flagship plan
(`handoff/plans/2026-07-notebook-restoration-phase-1.md`).

---

## F5 — Model-ID drift with no as-of dates

**What happened:** the corpus references 17 distinct model-ID strings,
including `gemini-2.0-flash-exp` in 10+ files (an experimental alias Google
has since retired) and `gemini-1.5-flash-latest` / `gemini-1.5-pro-latest`
(the 1.5 line was deprecated for new projects in 2025). None of these carries
any record of when it was known-valid, so a reader in 2026 cannot tell "this
worked in early 2025" from "this is current." A claim about what a provider
serves *today* was written as if timeless.

**Verify:**
```
grep -ohE '(gemini|gpt|claude)[- ]?[a-zA-Z0-9._-]+' notebooks/* | sort | uniq -c | sort -rn | head -5
# expected (as of 2026-07-06):
#      18 gemini-2.0-flash
#      15 gemini-2.0-flash-exp
#       9 gpt-4o
#       6 gpt-4o-mini
#       3 gemini-2.5-flash
```

**Motivates:** `fact-discipline` (every claim gets a source and an as-of
date), `spec-fidelity` (model IDs are spec surface).

---

## F6 — Filenames that assert falsehoods; duplicates edited while "which is canonical" stayed open

**What happened, part 1:** `notebooks/Copy of Chapter 8_ Memory Management -
Code Example (LangChain and LangGraph)` is **not** a copy of the Chapter 8
LangChain file — it contains entirely different content (a
`VertexAiMemoryBankService` snippet). The filename makes a factual claim the
content disproves.

**What happened, part 2:** `Chapter 18_ ... (Practical Code Examples for
Guardrails)` and its `(1)` twin began as one file and were then *both* edited
— they now differ in LLM provider (OpenAI vs Google), imports, and logging
setup. The question "which one is canonical?" was never answered; work
proceeded on both anyway, and now neither can be deleted safely without the
author. A "pending confirmation" state hardened into permanent divergence.

**What happened, part 3:** `Chapter 16_ ... (code snippets)` opens with
*"Conceptual Python-like structure, not runnable code"* — but nothing in the
filename or any index distinguishes it from runnable examples.

**Verify:**
```
grep -c 'VertexAiMemoryBankService' 'notebooks/Copy of Chapter 8_ Memory Management - Code Example (LangChain and LangGraph)'
# expected: 1
diff <(python3 -c "import json;print(''.join(json.load(open('notebooks/Chapter 18_ Guardrails_Safety Patterns (Practical Code Examples for Guardrails)'))['cells'][0]['source']))") \
     <(python3 -c "import json;print(''.join(json.load(open('notebooks/Chapter 18_ Guardrails_Safety Patterns (Practical Code Examples for Guardrails)(1)'))['cells'][0]['source']))") | wc -l
# expected: non-zero (they have materially diverged)
```

**Motivates:** `gated-scope` (part 2), `fact-discipline` (parts 1 and 3).

---

## F7 — Predicted expected-output written into the handoff itself (near-miss, caught)

**What happened:** while authoring this handoff (2026-07-06 session), the F1
verification was first drafted as `grep -c 'gpt4omini' ... # expected: 2` —
the count *predicted* from memory of an earlier occurrence scan. Notebook
files are single-line JSON, so `grep -c` (which counts lines) returns 1. The
wrong expectation was caught only because every published command was re-run
verbatim before commit. The same session's `build_index.py` first shipped a
framework scanner whose word-boundary regex missed `langchain_openai`-style
imports — visible only by reading the generated output, not the code. Both
are the F1–F3 failure mode aimed at our own instruments: a verification
artifact is just as capable of mirroring memory instead of reality as the
code it checks.

**Verify** (the shape trap that made the prediction wrong):
```
awk 'END{print NR}' 'notebooks/Chapter 1_ Prompt Chaining (Code Example)'
# expected: 1   (every notebook is single-line JSON; line-based counts lie)
```

**Motivates:** `fact-discipline` (captured-not-predicted rule),
`context-economy`.

---

## How to add an entry

Append below this line; never rewrite or delete an existing entry (strike
through with a dated correction note if one proves wrong). An entry needs:
what happened, a verification command with expected output, an as-of date,
and which skill(s) it motivates.
