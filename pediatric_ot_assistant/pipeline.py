"""Pipeline orchestration: intake -> redact -> generate -> review.

The client is injected so the stages can be exercised offline; anything
satisfying OTClient's two public methods (generate_text,
parse_structured) works.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from . import generation, intake as intake_mod, redaction, review as review_mod
from .client import OTAssistError, OTClient, default_model
from .models import CaseFile, DocumentType, IntakeReport, ReviewReport


class BlockingIntakeError(OTAssistError):
    def __init__(self, report: IntakeReport) -> None:
        self.report = report
        details = "\n".join(f"  - {i.field}: {i.message}" for i in report.blocking())
        super().__init__(
            "Required data is missing for this document type "
            "(rerun with --allow-missing to draft anyway, with gaps "
            f"flagged):\n{details}"
        )


class PHILeakError(OTAssistError):
    def __init__(self, leaked: list[str]) -> None:
        self.leaked = leaked
        super().__init__(
            "Redaction leak: the generated document contains identifying "
            f"tokens that should have been redacted: {', '.join(leaked)}. "
            "The document was NOT written."
        )


@dataclass
class PipelineResult:
    document: str
    intake: IntakeReport
    review: Optional[ReviewReport]
    token_map: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


def run(
    case: CaseFile,
    doc_type: DocumentType,
    client=None,
    *,
    model: Optional[str] = None,
    redact: Optional[bool] = None,
    allow_missing: bool = False,
    deep: bool = False,
    do_review: bool = True,
    verbose: bool = False,
) -> PipelineResult:
    client = client if client is not None else OTClient()
    model = model or default_model()
    warnings: list[str] = []

    # Stage 1: intake
    report = intake_mod.run_intake(case, doc_type)
    if report.blocking():
        if not allow_missing:
            raise BlockingIntakeError(report)
        for issue in report.issues:
            issue.severity = "warning"

    # Stage 2: redaction (deterministic, before any API call)
    redact = case.privacy.redact if redact is None else redact
    token_map: dict[str, str] = {}
    if redact:
        case, token_map = redaction.redact_case(case)

    case_block = generation.serialize_case(case)

    if deep:
        deep_report = intake_mod.deep_intake(case_block, doc_type, client, model)
        report.issues.extend(deep_report.issues)

    # Stage 3: generation
    document, gen_warnings = generation.generate_document(
        doc_type, case_block, report, client, model, verbose=verbose
    )
    warnings.extend(gen_warnings)

    def leak_check(text: str) -> None:
        if token_map:
            leaked = redaction.find_leaks(text, token_map)
            if leaked:
                raise PHILeakError(leaked)

    leak_check(document)

    # Stage 4: review, with a single revision attempt on blocking findings
    review_report: Optional[ReviewReport] = None
    if do_review:
        review_report = review_mod.review_document(
            document, case_block, doc_type, client, model
        )
        if review_report.blocking():
            notes = review_mod.findings_as_notes(review_report)
            document, gen_warnings = generation.generate_document(
                doc_type,
                case_block,
                report,
                client,
                model,
                verbose=verbose,
                revision_notes=notes,
            )
            warnings.extend(gen_warnings)
            leak_check(document)
            review_report = review_mod.review_document(
                document, case_block, doc_type, client, model
            )
            if review_report.blocking():
                warnings.append(
                    "The reviewer still reports blocking findings after one "
                    "revision — inspect the review notes carefully before "
                    "using this draft."
                )

    return PipelineResult(
        document=document,
        intake=report,
        review=review_report,
        token_map=token_map,
        warnings=warnings,
    )
