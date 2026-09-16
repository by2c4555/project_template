# Evaluation Review Vx

Use when Codex Diagnosis determines that a prior Evaluation finding itself was defective.

```yaml
review_version: Evaluation_Review_Vx
evaluation_under_review: Evaluation_Vx
source_diagnosis: Diagnosis_Vx
review_result: EVALUATION_DEFECT
requires_code_change: false
requires_replan: false
requires_scope_review: false
```

## Invalidated Findings

### EVAL-NNN

## Why the Finding Was Invalid

## Authoritative References

- approved Research/scope
- approved Planning/Task
- implementation evidence

## Resolution

Specify whether the finding is invalidated, narrowed, or replaced.

## Next Action

Run a new immutable Evaluation Vx+1. Never overwrite the historical Evaluation report.
