---
task_id: TASK_NNN
type: normal
status: PENDING
stage: pending

required_builder_profile: Builder64K
builder_profile_source: .github/agents/builder64k.agent.md
planned_context_tokens: 0
context_assessment: SAFE

depends_on: []
plan_refs: []
knowledge_refs: []
history_refs: []
issue_refs: []
---

# TASK_NNN — <Title>

## Objective
One bounded outcome.

## Definition of Done
Observable completion condition.

## Plan References
Exact stable Plan IDs only.

## Knowledge References
Exact Knowledge IDs only.

## Dependencies
All required dependencies must be PASS.

## Builder / Context Budget
Derived from the selected Builder agent.

## Exploration Budget

```yaml
search_rounds: 3
additional_files: 6
log_lines: 200
```

## External I/O Budget

Use zero when external access is not required.

```yaml
db_queries: 0
db_rows_per_query: 0
db_pages: 0

api_requests: 0
api_items_per_page: 0
api_pages: 0

repeated_equivalent_calls: 2
transient_retries_per_operation: 2
```

## Environment Contract

```yaml
live_external_access: false
required_user_env: []
optional_user_env: []
database_access: none
production_access: false
```

Missing required `.env.user` values -> `WAITING_USER` -> STOP.
Never guess credentials or endpoints.

## Context Manifest

### Source
- exact path/symbol

### Tests
- exact path/test

### Supporting Context
- exact file/section

### Plan / Knowledge
- exact refs

## Required Evidence
State exactly what evidence is sufficient to implement safely.

## Current State / Verified Baseline
Only verified task-relevant state.

## Expected Behavior
Observable required behavior.

## Allowed Scope
- ...

## Out of Scope
- ...

## Implementation Requirements
- ...

## Error / Edge Cases
- ...

## Acceptance Criteria

```text
AC-01:
AC-02:
```

## Test Ownership
Mode: HYBRID

### Planner-Owned Contract Tests
None unless stable specification-derived tests were generated.

### Builder-Owned Tests
Focused unit/integration/regression tests required by implementation.

## Verification Matrix

| Check | Owner | Command / Procedure | Expected | Covers |
|---|---|---|---|---|

## Exploration Stop Conditions
Stop discovery when sufficient evidence exists, two equivalent searches/calls yield no new evidence, or budget is exhausted.

## Failure / Blocker Rules
Budget exhaustion, environment failure, requirement conflict, knowledge conflict, or executor mismatch must produce a bounded stop.

## Completion Condition

After required verification passes:

1. stop exploration;
2. stop optional refactoring;
3. do not rerun unchanged passing checks;
4. persist Task/history/project state;
5. signal completion when supported;
6. stop.

## Current Result

Status: PENDING
Stage: pending
Latest history: none
Latest issue: none
Summary: Not started.
