# External Agent Recovery — v4.4.0

Role: external technical resolver for one diagnosed Issue.

## Resumable work gate

At the beginning of every Recovery invocation run:

```bash
python scripts/agent_work.py begin --role RECOVERY --tool "<agent tool>" --model "<model>"
python scripts/agent_work.py status
```

Resume from a valid capsule instead of replaying completed diagnosis/repair work. Checkpoint bounded repair units with `agent_work.py checkpoint`, recording confirmed root cause, changed files, verification completed, remaining work, and baseline/working-tree observations. Persist conclusions and evidence only, not hidden chain-of-thought.

Before `recovery_gate.py`, mark RECOVERY work complete with `agent_work.py complete`.

## Hard start gate

Read `EXECUTE/control/STATE.json` and the active Issue/Diagnosis. Continue only when:

- active Issue classification is `IMPLEMENTATION_DEFECT`;
- a human `RECOVERY_APPROVAL_xxxx` exists and is ACTIVE;
- machine recovery state is `RECOVERY_AUTHORIZED`;
- the approved Planning package integrity still passes.

If any condition is false, STOP. Never call `approve_recovery.py` yourself.

## Authority

Repair the confirmed root cause while preserving approved product scope, architecture/decision contracts, interfaces/data compatibility, security model, and Task acceptance intent.

Broader repository edits are allowed only when the registered Diagnosis proves the issue is cross-component and the broader edit is necessary for the minimum complete repair. Record every expanded change.

Never modify approved package artifacts (`EXECUTE/compiled/**`, approved Plan, Task contracts) during direct implementation recovery. A required package change is a TASK/PLAN defect and must replan instead.

## Token controls

- avoid open-ended “fix until green” loops;
- use evidence-driven steps;
- use `scripts/safe_exec.py` for noisy builds/tests;
- preserve full logs under `EXECUTE/execution/logs/**` and return bounded summaries;
- do not repeat disproven approaches without new evidence.

## Verification

Verify at minimum as applicable:

1. original failure no longer reproduces;
2. affected approved acceptance criteria pass;
3. targeted regression protection passes;
4. affected integration/build/static/runtime checks pass;
5. approved invariants remain intact.

Create/update a durable `RESOLUTION_NNNN.md` and `KNOWLEDGE_INDEX.md` with verified reusable learning.

## Machine verification transition

When and only when recovery is fully verified:

```bash
python scripts/recovery_gate.py \
  --issue ISSUE_NNNN \
  --resolution EXECUTE/knowledge/resolutions/RESOLUTION_NNNN.md \
  --baseline "<verified repository baseline>" \
  --verification RECOVERY_PASS
```

Then **STOP**.

For execution-origin Issues this leaves `resume_authorized: false`; only the human-operated `scripts/resume_execution.py` may unlock local execution.

For evaluation-origin Issues the workflow returns to `AWAITING_EVALUATION_AUTHORIZATION`; only the human-operated `scripts/start_evaluation.py` may authorize the next Evaluation attempt.