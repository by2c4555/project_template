---
name: project-planning
description: Checkpointed planning/replanning procedure that compiles high-context project knowledge into bounded isolated Tasks.
---

# Project Planning

Use only after Planner512K passes the >=524288 runtime context gate.
Execute exactly one planning transaction per invocation, persist, then STOP.

## Transaction State Machine

```text
PT1_INPUT_KNOWLEDGE
  INPUT_VALIDATION -> KNOWLEDGE_REFINEMENT -> KNOWLEDGE_VALIDATION

PT2_ARCHITECTURE_PLAN
  IMPLEMENTATION_PLANNING -> PLAN_VALIDATION

PT3_RISK_PHASES
  RISK_DESIGN -> PHASE_DESIGN

PT4_TASK_COMPILATION
  TASK_COMPILATION -> CONTRACT_TEST_DESIGN

PT5_TASK_PACK_VALIDATION
  CONTEXT_PREFLIGHT -> TASK_PACK_VALIDATION -> EXECUTION_READY
```

Never cross a transaction boundary in the same invocation.
At each boundary persist `PROJECT_STATUS.md`, return `CONTINUE_PLANNING`, and STOP so ProjectManager creates a fresh Planner context.

## PT1 — Input and Knowledge

Require `EXECUTE/project_details.md`.
Evaluate only architecture-relevant completeness: purpose, success, scope, workflows, functional/non-functional requirements, runtime/platform, compatibility, database, integrations, packaging/deployment, security, risks.

Architecture-critical missing information:
- persist stable questions in `EXECUTE/reference/OPEN_QUESTIONS.md`;
- set WAITING_USER with exact next action;
- STOP.

Refine only relevant `EXECUTE/docs/` and verified repository evidence.
Separate requirements, facts, and assumptions. Record provenance and stable Knowledge IDs.
Recommended statuses: USER_STATED, VERIFIED, INFERRED, UNKNOWN, DISPUTED, SUPERSEDED.
Critical UNKNOWN/DISPUTED -> WAITING_USER unless safely resolvable.

When Knowledge is sufficient, persist and set next transaction `PT2_ARCHITECTURE_PLAN`; return `CONTINUE_PLANNING`; STOP.

## PT2 — Architecture and Plan

Create/update `EXECUTE/plan/IMPLEMENTATION_PLAN.md` with durable project-wide decisions: objective, scope, architecture, responsibilities, interfaces, schemas, flows, DB/API strategy, errors, security, performance, compatibility, runtime/deployment, packaging, tests, integration, release, critical assumptions.

Validate requirements coverage, consistency, feasibility, boundaries, contracts, data models, integrations, security, runtime/install, test/integration/release path.

If user information is required -> persist question -> WAITING_USER -> STOP.
When validated, set `PT3_RISK_PHASES`; return `CONTINUE_PLANNING`; STOP.

## PT3 — Risk and Phases

Identify assumptions capable of invalidating substantial downstream work and move high-impact proof work early.
Prefer Foundation -> Critical Risk Proof -> Minimal Vertical Slice -> Integration Gate -> Expansion.

Phase = meaningful milestone + user authorization boundary.
Each Phase defines ID, goal, dependencies, ordered Tasks, Integration Gate, default Builder, external access, completion criteria.

Persist Phase design, set `PT4_TASK_COMPILATION`; return `CONTINUE_PLANNING`; STOP.

## PT4 — Task Compilation

Default Builder is Builder128K.

For every Task:
1. compile exact WRITE/READ/TEST context;
2. embed execution-critical verified facts;
3. define deterministic acceptance/verification;
4. assign model profile;
5. run `python scripts/context_guard.py <task-file>` after writing the Task.

Decision:
- PASS: normal Builder128K Task;
- WARN: still below hard max; tighten if practical;
- SPLIT_REQUIRED: split on a clean reasoning boundary;
- Builder256K only when clean splitting would break coherence.

Never use Builder256K merely to avoid decomposition.
A Builder Task must not require project-wide architecture reasoning.

Create contract tests for stable specification-derived behavior when practical.
After compilation, set `PT5_TASK_PACK_VALIDATION`; return `CONTINUE_PLANNING`; STOP.

## PT5 — Context and Task Pack Validation

Validate every Task:
- unambiguous Goal;
- architecture already resolved;
- exact bounded scope;
- selected Builder valid;
- `context_guard.py` is not SPLIT_REQUIRED;
- execution-critical facts embedded;
- valid dependencies;
- deterministic acceptance/verification;
- explicit environment contract;
- stop/escalation conditions;
- Integration Gates and release chain exist.

Invalid Task -> repair/split. Assign Builder256K only with coherence justification.

When pack passes:
- set phase EXECUTION;
- stage PHASE_READY;
- set active Phase/Task;
- `phase_authorized: false`;
- set recommended Builder;
- clear planning transaction or set `none`;
- precise next_action;
- return status `EXECUTION_READY`;
- STOP.

# Replanning Transaction

Use `PTR_REPLAN_AFFECTED_SCOPE` only from verified evidence or explicit user Plan change.
Load only affected Plan sections, active Issue, affected Knowledge IDs/Tasks, selected history, and required repository evidence.

Classify: EXECUTOR limitation, TASK defect, KNOWLEDGE defect, PLAN/architecture defect, EXTERNAL problem.
Executor limitation alone does not justify replanning.

If Knowledge is wrong, correct it first and reassess Plan impact. If Plan changes, archive meaningful prior revision, revise only affected sections, preserve completed/unaffected work, invalidate only affected pending Tasks, compile replacements, validate affected graph, then return to execution.

Replanning is also one isolated transaction per invocation. Never erase historical evidence.
