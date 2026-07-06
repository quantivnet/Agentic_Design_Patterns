# Maintenance Rules

Every artifact in this handoff names the trigger that forces its refresh. An
artifact whose trigger fires and isn't refreshed is stale, and stale
infrastructure is worse than none — it lends tier-nothing claims the smell of
authority (`fact-discipline`).

| Artifact | Refresh trigger | Refresh action | Verify |
|---|---|---|---|
| `notebooks/INDEX.md` | Any add/remove/rename/edit under `notebooks/` | Re-run `python3 tools/build_index.py` in the same PR | Re-run again → empty diff; `rows=` matches file count |
| `handoff/FAILURE-LOG.md` | Any skill rule fires in anger, or a new failure class is observed | Append entry (what happened, verify command, as-of date, motivated skill). Never rewrite old entries | New entry's verify command runs green |
| `handoff/OPEN-QUESTIONS.md` | A task hits an unanswerable external question; or an answer arrives | Append question, or fill `Answer:` with verbatim quote + who + date + where | No entry may say "probably" |
| `handoff/skills/*/SKILL.md` | Only a FAILURE-LOG entry (new or existing) justifying the edit | Edit skill citing the entry; human review per MODEL-ROUTING | PR links the entry |
| `specs/*.md` captures | 90 days after capture date, or any major release of the captured library, whichever first | Re-fetch source, re-verify excerpt, bump `Captured:` date — or mark `STALE` prominently | Every capture's date < 90 days old or marked STALE |
| `handoff/plans/*.md` (APPROVED) | Preconditions no longer reproduce | Status → DRAFT; re-baseline expected outputs; human re-approves | Precondition block passes verbatim |
| `handoff/plans/*.md` (DONE) | Execution complete | Move to `handoff/plans/done/`, evidence appendix filled | Appendix has all steps' pasted output |
| `handoff/docs/MODEL-ROUTING.md` | A task matches no row; or a solo task fails twice (escalation rule); or new tooling/CI appears | Add or tighten a row; loosening a row is human-review only | Every routing decision in a PR cites a row |
| `handoff/docs/ONBOARDING.md` | A session wastes >15 minutes on something onboarding should have prevented (e.g. reads the PDF wholesale) | Add the specific guardrail, with the incident as a FAILURE-LOG entry if it caused damage | — |
| `handoff/FAILURE-LOG.md` evidence baselines | `main` moves past commit `41e082a` | Re-run each entry's verify command; annotate entries whose expected output changed (dated note, no rewrites) | All verify commands' outputs current |
| `handoff/README.md` / `INSTALL.md` | Any structural change to the handoff tree | Update the map/steps | Paths named in them exist |

## Two standing invariants

1. **Append-only history:** FAILURE-LOG and OPEN-QUESTIONS never lose
   entries. Corrections are dated notes, not deletions.
2. **Generated files are never hand-edited:** `notebooks/INDEX.md` changes
   only via its generator. A hand edit there is a fact-discipline violation
   (it forges repo-tier evidence).
