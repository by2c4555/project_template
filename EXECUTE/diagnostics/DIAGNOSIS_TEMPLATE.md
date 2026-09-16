# Diagnosis Vx

```yaml
diagnosis_version: Diagnosis_Vx
source_type: ISSUE | EVALUATION_FINDING
source_issue: ISSUE_NNNN | none
source_evaluation: Evaluation_Vx | none
source_finding: EVAL-NNN | none
source_task: TASK_NNN | none
status: IN_PROGRESS
classification: UNKNOWN
root_cause_confirmed: false
repair_authorized: false
next_route: CONTINUE_DIAGNOSIS
```

## Trigger

## Reproduced / Independently Verified Failure

## Expected vs Actual

## Evidence

## Root Cause

State the narrowest evidence-supported cause. Separate confirmed fact from bounded hypothesis.

## Affected Scope

## Unaffected Scope

## Hypotheses Ruled Out

## Approved Decisions / Contracts Involved

## Risk of Repair

## Classification

Choose exactly one primary classification:

- `IMPLEMENTATION_DEFECT`
- `TASK_DEFECT`
- `PLAN_DEFECT`
- `EVALUATION_DEFECT`
- `SCOPE_AMBIGUITY`
- `EXTERNAL_BLOCKER`
- `UNKNOWN`

## Authority Decision

```yaml
direct_repair_allowed: false
requires_replan: false
requires_scope_clarification: false
requires_external_action: false
requires_re_evaluation: false
```

## Required Next Action

One concrete route:

- `DIRECT_REPAIR`
- `TASK_REVISION`
- `REPLAN`
- `INVALIDATE_EVALUATION_FINDING`
- `SCOPE_CLARIFICATION`
- `EXTERNAL_ACTION`
- `CONTINUE_DIAGNOSIS`
