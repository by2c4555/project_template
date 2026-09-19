> PROJECT TEMPLATE DEVELOPMENT CONSTITUTION 1.2 — Human owned. AI may read and apply this guidance; modification requires explicit authorization from a trusted repository-owner channel covering the change.

# Project Template Reference Architecture

## 1. Purpose

This document is the compact integration map for the intended system. It identifies boundaries and canonical owners. It does not duplicate their detailed rules and does not prove implementation conformance.

## 2. System context

```text
EXTERNAL
User -> External Research -> Research Handoff

PROJECT TEMPLATE RUNTIME
Import and trust validation
    -> immutable archived Research revision
    -> Planning A: sufficiency and Scope finalization
       -> Research revision loop when insufficient
    -> bound Scope Approval
    -> Accepted Scope / active Cycle
    -> Planning B: implementation authority design
    -> deterministic Planning Package validation
    -> bound Execution Approval
    -> PLAN_READY / production execution authority
    -> Manager + bounded Builder Attempts
    -> Task and Phase Gates
    -> Independent Evaluation
    -> Completion Knowledge Package
    -> deterministic finalization
    -> CLOSED_VALIDATED / runtime ends

FUTURE EXTERNAL ACTION
Completion knowledge -> separately requested Research -> new Handoff
```

Pause, block, cancel, local Repair, Diagnosis, Recovery, material Change Approval, Planning revision, and Research revision are controlled exception paths. Their transitions are owned exclusively by [RUNTIME_LIFECYCLE_AND_TRANSITIONS.md](architecture/RUNTIME_LIFECYCLE_AND_TRANSITIONS.md).

## 3. Authority boundaries

Three boundaries MUST remain distinct:

| Boundary | Begins when | Does not grant |
|---|---|---|
| Runtime ingress | A Research Handoff enters validated import processing | Accepted Scope, active Cycle, Task or mutation authority |
| Active Cycle | Valid Scope Approval is consumed and Accepted Scope is bound | Production mutation before a validated approved plan |
| Production execution | Valid Execution Approval is consumed and `PLAN_READY` is established | PASS, unbounded mutation, or later material expansion |

A provisional identifier may exist for bookkeeping before active Cycle authority. It cannot authorize Phase, Task, Attempt, Builder, gate, or production effects.

## 4. Runtime hierarchy

```text
Cycle
  -> Phase
      -> Task
          -> Attempt (INITIAL | REPAIR | RECOVERY)
```

Every new Builder implementation authorization creates a fresh Attempt. Reacquiring interrupted still-valid Work is resume, preserves Attempt identity and repair accounting, and requires reconciliation.

## 5. Capability and authority map

| Concern | Semantic/decision owner | Authority publisher or validator |
|---|---|---|
| External evidence | Research source | Import validates structure/trust and archives identity |
| Research sufficiency | Planning A | Runtime validates bound result and transition prerequisites |
| Product WHAT/WHY | Planning A proposes; user approves | Deterministic Accepted Scope binding |
| Architecture and technical HOW | Planning B | Planning-package validator checks structure/bindings/traceability |
| Material approvals | Authenticated user | Deterministic approval/binding mechanism |
| Routing and eligibility | None delegated to models | Deterministic Workplan |
| Task-local diagnosis | Manager | Runtime issues bounded Repair or escalation continuation |
| Repository mutation | Builder under ticket | Mutation boundary and Task Gate validate actual effects |
| Task/Phase PASS | No model or user | Deterministic Task/Phase Gates |
| Escalated classification/design | Diagnosis/Recovery agents | Runtime validates continuation and replacement authority |
| Final acceptance | Independent Evaluation | Deterministic finalization establishes closure |
| Human reports | Reporting surface | Reports reference authority and grant none |

Detailed authority is owned by [AUTHORITY_MODEL.md](architecture/AUTHORITY_MODEL.md).

## 6. Portable core and reference execution profile

The portable core consists of lifecycle, authority, approval, trust, state, ticket, mutation, evidence, gate, recovery, adapter, Evaluation, and closure contracts.

The current reference execution profile is:

```text
VS Code + Copilot Agent + ExecutionManager + Builder
```

Another environment is supported only when its integration demonstrates the applicable portable-core requirements. Model/provider/editor choice never grants additional authority. See [AGENT_ADAPTER_BOUNDARIES.md](architecture/AGENT_ADAPTER_BOUNDARIES.md) and [EXECUTION_MODEL.md](architecture/EXECUTION_MODEL.md).

## 7. Canonical concern ownership

| Concern | Owner |
|---|---|
| Package governance, terminology, profiles | [GOVERNANCE_AND_TERMINOLOGY.md](GOVERNANCE_AND_TERMINOLOGY.md) |
| Product identity and stable invariants | [OBJECTIVE.md](OBJECTIVE.md) |
| External Research through Accepted Scope | [RESEARCH_AND_SCOPE_MODEL.md](RESEARCH_AND_SCOPE_MODEL.md) |
| Planning A/B and Planning Package | [PLANNING_MODEL.md](PLANNING_MODEL.md) |
| Transition semantics and control conditions | [RUNTIME_LIFECYCLE_AND_TRANSITIONS.md](architecture/RUNTIME_LIFECYCLE_AND_TRANSITIONS.md) |
| Research archive/revision/carry-forward | [RESEARCH_REVISION_AND_CARRY_FORWARD.md](architecture/RESEARCH_REVISION_AND_CARRY_FORWARD.md) |
| Provider/model adapter contract | [AGENT_ADAPTER_BOUNDARIES.md](architecture/AGENT_ADAPTER_BOUNDARIES.md) |
| Instruction, data, path, privacy and side-effect trust | [TRUST_AND_INPUT_BOUNDARIES.md](architecture/TRUST_AND_INPUT_BOUNDARIES.md) |
| Approval identity, materiality and cost envelope | [USER_APPROVAL_AND_COST_CONTROL.md](architecture/USER_APPROVAL_AND_COST_CONTROL.md) |
| Decision and publication ownership | [AUTHORITY_MODEL.md](architecture/AUTHORITY_MODEL.md) |
| Manager/Builder/ticket/mutation execution | [EXECUTION_MODEL.md](architecture/EXECUTION_MODEL.md) |
| Task/Phase evidence and PASS | [TASK_AND_PHASE_GATES.md](architecture/TASK_AND_PHASE_GATES.md) |
| Local failure and Repair | [FAILURE_AND_REPAIR_MODEL.md](architecture/FAILURE_AND_REPAIR_MODEL.md) |
| Escalated Diagnosis and Recovery | [DIAGNOSIS_AND_RECOVERY.md](architecture/DIAGNOSIS_AND_RECOVERY.md) |
| Durable state, concurrency and resume | [STATE_BINDING_AND_RESUME.md](architecture/STATE_BINDING_AND_RESUME.md) |
| Evaluation, closure and next-version knowledge | [EVALUATION_CLOSURE_AND_NEXT_VERSION.md](architecture/EVALUATION_CLOSURE_AND_NEXT_VERSION.md) |
| Human-facing history and derived indexes | [REPORTING_AND_HUMAN_REVIEW.md](architecture/REPORTING_AND_HUMAN_REVIEW.md) |
| Context selection, capability and budgets | [CONTEXT_AND_COST_MODEL.md](architecture/CONTEXT_AND_COST_MODEL.md) |
| Requirement/evidence traceability | [CONFORMANCE.md](CONFORMANCE.md) |

## 8. Cross-cutting integration rules

- A subsystem artifact becomes authority only through its owning deterministic transition.
- Summaries and reports reference authoritative identities rather than copying authority into prose.
- A revision preserves predecessor identity, records changed meaning, invalidates affected downstream evidence, and obtains applicable approval.
- Control conditions such as pause and block qualify an underlying stage; they do not erase or guess that stage.
- Content changes after verification invalidate only affected evidence, determined by recorded dependencies and conservative impact analysis.
- Unsupported controls remain unavailable or explicitly non-conformant; prompts do not substitute for enforcement.

## 9. Resume architecture

A fresh capable agent/provider MUST be able to continue from durable state, bindings, archive identity, checkpoints, approvals, tickets, Attempt/failure history, issues, evidence, and repository baseline. Chat replay MUST NOT be required.

Uncertain in-flight actions, mismatched records, or changed relevant content are reconciled before new dependent dispatch or authoritative completion.

## 10. Conformance boundary

The constitution describes required behavior. Implementation and release status are recorded outside this package through release/reporting surfaces. [CONFORMANCE.md](CONFORMANCE.md) defines what evidence those records need and how claims are classified.

Conformance coverage: `C-007`, `C-009`, `C-015`, `C-019`, `C-022`.
