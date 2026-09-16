# Planning Revision — Revision_N

```yaml
planning_version: Planning_Vx
planning_revision: Revision_N
based_on_scope_revision: SCOPE_NNN
based_on_scope_digest: sha256:...
status: IN_PROGRESS
material_unknowns: unknown
package_status: NOT_COMPILED
supersedes_revision: none
```

## Trigger
Why this revision exists: initial planning, user feedback, clarification answer, repository finding, or replan input.

## User Feedback / Decisions Incorporated
- ...

## Decision Provenance
For each material decision, record the user message/decision source and technical consequence. Product/scope changes must first enter through a new immutable Scope revision; do not silently rewrite external scope inside Planning.

## Repository Findings Incorporated
- ...

## Changes From Previous Revision
- ...

## Material Unknowns
List only unknowns capable of changing scope, architecture, public behavior, data compatibility, dependency strategy, security, migration behavior, or acceptance criteria.

If a missing answer is a product/scope decision rather than repository truth, stop for clarification. Do not claim zero until repository research and user decisions prove it.

## Plan Impact
- architecture:
- tasks:
- interfaces/data:
- testing/validation:
- risks:

## v4.3 State Rule

- material unknowns > 0 -> call `planning_gate.py hold-material-feedback` and **STOP**;
- external scope changes -> user runs `import_scope.py`, producing a new `SCOPE_NNN` before Planning continues;
- material unknowns = 0 -> call `planning_gate.py set-material-zero`, then `authorize-expansion` before compiling Tasks;
- compiled package ready -> call `planning_gate.py mark-plan-ready` and **STOP**;
- `PLAN_READY` binds both the active Scope digest and package digest;
- any later chat message is feedback/question only; it can cause a new revision but never implementation approval;
- only the human-operated `scripts/approve_plan.py` can cross `PLAN_READY -> APPROVED`.
