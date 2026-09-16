---
task_id: TASK_NNN
planning_version: Planning_Vx
phase: PHASE_NN
status: PENDING
builder: Builder100K
depends_on: []
decision_refs: []
requirement_refs: []
recovery_refs: []
---

# TASK_NNN — Title

## Objective

One atomic, independently verifiable outcome.

## Why This Task Exists

Compiled causal reason from the approved plan.

## Context Manifest

### mandatory
- `EXECUTE/compiled/GLOBAL_CONSTRAINTS.md`
- `path/to/relevant/file`

### relevant_prior_resolutions
- none

### useful
- `path/to/optional/context`

### do_not_load_by_default
- `EXECUTE/docs/raw/**`
- `EXECUTE/knowledge/**`
- unrelated repository areas

## Allowed Scope

### WRITE
- `path/to/file`

### READ
- `path/to/file`

### TEST
- `path/to/test`

## Architecture / Decisions

- execution-critical decision references

## Verified Facts

Only facts required to execute safely, with provenance.

## Prior Resolution Guardrails

Only relevant verified reusable lessons preselected by Codex/Manager.

- none

## Required Change

Exact behavior; no unresolved project-wide design decisions.

## Invariants / Must Preserve

- ...

## Out of Scope

- ...

## Acceptance Criteria

- AC-01:
- AC-02:

## Verification

```text
<exact command/procedure>
```

Expected: PASS

## Local Repair Budget

```yaml
max_evidence_driven_repair_attempts: 2
open_ended_recovery_allowed: false
```

If the Task remains failing after the bounded repair budget, Builder must persist evidence and return `external_recovery_required: true`.

## Context Budget

```yaml
profile: Builder100K
controlled_target_tokens: 40000
controlled_max_tokens: 52000
expected_tool_output_reserve_tokens: 5000
preflight: python scripts/context_guard.py EXECUTE/tasks/TASK_NNN.md
```

## Stop If

- compiled facts contradict implementation reality;
- a required decision is missing;
- material scope/architecture/requirement change is required;
- context exceeds budget;
- verification cannot be made deterministic enough;
- safe repair requires broader repository authority than this Task permits;
- bounded repair attempts are exhausted.

## Evidence Output

Persist `EXECUTE/execution/evidence/TASK_NNN.md` with changed files, AC mapping, verification, deviations, assumptions, risks, and failure/repair evidence when applicable.

## Allowed Final Status

- `PASS`
- `BLOCKED`
- `PASS_RECOVERED` — may only be assigned by verified external Recovery, never by ordinary Builder execution.
