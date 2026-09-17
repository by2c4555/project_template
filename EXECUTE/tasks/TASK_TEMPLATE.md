---
task_id: TASK_NNN
artifact_status: COMPILED
planning_version: Planning_Vx
planning_revision: Revision_N
phase: PHASE_NN
builder: Builder100K
depends_on: []
decision_refs: []
requirement_refs: []
recovery_refs: []
---

# TASK_NNN — Title

> **Immutable approved contract.** Runtime status, dispatch counters, repair counters, and recovery status live only in `EXECUTE/control/STATE.json` and must never be written into this Task file after approval.

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

For potentially verbose commands use `python scripts/safe_exec.py --label <TASK>_<CHECK> -- <command>` so full logs are durable but agent-visible output is bounded.

## Local Repair Budget

```yaml
max_evidence_driven_repair_attempts: 2
open_ended_recovery_allowed: false
```

Each post-failure code-repair attempt requires `python scripts/execution_gate.py authorize-repair TASK_NNN` first. When the machine counter is exhausted, persist evidence and return BLOCKED.

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
- `execution_gate.py` denies dispatch/repair;
- bounded repair attempts are exhausted.

## Evidence Output

Persist `EXECUTE/execution/evidence/TASK_NNN.md` with changed files, AC mapping, verification, deviations, assumptions, risks, and failure/repair evidence when applicable.
