# Open Questions

Live gates. Per the `gated-scope` skill: work that depends on an OPEN entry is
refused outright — reported as `BLOCKED: gated on Q-NNN` — until `Answer:` is
filled with a verbatim quote, who said it, when, and where. Append-only;
answered questions stay for the record.

## Q-001 — Which Chapter 18 Guardrails file is canonical?

`Chapter 18_ Guardrails_Safety Patterns (Practical Code Examples for Guardrails)`
and its `(1)` twin have materially diverged (OpenAI vs Google provider,
different imports/logging — see FAILURE-LOG F6). Should one be deleted,
or both kept as named variants, and which?

- Raised: 2026-07-06 by departing-architect session. Blocks: any dedup,
  deletion, or merging of duplicate notebooks (including `Copy of ...` files).
- Answer: OPEN

## Q-002 — May files be renamed beyond appending `.ipynb`?

Candidates: the `Chapter 21_ Chapter 21_` stutter, trailing space in
`Chapter 5_ Tool Use (LangChain Code Example )`, the misleading `Copy of`
prefixes. The published book, its site, or readers' bookmarks may reference
exact current names.

- Raised: 2026-07-06 by departing-architect session. Blocks: any cosmetic
  renaming (flagship plan step 2 explicitly excludes it).
- Answer: OPEN

## Q-003 — Which framework versions does the book target?

The code references APIs current in early–mid 2025 (ADK pre/post-1.0
ambiguity, Weaviate v3 client, retired `gemini-2.0-flash-exp`). Should
notebooks be fixed *forward* to current library versions, or *pinned* to
book-era versions with a manifest, so they match the printed text?

- Raised: 2026-07-06 by departing-architect session. Blocks: any behavioral
  code change in `notebooks/`, including the F1 `gpt4omini` and F2 blob-URL
  fixes (the fix direction depends on the answer).
- Answer: OPEN
