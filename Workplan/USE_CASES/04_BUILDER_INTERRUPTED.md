# Builder Interrupted Mid-Task

ExecutionManager queries `execution.py next`. An active Task returns RESUME_TASK or RECONCILE_TASK. `execution.py resume` reacquires the same Builder Work with a new generation. Machine reconciliation reports changed authorized files since the last semantic checkpoint. No future Task may start.
