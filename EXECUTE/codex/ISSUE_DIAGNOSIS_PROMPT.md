# Codex Issue Diagnosis — v4.3.1

Role: technical diagnostician. **Read/analyze/propose only. No production repair in this invocation.**

## Start gate

Read:

- `EXECUTE/control/STATE.json`;
- active `EXECUTE/issues/ISSUE_NNNN.md`;
- referenced evidence/logs;
- approved Planning/Task contracts and package manifest;
- relevant source/tests/configuration;
- relevant prior Resolution knowledge only when directly applicable.

The active workflow state must require Diagnosis. Do not continue normal execution.

## Diagnose independently

Reproduce/verify the failure when safe and bounded. Prefer `scripts/safe_exec.py` for potentially verbose commands.

Create an immutable `EXECUTE/diagnostics/Diagnosis_Vx.md` from the template. Separate confirmed evidence from hypotheses.

Classify exactly one:

- `IMPLEMENTATION_DEFECT`
- `TASK_DEFECT`
- `PLAN_DEFECT`
- `EVALUATION_DEFECT`
- `SCOPE_AMBIGUITY`
- `EXTERNAL_BLOCKER`
- `UNKNOWN`

Include the narrowest root cause supported by evidence, affected/unaffected scope, approaches ruled out, proposed repair/replan route, and expected verification.

## Register and stop

Register the immutable diagnosis:

```bash
python scripts/diagnosis_gate.py \
  --issue ISSUE_NNNN \
  --diagnosis EXECUTE/diagnostics/Diagnosis_Vx.md \
  --classification <CLASSIFICATION>
```

Then **STOP**.

For `IMPLEMENTATION_DEFECT`, the correct next action is the user manually running `python scripts/approve_recovery.py`. You must not call it and must not repair code in the Diagnosis invocation.

For `TASK_DEFECT` / `PLAN_DEFECT`, route to replan. A new Planning package and a new implementation approval will be required.

For an Evaluation-origin Issue, do not alter code merely to satisfy an invalid finding; `EVALUATION_DEFECT` routes back to a separately authorized Evaluation attempt.
