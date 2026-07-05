"""LLM self-check guardrail (reflection stage).

A second, structured call judges the draft against the SMART-goal,
scope, tone, and no-fabrication rules. Blocking findings trigger one
revision attempt in the pipeline; advisory findings are surfaced to the
operator.
"""

from __future__ import annotations

from .models import DocumentType, ReviewReport
from .prompts import load_prompt

_REVIEWER_SYSTEM = (
    "You are a strict quality reviewer for school-based pediatric "
    "occupational therapy documentation. You only report genuine problems."
)


def review_document(
    document: str,
    case_block: str,
    doc_type: DocumentType,
    client,
    model: str,
) -> ReviewReport:
    prompt = load_prompt("review").format(
        document_type=doc_type.value,
        document_description=doc_type.description,
        document=document,
        case_block=case_block,
    )
    return client.parse_structured(
        system=_REVIEWER_SYSTEM,
        prompt=prompt,
        output_model=ReviewReport,
        model=model,
    )


def findings_as_notes(report: ReviewReport) -> str:
    return "\n".join(
        f"- [{f.category}/{f.severity}] {f.detail}" for f in report.findings
    )
