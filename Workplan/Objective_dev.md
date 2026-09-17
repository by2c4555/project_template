# Project Template Development Objective — v5.0.0

> Maintainer reference for developing **Project Template itself**. This is not user-project scope.

## Purpose

Project Template exists to maximize engineering quality per token/cost.

> **Expensive models = planning, architecture, diagnosis, recovery reasoning, evaluation.**  
> **Low-cost models = bounded implementation work.**  
> **Deterministic tools/scripts = authority, state, validation, integrity, resumability, and verification.**

## User-Mandated Invariants — MUST

1. **Workplan control-plane boundary.** `Workplan/` is the canonical AI-development control plane. Workflow authority, scripts, prompts, Tasks, state, checkpoints, approvals, evidence, diagnosis, recovery, evaluation, and workflow documentation live under `Workplan/`, except thin platform-required adapters.
2. **User-project boundary.** Files outside `Workplan/` are user-project space and must not be treated as workflow authority.
3. **Universal resumability.** Planning, Manager/Builder execution, Diagnosis, Recovery, and Evaluation must recover from arbitrary session loss using durable repository state, without requiring prior chat history.
4. **Cross-machine portability.** A transferred workspace containing `Workplan/` must preserve enough state for a fresh compatible agent on another machine to identify the current stage and next safe action.
5. **Interruption loss bound.** An interruption may require repetition/reconciliation of at most the currently active bounded work unit; completed validated units must not be replayed solely because a session/provider/network/machine was lost.
6. **Mapped expensive reasoning.** Initial External Agent work for Planning, Diagnosis, Recovery, and Evaluation must establish a scope-bound Work Map before deep reasoning; later compatible agents resume from the map and latest valid checkpoint.
7. **Provider neutrality.** Provider/model identity is metadata, not workflow authority. Compatible agents may hand off by durable state.
8. **Single human approval interface.** Human token-risk authorization is performed only through `Workplan/scripts/approve.py -- <challenge>`.
9. **Approval purpose.** Human approval exists only for material token/cost-runaway risk or equivalent expensive-work expansion. Routine checkpointing, resume, provider handoff, bounded progression, and normal transitions inside an approved envelope must not require approval.
10. **Challenge binding.** Approval challenge must bind to the exact pending approval and authoritative state. Any wrong challenge invalidates that challenge and rotates to a new challenge.
11. **Approval isolation.** AI uses `Workplan/scripts/tools/approve_req.py` and `approve_res.py`; agents must never execute `approve.py`.
12. **Minimal state exposure.** Agents consume deterministic bounded projections and transitions instead of loading raw `Workplan/control/STATE.json` when a smaller interface is sufficient.
13. **Script interface separation.** `Workplan/scripts/*.py` is the human-facing CLI; `Workplan/scripts/tools/*.py` is the bounded AI/advanced-user CLI; `Workplan/scripts/_core/` is internal implementation and not a direct workflow surface.
14. **Bounded Builder.** Manager dispatches immutable approved Tasks; one fresh Builder works one Task at a time; local repairs are bounded and machine-counted.
15. **Deterministic authority.** Natural-language chat never grants workflow authority. State transitions must pass deterministic validation.
16. **Immutable scope/package integrity.** Scope snapshots, approved planning packages, and Task contracts remain bound by exact digests downstream.
17. **Independent Evaluation.** Evaluation must produce independent evidence; Planning/Builder/Recovery claims are context, not proof.
18. **Diagnosis/Recovery separation.** Diagnosis establishes evidence/classification; Recovery performs authorized repair work. Root cause must not be assumed from an Evaluation finding.
19. **Cycle handoff.** A validated cycle produces a Completion Report containing verified actual-system truth for the next research/scope cycle.
20. **Operational use cases.** Material workflow changes must update `Workplan/USE_CASES/`; a new behavior not demonstrated by an existing use case requires a new use case.

## Design Principles — SHOULD

- Reason once; persist verified conclusions, evidence pointers, rejected approaches with concise reason, material unknowns, and exact next work.
- Never persist hidden chain-of-thought.
- Prefer semantic checkpoints after useful bounded units, not time-based checkpoints.
- Prefer immutable artifacts then atomic authoritative-pointer updates.
- Treat chats, sessions, models, providers, and machines as disposable compute.
- Escalate to expensive reasoning only for material uncertainty, root-cause work, architectural decisions, or independent evaluation.
- Avoid unnecessary agents, prompts, files, gates, and duplicated state.

## Canonical Mental Model

```text
User Project = what is being built
Workplan     = how AI work is planned, controlled, resumed, verified, and approved
```

## Owner Feedback / Change Policy

Do not silently weaken a MUST. When the owner changes a MUST or architecture expectation, update this file, the canonical Workplan README flow, validation, affected USE_CASES, and CHANGELOG in the same release.
