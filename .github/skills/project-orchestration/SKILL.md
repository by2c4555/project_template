---
name: project-orchestration
description: Persistent project orchestration for knowledge refinement, planning, task graph validation, issue routing, replanning, integration gates, and release handoff.
user-invocable: false
disable-model-invocation: false
---

# Project Orchestration

This skill manages project-level workflow. It does not implement production code.

## State First

Always read:

```text
EXECUTE/PROJECT_STATUS.md
EXECUTE/PROJECT_CONFIG.md
```

before project-level work.

Do not rely on previous chat state.

## Authority

```text
EXECUTE/docs/
= raw source material
= AI read-only

EXECUTE/reference/
= curated project knowledge
= Planning/Replanning read-write
= Execution read-only

EXECUTE/plan/
= project-wide decisions

EXECUTE/tasks/
= bounded work orders

EXECUTE/issues/
= persistent problem/handoff state

src/ + test/
= implementation reality
```

## Lazy Context Rule

Load only context required for the current phase.

### Planning
May load project details, raw docs selectively, Knowledge Index and selected reference files, and relevant repository evidence.

### Execution Routing
Do not replay Planning. Read only global status, active Task metadata, selected Builder profile, and exact referenced context.

### Replanning
Load current Plan, active Issue, affected Knowledge IDs, selected history, affected Tasks, and selected source documents only when needed.

Never read all history or all source documents by default.

## Input / Knowledge Refinement

Before architecture planning:

1. validate `EXECUTE/project_details.md`;
2. inventory `EXECUTE/docs/`;
3. separate requirements from factual claims;
4. normalize terminology;
5. detect duplication, contradiction, and unsupported assumptions;
6. verify architecture-critical claims when evidence is available;
7. write only useful refined knowledge under `EXECUTE/reference/`;
8. update `KNOWLEDGE_INDEX.md` with stable IDs, status, provenance, and evidence;
9. mark unresolved items `USER_STATED`, `INFERRED`, `UNKNOWN`, or `DISPUTED`;
10. increment knowledge revision and persist state.

Do not rewrite raw docs. Do not create empty reference files without useful content.

## Knowledge Promotion

Execution discoveries are not automatically project knowledge.

Builder discoveries first belong in Task history or Issues.

During Planning/Replanning, promote a discovery to `reference/` only when it is verified, durable, useful beyond the current Task, and not already represented by a more authoritative artifact.

Preserve provenance. Supersede incorrect/outdated knowledge rather than silently erasing why it changed.

## Planning

Architecture planning is independent of Builder size.

Create/refine `EXECUTE/plan/IMPLEMENTATION_PLAN.md`.

Before Task design, validate:

- requirements coverage;
- architecture consistency;
- component boundaries;
- interfaces/contracts;
- data models;
- DB/API behavior where applicable;
- error behavior;
- external dependencies;
- runtime/install model;
- security/performance constraints;
- critical end-to-end path;
- release criteria.

Do not create final executable Tasks before the Plan is valid.

## Risk-First Planning

Identify assumptions which, if false, would invalidate substantial downstream work.

Create early validation work for external APIs, DB/schema compatibility, authentication/provider compatibility, hardware/OS/runtime support, packaging/install feasibility, performance assumptions, and other architecture-critical dependencies.

Prefer early proof over late discovery.

## Vertical Slice

The early Task graph should normally establish:

```text
foundation
-> critical risk proof
-> minimal end-to-end vertical slice
-> integration validation
-> feature expansion
```

Do not postpone first realistic integration until project end.

## Builder Selection

Builder agent files are the authoritative source of context profiles.

Discover profiles from:

```text
.github/agents/builder*.agent.md
```

If project config is `AUTO`, assign the smallest safe Builder per Task.

Do not duplicate Builder limits in this skill.

Every Task must record required Builder profile, profile source, planned context estimate, and `SAFE` assessment.

If a Task does not safely fit:

1. split by reasoning boundary;
2. select a larger Builder only when the work remains inherently indivisible.

## Test Generation

Follow `PROJECT_CONFIG.md`.

For `hybrid`:

- Planning creates stable specification-derived tests under `test/contract/`;
- Builder creates implementation-specific unit/integration/regression tests.

Planner-owned tests must map to stable requirements/contracts and avoid unnecessary private implementation details.

## Task Contract

Every Task must define:

- objective / Definition of Done;
- Plan refs;
- Knowledge refs;
- dependencies;
- required Builder;
- Context Budget;
- Exploration Budget;
- External I/O Budget;
- Environment Contract;
- bounded Context Manifest;
- Required Evidence;
- Allowed/Out-of-Scope;
- acceptance criteria;
- test ownership;
- verification matrix;
- stop conditions;
- completion condition;
- current result.

## Environment Contract

Any Task requiring external access must explicitly name required `.env.user` variables.

If `.env.user` is absent, create placeholders only:

```text
KEY=__REQUIRED__
```

Never guess API keys, passwords, tokens, endpoints, DB URLs, hosts, ports, or credentials.

Missing/invalid values:

```text
PROJECT_STATUS = WAITING_USER
-> report exact variables
-> STOP before external access
```

Production access and database write access are denied by default.

## Issue Routing

Classify meaningful issues:

```text
LOCAL_REPAIR
CORRECTIVE_TASK
KNOWLEDGE_REVIEW_REQUIRED
REPLAN_REQUIRED
EXTERNAL_ACTION_REQUIRED
EXECUTOR_SWITCH_REQUIRED
```

### LOCAL_REPAIR
Current Plan and Task remain valid.

### CORRECTIVE_TASK
Plan remains valid but additional bounded work is required. Create a new Task ID. Do not rewrite completed history.

### KNOWLEDGE_REVIEW_REQUIRED
Execution evidence conflicts with curated project knowledge. Stop normal execution and return control to the configured Planning model.

### REPLAN_REQUIRED
A verified assumption, contract, architecture rule, or Task graph is no longer valid. Stop normal execution and replan affected scope only.

### EXTERNAL_ACTION_REQUIRED
Credentials, permissions, service availability, or user-owned environment action is required. Persist `WAITING_USER` and stop.

### EXECUTOR_SWITCH_REQUIRED
Task is valid but selected executor is too small/incompatible. Do not alter the Task to bypass the mismatch.

## Replanning

Replanning is continuation, not restart.

Preserve completed Tasks, execution history, verified knowledge, valid tests, and valid decisions.

If knowledge was wrong, refine it first.

If the Plan changes materially:

1. archive the previous validated Plan under `EXECUTE/plan/revisions/`;
2. increment Plan revision;
3. update affected Plan sections only;
4. invalidate affected pending Tasks;
5. generate new corrective/replacement Tasks;
6. preserve historical Tasks/Runs;
7. revalidate the Task graph.

If a Planning model is required but unavailable/unspecified:

```text
PLANNING_MODEL_REQUIRED
-> WAITING_USER
-> STOP
```

## Integration Gates

Do not infer integrated correctness from isolated Task PASS results.

At planned integration points, exercise realistic cross-component paths and actual contract/environment constraints.

Gate failure blocks dependent downstream work until repaired or replanned.

## Release

Required final Task chain:

```text
system-test
-> package
-> clean-install
-> release-gate
```

Project COMPLETE requires all enabled release gates PASS.

## Checkpointing

Before a major stage:

```text
stage = IN_PROGRESS
persist
```

After validated completion:

```text
stage = PASS
persist next_action
```

On interruption resume, inspect and validate current incomplete artifacts before continuing.

## Project-Level Stop Rules

Stop and persist state when user input, Planning model selection, Knowledge review, Replan, external action, executor switch, or unresolved required gate failure is encountered.

Do not bypass these states.
