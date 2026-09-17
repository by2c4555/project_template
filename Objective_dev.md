# Project Template Development Objective

> Maintainer reference for developing **Project Template itself**. This file is not user-project scope, is not a runtime handoff, and must not be treated as `EXECUTE/project_details.md`.

## Purpose

Project Template exists to maximize engineering quality per token/cost by separating expensive reasoning, bounded implementation, and deterministic authority.

Core principle:

> **Expensive models = planning, architecture, diagnosis, review.**  
> **Low-cost models = bounded implementation work.**  
> **Deterministic tools/scripts = validation, state, gates, integrity, and verification.**

Read repository root `VERSION` first. `main` and the executable workflow are the source of truth for current behavior.

## Mandatory Repository Structure — MUST

The repository must retain clear top-level references for:

- `VERSION` — current Project Template version.
- `Objective_dev.md` — Project Template development intent, owner constraints, and maintainer reference.
- `README.md` — current usage and canonical workflow architecture.
- `CHANGELOG.md` — version evolution history.
- `EXECUTE/` — user-project workflow/runtime templates and artifacts.
- `scripts/` — deterministic workflow state, gates, validation, and verification.

Internal directories may evolve when justified. Do not add agents, prompts, files, gates, or persistent state without a concrete reliability, cost, resumability, or control benefit.

## User-Mandated Invariants — MUST

1. `README.md` must always contain the current canonical **`VERSION / CHANGE CYCLE`** flow diagram. Architecture may change, but the diagram must change in the same version/change so it never describes an obsolete workflow.
2. `README.md` must reference `Objective_dev.md` and explain that it is for developing Project Template itself, not user-project runtime scope.
3. External Research does not require a `Research_Vx.md` handoff. Final scope handoff is `EXECUTE/project_details.md` plus only useful declared `EXECUTE/docs/raw/*` evidence.
4. External reasoning roles must be provider-neutral where practical. Codex, Claude Code, OpenCode, Antigravity, or future agents may perform Planning, Diagnosis, Recovery, or Evaluation. Agent/provider identity is not workflow authority.
5. Expensive reasoning-heavy work must be resumable from workspace state so a fresh compatible agent can continue without replaying completed expensive reasoning.
6. Manager / Builder remain the bounded local execution layer unless the user explicitly agrees to an architectural change. Manager orchestrates approved Tasks; fresh Builders perform bounded implementation.
7. `EXECUTE/control/STATE.json` and deterministic scripts remain authoritative for workflow transitions. Natural-language chat must not grant critical execution authority.
8. A validated cycle feeds verified actual-system truth into the next External Research/change cycle through the Completion Report.

## Preferred Design Principles — SHOULD

- Reason once, persist verified conclusions, and avoid repeated repository-wide analysis.
- Prefer compact evidence-backed resume capsules over chat history or verbose scratchpads.
- Use selective context loading and bounded logs.
- Escalate to expensive reasoning only when a material decision/root cause/evaluation question requires it.
- Keep normal implementation Task-driven, bounded, and independently verifiable.
- Preserve immutable approved package boundaries and explicit human approvals.
- Prefer deterministic invalidation/fingerprints over asking an agent to guess whether old reasoning is still valid.

## Current Architecture — MAY EVOLVE WITH USER REVIEW

```text
External Research
  -> immutable Scope Snapshot
  -> External Agent Planning
  -> Human approval
  -> Manager
  -> Fresh Builder / Task
  -> External Agent Evaluation
  -> Diagnosis / Recovery / Replan when required
  -> Project Completion Report
  -> CLOSED_VALIDATED
  -> External Research for next change/version
```

External Agent sessions are disposable compute. Workspace checkpoints are durable working memory. Deterministic state/scripts are authority.

## External Agent Resumability Contract

A fresh compatible External Agent with zero prior conversation history must be able to:

1. read authoritative workflow state;
2. verify the active work binding/fingerprint;
3. load a compact resume capsule;
4. identify completed work units and the next bounded unit;
5. continue without redoing valid expensive reasoning.

Planning, Diagnosis, Recovery, and Evaluation use this principle. Recovery additionally verifies working-tree/baseline state because it may modify production code.

## Manager / Builder Boundary

External Agent checkpoint/scratch context must not automatically enter Builder context. Manager and Builder consume the approved execution package and runtime Task state, not Planning conversations or provider-specific reasoning history.

## Owner Feedback / Change Policy

This is a living owner-intent document. It may be changed when the user/owner:

- changes or clarifies a requirement;
- agrees to a new architecture principle;
- intentionally replaces or retires an invariant;
- provides new expectations for how Project Template should evolve.

Do not silently weaken, remove, or reinterpret a **MUST** requirement. When user feedback changes a MUST or architecture-level expectation:

1. update `Objective_dev.md`;
2. update the README `VERSION / CHANGE CYCLE` when workflow architecture is affected;
3. update deterministic validation when the invariant is machine-checkable;
4. record the material change in `CHANGELOG.md`.

## New Maintainer / Model Bootstrap

When another model, agent provider, or human continues development of Project Template itself:

1. read `VERSION`;
2. read `Objective_dev.md`;
3. read the README canonical `VERSION / CHANGE CYCLE`;
4. inspect relevant current repository implementation;
5. use `CHANGELOG.md` only as needed for historical rationale;
6. identify the actual problem/root cause before redesigning;
7. preserve MUST invariants unless the user explicitly changes them;
8. evaluate token/cost and reliability impact;
9. define deterministic verification for the change.

## Scope Boundary

`Objective_dev.md` is **not**:

- External Research input for an unrelated user project;
- a Scope Snapshot;
- `EXECUTE/project_details.md`;
- normal Manager/Builder context;
- runtime authority.

It exists to preserve the intent and owner expectations of the **Project Template repository itself** across future development tools, models, and providers.
