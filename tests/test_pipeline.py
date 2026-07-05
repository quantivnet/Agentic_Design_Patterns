import pytest

from conftest import FakeOTClient
from pediatric_ot_assistant import pipeline
from pediatric_ot_assistant.models import (
    DocumentType,
    ReviewFinding,
    ReviewReport,
)


def test_happy_path(maya, fake_client):
    result = pipeline.run(
        maya, DocumentType.IEP_EVALUATION, client=fake_client, model="m"
    )
    assert result.document.startswith("# Occupational Therapy Evaluation")
    assert result.review is not None and result.review.passed
    assert result.token_map == {}  # maya's privacy.redact is False
    assert len(fake_client.generate_calls) == 1
    assert len(fake_client.parse_calls) == 1  # review only


def test_blocking_intake_raises(deshawn, fake_client):
    with pytest.raises(pipeline.BlockingIntakeError):
        pipeline.run(deshawn, DocumentType.IEP_EVALUATION, client=fake_client, model="m")
    assert fake_client.generate_calls == []  # no API call was made


def test_allow_missing_downgrades_and_injects(deshawn, fake_client):
    result = pipeline.run(
        deshawn,
        DocumentType.IEP_EVALUATION,
        client=fake_client,
        model="m",
        allow_missing=True,
    )
    assert result.intake.blocking() == []
    prompt = fake_client.generate_calls[0]["prompt"]
    # the downgraded gap is injected into the prompt as a warning
    assert "(warning) context.referral_reason" in prompt


def test_redacted_pipeline_never_sends_real_name(maya, fake_client):
    result = pipeline.run(
        maya,
        DocumentType.IEP_EVALUATION,
        client=fake_client,
        model="m",
        redact=True,
    )
    assert result.token_map
    for call in fake_client.generate_calls + fake_client.parse_calls:
        assert "Maya" not in call["prompt"]
        assert "Rodriguez" not in call["prompt"]
        assert "Lincoln" not in call["prompt"]
        assert "[STUDENT]" in call["prompt"]


def test_case_privacy_flag_enables_redaction(deshawn, fake_client):
    result = pipeline.run(
        deshawn,
        DocumentType.SUMMARY,
        client=fake_client,
        model="m",
    )
    assert result.token_map  # deshawn_t.yaml sets privacy.redact: true
    assert "DeShawn" not in fake_client.generate_calls[0]["prompt"]


def test_leak_detection(maya):
    leaky = FakeOTClient(document="# Report\n\nMaya attends Lincoln Elementary.\n")
    with pytest.raises(pipeline.PHILeakError) as excinfo:
        pipeline.run(
            maya, DocumentType.IEP_EVALUATION, client=leaky, model="m", redact=True
        )
    assert "Maya" in str(excinfo.value)


def test_blocking_review_triggers_one_revision(maya):
    failing_review = ReviewReport(
        passed=False,
        findings=[
            ReviewFinding(
                category="smart_goal",
                severity="blocking",
                detail="Goal lacks a measurable criterion.",
            )
        ],
    )
    client = FakeOTClient(structured=failing_review)
    result = pipeline.run(maya, DocumentType.IEP_EVALUATION, client=client, model="m")
    # generate, review(fail), regenerate with notes, re-review
    assert len(client.generate_calls) == 2
    assert len(client.parse_calls) == 2
    assert "measurable criterion" in client.generate_calls[1]["prompt"]
    assert any("blocking findings" in w for w in result.warnings)


def test_no_review_skips_review(maya, fake_client):
    result = pipeline.run(
        maya, DocumentType.IEP_EVALUATION, client=fake_client, model="m", do_review=False
    )
    assert result.review is None
    assert fake_client.parse_calls == []


def test_deep_intake_adds_warnings_only(maya, fake_client):
    from pediatric_ot_assistant.models import IntakeIssue, IntakeReport

    fake_client.structured = IntakeReport(
        issues=[IntakeIssue(field="assessment", message="No work sample.", severity="blocking")]
    )
    result = pipeline.run(
        maya,
        DocumentType.IEP_EVALUATION,
        client=fake_client,
        model="m",
        deep=True,
        do_review=False,
    )
    deep_issues = [i for i in result.intake.issues if i.message == "No work sample."]
    assert deep_issues and deep_issues[0].severity == "warning"
