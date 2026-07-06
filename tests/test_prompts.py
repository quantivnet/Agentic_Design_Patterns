import re

import pytest

from pediatric_ot_assistant.generation import render_prompt, serialize_case
from pediatric_ot_assistant.models import DocumentType, IntakeReport
from pediatric_ot_assistant.prompts import load_prompt

ALL_PROMPTS = [
    "system",
    "iep_evaluation",
    "progress_note",
    "teacher_checklist",
    "parent_handout",
    "summary",
    "intake_review",
    "review",
]


@pytest.mark.parametrize("name", ALL_PROMPTS)
def test_prompt_loads(name):
    assert load_prompt(name).strip()


@pytest.mark.parametrize("doc_type", list(DocumentType))
def test_document_templates_render_fully(doc_type, maya):
    prompt = render_prompt(
        doc_type,
        case_block=serialize_case(maya),
        intake_block=IntakeReport().to_prompt_block(),
    )
    # No unresolved {placeholders} may survive rendering
    assert not re.search(r"\{[a-z_]+\}", prompt), prompt


def test_system_prompt_contains_guardrails():
    system = load_prompt("system")
    for load_bearing in (
        "Never state, imply, or suggest a medical diagnosis",
        "prosthetics",
        "Never invent data",
        "Missing Information / Assumptions",
        "2–3 alternate goals",
        "[STUDENT]",
    ):
        assert load_bearing in system, load_bearing


def test_revision_notes_appended(maya):
    prompt = render_prompt(
        DocumentType.SUMMARY,
        case_block=serialize_case(maya),
        intake_block="none",
        revision_notes="- [scope/blocking] Implied a diagnosis.",
    )
    assert "Implied a diagnosis" in prompt
    assert "corrected draft" in prompt


def test_serialize_case_prunes_empty_and_excludes_privacy(deshawn):
    block = serialize_case(deshawn)
    assert "DeShawn Taylor" in block
    assert "privacy" not in block
    assert "null" not in block
    assert "dob" not in block  # empty field pruned
