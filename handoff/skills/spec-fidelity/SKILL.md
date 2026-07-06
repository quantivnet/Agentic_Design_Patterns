---
name: spec-fidelity
description: Use when writing or editing code that mirrors an external API — SDK signatures, import paths, model IDs, endpoints, wire formats (ADK, LangChain, CrewAI, MCP, A2A, OpenAI/Gemini). Only from a captured spec, never memory; a failing contract test is never fixed by editing the assertion.
---

# Spec Fidelity

Justified by `handoff/FAILURE-LOG.md` F1 (`gpt4omini` typed from memory), F2
(removed Weaviate v3 API, deprecated import path), F3 (guessed ADK event
shape behind `hasattr` + hedge comment), F5 (undated model-ID drift). This
repo's code exists to teach external APIs — spec drift is the product being
wrong.

## Hard rules

1. **Captured spec or no code.** Any line mirroring an external API comes
   only from a capture in `specs/` (create on first use): source URL,
   version, retrieval date, verbatim excerpt of the signature/ID/schema.
   Confidence is memory, and memory produced `gpt4omini`.

2. **Model IDs are spec surface.** Introduce or change one only by citing a
   capture of the provider's current model list, dated. Never "upgrade" a
   model ID in passing.

3. **A failing contract test is never fixed by editing the assertion.**
   Sequence: re-capture spec from primary source → determine whether reality
   changed or code is wrong → if reality changed, update capture and code in
   the same commit. Weakening the assertion falsifies the instrument.

4. **Import paths and call shapes count** — `langchain_community` vs
   `langchain_openai`, sync vs async. No capture for the shape you're
   writing = stop and capture first.

5. **Uncertainty is a STOP, not a guard.** `hasattr` probes, broad
   `try/except`, "might trigger warning" comments around external calls are
   the F3 signature. Unknown attribute = blocked on a spec capture, not
   handled at runtime.

## Capture template (`specs/<library>-<topic>.md`)

```
# <library> <version> — <topic>
Source: <URL>
Captured: <YYYY-MM-DD> by <session/PR>
Verbatim excerpt:
> ...
Re-verify after: <date, default capture + 90 days> or any major release.
```
