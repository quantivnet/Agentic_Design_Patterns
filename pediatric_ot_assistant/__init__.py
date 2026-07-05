"""Documentation assistant for school-based pediatric occupational therapists.

Drafts IEP evaluation sections, progress notes, teacher checklists, parent
handouts, and case summaries from structured case files, with missing-data
flagging, PHI redaction, and an LLM review pass.

All output is a draft: a licensed occupational therapist must review, edit,
and approve every document before use.
"""

__version__ = "0.1.0"

from .models import (
    AssessmentData,
    CaseContext,
    CaseFile,
    DocumentType,
    IntakeIssue,
    IntakeReport,
    PrivacySettings,
    ReviewFinding,
    ReviewReport,
    StandardizedTest,
    StudentProfile,
)
from .pipeline import PipelineResult, run

__all__ = [
    "AssessmentData",
    "CaseContext",
    "CaseFile",
    "DocumentType",
    "IntakeIssue",
    "IntakeReport",
    "PipelineResult",
    "PrivacySettings",
    "ReviewFinding",
    "ReviewReport",
    "StandardizedTest",
    "StudentProfile",
    "run",
]
