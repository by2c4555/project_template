# Project Configuration — v4.1

## Lifecycle
`Research Vx -> Planning Vx -> USER APPROVAL -> Execution Vx -> Evaluation Vx -> route`

Evaluation routes to VALIDATED, PHASE 2 correction, Planning Vx+1, or Research Vx+1.

## Intelligence Roles
- ChatGPT Project: research, requirements, clarification, Research Vx.
- Codex / GPT-6 Astra: external Planning & Knowledge Compilation and Independent Evaluation.
- ProjectManager500K: local deterministic orchestration of an approved execution package.
- Builder100K: local atomic implementation worker.

## Hard Authority Rules
1. No approved Planning Vx -> no execution.
2. Execution is bound to one approved Planning Vx.
3. Local models may not silently change approved architecture/intent.
4. Material deviation -> REPLAN_REQUIRED.
5. Local execution complete != project validated.
6. Only independent Evaluation Vx may validate the implementation iteration.
7. Evaluation is read-only with respect to production implementation.
8. Research/Evaluation/Planning history is immutable; current aliases may advance to a new Vx.

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
Local models receive compiled knowledge, context manifests, repository files named by Tasks, and persisted execution evidence. They must not depend on semantic RAG. Missing knowledge is surfaced as a Task/context defect rather than guessed.

## Planning Approval
Codex creates Planning Vx with `AWAITING_USER_APPROVAL`. Only explicit user approval changes it to `APPROVED` and binds Execution Vx.

## Evaluation Results
Exactly one of: `PASS`, `PASS_WITH_FINDINGS`, `CORRECTION_REQUIRED`, `REPLAN_REQUIRED`, `RESEARCH_REQUIRED`.

## Environment Safety
Never guess credentials/external configuration. Production access and destructive database operations are denied unless explicitly authorized in the Task.
