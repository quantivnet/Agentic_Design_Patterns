---
name: spec-fidelity
description: Use whenever writing or editing code that mirrors an external API — SDK call signatures, import paths, model IDs, endpoint URLs, wire formats (ADK, LangChain, CrewAI, MCP, A2A, OpenAI/Gemini APIs). Such code may only come from a captured spec, never from memory; a failing contract test is never fixed by editing the assertion.
---

# Spec Fidelity

## Why this skill exists (documented failure)

`handoff/FAILURE-LOG.md` **F1**: `"gpt4omini"` — a model ID that has never
existed — was typed from memory into Chapter 21 and shipped. **F2**: Chapter
14 uses the Weaviate v3 client API and a deprecated LangChain import path;
neither installs-and-runs today. **F3**: Chapter 2 guesses at the ADK event
API behind a `hasattr` and a hedge comment. **F5**: 17 distinct model-ID
strings drift across the corpus with no record of when any was valid. Every
one of these is the same failure: *mirroring an external surface from memory.*
This repo's code exists to teach external APIs — spec drift is not a nuisance
here, it is the product being wrong.

## Hard rules

1. **Captured spec or no code.** Any line that mirrors an external API may
   only be written from a capture in `specs/` (create the directory on first
   use). A capture is a markdown file recording: source URL, library/API
   version, retrieval date, and a *verbatim* excerpt of the relevant
   signature/ID list/schema. "I'm confident about this API" is memory, and
   memory is what produced `gpt4omini`.

2. **Model IDs are spec surface.** A model ID may only be introduced or
   changed by citing a capture of the provider's current model list, with
   as-of date. Never "upgrade" a model ID in passing while editing a file for
   another reason.

3. **A failing contract test is never fixed by editing the assertion.** If a
   check that encodes external behavior fails, the sequence is: re-capture
   the spec from the primary source → determine whether reality changed or
   the code is wrong → if reality changed, update the capture *and* the code
   in the same commit, citing the new capture. Weakening the assertion so the
   suite goes green is falsifying the instrument.

4. **Import paths and call shapes count.** `from langchain_community.embeddings
   import OpenAIEmbeddings` vs `from langchain_openai import OpenAIEmbeddings`
   is a spec question (see F2), as is sync-vs-async (`create_session`, F3).
   If you cannot cite a capture for the shape you are writing, stop and
   capture first.

5. **Uncertainty is expressed as a STOP, not a guard.** `hasattr(...)` probes,
   broad `try/except`, and comments like "might trigger warning" around an
   external call are the F3 signature. If you don't know whether the
   attribute exists, the task is blocked on a spec capture, not on a runtime
   guard.

## Capture template (`specs/<library>-<topic>.md`)

```
# <library> <version> — <topic>
Source: <URL>
Captured: <YYYY-MM-DD> by <session/PR>
Verbatim excerpt:
> ...
Re-verify after: <date, default capture + 90 days> or any major release.
```
