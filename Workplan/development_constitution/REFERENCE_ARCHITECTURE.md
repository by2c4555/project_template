> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Project Template Reference Architecture

## 1. Purpose

This document is the canonical whole-system architecture map.

Detailed subsystem semantics are owned by the architecture modules referenced below.

## 2. System Context

```text
════════ EXTERNAL RESEARCH ENVIRONMENT ════════

User
    ↓
External Research AI / Human Research
    ↓
Research Handoff

════════ PROJECT TEMPLATE RUNTIME ═════════════

Research Import / Structural Validation
    ↓
Immutable Archived Research Revision
    ↓
consumed package cleared from ingest
    ↓
Planner Adapter
    ↓
Planning A
Research Investigation & Finalization
    │
    ├─ RESEARCH_REVISION_REQUIRED
    │      ↓
    │  Human-facing Research Revision Report
    │      ↓
    │  AWAITING_RESEARCH
    │      ↓
    │  new Research Handoff / revision
    │      ↓
    │  Planning A revision / delta reconciliation
    │
    └─ RESEARCH_SUFFICIENT
           ↓
       Draft Finalized Scope
    ↓
USER SCOPE APPROVAL
    ↓
Accepted Scope
    ↓
Planning B
Implementation Planning
    ↓
Candidate Planning Package
    ↓
Deterministic Planning Package Validation
    ↓
Validated Planning Package
    ↓
USER EXECUTION APPROVAL
    ↓
PLAN_READY
    ↓
VS Code Copilot Execution
    ↓
Task / Phase Gates
    ↓
Evaluation Adapter
    ↓
Independent Evaluation
    ↓
Completion Knowledge Package preparation
    ↓
Deterministic Finalization
    ↓
CLOSED_VALIDATED
    ↓
Completion Knowledge Package exported

════════ EXTERNAL NEXT VERSION ════════════════

Completion Knowledge Package exported/available
    ↓
new external action/request
    ↓
Next-Version External Research
```

## 3. Environment Boundaries

Project Template coordinates runtime across:

```text
1. Research Import + Trust Boundary
2. Runtime-Controlled External High-Reasoning Planning Environment
3. VS Code Copilot Execution Environment
4. Runtime-Controlled External Diagnosis / Recovery / Evaluation Environment
5. Deterministic State / Authority / Reporting Surfaces
```

Planner and Evaluation providers may change. Provider/model-specific behavior must cross a canonical adapter boundary before becoming runtime-consumable artifacts or results. Adapter semantics are owned by `architecture/AGENT_ADAPTER_BOUNDARIES.md`.

External Research itself is outside runtime.

`External` in the Diagnosis / Recovery / Evaluation environment describes where strong reasoning may execute; it does **not** mean that lifecycle authority is outside Project Template runtime control.

### 3.1 Lifecycle Authority Boundaries

Runtime presence, active Cycle authority, and production execution authority are different boundaries:

```text
Research Handoff enters Import
    ↓
PROJECT TEMPLATE RUNTIME INGRESS
    │
    │ no active development Cycle authority yet
    ▼
Planner Adapter
    ↓
Planning A
Research Investigation & Finalization
    │
    ├─ insufficient Research → AWAITING_RESEARCH + new Research revision
    └─ sufficient Research
           ↓
       Draft Finalized Scope
    ↓
valid SCOPE_APPROVAL
    ↓
Accepted Scope is deterministically bound
    ↓
ACTIVE DEVELOPMENT CYCLE AUTHORITY BEGINS
    ↓
Planning B
Implementation Planning
    ↓
valid EXECUTION_APPROVAL
    ↓
PLAN_READY
    ↓
PRODUCTION EXECUTION AUTHORITY BEGINS
```

A provisional Cycle identifier may exist earlier for bookkeeping if implementation requires it, but it must not grant active Cycle authority before Accepted Scope exists.

Detailed binding/resume semantics are owned by `architecture/STATE_BINDING_AND_RESUME.md`.

## 4. Capability Allocation

```text
External Research
    -> broad/deep preparation

Planner / Evaluation Adapters
    -> provider/model invocation boundary
    -> canonical context/output normalization
    -> no lifecycle or approval authority

Planning
    -> strongest normal runtime reasoning
    -> semantic finalization
    -> implementation authority synthesis

Manager
    -> execution coordination
    -> local debugging
    -> repair strategy

Builder
    -> bounded implementation

Deterministic Workplan
    -> state
    -> Research revision identity/archive binding
    -> routing
    -> approvals
    -> tickets
    -> bindings
    -> generations
    -> gates
    -> repair limits
    -> closure

Human-Facing Report Surface
    -> one discoverable project report history
    -> presentation/reference only, never authority
```

## 5. Planning Boundary

Planning has two logical sub-phases:

```text
Planning A
Research Investigation & Finalization
    ↓
Draft Finalized Scope
    ↓
User Scope Approval
    ↓
Accepted Scope

Planning B
Implementation Planning
    ↓
Candidate Planning Package
    ↓
Deterministic Planning Package Validation
    ↓
Validated Planning Package
    ↓
User Execution Approval
    ↓
PLAN_READY
```


### 5.1 Research Revision Boundary

A consumed Research Handoff becomes an immutable archived Research revision before Planning depends on it.

`Workplan/ingest/` is a transient ingress mailbox, not durable Research storage. After successful import/archive verification, runtime binds to the archived Research revision and the consumed package is cleared from ingest.

Planning A may return `RESEARCH_REVISION_REQUIRED` when material missing, contradictory, stale, or weak evidence prevents responsible Scope finalization. This is a normal controlled outcome, not Scope rejection and not implementation failure.

A replacement Research Handoff creates a new Research revision and new Planning revision/binding. Valid prior reasoning may be carried forward as knowledge, but prior Research/Planning identity is never silently rebound.

## 6. User Approval Points

Normal material approval points:

```text
SCOPE_APPROVAL
EXECUTION_APPROVAL
CHANGE_APPROVAL
```

Approval details are owned by:

`architecture/USER_APPROVAL_AND_COST_CONTROL.md`

Research insufficiency is also separate from approvals. `RESEARCH_REVISION_REQUIRED` returns the workflow to an awaiting-Research boundary without creating an approval rejection.

User control actions are separate from approvals:

```text
PAUSE
RESUME
CANCEL
```

Their lifecycle semantics are owned by `architecture/RUNTIME_LIFECYCLE_AND_TRANSITIONS.md`.

## 7. Execution Hierarchy

```text
Cycle
  └─ Phase
      └─ Task
          └─ Attempt
```

Attempt kinds:

```text
INITIAL
REPAIR
RECOVERY
```

Every Builder dispatch creates a fresh Attempt.

The canonical `Cycle -> Phase -> Task -> Attempt` hierarchy refers to an **active development Cycle**, whose authority begins at Accepted Scope.

No Phase, Task, or production Attempt authority may exist before that boundary.

## 8. Execution Environment

```text
VS Code
  +
Copilot Agent
  +
ExecutionManager
  +
Builder
```

### Manager

- coordination;
- Task-local reasoning;
- debugging;
- failure interpretation;
- repair strategy;
- escalation recognition.

### Builder

- bounded mutation;
- CLI/file operations;
- straightforward implementation;
- verification execution;
- evidence production.

### Deterministic Workplan

- lifecycle routing;
- tickets;
- bindings;
- generations;
- approval validity;
- mutation authority;
- gates;
- issue routing;
- finalization.

## 9. Canonical Task Flow

```text
Eligible Task
    ↓
fresh INITIAL Attempt
    ↓
Builder
    ↓
Verification / Evidence
    ↓
Task Gate
    ├─ PASS → next Task / Phase Gate
    └─ FAIL
         ↓
       Failure Record
         ↓
       Manager Diagnosis
         ↓
       REPAIR or Escalation
```

## 10. Local Repair

```text
INITIAL FAIL
    ↓
Manager Diagnosis #1
    ↓
REPAIR #1
    ↓
...
    ↓
Manager Diagnosis #5
    ↓
REPAIR #5
    ↓ FAIL
ESCALATED ISSUE
```

No sixth local Repair Attempt.

## 11. Gates

Task Gate owns deterministic Task PASS.

Phase Gate owns deterministic Phase PASS.

Details:

`architecture/TASK_AND_PHASE_GATES.md`

## 12. Escalation

Structural, exhausted, or authority-level failures may route to:

```text
External Diagnosis
    ↓
External Recovery / Planning / Owner Action
```

If the required continuation materially changes cost or authority beyond the approved envelope:

```text
USER RE-APPROVAL REQUIRED
```

## 13. Independent Evaluation

After required Phase Gates pass:

```text
Evaluation Adapter
    ↓
Independent Evaluation
    ↓
PASS / PASS_WITH_FINDINGS
    ↓
Completion Knowledge Package preparation
    ↓
Deterministic Finalization
    ↓
CLOSED_VALIDATED
```

Blocking evaluation routes through Diagnosis/Recovery/Planning as applicable.

## 14. CLOSED_VALIDATED

`CLOSED_VALIDATED` is both:

1. terminal state of the current Cycle;
2. producer boundary for durable next-version knowledge.

Required Completion Knowledge Package contents must exist and validate before deterministic finalization may establish `CLOSED_VALIDATED`.

## 15. Completion Knowledge Package

Conceptually:

```text
Completion Knowledge Package
├─ Completion Report
├─ Final Repository Baseline
├─ Verified Architecture State
├─ Scope Outcome
├─ Accepted Decisions
├─ Known Limitations
├─ Deferred Work
├─ Repair / Recovery Lessons
└─ Next-Version Research Seed
```

It is knowledge, not next Scope.

`CLOSED_VALIDATED` ends the current runtime. The package becomes available to a future separately initiated External Research process; next-version Research does not auto-start.

## 16. Authority Matrix

| Concern | Authority |
|---|---|
| User intent | User |
| External Research | Outside runtime |
| Research Handoff | External input intentionally submitted for processing; not semantic truth/authority |
| Research revision identity/archive binding | Deterministic import/runtime |
| Research semantic sufficiency | Planning |
| Planner/Evaluation provider adaptation | Adapter boundary; no approval/lifecycle authority |
| Import structure/integrity | Deterministic import |
| Research semantic finalization | Planning |
| Draft Finalized Scope | Planning |
| Scope approval | User approval + deterministic binding |
| Accepted Scope | Bound approved Scope |
| Implementation Planning | Planning |
| Planning Package structural/binding/traceability validation | Deterministic Workplan/validator |
| Execution approval | User approval + deterministic binding |
| PLAN_READY | Deterministic Workplan after valid approval |
| Routing | Deterministic Workplan |
| Local debugging | Manager |
| Production mutation | Builder under bounded ticket |
| Task PASS | Task Gate |
| Phase PASS | Phase Gate |
| Escalated root-cause reasoning | External Diagnosis |
| Recovery design | External Recovery |
| Material re-approval | User |
| Runtime pause/cancel control | User + deterministic runtime handling |
| Trust/instruction classification | Deterministic policy + current authority |
| Final acceptance | Independent Evaluation + deterministic finalization |
| Human-facing report history | `Workplan/reports/` presentation/reference surface; no runtime authority |
| Durable workflow truth | Repository/filesystem state |
| Development constitution | Human repository owner |

## 17. Canonical Runtime Intent

```text
RUNTIME INGRESS / PRE-CYCLE AUTHORITY
IMPORT
  ↓
ARCHIVE RESEARCH REVISION + CLEAR INGEST
  ↓
PLANNING A
Research Investigation & Finalization
  │
  ├─ RESEARCH_REVISION_REQUIRED
  │      ↓
  │  AWAITING_RESEARCH
  │      ↓
  │  NEW RESEARCH REVISION
  │      ↓
  │  PLANNING A REVISION
  │
  └─ RESEARCH_SUFFICIENT
         ↓
     SCOPE_APPROVAL
  ↓
Accepted Scope
  ↓
════════ ACTIVE DEVELOPMENT CYCLE AUTHORITY BEGINS ════════
  ↓
PLANNING B
Implementation Planning
  ↓
PLANNING PACKAGE VALIDATION
  ↓
EXECUTION_APPROVAL
  ↓
PLAN_READY
  ↓
════════ PRODUCTION EXECUTION AUTHORITY BEGINS ════════════
  ↓
EXECUTION
  ↓
EVALUATION
  ↓
CLOSURE PREPARATION
  ↓
CLOSED_VALIDATED
```

External Research is not a runtime state.

Planning A is runtime activity but occurs before active development Cycle authority.

## 18. Exception Path

```text
Task/Phase/Evaluation failure
    ↓
Failure Record
    ↓
Manager local repair when legal
    ↓
or
External Diagnosis
    ↓
Recovery / Planning / Owner Action
    ↓
if material envelope changed
USER RE-APPROVAL
    ↓
revised authority
```

## 19. Resume Architecture

A fresh runtime session should be able to continue from durable:

- state;
- immutable archived Research revision(s) and lineage;
- Research revision reports/carry-forward knowledge where relevant;
- Planning checkpoints;
- approvals;
- Accepted Scope;
- Planning Package;
- tickets;
- Attempts;
- gates;
- Failure Records;
- issues;
- bindings.

External Research chat replay must not be required.

## 20. Detailed Architecture Module Index

- Research/Scope: `RESEARCH_AND_SCOPE_MODEL.md`
- Planning: `PLANNING_MODEL.md`
- Runtime Lifecycle / Transitions: `architecture/RUNTIME_LIFECYCLE_AND_TRANSITIONS.md`
- Research Revision / Carry-Forward: `architecture/RESEARCH_REVISION_AND_CARRY_FORWARD.md`
- Reporting / Human Review: `architecture/REPORTING_AND_HUMAN_REVIEW.md`
- Agent Adapter Boundaries: `architecture/AGENT_ADAPTER_BOUNDARIES.md`
- Trust / Input Boundaries: `architecture/TRUST_AND_INPUT_BOUNDARIES.md`
- User Approval / Cost Control: `architecture/USER_APPROVAL_AND_COST_CONTROL.md`
- Authority: `architecture/AUTHORITY_MODEL.md`
- Execution: `architecture/EXECUTION_MODEL.md`
- Gates: `architecture/TASK_AND_PHASE_GATES.md`
- Failure / Repair: `architecture/FAILURE_AND_REPAIR_MODEL.md`
- Diagnosis / Recovery: `architecture/DIAGNOSIS_AND_RECOVERY.md`
- Evaluation / Closure / Next Version: `architecture/EVALUATION_CLOSURE_AND_NEXT_VERSION.md`
- State / Binding / Resume: `architecture/STATE_BINDING_AND_RESUME.md`
- Context / Cost: `architecture/CONTEXT_AND_COST_MODEL.md`
