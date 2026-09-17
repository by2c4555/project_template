# Diagnosis Vx

```yaml
diagnosis_version: Diagnosis_Vx
cycle_id: CYCLE_NNN
source_type: ISSUE
source_issue: ISSUE_NNNN
source_evaluation: Evaluation_Vx | none
source_task: TASK_NNN | none
status: COMPLETE
classification: UNKNOWN
root_cause_confirmed: false
repair_authorized: false
next_route: CONTINUE_DIAGNOSIS
```

> Diagnosis never grants repair authority. `repair_authorized` remains `false` in this artifact. For `IMPLEMENTATION_DEFECT`, only `scripts/approve_recovery.py` can authorize the separate Recovery invocation.

## Trigger

## Reproduced / Independently Verified Failure

## Expected vs Actual

## Evidence

## Root Cause

State the narrowest evidence-supported cause. Separate confirmed facts from bounded hypotheses.

## Affected Scope

## Unaffected Scope

## Hypotheses Ruled Out

## Approved Decisions / Contracts Involved

## Proposed Repair / Replan Scope

List concrete components/files likely required, why, expected verification, and whether the scope crosses the original Task boundary.

## Risk of Repair

## Classification

Choose exactly one:

- `IMPLEMENTATION_DEFECT`
- `TASK_DEFECT`
- `PLAN_DEFECT`
- `EVALUATION_DEFECT`
- `SCOPE_AMBIGUITY`
- `EXTERNAL_BLOCKER`
- `UNKNOWN`

## Required Next Action

- `AWAIT_RECOVERY_APPROVAL`
- `REPLAN`
- `RE_EVALUATE`
- `SCOPE_CLARIFICATION`
- `EXTERNAL_ACTION`
- `CONTINUE_DIAGNOSIS`
