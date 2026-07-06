import pytest

from pediatric_ot_assistant.client import OTAssistError
from pediatric_ot_assistant.generation import generate_document, serialize_case
from pediatric_ot_assistant.models import DocumentType, IntakeIssue, IntakeReport
from conftest import FakeOTClient


def test_case_data_reaches_prompt(maya, fake_client):
    generate_document(
        DocumentType.IEP_EVALUATION,
        serialize_case(maya),
        IntakeReport(),
        fake_client,
        "test-model",
    )
    call = fake_client.generate_calls[0]
    assert "Maya Rodriguez" in call["prompt"]
    assert "BOT-2" in call["prompt"]
    assert call["model"] == "test-model"
    assert "Never state, imply, or suggest a medical diagnosis" in call["system"]


def test_intake_warnings_injected(maya, fake_client):
    intake = IntakeReport(
        issues=[IntakeIssue(field="x", message="score sheet missing", severity="warning")]
    )
    generate_document(
        DocumentType.SUMMARY, serialize_case(maya), intake, fake_client, "m"
    )
    assert "score sheet missing" in fake_client.generate_calls[0]["prompt"]


def test_refusal_raises(maya):
    client = FakeOTClient(stop_reason="refusal")
    with pytest.raises(OTAssistError, match="declined"):
        generate_document(
            DocumentType.SUMMARY, serialize_case(maya), IntakeReport(), client, "m"
        )


def test_truncation_warns(maya):
    client = FakeOTClient(stop_reason="max_tokens")
    _, warnings = generate_document(
        DocumentType.SUMMARY, serialize_case(maya), IntakeReport(), client, "m"
    )
    assert any("truncated" in w for w in warnings)


def test_empty_output_raises(maya):
    client = FakeOTClient(document="   \n")
    with pytest.raises(OTAssistError, match="empty"):
        generate_document(
            DocumentType.SUMMARY, serialize_case(maya), IntakeReport(), client, "m"
        )
