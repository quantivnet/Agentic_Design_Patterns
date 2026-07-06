from pediatric_ot_assistant.redaction import (
    apply_tokens,
    build_token_map,
    find_leaks,
    redact_case,
)


def test_structured_fields_redacted(maya):
    redacted, token_map = redact_case(maya)
    assert redacted.student.name == "[STUDENT]"
    assert redacted.student.school == "[SCHOOL]"
    assert redacted.student.dob == "[DOB]"
    assert redacted.student.parent_names == ["[PARENT]"]
    assert redacted.student.teacher_name == "[TEACHER]"
    assert token_map


def test_free_text_redacted(maya):
    # maya_r.yaml intentionally repeats the name and school in the notes
    redacted, _ = redact_case(maya)
    observations = redacted.assessment.observations
    assert "Maya" not in observations
    assert "Lincoln" not in observations
    assert "[STUDENT]" in observations
    assert "[SCHOOL]" in observations


def test_possessive_and_first_name_variants():
    token_map = {"Maya Rodriguez": "[STUDENT]", "Maya": "[STUDENT]"}
    text = "Maya's grasp improved. maya was seated. Maya Rodriguez arrived."
    result = apply_tokens(text, token_map)
    assert result == (
        "[STUDENT]'s grasp improved. [STUDENT] was seated. [STUDENT] arrived."
    )


def test_longest_token_first():
    token_map = {"Maya": "[STUDENT]", "Maya Rodriguez": "[STUDENT]"}
    assert apply_tokens("Maya Rodriguez", token_map) == "[STUDENT]"


def test_initial_form_variant(maya):
    token_map = build_token_map(maya)
    assert apply_tokens("Maya R. participated.", token_map) == "[STUDENT] participated."


def test_dob_variants(maya):
    token_map = build_token_map(maya)
    for rendering in ("2018-09-14", "9/14/2018", "09/14/2018", "September 14, 2018"):
        assert apply_tokens(f"DOB {rendering}.", token_map) == "DOB [DOB].", rendering


def test_short_tokens_skipped():
    from pediatric_ot_assistant.models import CaseFile

    case = CaseFile.model_validate(
        {"student": {"name": "Al Smith"}, "privacy": {"redact": True}}
    )
    token_map = build_token_map(case)
    # "Al" is below the length threshold; must not appear as a token
    assert "Al" not in token_map
    assert "Al Smith" in token_map and "Smith" in token_map
    # "Al" inside ordinary words must survive
    assert "normally" in apply_tokens("normally", token_map)


def test_no_partial_word_matches(maya):
    token_map = build_token_map(maya)
    # "Carter" must not match inside "Cartersville"
    assert apply_tokens("Cartersville is a town.", token_map) == "Cartersville is a town."


def test_extra_identifiers(maya):
    maya.privacy.extra_identifiers = ["Mimi"]  # a nickname only in free text
    token_map = build_token_map(maya)
    assert apply_tokens("Mimi smiled.", token_map) == "[REDACTED_1] smiled."


def test_redaction_idempotent(maya):
    redacted_once, token_map = redact_case(maya)
    redacted_twice, _ = redact_case(redacted_once)
    assert redacted_twice.assessment.observations == redacted_once.assessment.observations


def test_find_leaks(maya):
    token_map = build_token_map(maya)
    assert find_leaks("A clean [STUDENT] document.", token_map) == []
    leaks = find_leaks("Maya attends Lincoln Elementary.", token_map)
    assert "Maya" in leaks
    assert "Lincoln Elementary" in leaks


def test_original_case_unmodified(maya):
    redact_case(maya)
    assert maya.student.name == "Maya Rodriguez"
