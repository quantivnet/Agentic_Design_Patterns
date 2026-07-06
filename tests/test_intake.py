from pediatric_ot_assistant.intake import run_intake
from pediatric_ot_assistant.models import CaseFile, DocumentType


def test_complete_case_iep_no_blockers(maya):
    report = run_intake(maya, DocumentType.IEP_EVALUATION)
    assert report.blocking() == []


def test_sparse_case_iep_blocks(deshawn):
    report = run_intake(deshawn, DocumentType.IEP_EVALUATION)
    fields = [i.field for i in report.blocking()]
    assert "context.referral_reason" in fields


def test_sparse_case_summary_warns_only(deshawn):
    report = run_intake(deshawn, DocumentType.SUMMARY)
    assert report.blocking() == []
    assert report.warnings()  # missing referral reason


def test_progress_note_requires_session_data(maya):
    report = run_intake(maya, DocumentType.PROGRESS_NOTE)
    fields = [i.field for i in report.blocking()]
    assert "context.session_date" in fields
    assert "context.session_activities" in fields

    maya.context.session_date = "2026-06-01"
    maya.context.session_activities = "Handwriting warm-up, cutting practice."
    assert run_intake(maya, DocumentType.PROGRESS_NOTE).blocking() == []


def test_no_assessment_data_blocks_iep():
    case = CaseFile.model_validate(
        {
            "student": {"name": "Test Student"},
            "context": {"referral_reason": "Handwriting concerns."},
        }
    )
    report = run_intake(case, DocumentType.IEP_EVALUATION)
    assert any(i.field == "assessment" for i in report.blocking())


def test_test_without_scores_warns(maya):
    maya.assessment.standardized_tests[0].scores = None
    report = run_intake(maya, DocumentType.IEP_EVALUATION)
    assert any("without scores" in i.message for i in report.warnings())


def test_teacher_checklist_and_parent_handout_never_block(deshawn):
    for doc_type in (DocumentType.TEACHER_CHECKLIST, DocumentType.PARENT_HANDOUT):
        assert run_intake(deshawn, doc_type).blocking() == []


def test_missing_vision_hearing_warns_for_iep(maya):
    maya.student.vision_hearing = None
    report = run_intake(maya, DocumentType.IEP_EVALUATION)
    assert any(i.field == "student.vision_hearing" for i in report.warnings())
