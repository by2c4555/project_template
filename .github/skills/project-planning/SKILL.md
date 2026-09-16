---
name: project-planning
description: Validate project input, refine Knowledge, create and validate the Implementation Plan, design Phases, compile bounded Tasks, and perform evidence-driven replanning.
---

# Project Planning

Use this procedure only with a Planner that has already passed the >=512K Context Gate.

## State Machine

Use exactly this order:

INPUT_VALIDATION
→ KNOWLEDGE_REFINEMENT
→ KNOWLEDGE_VALIDATION
→ IMPLEMENTATION_PLANNING
→ PLAN_VALIDATION
→ RISK_DESIGN
→ PHASE_DESIGN
→ TASK_COMPILATION
→ CONTRACT_TEST_DESIGN
→ TASK_PACK_VALIDATION
→ EXECUTION_READY

Never skip a failed stage.

Persist `EXECUTE/PROJECT_STATUS.md` before and after each major stage.

---

## 1. Input Validation

Required input:

`EXECUTE/project_details.md`

If missing:
- set WAITING_USER;
- identify the required file;
- STOP.

Evaluate whether the available project input contains enough information to make architecture decisions.

Check only architecture-relevant subjects:
- purpose;
- success criteria;
- scope;
- functional requirements;
- important non-functional requirements;
- critical workflows;
- runtime/platform;
- compatibility;
- database constraints;
- external systems;
- packaging/deployment;
- security;
- known risks.

Do not demand irrelevant information.

If architecture-critical information is missing:
1. create/update `EXECUTE/reference/OPEN_QUESTIONS.md`;
2. use stable question IDs;
3. explain why each answer affects architecture;
4. identify where the user should persist the answer;
5. set `project_status: WAITING_USER`;
6. set the exact `next_action`;
7. STOP.

Important answers must ultimately exist in project files, not only chat history.

---

## 2. Knowledge Refinement

Inputs:
- `EXECUTE/project_details.md`;
- relevant `EXECUTE/docs/`;
- verified repository evidence when applicable.

`EXECUTE/docs/` is raw source material. Do not silently rewrite it.

Separate:
- requirements;
- factual claims;
- assumptions.

Normalize project terminology.

Identify contradictions.

Verify architecture-critical claims when evidence is available.

Recommended Knowledge statuses:
- USER_STATED
- VERIFIED
- INFERRED
- UNKNOWN
- DISPUTED
- SUPERSEDED

Use stable Knowledge IDs.

Record provenance sufficient to trace important facts.

Create only useful Knowledge files under `EXECUTE/reference/`.

Do not create large empty documentation trees.

Update `EXECUTE/reference/KNOWLEDGE_INDEX.md`.

---

## 3. Knowledge Validation

Ask:

Is Knowledge sufficient to make architecture-critical decisions?

`UNKNOWN` or `DISPUTED` facts may remain only when they do not block architecture.

If a critical fact cannot be resolved safely:
- persist a question;
- set WAITING_USER;
- STOP.

No sufficient Knowledge
→ no Implementation Plan.

---

## 4. Implementation Planning

Create/update:

`EXECUTE/plan/IMPLEMENTATION_PLAN.md`

This is the authoritative current project decision document only after validation.

It should define durable project-wide decisions:
- project objective and success;
- scope and exclusions;
- requirements;
- architecture and rationale;
- component responsibilities;
- interfaces/contracts;
- schemas/data models;
- data/control/state flows;
- database strategy;
- external API/integration strategy;
- error semantics;
- security;
- performance;
- compatibility;
- runtime/deployment;
- packaging/install;
- testing;
- integration;
- release criteria;
- critical assumptions.

Do not put detailed Task execution logs into the Plan.

---

## 5. Plan Validation

Do not accept the Plan because a file exists.

Validate:
- requirements coverage;
- internal consistency;
- architecture feasibility;
- component boundaries;
- interface completeness;
- data-model consistency;
- database/API assumptions;
- error behavior;
- security constraints;
- compatibility;
- runtime/install behavior;
- test strategy;
- integration path;
- release path.

If invalid:
- repair only affected sections;
- validate again.

If resolution needs user information:
- persist the question;
- WAITING_USER;
- STOP.

No validated Plan
→ no executable Tasks.

---

## 6. Current User Request Compatibility

Before compiling new work from a user request, compare it with:
- validated Plan;
- current Knowledge;
- repository reality;
- completed Task state.

If the user request conflicts with a validated architectural decision:
- do not silently override the Plan;
- classify `PLAN_CHANGE_REQUIRED`;
- enter Replanning.

Task Compilation is not a second architecture-design phase.

---

## 7. Risk Design

Identify assumptions that could invalidate substantial downstream work.

Examples:
- API feasibility;
- database/schema compatibility;
- authentication provider behavior;
- platform/runtime support;
- hardware requirements;
- packaging/install feasibility;
- external service limitations;
- critical performance assumptions.

Move high-impact proof work early.

Prefer:

Foundation
→ Critical Risk Proof
→ Minimal Vertical Slice
→ Integration Gate
→ Feature Expansion

Do not postpone the first realistic integration until the project end.

---

## 8. Phase Design

Phase = meaningful project milestone + user authorization boundary.

A typical Phase contains several bounded Tasks plus one Integration Gate.

Each Phase must define:
- Phase ID;
- Goal;
- dependencies;
- ordered Tasks;
- Integration Gate;
- default Builder profile;
- external-access requirements;
- completion criteria.

Tasks inside an authorized Phase may auto-continue only after PASS.

---

## 9. Task Compilation

Default target:

Builder128K.

For every Task ask:

Can the Task safely fit Builder128K with controlled context <= 64K?

If YES:
- Builder128K.

If NO:
- determine whether it can be split along a clean reasoning boundary.

If it can be split:
- SPLIT.

If it cannot be split without breaking coherence:
- Builder256K.

Never use Builder256K merely to avoid good decomposition.

Each Task must represent one coherent, independently verifiable implementation behavior.

A normal Builder Task must not require project-wide architecture reasoning.

---

## 10. Task Execution Contract

Every Task must explicitly define:
- Goal;
- exact WRITE scope;
- exact READ context;
- focused TEST context;
- execution-critical verified facts;
- required behavior/change;
- Must Preserve behavior;
- acceptance criteria;
- verification command/procedure;
- environment requirements;
- Task-specific stop/escalation conditions;
- Builder profile;
- dependencies;
- Plan/Knowledge provenance IDs.

Avoid copying global workflow philosophy into Tasks.

---

## 11. Context Compilation

Planner owns context reduction.

Prefer:
- exact files;
- exact symbols;
- exact tests;
- exact Knowledge facts.

Avoid:
- `read src/`;
- `read all docs/`;
- loading the whole Plan for routine execution;
- loading the whole Knowledge Base;
- broad repository discovery.

Embed execution-critical facts directly in the Task.

Keep Knowledge IDs for provenance.

A Builder should not need to open a large Knowledge file merely to discover one or two facts.

---

## 12. Contract Test Design

For stable specification-derived behavior, create or define contract tests when practical.

Map:

Requirement
→ Contract
→ Contract Test
→ Task

Do not over-specify private implementation.

Builder may add:
- unit tests;
- integration tests;
- regression tests.

Builder must not weaken valid contract tests merely to obtain PASS.

---

## 13. Task Pack Validation

Before `EXECUTION_READY`, verify every Task:

- Goal is unambiguous.
- Architecture decision is already resolved.
- Scope is bounded.
- Required Builder is valid.
- Controlled context fits the selected Builder.
- Execution-critical facts are present.
- Dependencies are valid.
- Acceptance criteria are deterministic.
- Verification is executable.
- Environment contract is explicit when needed.
- Stop conditions are defined.
- Required Integration Gates exist.
- Release chain exists.

If a Task fails validation:
- repair it;
- split it;
- or assign Builder256K only when splitting would break coherence.

Do not publish an invalid Task Pack.

---

## 14. Execution Ready

When the Task Pack passes:
- set `phase: EXECUTION`;
- set `stage: PHASE_READY`;
- set `active_phase` to the first executable Phase;
- set `phase_authorized: false`;
- set `active_task` to the first Task;
- set `recommended_agent` to the required Builder;
- set precise `next_action`;
- return control to ProjectManager;
- STOP.

---

# Replanning

Replanning is continuation, not restart.

Trigger Replanning only from verified evidence or an explicit user-requested Plan change.

Load only affected context:
- current Plan;
- active Issue;
- affected Knowledge IDs;
- selected Task history;
- affected Tasks;
- repository evidence when required.

First classify the problem:

- EXECUTOR limitation;
- TASK planning defect;
- KNOWLEDGE defect;
- PLAN/architecture defect;
- EXTERNAL problem.

If only executor limitation:
- do not replan.

If Knowledge is wrong:
- correct Knowledge first;
- reassess Plan impact.

If Plan is affected:
- archive the previous meaningful Plan revision;
- revise only affected sections;
- preserve completed Tasks, valid tests, verified Knowledge, and unaffected decisions;
- invalidate only affected pending Tasks;
- compile replacement/corrective Tasks;
- validate the affected Task graph;
- return to EXECUTION_READY.

Never erase historical evidence.
