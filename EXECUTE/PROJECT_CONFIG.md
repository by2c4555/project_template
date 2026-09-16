# Project Configuration — v4.1.3

## Canonical Lifecycle

`Research Vx -> Codex Preparation/Planning Vx -> USER IMPLEMENTATION APPROVAL -> Execution Vx -> Evaluation Vx -> route`

The preparation phase contains a user feedback loop before the implementation approval gate:

```text
ChatGPT Research (define scope)
  -> Codex implementation research / repository discovery
  -> user clarification + plan revision loop
  -> execution-ready package
  -> explicit implementation approval request
  -> Local Manager + Builder execution
  -> independent Codex Evaluation
```

## Intelligence Roles
- **ChatGPT Project — Scope Definition:** problem research, requirements, scope, success intent, Research Vx.
- **Codex / GPT-6 Astra — Work Preparation:** repository-level implementation research, user clarification, context compilation, Planning Vx, task packaging, and independent Evaluation Vx.
- **ProjectManager500K — Execution Orchestration:** deterministic orchestration of one approved execution package.
- **Builder100K — Implementation:** one bounded approved Task per fresh invocation.

Canonical shorthand:

```text
ChatGPT Research = Define the scope.
Codex GPT-6      = Prepare the work.
Manager          = Manage the work.
Builder          = Perform the work.
```

## Hard Authority Rules
1. No approved Planning Vx -> no execution.
2. Planning feedback/review is not implementation approval.
3. Codex must resolve material unknowns before requesting implementation approval.
4. `AWAITING_USER_FEEDBACK` != `AWAITING_USER_APPROVAL`.
5. Execution is bound to one exact approved Planning Vx.
6. Local models may not silently change approved architecture/intent/scope.
7. Missing or conflicting material requirements discovered during execution -> STOP and escalate for Codex/user resolution; do not guess.
8. Material deviation -> `REPLAN_REQUIRED`.
9. Local execution complete != project validated.
10. Only independent Evaluation Vx may validate the implementation iteration.
11. Evaluation is read-only with respect to production implementation.
12. Research/Evaluation/approved Planning history is immutable; current aliases may advance to a new Vx.

## Planning Revision Policy
Pre-approval user feedback normally creates revisions inside the same Planning Vx. Do not increment Planning Vx for every comment. Increment Planning Vx for a materially new planning cycle, especially after an approved plan requires replan or Evaluation returns `REPLAN_REQUIRED`.

## Model Policy
```yaml
local_models:
  ProjectManager500K:
    minimum_context_tokens: 512000
  Builder100K:
    minimum_context_tokens: 102400
    controlled_target_tokens: 40000
    controlled_max_tokens: 52000
external_intelligence:
  environment: Codex
  recommended_model: GPT-6 Astra
  binding: user-managed
```

## No-RAG Local Policy
Local models receive compiled knowledge, context manifests, repository files named by Tasks, and persisted execution evidence. They must not depend on semantic RAG. Missing material knowledge is surfaced as a preparation/context defect and escalated rather than guessed.

## Planning Approval
Codex may set `AWAITING_USER_APPROVAL` only when `material_unknowns: 0` and `implementation_approval_requested: true`. Only explicit user authorization plus `scripts/approve_plan.py` changes the plan to `APPROVED` and binds Execution Vx.

## Evaluation Results
Exactly one of: `PASS`, `PASS_WITH_FINDINGS`, `CORRECTION_REQUIRED`, `REPLAN_REQUIRED`, `RESEARCH_REQUIRED`.

## Environment Safety
Never guess credentials/external configuration. Production access and destructive database operations are denied unless explicitly authorized in the approved Task.
