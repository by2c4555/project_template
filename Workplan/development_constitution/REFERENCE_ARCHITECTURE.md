> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.
# Project Template Reference Architecture

## 1. Purpose

This document is the canonical architectural realization of `OBJECTIVE.md`.

Detailed Research/Scope semantics are owned by `RESEARCH_AND_SCOPE_MODEL.md`.

Detailed Planning semantics are owned by `PLANNING_MODEL.md`.

This document owns:

- system/environment boundaries;
- end-to-end runtime flow;
- execution hierarchy;
- Manager/Builder roles;
- deterministic Workplan responsibilities;
- Task/Phase gates;
- local repair;
- durable failure records;
- external Diagnosis/Recovery;
- issue lifecycle;
- Evaluation;
- closure;
- authority matrix;
- canonical state-machine intent.

It is development guidance, not runtime authority for a user project.

## 2. System Context

Project Template separates external preparation from runtime authority.

```text
OUTSIDE PROJECT TEMPLATE RUNTIME
────────────────────────────────────────
External Research Environment
    ↓
Research Handoff
    │
    │ high-value, non-authoritative input
    ▼

PROJECT TEMPLATE RUNTIME
────────────────────────────────────────
Research Import / Structural Validation
    ↓
Imported Research Package
    ↓
External Planning Environment
    ├─ Research Investigation & Finalization
    │      ↓
    │   Accepted Scope
    │   Finalized Research Knowledge
    │
    └─ Implementation Planning
           ↓
       Validated Planning Package
           ↓
        PLAN_READY
    ↓
VS Code Copilot Execution Environment
    ↓
External Reasoning / Acceptance Environment
    ↓
CLOSED_VALIDATED
```

The main capability allocation is:

```text
External Research AI
    -> broad product/technical preparation
    -> evidence gathering
    -> candidate design analysis

Planning AI
    -> strongest normal runtime reasoning
    -> Research semantic finalization
    -> selective independent verification
    -> Accepted Scope synthesis
    -> authoritative implementation planning

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
    -> import integrity
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

External Research is outside runtime.

Its recommended responsibilities and handoff contents are defined in `RESEARCH_AND_SCOPE_MODEL.md`.

Architecturally:

```text
External Research
    ↓
Research Handoff
    ↓
runtime ingress
```

Research may provide:

- Scope Candidate;
- Research Knowledge;
- candidate architecture/design;
- evidence;
- unresolved questions.

Research does not create runtime authority.

## 4. Research Import Boundary

Import is deterministic runtime ingress.

Applicable validation may include:

- file/package structure;
- schema/syntax;
- path safety;
- declared support-file presence;
- integrity/digest;
- protocol compatibility.

Successful import produces:

```text
Imported Research Package
```

It does not produce Accepted Scope.

Semantic finalization belongs to Planning.

## 5. External Planning Environment

Planning is the strongest normal runtime reasoning stage.

Detailed Planning behavior is defined in `PLANNING_MODEL.md`.

Canonical Planning flow:

```text
══════════════ EXTERNAL PLANNING ENVIRONMENT ══════════════

Imported Research Package
        +
Current repository
        +
Applicable previous durable knowledge
 │
 ▼
Planning AI
 │
 ├─ Research Investigation & Finalization
 │    ├─ detect gaps/contradictions
 │    ├─ inspect current repository selectively
 │    ├─ investigate missing technical facts
 │    ├─ classify material unknowns
 │    ├─ selectively verify material claims
 │    ├─ request user decisions when required
 │    ├─ finalize acceptance interpretation
 │    ├─ finalize Accepted Scope
 │    └─ finalize Research Knowledge
 │
 ├─ Implementation Planning
 │    ├─ Final Architecture
 │    ├─ Interface Design
 │    ├─ Data Model Design
 │    ├─ Constraint Design
 │    ├─ Phase Design
 │    ├─ Task Design
 │    ├─ Dependency Design
 │    ├─ Verification Design
 │    ├─ Evidence Design
 │    ├─ Builder Context Design
 │    ├─ Authorized Path Design
 │    ├─ Repair Policy Design
 │    └─ Scope Coverage Validation
 │
 ▼
Validated Planning Package
 │
 ▼
PLAN_READY
```

Material Planning authority is bound before execution.

## 6. Planning Authority Boundary

Planning may create applicable authority for:

- Accepted Scope after semantic finalization;
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

Planning does not own deterministic Task PASS, Phase PASS, or final closure.

## 7. Execution Environment

### 7.1 Mandatory Environment

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

### 7.2 Manager AI

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

### 7.3 Builder AI

Builder is the lower-cost bounded implementation worker.

Typical Builder responsibilities:

- execute CLI commands;
- perform authorized file operations;
- implement straightforward code from a Task;
- apply a Manager-defined repair;
- edit configuration within authority;
- execute declared verification;
- produce structured evidence;
- stop.

Builder must not:

- expand Scope;
- redesign Planning authority;
- expand authorized write paths;
- choose lifecycle stage;
- grant deterministic PASS;
- invent an unrestricted repair strategy after failure;
- enter an open-ended diagnose/edit/retry loop.

Unexpected failure returns control to Manager.

### 7.4 Deterministic Workplan

Workplan selects and enforces:

- current lifecycle continuation;
- Planning/Execution/Evaluation routing;
- Phase;
- Task;
- Attempt kind;
- ticket;
- authorized paths;
- repair count;
- binding validity;
- generation validity;
- Task Gate;
- Phase Gate;
- external escalation;
- final closure.

No model owns deterministic PASS authority.

## 8. Execution Hierarchy

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

No production Attempt may be issued before:

```text
Accepted Scope
    +
valid bound Planning Package
```

## 9. Canonical Execution Flow

The normal Task-local path is:

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

## 10. Repair Limit

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

## 11. Task Gate

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

## 12. Phase Gate

Phase Gate owns Phase progression.

It validates applicable:

- Phase dependencies;
- all required Tasks PASS;
- declared Phase verification;
- required Phase evidence;
- integration/regression behavior;
- unresolved blocking issues.

Only Phase Gate PASS makes dependent Phases eligible.

## 13. Durable Failure Record

Every authoritative runtime failure produces or contributes to durable failure evidence.

Applicable sources include:

```text
RESEARCH_IMPORT
PLANNING_FINALIZATION
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

External Research conversation failure is outside runtime.

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

Exact runtime schema belongs to implementation.

## 14. External Reasoning Environment

External runtime reasoning contains:

```text
External Diagnosis
External Recovery
External Evaluation
```

External Research is not part of this runtime environment.

Planning is normal runtime reasoning, not an exception path.

For ordinary Task implementation failure, External Diagnosis is not the first repair path.

Default local path:

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

## 15. External Diagnosis

External Diagnosis is reasoning-only.

Inputs should include applicable:

- Accepted Scope;
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

Canonical classification vocabulary should align with runtime implementation. Applicable classes include:

```text
IMPLEMENTATION_DEFECT
TASK_DEFECT
PLAN_DEFECT
EVALUATION_DEFECT
SCOPE_DEFECT
SCOPE_AMBIGUITY
ENVIRONMENT_DEFECT
TOOLING_DEFECT
VERIFICATION_DEFECT
EXTERNAL_BLOCKER
UNKNOWN
```

Every classification must have a deterministic continuation.

A Scope defect must not be silently rewritten by execution/recovery agents.

## 16. External Recovery

External Recovery is reasoning-only.

It converts eligible Diagnosis results into a durable Recovery Contract.

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

If the required correction exceeds current Task authority, Recovery must route to the appropriate Planning/owner boundary rather than silently broaden the Task.

Recovery cannot create new product Scope.

## 17. Issue Lifecycle

Escalated issues require deterministic status progression.

Conceptually:

```text
OPEN
    ↓
AWAITING_DIAGNOSIS
    ↓
DIAGNOSED
    ↓
appropriate continuation
    ├─ RECOVERY_READY
    ├─ PLAN_REVISION_REQUIRED
    ├─ OWNER_ACTION_REQUIRED
    └─ other explicit terminal/continuation state
```

Recovery-capable path may continue:

```text
RECOVERY_READY
    ↓
IN_RECOVERY
    ↓
RESOLVED
```

Alternative dispositions may include:

```text
SUPERSEDED
PLAN_REVISION_REQUIRED
OWNER_ACTION_REQUIRED
```

Exact state names belong to implementation.

A replaced/resolved historical issue must not remain accidentally blocking.

## 18. Independent Evaluation

Evaluation begins after required Phase Gates PASS.

Canonical flow:

```text
All Required Phase Gates PASS
        │
        ▼
External Evaluation AI
        │
        ├─ Read Accepted Scope
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
Recovery / Planning / owner correction
    ↓
Manager → Builder → Gates when applicable
    ↓
Evaluation again
```

Evaluation does not repair production code directly.

## 19. CLOSED_VALIDATED and Next Cycle

Closure produces durable completion knowledge.

A completed Cycle does not automatically start another Cycle.

Conceptually:

```text
CLOSED_VALIDATED
        ↓
Completion Report
        │
        │ durable knowledge only
        ▼
════════ OUTSIDE PROJECT TEMPLATE RUNTIME ════════
User / External Research Process
        ↓
new Research Handoff
        ↓
════════ PROJECT TEMPLATE RUNTIME ════════════════
Research Import
        ↓
Planning Finalization
        ↓
new Accepted Scope
        ↓
Implementation Planning
        ↓
new execution authority
```

A future Research process may use:

- previous Completion Report;
- previous Research Knowledge;
- current repository;
- new user requirement.

Previous Scope does not silently become new Scope authority.

## 20. Authority Matrix

| Concern | Authority |
|---|---|
| User intent | User |
| External Research process | Outside Project Template runtime |
| Research Handoff | External high-value input |
| Import structure/integrity | Deterministic import/validation |
| Research semantic finalization | Planning |
| Product Scope | Planning-finalized + deterministically bound Accepted Scope |
| Finalized Research Knowledge | Planning-finalized durable knowledge |
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

## 21. Canonical State-Machine Intent

Normal runtime:

```text
IMPORT
   ↓
PLANNING
   ├─ Research Investigation & Finalization
   │      ↓
   │  Accepted Scope
   │
   └─ Implementation Planning
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

The two Planning responsibilities are logical sub-phases of Planning and need not become separate public lifecycle stages.

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
       RECOVERY / PLANNING /
          OWNER ACTION
```

Diagnosis and Recovery must not become permanent loops.

## 22. Resume Architecture

A fresh runtime session should be able to continue from durable:

- current lifecycle state;
- Imported Research Package where relevant;
- Planning checkpoints;
- Accepted Scope;
- Planning Package;
- tickets;
- Attempts;
- gate evidence;
- Failure Records;
- issue state;
- immutable bindings.

External Research conversation replay must not be required.

## 23. Development Constitution Boundary

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
repository owner updates constitution explicitly
        ↓
AI rereads complete constitution
        ↓
development resumes
```
