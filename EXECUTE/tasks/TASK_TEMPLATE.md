---
task_id: TASK_NNN
phase: PHASE_NN
status: PENDING

builder: Builder128K

depends_on: []

plan_refs: []
knowledge_refs: []
issue_refs: []
---

# TASK_NNN — Title

## Goal

One coherent, independently verifiable outcome.

## Context

### WRITE

- `path/to/file`
  - `Exact.symbol` when known

### READ

- `path/to/file`
  - relevant symbol/section when known

### TEST

- `path/to/focused_test`

Do not load unrelated project context.

## Verified Facts

Include only execution-critical facts.

- FACT 1
- FACT 2

Sources:
- KNOWLEDGE-ID
- CONTRACT-ID

## Required Change

Describe the exact required behavior.

Do not leave architecture decisions unresolved.

## Must Preserve

- existing required behavior;
- named contracts;
- unrelated functionality.

## Acceptance Criteria

- AC-01:
- AC-02:

## Verify

```text
<exact command or deterministic verification procedure>
```

Expected result:

`PASS`

## Environment

```yaml
external_access: false

required_user_env: []

production_access: false
database_access: none
```

## External I/O Budget

Use only when external access is required.

```yaml
api_requests: 0
api_pages: 0
api_items_per_page: 0

db_queries: 0
db_rows_per_query: 0

repeated_equivalent_calls: 2
transient_retries_per_operation: 2
```

## Stop If

Stop and create/escalate an Issue when:
- Task facts conflict with repository/external reality;
- required scope expands materially;
- a required architecture decision is missing;
- external configuration is missing;
- equivalent failure repeats without new evidence;
- two meaningful repairs fail;
- unrelated regression is introduced.

## Result

Status: PENDING

Latest history: none

Latest issue: none
