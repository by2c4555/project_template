# Planning Status

```yaml
planning_version: none
planning_revision: none
based_on_research_version: none
planning_status: NOT_CREATED
material_unknowns: unknown
implementation_approval_requested: false
approved_by: none
approved_at: none
execution_locked: true
```

Allowed pre-approval states:
- `NOT_CREATED`
- `IN_PROGRESS`
- `AWAITING_USER_FEEDBACK`
- `AWAITING_USER_APPROVAL`

`AWAITING_USER_FEEDBACK` means Codex is still resolving requirements/technical decisions or revising the package.
`AWAITING_USER_APPROVAL` means the package is execution-ready, `material_unknowns: 0`, and Codex has explicitly asked the user whether to proceed with implementation.

Only the user may approve a Planning Vx for execution. Plan acceptance, comments, or clarification answers are not implementation authorization by themselves.
