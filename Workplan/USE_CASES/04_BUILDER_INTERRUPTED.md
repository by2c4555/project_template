# Builder Interrupted Mid-Task

ExecutionManager queries `execution.py next`. An active Task returns resume/reconciliation authority rather than selecting a new Task. `execution.py resume` reacquires the same Builder Work with a new generation after exact binding comparison. Reconciliation reports production-worktree changes relative to the persisted Work baseline. No future Task/Phase may advance until the current Attempt reaches a deterministic gate result.
