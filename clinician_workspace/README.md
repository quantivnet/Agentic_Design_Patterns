# Clinician Workspace — Setup

A ready-to-use Claude workspace for school-based pediatric OT documentation. Copy this whole `clinician_workspace/` folder anywhere on your machine and open it with Claude — every session starts pre-configured; nothing to paste.

## What's inside

| Path | Purpose |
|---|---|
| `CLAUDE.md` | **Starting context** — loaded automatically when a session opens in this folder: your role, the standing clinical/privacy rules, and how each session should begin |
| `.claude/skills/school-ot-docs/` | **The skill** — intake-check workflow, SMART-goal rules, and exact per-document formats (loaded on demand via `references/`) |
| `cases/_intake_template.md` | Fill-in case template (redact before filling — placeholders only) |
| `cases/example_student.md` | Worked fictional example |
| `output/` | Save finished drafts here |

## How to use it

**Claude Code / Claude Desktop (Cowork):** open this folder as your project and start a session. `CLAUDE.md` loads automatically; the `school-ot-docs` skill activates whenever you ask for any OT document. Say: *"New case — 2nd grader, handwriting referral. Here's my data…"* or *"Draft the IEP evaluation for cases/student_ab.md."*

**claude.ai (web/mobile):** create a Project, add `CLAUDE.md`'s content as the project's custom instructions, and upload the skill (zip the `school-ot-docs/` folder and add it under Settings → Capabilities → Skills, if available on your plan). Or simply attach `SKILL.md` + the relevant `references/` file to a chat.

## The workflow in every session

1. You say which student and which document (IEP evaluation, progress note, teacher checklist, parent handout, or summary).
2. Claude runs an **intake check** — what data it has, what's missing (blocking vs. helpful) — and waits for your go-ahead.
3. Claude drafts in the exact format; you revise conversationally ("3 alternates for goal 2, less support").
4. Save the draft to `output/`, then swap placeholders back to real names **in your own editor** — never in the chat.

> **Every document is a draft.** You review, edit, and sign everything. Claude never diagnoses, never recommends prescription devices (it refers to a physician instead), and flags anything it doesn't know rather than inventing it.
