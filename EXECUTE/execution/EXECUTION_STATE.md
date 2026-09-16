# Execution State

```yaml
execution_version: none
execution_status: LOCKED
execution_bound_planning_version: none

completed_tasks: []
recovered_tasks: []
active_task: none
blocked_tasks: []

active_issue: none
last_resolved_issue: none

recovery:
  status: NOT_ACTIVE
  owner: none
  diagnosis: none
  resolution: none
  verification: none
  resume_authorized: false
  recovery_baseline: none
  next_task: none

replan_required: false
scope_clarification_required: false
evaluation_required: false
```

## Execution Status State Machine

Allowed primary execution states:

- `LOCKED`
- `READY`
- `IN_PROGRESS`
- `ISSUE_DETECTED`
- `PAUSED_FOR_DIAGNOSIS`
- `PAUSED_FOR_EXTERNAL_REPAIR`
- `RECOVERY_VERIFICATION`
- `READY_TO_RESUME`
- `COMPLETE`
- `AWAITING_EVALUATION`

Local Manager/Builder execution is permitted only in `READY`, `IN_PROGRESS`, or `READY_TO_RESUME`.

Any `PAUSED_*` or `RECOVERY_VERIFICATION` state is a hard stop for normal Builder dispatch.
