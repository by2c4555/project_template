---
issue_id: ISSUE_NNNN
status: OPEN
origin_type: EXECUTION | EVALUATION
origin_execution: Execution_Vx
origin_task: TASK_NNN | none
origin_evaluation: Evaluation_Vx | none
opened_at: unknown
resume_authorized: false
---

# ISSUE_NNNN — Title

## Failure Summary

Verified symptom only; do not claim root cause before Diagnosis.

## Expected Behavior

## Observed Behavior

## Reproduction / Finding Reference

## Failure Signature

## Evidence Pointers

Store giant logs under `EXECUTE/execution/logs/**` or evidence directories and link them here.

## Relevant Repository Scope

## Attempts Already Made / Ruled Out

## Approved Contract References

## Safe Baseline

## Recovery Control

```yaml
local_execution_paused: true
resume_authorized: false
diagnosis_artifact: none
recovery_approval: none
resolution_artifact: none
recovery_verification: none
```

## Next Action

Run `EXECUTE/codex/ISSUE_DIAGNOSIS_PROMPT.md`.

Diagnosis is a separate read/analyze/propose invocation. Do not use the deprecated combined Diagnosis+Recovery prompt.
