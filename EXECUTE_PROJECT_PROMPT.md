# Execute / Resume Approved Project — v4.3.1

Use `ProjectManager500K` as the only user-facing local execution agent.

Read `EXECUTE/control/STATE.json` first. Markdown status files are generated views only.

## Start

A Planning chat message never authorizes implementation. Local execution starts only after the user manually runs:

```bash
python scripts/approve_plan.py
```

and machine state contains an ACTIVE cycle-scoped approval plus exact approved package digest.

## Per-Task control

Manager must call `execution_gate.py begin-task` before every Builder dispatch and `complete-task`/`fail-task` afterward. Builder repair attempts require `execution_gate.py authorize-repair` one at a time.

A gate failure is a hard stop. Never repair state manually.

## Manager context reset

When the configured dispatch batch is exhausted, the Manager must STOP. User manually runs `reset_manager_batch.py` and starts a fresh Manager conversation.

## Incident flow

Builder failure beyond bounded local repair:

```text
execution_gate.py fail-task
 -> Issue + PAUSED_FOR_DIAGNOSIS
 -> Codex ISSUE_DIAGNOSIS_PROMPT.md (diagnosis only)
 -> user approve_recovery.py when IMPLEMENTATION_DEFECT
 -> Codex RECOVERY_PROMPT.md
 -> recovery_gate.py verification
 -> user resume_execution.py (execution-origin issue)
 -> fresh Manager resumes
```

No combined diagnosis+repair invocation is allowed.

## Completion

All Tasks PASS/PASS_RECOVERED -> Manager calls `execution_gate.py finalize-execution` -> STOP.

The user then manually runs `start_evaluation.py` and launches Codex Evaluation. A passing Evaluation is closed only by `finalize_evaluation.py` after a Completion Report exists.

After a Cycle is `CLOSED_VALIDATED`, do not reopen it. New feature/version/debug scope starts a new Cycle with `start_cycle.py`; old approvals never carry forward.
