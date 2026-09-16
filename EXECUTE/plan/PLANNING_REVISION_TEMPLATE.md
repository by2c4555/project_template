# Planning Revision — Revision_N

```yaml
planning_version: Planning_Vx
planning_revision: Revision_N
based_on_research_version: Research_Vx
status: IN_PROGRESS
material_unknowns: unknown
feedback_reason: none
plan_review_status: NOT_STARTED
package_status: NOT_COMPILED
supersedes_revision: none
```

## Trigger
Why this revision exists: initial draft, user feedback, clarification answer, repository finding, plan-review change, or evaluation/replan input.

## User Feedback / Decisions Incorporated
- ...

## Decision Provenance
For each material decision, record the user message/decision source and the technical consequence.

- ...

## Repository Findings Incorporated
- ...

## Changes From Previous Revision
- ...

## Material Unknowns
List only unknowns capable of changing scope, architecture, public behavior, data compatibility, dependency strategy, security, migration behavior, or acceptance criteria.

Do **not** initialize this section to `None` until research and user-decision checks actually prove zero material unknowns.

- unknown at revision creation

## Plan Impact
- architecture:
- tasks:
- interfaces/data:
- testing/validation:
- risks:

## Review State
- `AWAITING_USER_FEEDBACK` + `MATERIAL_DECISION`: stop the current invocation; do not expand Tasks/package.
- `AWAITING_USER_FEEDBACK` + `PLAN_REVIEW`: compiled draft presented; stop the current invocation and wait for review.
- `AWAITING_USER_APPROVAL`: only after plan review is accepted, `material_unknowns: 0`, and explicit implementation permission is being requested.

Do not treat this revision record as implementation authorization.
