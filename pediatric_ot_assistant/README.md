# Pediatric OT Assistant

A drafting assistant for **school-based pediatric occupational therapists**. It turns a structured case file (student profile, assessment data, referral context) into draft documentation focused on fine motor skills and sensory processing:

| Format | Audience | Output |
|---|---|---|
| `iep` | Evaluation team | Full IEP evaluation section with SMART goals, services, accommodations |
| `progress-note` | Clinical record | Condensed session note |
| `teacher-checklist` | Teacher | One-page accommodations checklist with cueing hierarchy |
| `parent-handout` | Parents/caregivers | Plain-language home activities handout |
| `summary` | Any | Bullet-point case summary |

> **Disclaimer:** This tool produces *drafts only*. A licensed occupational therapist must review, edit, and approve every document before it is used. It does not make medical diagnoses and will not recommend devices outside school-based OT scope. All example data in this repository is fictional.

## Install

From the repository root:

```bash
pip install -e ".[dev]"
```

## Setup

Generation requires an Anthropic API key (see `.env.example` at the repo root):

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export OT_ASSIST_MODEL=claude-sonnet-5   # optional; this is the default
```

`ot-assist validate`, `ot-assist formats`, and the test suite run fully offline — no key needed.

## Quickstart

```bash
# List document types
ot-assist formats

# Validate a case file and see what's missing (offline)
ot-assist validate --case examples/cases/deshawn_t.yaml --format iep
# -> blocking issues listed, exit code 2 (no formal referral reason documented)

# The sparse case still supports a summary (with flagged gaps)
ot-assist generate --case examples/cases/deshawn_t.yaml --format summary

# Full IEP evaluation from the rich case, with PHI redaction
ot-assist generate --case examples/cases/maya_r.yaml --format iep --redact -o maya_iep.md

# Parent-facing handout (plain language)
ot-assist generate --case examples/cases/maya_r.yaml --format parent-handout
```

The document goes to stdout (or `-o FILE`); all diagnostics — intake warnings, the redaction map, reviewer findings — go to stderr, so output pipes cleanly.

## How it works

A four-stage pipeline (see `pipeline.py`), which also maps onto patterns from the book this repository accompanies:

1. **Intake** (`intake.py`) — a deterministic requirements matrix flags missing data per document type. Blocking gaps stop generation (override with `--allow-missing`, which turns them into flagged assumptions); warnings are injected into the prompt so the draft's "Missing Information" section matches reality. Optional `--deep-intake` adds an LLM pass for qualitative gaps (*input validation / guardrails*).
2. **Redaction** (`redaction.py`) — pure-code placeholder substitution (`[STUDENT]`, `[SCHOOL]`, `[DOB]`, …) applied to structured fields *and* free-text notes before anything is sent to the API, including name variants (first name, `First L.`, possessives) and multiple date renderings. After generation, a leak check scans the output for any original token and refuses to write the file if one appears (*deterministic tooling around the model*).
3. **Generation** (`generation.py`, `prompts/`) — one cached system prompt carries the invariant clinical rules (no diagnoses, no out-of-scope devices, SMART-goal structure, never invent data); one template per document type carries the section structure and audience tone (*prompt templating / routing by template*).
4. **Review** (`review.py`) — a second, structured LLM call judges the draft against the SMART/scope/tone/no-fabrication checklist. A blocking finding triggers exactly one revision attempt (*reflection*).

## Case file schema

Case files are YAML (comments and multiline notes welcome). See `examples/cases/` for complete examples.

| Section | Fields |
|---|---|
| `student` | `name` (required), `dob`, `grade`, `school`, `diagnoses[]`, `medical_history`, `vision_hearing`, `parent_names[]`, `teacher_name` |
| `assessment` | `standardized_tests[]` (`name`, `date`, `scores`, `interpretation`), `observations`, `functional_performance`, `sensory_checklists`, `prior_iep_goals` |
| `context` | `referral_reason`, `classroom_environment`, `teacher_concerns`, `parent_concerns`, `session_frequency`, `session_date`, `session_activities` |
| `privacy` | `redact` (bool), `extra_identifiers[]` |

Everything except `student.name` is optional — the intake stage decides per document type which gaps block and which merely warn.

## Privacy & redaction

Set `privacy.redact: true` in the case file (or pass `--redact`) and no real identifiers are sent to the API or written to output. The placeholder↔original map is printed to stderr for the operator only.

**Limitation:** redaction is deterministic, so a nickname or misspelling that appears *only* in free text and matches no structured field cannot be detected. Add such strings to `privacy.extra_identifiers`.

## Exit codes

`0` success · `1` runtime/API/case-file error · `2` blocking intake issues · `3` output-file collision (use `--force`) · `4` PHI leak detected (document not written)

## Testing

```bash
python -m pytest
```

The suite runs entirely offline against a fake client (the pipeline takes an injected client). One live end-to-end test runs only when `ANTHROPIC_API_KEY` is set.

## Troubleshooting

- **"No usable Anthropic credentials"** — set `ANTHROPIC_API_KEY` (see `.env.example`).
- **"The model declined to generate"** — check the case data for content outside school-based OT documentation scope.
- **Truncated output** — the document hit the token limit; trim the case data or generate a shorter format first.
