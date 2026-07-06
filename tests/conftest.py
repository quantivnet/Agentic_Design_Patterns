from pathlib import Path

import pytest
import yaml

from pediatric_ot_assistant.client import GenerationResult
from pediatric_ot_assistant.models import CaseFile, ReviewReport

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = REPO_ROOT / "examples" / "cases"

CANNED_DOCUMENT = (
    "# Occupational Therapy Evaluation\n\n"
    "## Background and Reason for Referral\n\n"
    "The student was referred for fine motor concerns.\n"
)


class FakeOTClient:
    """Offline stand-in for OTClient. Records every prompt it receives."""

    def __init__(self, document=CANNED_DOCUMENT, structured=None, stop_reason="end_turn"):
        self.document = document
        self.structured = structured if structured is not None else ReviewReport(passed=True)
        self.stop_reason = stop_reason
        self.generate_calls: list[dict] = []
        self.parse_calls: list[dict] = []

    def generate_text(self, system, prompt, model, max_tokens=8000, verbose=False):
        self.generate_calls.append(
            {"system": system, "prompt": prompt, "model": model}
        )
        return GenerationResult(text=self.document, stop_reason=self.stop_reason)

    def parse_structured(self, system, prompt, output_model, model, max_tokens=2000):
        self.parse_calls.append(
            {"system": system, "prompt": prompt, "output_model": output_model, "model": model}
        )
        return self.structured


def load_example(name: str) -> CaseFile:
    data = yaml.safe_load((EXAMPLES / name).read_text(encoding="utf-8"))
    return CaseFile.model_validate(data)


@pytest.fixture
def maya() -> CaseFile:
    return load_example("maya_r.yaml")


@pytest.fixture
def deshawn() -> CaseFile:
    return load_example("deshawn_t.yaml")


@pytest.fixture
def fake_client() -> FakeOTClient:
    return FakeOTClient()
