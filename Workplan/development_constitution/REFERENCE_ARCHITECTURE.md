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
Imported Research Package
    ↓
Planning A
Research Investigation & Finalization
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
Independent Evaluation
    ↓
Deterministic Finalization
    ↓
CLOSED_VALIDATED
    ↓
Completion Knowledge Package

════════ EXTERNAL NEXT VERSION ════════════════

Completion Knowledge Package
    ↓
Next-Version External Research
```

## 3. Environment Boundaries

Project Template coordinates runtime across:

```text
1. Research Import Boundary
2. External Planning Environment
3. VS Code Copilot Execution Environment
4. External Reasoning / Acceptance Environment
```

External Research itself is outside runtime.

## 4. Capability Allocation

```text
External Research
    -> broad/deep preparation

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
    -> routing
    -> approvals
    -> tickets
    -> bindings
    -> generations
    -> gates
    -> repair limits
    -> closure
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
Planning Package
    ↓
User Execution Approval
    ↓
PLAN_READY
```

## 6. User Approval Points

Normal material approval points:

```text
SCOPE_APPROVAL
EXECUTION_APPROVAL
CHANGE_APPROVAL
```

Approval details are owned by:

`architecture/USER_APPROVAL_AND_COST_CONTROL.md`

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
Independent Evaluation
    ↓
PASS / PASS_WITH_FINDINGS
    ↓
Completion Report
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

It must produce a Completion Knowledge Package.

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

## 16. Authority Matrix

| Concern | Authority |
|---|---|
| User intent | User |
| External Research | Outside runtime |
| Research Handoff | External input |
| Import structure/integrity | Deterministic import |
| Research semantic finalization | Planning |
| Draft Finalized Scope | Planning |
| Scope approval | User approval + deterministic binding |
| Accepted Scope | Bound approved Scope |
| Implementation Planning | Planning |
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
| Final acceptance | Independent Evaluation + deterministic finalization |
| Durable workflow truth | Repository/filesystem state |
| Development constitution | Human repository owner |

## 17. Canonical Runtime Intent

```text
IMPORT
  ↓
PLANNING
  ├─ Research Investigation & Finalization
  ├─ Scope Approval
  ├─ Accepted Scope
  ├─ Implementation Planning
  └─ Execution Approval
  ↓
PLAN_READY
  ↓
EXECUTION
  ↓
EVALUATION
  ↓
CLOSED_VALIDATED
```

External Research is not a runtime state.

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
- Imported Research Package where relevant;
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
- User Approval / Cost Control: `architecture/USER_APPROVAL_AND_COST_CONTROL.md`
- Authority: `architecture/AUTHORITY_MODEL.md`
- Execution: `architecture/EXECUTION_MODEL.md`
- Gates: `architecture/TASK_AND_PHASE_GATES.md`
- Failure / Repair: `architecture/FAILURE_AND_REPAIR_MODEL.md`
- Diagnosis / Recovery: `architecture/DIAGNOSIS_AND_RECOVERY.md`
- Evaluation / Closure / Next Version: `architecture/EVALUATION_CLOSURE_AND_NEXT_VERSION.md`
- State / Binding / Resume: `architecture/STATE_BINDING_AND_RESUME.md`
- Context / Cost: `architecture/CONTEXT_AND_COST_MODEL.md`
