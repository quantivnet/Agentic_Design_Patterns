"""Case-file schema and structured pipeline models.

Nearly every field is optional so that partial case files load cleanly;
the intake stage (not pydantic) decides which gaps block which document
types.
"""

from __future__ import annotations

import datetime
from enum import Enum
from typing import Annotated, Literal, Optional

from pydantic import BaseModel, BeforeValidator, Field


def _coerce_date(value):
    # yaml.safe_load turns unquoted ISO dates into date objects; keep
    # everything as strings since real-world source data is messy.
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    return value


DateStr = Annotated[str, BeforeValidator(_coerce_date)]


class DocumentType(str, Enum):
    IEP_EVALUATION = "iep"
    PROGRESS_NOTE = "progress-note"
    TEACHER_CHECKLIST = "teacher-checklist"
    PARENT_HANDOUT = "parent-handout"
    SUMMARY = "summary"

    @property
    def description(self) -> str:
        return _DOCUMENT_DESCRIPTIONS[self]


_DOCUMENT_DESCRIPTIONS = {
    DocumentType.IEP_EVALUATION: (
        "Full IEP evaluation section: background, assessment methods, "
        "functional findings, interpretation, SMART goals, services, "
        "accommodations, and follow-up plan"
    ),
    DocumentType.PROGRESS_NOTE: (
        "Condensed session progress note: date, objectives, activities, "
        "outcomes, modifications, next steps"
    ),
    DocumentType.TEACHER_CHECKLIST: (
        "One-page teacher checklist: key accommodations, cueing hierarchy, "
        "materials required"
    ),
    DocumentType.PARENT_HANDOUT: (
        "Plain-language parent handout: home activities, purpose, safety "
        "notes, progress expectations"
    ),
    DocumentType.SUMMARY: "Bullet-point case summary",
}


class StudentProfile(BaseModel):
    name: str  # required — the redaction stage anchors on it
    dob: Optional[DateStr] = None
    grade: Optional[str] = None
    school: Optional[str] = None
    diagnoses: list[str] = Field(default_factory=list)
    medical_history: Optional[str] = None
    vision_hearing: Optional[str] = None
    parent_names: list[str] = Field(default_factory=list)
    teacher_name: Optional[str] = None


class StandardizedTest(BaseModel):
    name: str  # e.g. "BOT-2", "Sensory Profile 2"
    date: Optional[DateStr] = None
    scores: Optional[str] = None  # free text — score formats vary by instrument
    interpretation: Optional[str] = None


class AssessmentData(BaseModel):
    standardized_tests: list[StandardizedTest] = Field(default_factory=list)
    observations: Optional[str] = None
    functional_performance: Optional[str] = None  # handwriting, cutting, ADLs
    sensory_checklists: Optional[str] = None
    prior_iep_goals: Optional[str] = None
    work_sample_paths: list[str] = Field(default_factory=list)


class CaseContext(BaseModel):
    referral_reason: Optional[str] = None
    classroom_environment: Optional[str] = None
    teacher_concerns: Optional[str] = None
    parent_concerns: Optional[str] = None
    session_frequency: Optional[str] = None
    session_date: Optional[DateStr] = None  # for progress notes
    session_activities: Optional[str] = None  # for progress notes


class PrivacySettings(BaseModel):
    redact: bool = False
    extra_identifiers: list[str] = Field(default_factory=list)


class CaseFile(BaseModel):
    student: StudentProfile
    assessment: AssessmentData = Field(default_factory=AssessmentData)
    context: CaseContext = Field(default_factory=CaseContext)
    privacy: PrivacySettings = Field(default_factory=PrivacySettings)


class IntakeIssue(BaseModel):
    field: str
    message: str
    severity: Literal["blocking", "warning"]


class IntakeReport(BaseModel):
    issues: list[IntakeIssue] = Field(default_factory=list)

    def blocking(self) -> list[IntakeIssue]:
        return [i for i in self.issues if i.severity == "blocking"]

    def warnings(self) -> list[IntakeIssue]:
        return [i for i in self.issues if i.severity == "warning"]

    def to_prompt_block(self) -> str:
        """Render the report for injection into the generation prompt."""
        if not self.issues:
            return "No missing-data issues were detected during intake."
        lines = ["The following gaps were detected during intake:"]
        for issue in self.issues:
            lines.append(f"- ({issue.severity}) {issue.field}: {issue.message}")
        return "\n".join(lines)


class ReviewFinding(BaseModel):
    category: Literal[
        "smart_goal", "scope", "tone_reading_level", "missing_flagging", "other"
    ]
    severity: Literal["blocking", "advisory"]
    detail: str


class ReviewReport(BaseModel):
    passed: bool
    findings: list[ReviewFinding] = Field(default_factory=list)

    def blocking(self) -> list[ReviewFinding]:
        return [f for f in self.findings if f.severity == "blocking"]
