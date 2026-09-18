> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Project Template Reference Architecture

## 1. Purpose

This document is the canonical architectural interpretation of `OBJECTIVE.md`.

`OBJECTIVE.md` defines **what Project Template must remain and optimize for**.

This document defines **how those principles are organized into software-development environments, roles, authority boundaries, and control flow**.

It does not duplicate the full Development Objective and is not runtime authority for a user project.

## 2. System Context

Project Template coordinates software development across four environments:

```text
1. External Research Environment
2. External Planning Environment
3. VS Code Copilot Execution Environment
4. External Reasoning / Acceptance Environment
```

The main capability allocation is:

```text
External strong reasoning
    -> Research
    -> Planning
    -> escalated Diagnosis
    -> Recovery reasoning
    -> Independent Evaluation

Manager AI
    -> execution coordination
    -> local software debugging
    -> local diagnosis
    -> repair strategy

Builder AI
    -> bounded implementation
    -> CLI/file operations
    -> straightforward code changes
    -> Manager-defined repair changes

Deterministic Workplan
    -> state
    -> routing
    -> tickets
    -> bindings
    -> repair limits
    -> gates
    -> validation
    -> closure
```

## 3. External Research Environment

### 3.1 Purpose

Research converts user intent and available evidence into:

```text
Scope Authority
    +
Research Knowledge
```

Research owns product WHAT / WHY.

### 3.2 Canonical Flow

```text
══════════════ EXTERNAL RESEARCH ENVIRONMENT ══════════════

User
 │
 ▼
External Research AI talks with User
 │
 ├─ Scope Acquisition
 ├─ Implementation Research
 ├─ Repository Analysis
 ├─ Repository Selection
 ├─ External Technical Research
 ├─ Compatibility / constraint research
 └─ Preliminary Architecture Design
 │
 ▼
Approved Research Handoff
 │
 ├─ project_details.md
 │      └─ SCOPE AUTHORITY
 │
 └─ docs/*.md
        └─ KNOWLEDGE / EVIDENCE
 │
 ▼
Research Handoff Validation
```

### 3.3 Authority Boundary

`project_details.md` owns product Scope.

Research knowledge may include preliminary architecture and implementation analysis, but those are non-authoritative technical inputs to Planning.

Research must not create authoritative implementation Tasks or mutate production code.

## 4. External Planning Environment

### 4.1 Purpose

Planning converts approved Scope and Research Knowledge into executable technical authority.

### 4.2 Canonical Flow

```text
══════════════ EXTERNAL PLANNING ENVIRONMENT ══════════════

External Planning AI
(strongest suitable reasoning model)
 │
 ├─ Read Scope Authority
 ├─ Read all Research Knowledge
 ├─ Inspect current repository
 ├─ Verify technical research
 ├─ Additional external research when required
 ├─ Validate preliminary architecture
 ├─ Improve / Finalize Architecture
 ├─ Interface Design
 ├─ Data Model Design
 ├─ Constraint Design
 ├─ Phase Design
 ├─ Task Design
 ├─ Dependency Design
 ├─ Verification Design
 ├─ Evidence Design
 ├─ Builder Context Design
 ├─ Authorized Path Design
 ├─ Repair Policy Design
 └─ Scope Coverage Validation
 │
 ▼
Validated Planning Package
 │
 ▼
PLAN_READY
```

### 4.3 Planning Authority

The validated Planning Package owns applicable:

- final architecture;
- interfaces;
- data model;
- global constraints;
- Phases;
- Tasks;
- dependencies;
- authorized paths;
- required read context;
- acceptance criteria;
- verification;
- evidence requirements;
- repair policy.

Material Planning authority is bound before execution.

## 5. Execution Environment

### 5.1 Mandatory Environment

Normal production implementation is performed through:

```text
VS Code
  +
Copilot Agent
  +
ExecutionManager
  +
Builder
```

This environment is specifically for software repository development.

### 5.2 Manager AI

Manager is the local reasoning and debugging layer.

Manager responsibilities:

- invoke deterministic Workplan routing;
- coordinate Phase/Task execution;
- inspect Task-local code/context;
- interpret compiler/test/runtime failure;
- perform local software diagnosis;
- identify likely root cause;
- design the next bounded repair strategy;
- supervise Builder;
- recognize structural/escalation boundaries.

Manager is expected to use a reasoning-capable model, normally stronger than Builder.

Manager is not the normal production editor.

### 5.3 Builder AI

Builder is the low-cost bounded implementation worker.

Typical Builder responsibilities:

- execute CLI commands;
- perform authorized file operations;
- implement straightforward code from a Task;
- apply a Manager-defined repair;
- edit configuration within authority;
- execute declared verification;
- produce structured evidence;
- stop.

Builder must not invent a new repair strategy after a failure.

Unexpected failure returns control to Manager.

### 5.4 Deterministic Workplan

Workplan selects and enforces:

- current lifecycle continuation;
- Phase;
- Task;
- Attempt kind;
- ticket;
- authorized paths;
- repair count;
- binding validity;
- Task Gate;
- Phase Gate;
- external escalation;
- final closure.

Neither Manager nor Builder owns deterministic PASS authority.

## 6. Execution Hierarchy

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

## 7. Canonical Execution Flow

The normal Task-local repair path is:

```text
════════════════ EXECUTION ENVIRONMENT ════════════════
          VS CODE COPILOT AGENT ONLY

                    Manager AI
                        │
                        ▼
               Deterministic Routing
                        │
                        ▼
                      Phase
                        │
                        ▼
                       Task
                        │
                        ▼
                 Bounded Ticket
                        │
                        ▼
                    Builder AI
                        │
                        ▼
                 Implementation
                        │
                        ▼
               Verification / Evidence
                        │
                        ▼
                    Task Gate
                        │
               ┌────────┴────────┐
               │                 │
             PASS               FAIL
               │                 │
               │                 ▼
               │          Failure Record
               │                 │
               │                 ▼
               │             Manager AI
               │          Local Debugging /
               │             Diagnosis
               │                 │
               │                 ▼
               │       Repair Strategy N
               │            N = 1..5
               │                 │
               │                 ▼
               │       Fresh REPAIR Ticket
               │                 │
               │                 ▼
               │             Builder AI
               │                 │
               │                 ▼
               │       Fresh REPAIR Attempt
               │                 │
               │                 ▼
               │        Verification / Evidence
               │                 │
               │                 ▼
               │              Task Gate
               │                 │
               │          ┌──────┴──────┐
               │          │             │
               │        PASS           FAIL
               │          │             │
               │          │       local repair
               │          │       still legal?
               │          │        │        │
               │          │       YES       NO
               │          │        │        │
               │          │        │        ▼
               │          │        │   ESCALATED ISSUE
               │          │        │        │
               │          │        │        ▼
               │          │        │ External Diagnosis
               │          │        │
               │          │        └─ next Manager diagnosis
               │          │
               │          ▼
               │       Task PASS
               │
               ▼
            Phase Gate
               │
        ┌──────┴──────┐
        │             │
      PASS           FAIL
        │             │
        │             ▼
        │       Failure Record
        │             │
        │             ▼
        │      External Diagnosis
        │
        ▼
   Next Phase / Task
        │
        ▼
All Required Phases PASS
        │
        ▼
External Evaluation
```

### 7.1 Repair Limit

For an ordinary Task-local failure chain:

```text
INITIAL Attempt
    ↓ FAIL
Manager Diagnosis #1
    ↓
Builder REPAIR #1
    ↓ FAIL
Manager Diagnosis #2
    ↓
Builder REPAIR #2
    ↓ FAIL
Manager Diagnosis #3
    ↓
Builder REPAIR #3
    ↓ FAIL
Manager Diagnosis #4
    ↓
Builder REPAIR #4
    ↓ FAIL
Manager Diagnosis #5
    ↓
Builder REPAIR #5
    ↓ FAIL
ESCALATED ISSUE
    ↓
External Diagnosis
```

A successful Repair exits immediately.

A structural defect, invalid authority boundary, or clearly non-local failure may escalate before the fifth round.

No sixth local Repair Attempt is allowed for the same failure chain.

## 8. Task Gate

Task Gate owns deterministic Task PASS.

It validates applicable:

- Task/Phase/Attempt identity;
- current generation;
- completed Work;
- ticket identity and digest;
- immutable Scope/Planning/Phase/Task bindings;
- Recovery binding when applicable;
- verification result;
- required evidence;
- artifact integrity;
- mutation manifest;
- authorized-path compliance.

Conceptually:

```text
Builder says "done"
        ≠
Task PASS

Builder Work
    +
Verification
    +
Evidence
    +
Authority validation
    +
Mutation validation
        ↓
Task Gate
        ↓
PASS / FAIL
```

## 9. Phase Gate

Phase Gate owns Phase progression.

It validates applicable:

- Phase dependencies;
- all required Tasks PASS;
- declared Phase verification;
- required Phase evidence;
- integration/regression behavior;
- unresolved blocking issues.

Only Phase Gate PASS makes dependent Phases eligible.

## 10. Durable Failure Record

Every authoritative failure produces or contributes to durable failure evidence.

Applicable sources include:

```text
RESEARCH
PLANNING
BUILDER
TASK_GATE
PHASE_GATE
RECOVERY
EVALUATION
CONTROL_PLANE
ENVIRONMENT
TOOLING
```

A normalized Failure Record should preserve enough information for a fresh reasoning model to understand the failure without prior chat.

Applicable information includes:

```text
failure identity
Cycle / Phase / Task / Attempt / Work identity
generation
failure source
observed failure
expected behavior
actual behavior
command/check and exit result
logs or durable references
verification evidence
artifact references
mutation information
Scope / Planning / Phase / Task bindings
parent failure
prior Attempts
prior Manager diagnoses
prior repair strategies
status
```

Exact schema belongs to implementation, not this architecture document.

## 11. External Reasoning Environment

External Reasoning contains:

```text
External Diagnosis
External Recovery
External Evaluation
```

For ordinary Task implementation failure, External Diagnosis is not the first repair path.

The default local path is:

```text
Task FAIL
    ↓
Manager diagnosis
    ↓
Builder repair
    ↓
Task Gate
    ↓
repeat bounded local loop
```

External reasoning is used when the problem is structural, outside local authority, exhausted, or otherwise requires materially stronger reasoning.

## 12. External Diagnosis

External Diagnosis is reasoning-only.

Inputs should include applicable:

- approved Scope;
- Planning Package;
- current repository state;
- Failure Record;
- complete Attempt history;
- Manager diagnosis history;
- verification evidence;
- mutation history;
- relevant logs/artifacts.

Diagnosis determines:

```text
observed failure
root cause
affected component
violated invariant / contract
blast radius
classification
correct recovery boundary
```

Typical classifications:

```text
IMPLEMENTATION_DEFECT
TASK_DEFECT
PLAN_DEFECT
SCOPE_DEFECT
ENVIRONMENT_DEFECT
TOOLING_DEFECT
VERIFICATION_DEFECT
EXTERNAL_BLOCKER
UNKNOWN
```

Every classification must have a deterministic continuation.

## 13. External Recovery

External Recovery is reasoning-only.

It converts Diagnosis into a durable Recovery Contract.

Canonical flow:

```text
Escalated Failure
    ↓
External Diagnosis
    ↓
Diagnosis Record
    ↓
External Recovery
    ↓
Recovery Contract
    ↓
Manager
    ↓
fresh RECOVERY Builder Attempt
    ↓
Verification / Evidence
    ↓
Task Gate
    ↓
Phase Gate
```

Recovery cannot directly mark a Task PASS.

If the required correction exceeds current Task authority, Recovery must route back to the appropriate Scope/Planning authority rather than silently broaden the Task.

## 14. Issue Lifecycle

Escalated issues require deterministic status progression.

Conceptually:

```text
OPEN
    ↓
AWAITING_DIAGNOSIS
    ↓
DIAGNOSED
    ↓
RECOVERY_READY
    ↓
IN_RECOVERY
    ↓
RESOLVED
```

Alternative terminal/continuation states may include:

```text
SUPERSEDED
PLAN_REVISION_REQUIRED
SCOPE_REVISION_REQUIRED
OWNER_ACTION_REQUIRED
```

A replaced/resolved historical issue must not remain accidentally blocking.

Exact state names belong to implementation.

## 15. Independent Evaluation

Evaluation begins after required Phase Gates PASS.

Canonical flow:

```text
All Required Phase Gates PASS
        │
        ▼
External Evaluation AI
        │
        ├─ Read approved Scope
        ├─ Read Planning Package
        ├─ Read gate evidence
        ├─ Inspect current repository
        ├─ Run sufficient independent checks
        └─ Build final acceptance evidence
        │
        ▼
PASS / PASS_WITH_FINDINGS
        │
        ▼
Completion Report
        │
        ▼
Deterministic Finalization
        │
        ▼
CLOSED_VALIDATED
```

Blocking Evaluation result:

```text
Evaluation blocker
    ↓
Failure Record
    ↓
External Diagnosis
    ↓
Recovery / higher-level correction
    ↓
Manager → Builder → Gates
    ↓
Evaluation again
```

Evaluation does not repair production code directly.

## 16. CLOSED_VALIDATED and Next Research Cycle

Closure produces durable completion knowledge.

Conceptually:

```text
CLOSED_VALIDATED
        ↓
Completion Report
        │
        │ knowledge input only
        ▼
Next Research Cycle
        ↓
new Research Handoff
        ↓
new Scope
```

The next Cycle may use:

- previous Completion Report;
- previous Research Knowledge;
- current repository;
- new user requirement.

Previous Scope does not silently become new Scope authority.

## 17. Authority Matrix

| Concern | Authority |
|---|---|
| User intent | User |
| Product Scope | Approved Research Handoff / immutable Scope |
| Research knowledge | Research artifacts |
| Final architecture | Approved Planning Package |
| Phase/Task decomposition | Approved Planning Package |
| Routing | Deterministic Workplan |
| Local debugging / repair reasoning | Manager |
| Production mutation | Builder under bounded ticket |
| Retry limit | Deterministic Workplan / approved repair policy |
| Task PASS | Task Gate |
| Phase PASS | Phase Gate |
| Escalated root-cause reasoning | External Diagnosis |
| Recovery design | External Recovery Contract |
| Final acceptance | Independent Evaluation + deterministic finalization |
| Durable workflow truth | Repository/filesystem state |
| Development constitution | Human repository owner |

## 18. Canonical State-Machine Intent

Normal lifecycle:

```text
RESEARCH
   ↓
PLANNING
   ↓
EXECUTION
   ↓
EVALUATION
   ↓
CLOSED_VALIDATED
```

Task-local side loop:

```text
Task Gate FAIL
      │
      ▼
Manager Diagnosis
      │
      ▼
Builder REPAIR
      │
      ▼
Task Gate
      │
      ├─ PASS -> normal execution
      │
      └─ FAIL
           │
           ├─ local repair remains valid and count < 5
           │      ↓
           │   Manager Diagnosis
           │      ↓
           │   next fresh REPAIR
           │
           └─ structural / invalid / count == 5
                  ↓
             ESCALATED ISSUE
                  ↓
              DIAGNOSIS
                  ↓
               RECOVERY
                  ↓
       appropriate authoritative stage
```

Diagnosis and Recovery must not become permanent loops.

## 19. Development Constitution Boundary

This Reference Architecture is human-owned.

An AI developing a later Project Template version may identify an architectural conflict but may not edit this file.

Required behavior:

```text
Architecture conflict found
        ↓
report exact conflict
        ↓
propose change outside development_constitution/
        ↓
STOP affected redesign
        ↓
repository owner updates constitution externally
        ↓
AI rereads constitution
        ↓
development resumes
```
