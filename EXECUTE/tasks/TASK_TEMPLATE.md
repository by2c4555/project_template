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

## Context Budget

```yaml
profile: Builder128K
controlled_target_tokens: 49152
controlled_max_tokens: 65536
expected_tool_output_reserve_tokens: 6000
preflight: python scripts/context_guard.py EXECUTE/tasks/TASK_NNN.md
```

Planner must run the preflight before publishing the Task pack. Builder must run it again before loading implementation files.

Decision rules:
- PASS: within target;
- WARN: above target but within hard maximum;
- SPLIT_REQUIRED: above hard maximum;
- CONTEXT_BLOCKED: runtime/model capacity or required context cannot be established safely.

## Verified Facts

Include only execution-critical facts.

- FACT 1
- FACT 2

Sources:
- KNOWLEDGE-ID
- CONTRACT-ID

## Required Change

Describe the exact required behavior. Do not leave architecture decisions unresolved.

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

Expected result: `PASS`

## Environment

```yaml
external_access: false
required_user_env: []
production_access: false
database_access: none
```

## External I/O Budget

```yaml
api_requests: 0
api_pages: 0
api_items_per_page: 0
db_queries: 0
db_rows_per_query: 0
repeated_equivalent_calls: 2
transient_retries_per_operation: 2
```

## Local Output Budget

```yaml
max_command_output_chars_into_model: 12000
max_search_results_into_model: 100
max_log_excerpt_lines_into_model: 200
max_diff_lines_into_model: 400
max_test_failure_excerpt_lines_into_model: 250
```

Keep full raw output out of model context when a bounded summary is sufficient.

## Stop If

Stop and create/escalate an Issue when:
- Task facts conflict with repository/external reality;
- context preflight is SPLIT_REQUIRED or CONTEXT_BLOCKED;
- required scope expands materially;
- a required architecture decision is missing;
- external configuration is missing;
- equivalent failure repeats without new evidence;
- two meaningful repairs fail;
- unrelated regression is introduced.

## Result

Status: PENDING

Persist durable evidence before returning.
Return a bounded Result Capsule only:

```yaml
result_capsule:
  unit: TASK_NNN
  status: PENDING
  changed_files: []
  verification: NOT_RUN
  issue: none
  next_action: none
```
