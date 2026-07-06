# Clinician Handoff — Using Your AI Documentation Assistant

This guide is for the occupational therapist. It explains how to run your documentation assistant in any capable AI chat session (Claude is recommended) with no software to install. You need two things, both in this folder:

1. **`OT_ASSISTANT_PROMPT.md`** — the master prompt that turns a blank AI session into your assistant.
2. **This guide** — the workflow, the case intake template, and the privacy rules.

> **The one rule that matters most:** every document the AI produces is a **draft**. You review, edit, and sign everything. The assistant is a writing aid for your clinical reasoning — it is not a clinician, and its output is not clinical judgment.

---

## Quick start (5 steps)

1. **Open a new AI session** (e.g., claude.ai → new chat). Use a fresh chat per student to avoid mixing cases.
2. **Paste the master prompt** — everything below the divider line in `OT_ASSISTANT_PROMPT.md` — as your first message. The assistant will confirm and ask for your first case.
3. **Fill in the Case Intake Template** (below) and paste it. **Redact identifying details first** — see Privacy, next section.
4. **Read the intake check.** The assistant will tell you what's missing before drafting. Supply what you can, or say "draft anyway" to proceed with gaps flagged.
5. **Ask for the document you need** — "full IEP evaluation," "progress note," "teacher checklist," "parent handout," or "summary" — then revise in conversation: *"give me 2 easier alternates for goal 1," "make the parent handout shorter," "swap the slant board for something cheaper."*

---

## Privacy — read before your first case

Anything you paste into an AI chat leaves your device. Unless your district has an agreement covering AI use with student records (e.g., an enterprise/education deployment with appropriate terms), **do not paste identifiable student information**. Work with placeholders:

| Replace | With |
|---|---|
| Student's name (all forms: full, first, "Maya R.", possessives) | `[STUDENT]` |
| Date of birth (any format) | `[DOB]` — you can keep age, e.g. "age 7" |
| School name | `[SCHOOL]` |
| Parent/guardian names | `[PARENT]` |
| Teacher's name | `[TEACHER]` |
| Any other identifying detail (siblings, address, nicknames) | `[REDACTED]` |

The master prompt instructs the assistant to preserve these placeholders exactly, so the finished draft comes back with `[STUDENT]` throughout. Do the find-and-replace to real names **in your own document editor, after the draft leaves the AI session**.

Double-check free-text notes before pasting — names hide inside observation notes ("…Maya's grip fatigued…") far more often than in the profile fields.

---

## Case Intake Template

Copy, fill in what you have, delete what you don't. Partial is fine — the assistant will tell you what's missing and how much it matters.

```
CASE DATA

Student profile
- Student: [STUDENT], age ___, grade ___
- School: [SCHOOL]
- Documented diagnoses (with source): ___
- Relevant medical history: ___
- Vision/hearing status (and screening dates): ___

Referral & context
- Reason for referral: ___
- Classroom environment (class size, seating, writing demands): ___
- Teacher concerns: ___
- Parent concerns: ___
- Current/planned session frequency: ___

Standardized assessments (repeat per test)
- Test name & date: ___
- Scores: ___
- Interpretation notes: ___

Observations (setting, task, what you saw): ___

Functional performance
- Handwriting: ___
- Cutting/scissor skills: ___
- ADLs (fasteners, feeding, materials management): ___

Sensory processing (checklist results and/or observed behaviors): ___

Prior IEP goals & services (or "initial evaluation"): ___

For progress notes only
- Session date: ___
- Objectives targeted: ___
- Activities & data collected: ___
```

---

## What the assistant will and won't do

**It will:** structure your data into the five document formats; write measurable SMART goals with 2–3 ranked alternates per need; suggest specific adaptive equipment (with specs, rationale, expected benefit) and classroom accommodations; write parent/teacher materials in plain language; flag every data gap instead of papering over it.

**It won't (by design):** state or imply medical diagnoses; recommend prescription devices, prosthetics, or orthotics (it will suggest a physician/specialist referral instead); invent scores, dates, or history. If it ever does any of these, that's a defect — delete the content and rephrase your request.

**Trust but verify — your review checklist before anything leaves your desk:**
- [ ] Every score, date, and history detail matches your records (AI can transcribe wrong even when told not to invent)
- [ ] Goals are ones YOU would write — measurable, appropriate, achievable for this student
- [ ] Equipment/accommodation suggestions are appropriate, available, and within district practice
- [ ] The "Missing Information / Assumptions" section is resolved or acceptable
- [ ] Nothing implies a diagnosis or out-of-scope recommendation
- [ ] Placeholders are swapped back to real names (in your editor, not the chat)

---

## Tips that improve output quality

- **One student per chat.** Start fresh for each case; long multi-student chats degrade accuracy.
- **Paste raw observation notes.** Your unpolished jotted notes produce better drafts than summaries — the assistant is good at organizing; only you know what happened.
- **Ask for alternates freely.** "Give me 3 versions of that goal at different support levels" is exactly what it's for.
- **Push back.** If a goal is unmeasurable or a recommendation feels off-scope, say so — "goal 2 has no criterion, fix it."
- **Reuse the session for the family.** After the IEP draft, "now the parent handout" in the same chat produces consistent documents from the same data.

---

*The example below shows what a filled intake looks like (fictional data, already redacted):*

```
CASE DATA

Student profile
- Student: [STUDENT], age 7, grade 2
- School: [SCHOOL]
- Documented diagnoses (with source): Developmental coordination disorder (developmental pediatrician, 2025)
- Vision/hearing status: vision corrected with glasses (exam 11/2025); hearing WNL (screened 10/2025)

Referral & context
- Reason for referral: teacher referral for handwriting legibility, hand fatigue,
  and movement-seeking behaviors interfering with written work completion
- Teacher concerns: written output far below peers; often out of seat during seatwork
- Parent concerns: avoids coloring/drawing at home; frustrated by writing homework

Standardized assessments
- BOT-2, 5/12/2026: Fine Manual Control composite SS 38 (below average);
  Fine Motor Precision 9, Fine Motor Integration 10, Manual Dexterity 8
- Sensory Profile 2 (teacher form), 5/15/2026: Seeking – Much More Than Others;
  Registration – More Than Others; Body Position – More Than Others; Touch – typical

Observations: static tripod grasp with heavy pressure, breaks pencil tips; letter
formation inconsistent, b/d reversals 4/10 words; fatigues after ~5 min writing,
rocks in chair, chews sleeve; choppy scissor strokes, rotates paper only with cues

Functional performance
- Handwriting: writes first name legibly; copies from board slowly, loses place
- Cutting: straight lines with mild deviation; curves not yet accurate
- ADLs: zippers independent; buttons with moderate assist

Prior IEP goals & services: initial evaluation
```
