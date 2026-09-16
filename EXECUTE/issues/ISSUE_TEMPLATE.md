---
issue_id: ISSUE_NNNN
status: OPEN

origin_execution: Execution_Vx
origin_task: TASK_NNN
origin_phase: PHASE_NN
origin_builder: Builder100K
origin_type: LOCAL_EXECUTION

opened_at: unknown
current_owner: CODEX_OR_EXTERNAL_AGENT

safe_baseline: unknown
resume_authorized: false
---

# ISSUE_NNNN — Title

## Failure Summary

Concise description of the verified failure. Do not infer root cause here unless already proven.

## Expected Behavior

What the approved Task/plan requires.

## Observed Behavior

What actually happened.

## Reproduction

```text
Environment:
Prerequisites:
Command/procedure:
Steps:
Expected:
Actual:
```

## Failure Signature

```yaml
error_type: unknown
exit_code: unknown
failing_test: unknown
stack_location: unknown
first_known_bad_state: unknown
last_known_good_state: unknown
```

## Evidence Pointers

Keep giant logs outside this file under `EXECUTE/execution/evidence/**`.

- `EXECUTE/execution/evidence/...`

## Relevant Repository Scope

### Files / Symbols
- path / symbol

### Tests / Commands
- test / command

## Changes Related to Failure

- change / task evidence

## Attempts Already Made

- attempt — result

## Attempts Ruled Out

- approach — evidence-based reason not to repeat

## Affected Scope

- affected component / behavior

## Unaffected Scope

- verified unaffected component / behavior

## Approved References

- Planning: `Planning_Vx`
- Task: `TASK_NNN`
- Requirement/decision refs: ...

## Repository / Safe Baseline

Describe whether the failed Task's partial changes are reverted, safely retained, or uncertain. Never discard unrelated user work.

## Recovery Control

```yaml
local_execution_paused: true
resume_authorized: false
recovery_owner: CODEX_OR_EXTERNAL_AGENT
diagnosis_artifact: none
resolution_artifact: none
recovery_verification: none
```

## Uncertainties

Only unresolved facts that matter to diagnosis/recovery.

## Next Action

Run `EXECUTE/codex/ISSUE_DIAGNOSIS_AND_RECOVERY_PROMPT.md` with Codex or a compatible external recovery agent.
