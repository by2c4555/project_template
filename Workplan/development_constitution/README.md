> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Project Template Development Constitution

## Purpose

`Workplan/development_constitution/` is the human-owned development constitution for **Project Template itself**.

It exists to keep Project Template architecture stable across AI sessions, models, providers, machines, and future versions.

This directory defines:

- product identity and optimization goals;
- external Research vs runtime boundaries;
- Research revision, archival, and carry-forward semantics;
- Planning responsibilities;
- user approval and cost-control boundaries;
- runtime authority;
- execution architecture;
- Task/Phase gates;
- failure and repair;
- Diagnosis and Recovery;
- Evaluation and closure;
- centralized human-facing reporting;
- replaceable high-reasoning agent adapter boundaries;
- next-version handoff;
- durable state, binding, and resume;
- context and token/cost discipline;
- rules for AI developing Project Template.

This directory is not runtime authority for a user project.

## Ownership

The entire directory is:

```text
HUMAN OWNED
AI READABLE
AI NON-MUTABLE
```

AI may:

- read;
- inspect;
- analyze;
- compare implementation against it;
- explain it;
- use it as development guidance;
- draft proposals outside the protected repository area.

AI must not create, modify, delete, rename, reformat, migrate, or automatically synchronize files under this directory unless the repository owner explicitly authorizes modification of this protected area.

## Constitutional Layers

```text
Layer 1
OBJECTIVE.md
    ↓
What must Project Template remain?

Layer 2
REFERENCE_ARCHITECTURE.md
    ↓
How does the complete system fit together?

Layer 3
Detailed Architecture Models
    ↓
How must each subsystem behave?

DEVELOPMENT_PROMPT.md
    ↓
How must AI develop Project Template against this constitution?

Implementation + Tests
```

## Canonical Development Constitution Structure

```text
Workplan/development_constitution/
│
├─ README.md
├─ OBJECTIVE.md
├─ REFERENCE_ARCHITECTURE.md
├─ DEVELOPMENT_PROMPT.md
│
├─ RESEARCH_AND_SCOPE_MODEL.md
├─ PLANNING_MODEL.md
│
└─ architecture/
   ├─ RUNTIME_LIFECYCLE_AND_TRANSITIONS.md
   ├─ RESEARCH_REVISION_AND_CARRY_FORWARD.md
   ├─ REPORTING_AND_HUMAN_REVIEW.md
   ├─ AGENT_ADAPTER_BOUNDARIES.md
   ├─ TRUST_AND_INPUT_BOUNDARIES.md
   ├─ USER_APPROVAL_AND_COST_CONTROL.md
   ├─ AUTHORITY_MODEL.md
   ├─ EXECUTION_MODEL.md
   ├─ TASK_AND_PHASE_GATES.md
   ├─ FAILURE_AND_REPAIR_MODEL.md
   ├─ DIAGNOSIS_AND_RECOVERY.md
   ├─ EVALUATION_CLOSURE_AND_NEXT_VERSION.md
   ├─ STATE_BINDING_AND_RESUME.md
   └─ CONTEXT_AND_COST_MODEL.md
```

## Core End-to-End Boundary

```text
════════ EXTERNAL ════════

External Research
    ↓
Research Handoff

════════ PROJECT TEMPLATE RUNTIME ════════

Import / Structural Validation
    ↓
Immutable Archived Research Revision
    ↓
consumed package cleared from ingest
    ↓
Planning A
Research Investigation & Finalization
    │
    ├─ RESEARCH_REVISION_REQUIRED
    │      ↓
    │  Research revision report + carry-forward knowledge
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
Planning Package
    ↓
USER EXECUTION APPROVAL
    ↓
PLAN_READY
    ↓
Execution
    ↓
Task / Phase Gates
    │
    ├─ bounded local repair
    │
    └─ material authority/cost change
           ↓
       Diagnosis / Recovery
           ↓
       USER RE-APPROVAL
           ↓
       revised authority
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

════════ EXTERNAL NEXT VERSION ════════

Completion Knowledge Package exported/available
    ↓
new external action/request
    ↓
Next-Version External Research
    ↓
new Research Handoff
```

## Source-of-Truth Ownership Map

| Concern | Constitutional Owner |
|---|---|
| Product identity, objectives, invariants | `OBJECTIVE.md` |
| Whole-system architecture | `REFERENCE_ARCHITECTURE.md` |
| External Research → Accepted Scope | `RESEARCH_AND_SCOPE_MODEL.md` |
| Planning reasoning and implementation planning | `PLANNING_MODEL.md` |
| Runtime lifecycle and transition semantics | `architecture/RUNTIME_LIFECYCLE_AND_TRANSITIONS.md` |
| Research revision/archive/carry-forward semantics | `architecture/RESEARCH_REVISION_AND_CARRY_FORWARD.md` |
| Human-facing report surface and report history | `architecture/REPORTING_AND_HUMAN_REVIEW.md` |
| Planner/Evaluation adapter and provider boundaries | `architecture/AGENT_ADAPTER_BOUNDARIES.md` |
| Trust, untrusted input, instruction/data boundary | `architecture/TRUST_AND_INPUT_BOUNDARIES.md` |
| User approvals and cost/authority envelopes | `architecture/USER_APPROVAL_AND_COST_CONTROL.md` |
| Runtime authority ownership | `architecture/AUTHORITY_MODEL.md` |
| Manager/Builder execution | `architecture/EXECUTION_MODEL.md` |
| Task/Phase PASS | `architecture/TASK_AND_PHASE_GATES.md` |
| Task-local failure and repair | `architecture/FAILURE_AND_REPAIR_MODEL.md` |
| Escalated Diagnosis and Recovery | `architecture/DIAGNOSIS_AND_RECOVERY.md` |
| Evaluation, closure, next-version output | `architecture/EVALUATION_CLOSURE_AND_NEXT_VERSION.md` |
| State, binding, generation, resume | `architecture/STATE_BINDING_AND_RESUME.md` |
| Context and token/cost allocation | `architecture/CONTEXT_AND_COST_MODEL.md` |
| Rules for Project Template development AI | `DEVELOPMENT_PROMPT.md` |

## Reading Rule

For substantial development:

1. read `OBJECTIVE.md`;
2. read `REFERENCE_ARCHITECTURE.md`;
3. read `architecture/RUNTIME_LIFECYCLE_AND_TRANSITIONS.md` for substantial lifecycle/authority work;
4. read only the other detailed architecture modules relevant to the requested change;
5. read `DEVELOPMENT_PROMPT.md`;
6. inspect only relevant implementation/tests/config/docs.

Do not load every architecture module by default.

## Conflict Rule

If two constitutional files appear inconsistent:

1. preserve the higher-level product intent in `OBJECTIVE.md`;
2. use `REFERENCE_ARCHITECTURE.md` for whole-system integration;
3. `architecture/RUNTIME_LIFECYCLE_AND_TRANSITIONS.md` owns lifecycle transition interpretation whenever another module can be read as implying a competing transition;
4. use the specific detailed architecture module as owner of non-transition subsystem semantics;
5. report any remaining conflict rather than silently choosing a new architecture.

## Update Rule

Correct flow:

```text
AI identifies constitution conflict
    ↓
AI reports exact conflict
    ↓
AI proposes reviewable change
    ↓
AI does not modify protected constitution
    ↓
repository owner explicitly updates constitution
    ↓
AI rereads complete current constitution
    ↓
development continues
```
