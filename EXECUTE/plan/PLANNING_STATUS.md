# Planning Status

```yaml
planning_version: none
planning_revision: none
based_on_research_version: none
planning_status: NOT_CREATED
material_unknowns: unknown
feedback_reason: none
plan_review_status: NOT_STARTED
package_status: NOT_COMPILED
interaction_gate: NONE
invocation_stop_required: false
task_expansion_allowed: false
implementation_approval_requested: false
approved_by: none
approved_at: none
execution_locked: true
```

Allowed planning states:
- `NOT_CREATED`
- `IN_PROGRESS`
- `AWAITING_USER_FEEDBACK`
- `AWAITING_USER_APPROVAL`
- `APPROVED`
- `SUPERSEDED`

Allowed `feedback_reason` values:
- `none`
- `MATERIAL_DECISION`
- `PLAN_REVIEW`

Allowed `plan_review_status` values:
- `NOT_STARTED`
- `AWAITING_USER_FEEDBACK`
- `CHANGES_REQUESTED`
- `ACCEPTED`

Allowed `package_status` values:
- `NOT_COMPILED`
- `DRAFT_READY_FOR_REVIEW`
- `READY_FOR_APPROVAL`
- `APPROVED`
- `SUPERSEDED`

## Human-Gate Semantics

`AWAITING_USER_FEEDBACK` and `AWAITING_USER_APPROVAL` are **terminal states for the current external-planning invocation**.

- `AWAITING_USER_FEEDBACK` + `feedback_reason: MATERIAL_DECISION` means one or more material decisions remain. Current-Planning execution-package expansion is locked.
- `AWAITING_USER_FEEDBACK` + `feedback_reason: PLAN_REVIEW` means material unknowns are zero and a compiled draft has been presented. The agent must still stop and wait for a new user message.
- `AWAITING_USER_APPROVAL` means the reviewed package is execution-ready and the agent has explicitly asked whether implementation may begin. The agent must stop. It may not run the approval script.

Only the user/operator may approve a Planning Vx for execution. Plan acceptance, comments, clarification answers, or the existence of a complete plan are not implementation authorization by themselves.

See `EXECUTE/plan/PLANNING_CONTROL.md` for the normative interaction, expansion, and cost-control contract.
