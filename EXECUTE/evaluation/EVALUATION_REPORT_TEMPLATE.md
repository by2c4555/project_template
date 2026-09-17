# Evaluation Vx

```yaml
evaluation_version: Evaluation_Vx
cycle_id: CYCLE_NNN
evaluates_planning_version: Planning_Vx
evaluates_execution_version: Execution_Vx
evaluator_environment: External Agent
result: PENDING
blocking_findings: 0
recovered_tasks_reviewed: []
resolved_issues_reviewed: []
```

## Executive Summary
## Evaluation Scope
## Requirement Coverage
## Plan Compliance
## Functional Verification
## Architecture / Decision Compliance
## Interface / Data Compatibility
## Security / Reliability
## Test Adequacy and Regression Risk
## Recovery-History Verification
## Performance / Operability
## Documentation
## Invalidated Assumptions

## Findings

### EVAL-001

```yaml
severity: high
status: confirmed
blocking: true
category: implementation_or_contract_failure
related_requirement: none
related_decision: none
related_task: none
evidence_strength: confirmed
requires_diagnosis: true
```

**Evidence:**

**Expected behavior:**

**Actual behavior:**

**Bounded hypothesis (optional, not authoritative diagnosis):**

## Non-Blocking Findings / Technical Debt

## Final Status

Set the top-level `result` to exactly one of `PASS`, `PASS_WITH_FINDINGS`, or `DIAGNOSIS_REQUIRED` and set `blocking_findings` accurately before running `finalize_evaluation.py`.
