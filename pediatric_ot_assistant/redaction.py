"""Deterministic PHI redaction.

Runs entirely in code (no LLM) before any API call. Builds a map of
identifying tokens from the structured fields of a case file, then
replaces every occurrence — including occurrences buried inside
free-text fields such as observational notes — with bracketed
placeholders.

Known limitation: nicknames or misspellings that appear only in free
text and match no structured field cannot be detected deterministically.
Use ``privacy.extra_identifiers`` to scrub those.
"""

from __future__ import annotations

import re
from datetime import datetime

from .models import CaseFile

MIN_TOKEN_LENGTH = 3

_DATE_INPUT_FORMATS = ("%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y", "%B %d, %Y")


def _name_variants(full_name: str) -> list[str]:
    """Variants of a person's name likely to appear in free text."""
    variants = [full_name.strip()]
    parts = full_name.strip().split()
    if len(parts) >= 2:
        first, last = parts[0], parts[-1]
        variants.append(first)
        variants.append(last)
        variants.append(f"{first} {last[0]}.")  # "Maya R."
    return variants


def _date_variants(raw: str) -> list[str]:
    """Common renderings of a date, since notes often restate a DOB."""
    raw = raw.strip()
    variants = [raw]
    parsed = None
    for fmt in _DATE_INPUT_FORMATS:
        try:
            parsed = datetime.strptime(raw, fmt)
            break
        except ValueError:
            continue
    if parsed is not None:
        variants.extend(
            [
                parsed.strftime("%Y-%m-%d"),
                f"{parsed.month}/{parsed.day}/{parsed.year}",
                parsed.strftime("%m/%d/%Y"),
                f"{parsed.strftime('%B')} {parsed.day}, {parsed.year}",
            ]
        )
    return variants


def build_token_map(case: CaseFile) -> dict[str, str]:
    """Map each identifying token to its placeholder.

    Tokens shorter than MIN_TOKEN_LENGTH are skipped to avoid false hits
    (e.g. a middle initial matching inside ordinary words).
    """
    token_map: dict[str, str] = {}

    def add(tokens: list[str], placeholder: str) -> None:
        for token in tokens:
            token = token.strip()
            if len(token) >= MIN_TOKEN_LENGTH and token not in token_map:
                token_map[token] = placeholder

    student = case.student
    add(_name_variants(student.name), "[STUDENT]")
    if student.school:
        add([student.school], "[SCHOOL]")
    if student.dob:
        add(_date_variants(student.dob), "[DOB]")
    for i, parent in enumerate(student.parent_names):
        placeholder = "[PARENT]" if i == 0 else f"[PARENT_{i + 1}]"
        add(_name_variants(parent), placeholder)
    if student.teacher_name:
        add(_name_variants(student.teacher_name), "[TEACHER]")
    for i, identifier in enumerate(case.privacy.extra_identifiers):
        add([identifier], f"[REDACTED_{i + 1}]")

    return token_map


def _compile(token: str) -> re.Pattern[str]:
    # Lookarounds instead of \b so tokens ending in "." (e.g. "Maya R.")
    # still anchor correctly.
    return re.compile(rf"(?<!\w){re.escape(token)}(?!\w)", re.IGNORECASE)


def apply_tokens(text: str, token_map: dict[str, str]) -> str:
    """Replace every token in *text*, longest token first."""
    for token in sorted(token_map, key=lambda t: (-len(t), t)):
        text = _compile(token).sub(token_map[token], text)
    return text


def _redact_value(value, token_map: dict[str, str]):
    if isinstance(value, str):
        return apply_tokens(value, token_map)
    if isinstance(value, list):
        return [_redact_value(v, token_map) for v in value]
    if isinstance(value, dict):
        return {k: _redact_value(v, token_map) for k, v in value.items()}
    return value


def redact_case(case: CaseFile) -> tuple[CaseFile, dict[str, str]]:
    """Return a new CaseFile with all identifying tokens replaced.

    The returned token map (original token -> placeholder) is for the
    operator's reference and for the post-generation leak check; it must
    never be written into the generated document.
    """
    token_map = build_token_map(case)
    data = _redact_value(case.model_dump(), token_map)
    return CaseFile.model_validate(data), token_map


def find_leaks(text: str, token_map: dict[str, str]) -> list[str]:
    """Return original tokens that appear in *text* (should be empty)."""
    return sorted(token for token in token_map if _compile(token).search(text))
