---
name: builder-task-execution
description: v4.3 machine-gated single-Task execution kernel for Builder100K.
---

# Builder Task Execution v4.3

1. Confirm `STATE.json` names exactly one active `IN_PROGRESS` Task.
2. Run `context_guard.py` before loading implementation context.
3. Load only Task mandatory context first; expand context only via NEED -> JUSTIFICATION -> BUDGET -> LOAD.
4. Implement only the immutable Task contract and allowed file scope.
5. Run deterministic verification, preferably through `safe_exec.py` when output may be large.
6. After a failed verification, call `execution_gate.py authorize-repair TASK_NNN` **before each repair attempt**. No gate PASS -> no repair.
7. Persist durable evidence regardless of outcome.
8. Return one Result Capsule and STOP. Never begin another Task.

The Builder cannot grant PASS, open/close Issues, authorize Recovery, resume Execution, or start Evaluation. Those are machine/user transitions outside Builder authority.
