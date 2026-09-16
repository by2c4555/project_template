# Planning Interaction & Cost-Control Contract — v4.2.1

This file defines machine-checkable safety rules for external technical planning agents such as Codex, Claude, or another compatible high-capability agent.

The planning agent is powerful but is **not** the authority to cross a human interaction boundary. Reaching a human gate and stopping is a successful completion of the current invocation.

## Core Invariants

1. **No user decision -> no speculative task expansion.**
2. If `material_unknowns` is unknown or greater than zero, current-Planning execution-package expansion is locked.
3. `AWAITING_USER_FEEDBACK` is a terminal state for the current agent invocation.
4. `AWAITING_USER_APPROVAL` is a terminal state for the current agent invocation.
5. A plan review response is not implementation approval.
6. The planning agent must never execute `scripts/approve_plan.py` itself.
7. Only the user/operator may run the approval command after explicitly authorizing implementation.
8. Local Manager/Builder execution remains locked until the approval script records the exact Planning-to-Execution binding.

## Planning Interaction States

### `IN_PROGRESS`

The agent may inspect/research/revise. Expensive package expansion is still forbidden unless all of these are true:

```yaml
material_unknowns: 0
interaction_gate: NONE
invocation_stop_required: false
task_expansion_allowed: true
```

`task_expansion_allowed: true` must be established through `scripts/planning_gate.py authorize-expansion`.

### `AWAITING_USER_FEEDBACK`

The current invocation must stop after persisting state and asking focused questions/review feedback.

Two feedback reasons are supported:

- `MATERIAL_DECISION` — one or more material unknowns remain. Current-Planning task/package expansion is forbidden.
- `PLAN_REVIEW` — material unknowns are zero and a compiled draft package has been presented for user review. The current invocation still stops; implementation approval may not be inferred from silence or ordinary feedback.

While this state is active:

```yaml
interaction_gate: USER_FEEDBACK_REQUIRED
invocation_stop_required: true
implementation_approval_requested: false
```

### `AWAITING_USER_APPROVAL`

The plan review has been accepted and the exact execution-ready package is ready for explicit implementation authorization.

Required shape:

```yaml
planning_status: AWAITING_USER_APPROVAL
material_unknowns: 0
feedback_reason: none
plan_review_status: ACCEPTED
package_status: READY_FOR_APPROVAL
interaction_gate: USER_APPROVAL_REQUIRED
invocation_stop_required: true
task_expansion_allowed: true
implementation_approval_requested: true
execution_locked: true
```

The agent asks for implementation approval and **stops**. It must not execute the approval script.

### `APPROVED`

Only `scripts/approve_plan.py`, run by the user/operator with an explicit confirmation argument, may create this transition.

## Expansion Lock

Before creating or materially expanding any current-Planning execution package artifact, run:

```bash
python scripts/planning_gate.py authorize-expansion --planning Planning_Vx --revision Revision_N
```

The command fails unless the active Planning state has zero material unknowns and no human interaction gate is active.

Execution-package artifacts include:

- `EXECUTE/compiled/**`
- `EXECUTE/plan/IMPLEMENTATION_PLAN.md`
- `EXECUTE/tasks/TASK_INDEX.md`
- any `EXECUTE/tasks/TASK_NNN.md`

Repository research notes, Planning revision records, questions, and status updates are not execution-package expansion.

## Hard Stop Rule

When the agent asks the user a question that is required before safely continuing, or asks the user to review/approve a plan:

1. persist the appropriate status;
2. ask only the necessary user-facing question/request;
3. do not continue into a later phase;
4. do not perform speculative work "while waiting";
5. end the current invocation.

A later invocation may resume only because a new user message supplies the requested feedback or authorization.

## Cost-Control Rule

The following are prohibited while material unknowns remain:

- conditional implementation plans that attempt to cover every unresolved branch;
- speculative architecture variants expanded into executable detail;
- atomic Task generation;
- exhaustive file-by-file implementation decomposition;
- test matrices derived from unresolved product decisions;
- broad context compilation whose content depends on unresolved decisions.

Bounded alternatives may be presented only to help the user make the unresolved decision. They must remain concise and must not be expanded into execution Tasks.

## Validation

Run:

```bash
python scripts/validate_v4.py
```

The validator checks planning-state invariants and rejects illegal current-Planning task/package artifacts where mechanically detectable.
