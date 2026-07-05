"""Missing-data detection (intake stage).

A deterministic requirements matrix decides, per document type, which
gaps block generation and which are surfaced as warnings. Warnings are
also injected into the generation prompt so the drafted document's
"Missing Information" section matches what the operator saw.

An optional LLM pass (``deep_intake``) looks for qualitative gaps a
clinician would notice; it only ever adds warnings, never blockers.
"""

from __future__ import annotations

from .models import CaseFile, DocumentType, IntakeIssue, IntakeReport


def _issue(field: str, message: str, severity: str) -> IntakeIssue:
    return IntakeIssue(field=field, message=message, severity=severity)


def run_intake(case: CaseFile, doc_type: DocumentType) -> IntakeReport:
    issues: list[IntakeIssue] = []
    student, assessment, context = case.student, case.assessment, case.context

    has_evidence = bool(
        assessment.standardized_tests
        or assessment.observations
        or assessment.functional_performance
    )

    if doc_type == DocumentType.IEP_EVALUATION:
        if not context.referral_reason:
            issues.append(
                _issue(
                    "context.referral_reason",
                    "An IEP evaluation must document the reason for referral.",
                    "blocking",
                )
            )
        if not has_evidence:
            issues.append(
                _issue(
                    "assessment",
                    "No assessment data provided (standardized tests, "
                    "observations, or functional performance) — an IEP "
                    "evaluation cannot be drafted without at least one.",
                    "blocking",
                )
            )
        if not assessment.sensory_checklists:
            issues.append(
                _issue(
                    "assessment.sensory_checklists",
                    "No sensory processing checklist — sensory findings will "
                    "be limited to observation.",
                    "warning",
                )
            )
        if not assessment.prior_iep_goals:
            issues.append(
                _issue(
                    "assessment.prior_iep_goals",
                    "Prior IEP goals/services not provided (state 'initial "
                    "evaluation' in the case file if this is one).",
                    "warning",
                )
            )
        if not (context.teacher_concerns or context.parent_concerns):
            issues.append(
                _issue(
                    "context.teacher_concerns/parent_concerns",
                    "No teacher or parent concerns documented.",
                    "warning",
                )
            )
        if not context.session_frequency:
            issues.append(
                _issue(
                    "context.session_frequency",
                    "Current/planned session frequency not stated.",
                    "warning",
                )
            )

    elif doc_type == DocumentType.PROGRESS_NOTE:
        if not context.session_date:
            issues.append(
                _issue(
                    "context.session_date",
                    "A progress note requires the session date.",
                    "blocking",
                )
            )
        if not context.session_activities:
            issues.append(
                _issue(
                    "context.session_activities",
                    "A progress note requires a description of session "
                    "activities.",
                    "blocking",
                )
            )
        if not has_evidence:
            issues.append(
                _issue(
                    "assessment",
                    "No performance data to report outcomes against.",
                    "warning",
                )
            )

    elif doc_type == DocumentType.TEACHER_CHECKLIST:
        if not has_evidence:
            issues.append(
                _issue(
                    "assessment",
                    "No assessment data — accommodations will be generic.",
                    "warning",
                )
            )
        if not context.classroom_environment:
            issues.append(
                _issue(
                    "context.classroom_environment",
                    "Classroom environment not described — accommodations "
                    "cannot be tailored to the setting.",
                    "warning",
                )
            )
        if not context.referral_reason:
            issues.append(
                _issue(
                    "context.referral_reason",
                    "No referral reason to prioritize accommodations against.",
                    "warning",
                )
            )

    elif doc_type == DocumentType.PARENT_HANDOUT:
        if not has_evidence:
            issues.append(
                _issue(
                    "assessment",
                    "No assessment data — home activities will be generic.",
                    "warning",
                )
            )
        if not context.parent_concerns:
            issues.append(
                _issue(
                    "context.parent_concerns",
                    "Parent concerns not documented — the handout cannot "
                    "address them directly.",
                    "warning",
                )
            )

    elif doc_type == DocumentType.SUMMARY:
        if not context.referral_reason:
            issues.append(
                _issue(
                    "context.referral_reason",
                    "No referral reason provided.",
                    "warning",
                )
            )
        if not has_evidence:
            issues.append(
                _issue(
                    "assessment",
                    "No assessment data provided.",
                    "warning",
                )
            )

    # Cross-cutting checks
    for i, test in enumerate(assessment.standardized_tests):
        if not test.scores:
            issues.append(
                _issue(
                    f"assessment.standardized_tests[{i}].scores",
                    f"{test.name} is listed without scores — interpretation "
                    "will be qualitative only.",
                    "warning",
                )
            )
    if doc_type == DocumentType.IEP_EVALUATION:
        if not student.dob:
            issues.append(
                _issue(
                    "student.dob",
                    "Date of birth missing — standardized scores cannot be "
                    "verified against chronological age.",
                    "warning",
                )
            )
        if not student.grade:
            issues.append(
                _issue("student.grade", "Grade level missing.", "warning")
            )
        if not student.vision_hearing:
            issues.append(
                _issue(
                    "student.vision_hearing",
                    "Vision/hearing status not documented — required to rule "
                    "out sensory acuity contributions.",
                    "warning",
                )
            )

    return IntakeReport(issues=issues)


def deep_intake(case_block: str, doc_type: DocumentType, client, model: str) -> IntakeReport:
    """Optional LLM pass for qualitative gaps. Warnings only, by design."""
    from .models import IntakeReport as _IntakeReport
    from .prompts import load_prompt

    template = load_prompt("intake_review")
    prompt = template.format(
        document_type=doc_type.value,
        document_description=doc_type.description,
        case_block=case_block,
    )
    report = client.parse_structured(
        system="You are a meticulous school-based occupational therapy "
        "documentation reviewer.",
        prompt=prompt,
        output_model=_IntakeReport,
        model=model,
    )
    # An LLM must never be able to block generation.
    for issue in report.issues:
        issue.severity = "warning"
    return report
