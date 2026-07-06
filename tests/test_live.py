"""One live end-to-end call. Skipped unless ANTHROPIC_API_KEY is set."""

import os

import pytest

from pediatric_ot_assistant import pipeline
from pediatric_ot_assistant.models import DocumentType

pytestmark = pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"), reason="no ANTHROPIC_API_KEY"
)


def test_live_summary_redacted(maya):
    result = pipeline.run(maya, DocumentType.SUMMARY, redact=True)
    assert result.document.strip()
    assert "Maya" not in result.document
    assert "[STUDENT]" in result.document
    assert result.review is not None
