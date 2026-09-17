# External Agent Issue Diagnosis — v4.4.0

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

## Resumable work gate

Run `python scripts/agent_work.py begin --role DIAGNOSIS --tool "<agent tool>" --model "<model>"`. Resume from a valid capsule instead of reproducing completed probes. Checkpoint bounded reproduction/evidence/hypothesis-narrowing units. Persist confirmed facts, ruled-out hypotheses, evidence locations, unresolved hypotheses, and the exact next probe — never hidden chain-of-thought.

Before `diagnosis_gate.py`, mark DIAGNOSIS work complete with `agent_work.py complete`.

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
