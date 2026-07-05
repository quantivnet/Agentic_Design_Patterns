import pytest
from pydantic import ValidationError

from pediatric_ot_assistant.models import (
    CaseFile,
    DocumentType,
    IntakeIssue,
    IntakeReport,
)


def test_example_cases_round_trip(maya, deshawn):
    assert maya.student.name == "Maya Rodriguez"
    assert maya.student.dob == "2018-09-14"  # YAML date coerced to str
    assert len(maya.assessment.standardized_tests) == 2
    assert maya.assessment.standardized_tests[0].date == "2026-05-12"
    assert maya.privacy.redact is False

    assert deshawn.student.name == "DeShawn Taylor"
    assert deshawn.student.dob is None
    assert deshawn.privacy.redact is True
    assert deshawn.context.referral_reason is None


def test_minimal_case_valid():
    case = CaseFile.model_validate({"student": {"name": "Test Student"}})
    assert case.assessment.standardized_tests == []
    assert case.privacy.redact is False


def test_student_name_required():
    with pytest.raises(ValidationError):
        CaseFile.model_validate({"student": {"grade": "2"}})


def test_document_type_values():
    assert DocumentType("iep") is DocumentType.IEP_EVALUATION
    assert DocumentType("parent-handout") is DocumentType.PARENT_HANDOUT
    for doc_type in DocumentType:
        assert doc_type.description


def test_intake_report_helpers():
    report = IntakeReport(
        issues=[
            IntakeIssue(field="a", message="m1", severity="blocking"),
            IntakeIssue(field="b", message="m2", severity="warning"),
        ]
    )
    assert [i.field for i in report.blocking()] == ["a"]
    assert [i.field for i in report.warnings()] == ["b"]
    block = report.to_prompt_block()
    assert "m1" in block and "m2" in block


def test_intake_report_empty_prompt_block():
    assert "No missing-data issues" in IntakeReport().to_prompt_block()
