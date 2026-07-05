"""Document generation: case serialization, template rendering, LLM call."""

from __future__ import annotations

import yaml

from .client import OTAssistError
from .models import CaseFile, DocumentType, IntakeReport
from .prompts import load_prompt

_TEMPLATE_NAMES = {
    DocumentType.IEP_EVALUATION: "iep_evaluation",
    DocumentType.PROGRESS_NOTE: "progress_note",
    DocumentType.TEACHER_CHECKLIST: "teacher_checklist",
    DocumentType.PARENT_HANDOUT: "parent_handout",
    DocumentType.SUMMARY: "summary",
}


def _prune(value):
    """Drop empty fields so the prompt contains only real data."""
    if isinstance(value, dict):
        pruned = {k: _prune(v) for k, v in value.items()}
        return {k: v for k, v in pruned.items() if v not in (None, "", [], {})}
    if isinstance(value, list):
        return [_prune(v) for v in value if v not in (None, "", [], {})]
    return value


def serialize_case(case: CaseFile) -> str:
    data = _prune(case.model_dump(exclude={"privacy"}))
    dumped = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=80)
    return f"```yaml\n{dumped}```"


def render_prompt(
    doc_type: DocumentType,
    case_block: str,
    intake_block: str,
    revision_notes: str | None = None,
) -> str:
    template = load_prompt(_TEMPLATE_NAMES[doc_type])
    prompt = template.format(case_block=case_block, intake_block=intake_block)
    if revision_notes:
        prompt += (
            "\n\nA reviewer found the following problems in a previous draft. "
            "Produce a corrected draft that fixes every one of them:\n\n"
            f"{revision_notes}\n"
        )
    return prompt


def generate_document(
    doc_type: DocumentType,
    case_block: str,
    intake: IntakeReport,
    client,
    model: str,
    verbose: bool = False,
    revision_notes: str | None = None,
) -> tuple[str, list[str]]:
    """Return (document_markdown, warnings)."""
    system = load_prompt("system")
    prompt = render_prompt(doc_type, case_block, intake.to_prompt_block(), revision_notes)
    result = client.generate_text(
        system=system, prompt=prompt, model=model, verbose=verbose
    )
    warnings: list[str] = []
    if result.stop_reason == "refusal":
        raise OTAssistError(
            "The model declined to generate this document. Review the case "
            "data for content outside school-based OT documentation scope."
        )
    if result.stop_reason == "max_tokens":
        warnings.append(
            "Output was truncated at the token limit — the document is "
            "incomplete. Consider trimming the case data or generating a "
            "shorter format (e.g. summary) first."
        )
    if not result.text.strip():
        raise OTAssistError("The model returned an empty document.")
    return result.text, warnings
