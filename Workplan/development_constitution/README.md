> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.
# Project Template Development Constitution

## Purpose

`Workplan/development_constitution/` defines the human-owned development constitution for **Project Template itself**.

These documents keep Project Template development stable across AI sessions, models, providers, machines, and future versions. They define:

- what Project Template is;
- what it optimizes;
- what its runtime boundary is;
- how Research, Planning, Execution, Diagnosis, Recovery, and Evaluation relate;
- which authority belongs to deterministic software;
- which architectural invariants must not drift;
- how an AI developing Project Template must reason before changing implementation.

This directory is:

```text
development guidance for Project Template itself
NOT runtime authority for a user project
NOT a runtime system prompt
NOT user-project Scope
NOT Planning Package authority
```

## Ownership

The entire directory is:

```text
HUMAN OWNED
AI READABLE
AI NON-MUTABLE
```

An AI may:

- read these files;
- analyze and compare implementation against them;
- use them as development guidance;
- report conflicts;
- draft proposed changes outside this directory.

An AI must not create, edit, modify, rewrite, move, rename, delete, replace, reformat, migrate, or automatically synchronize any file under:

```text
Workplan/development_constitution/
```

If requested development conflicts with this constitution:

```text
AI detects conflict
    ↓
AI reports CONSTITUTION_CHANGE_REQUIRED
    ↓
AI identifies exact affected constitution
    ↓
AI proposes replacement/new content outside this directory
    ↓
repository owner reviews and updates constitution explicitly
    ↓
AI rereads the complete updated constitution
    ↓
development continues
```

## Core System Boundary

The constitutional boundary is:

```text
OUTSIDE PROJECT TEMPLATE RUNTIME
────────────────────────────────
User
    ↓
External Research AI / Web Chat / Human Research
    ↓
Research Handoff
    │
    │ high-value input, not authority
    ▼

PROJECT TEMPLATE RUNTIME
────────────────────────────────
Research Import / Structural Validation
    ↓
Imported Research Package
    ↓
Planning
    ├─ Research Investigation & Finalization
    │      ↓
    │   Accepted Scope
    │   Finalized Research Knowledge
    │
    └─ Implementation Planning
           ↓
       Validated Planning Package
    ↓
Execution
    ↓
Independent Evaluation
    ↓
CLOSED_VALIDATED
```

External Research is not a Workplan lifecycle stage.

Planning is the strongest normal runtime reasoning stage and is the mandatory semantic finalizer between external Research input and runtime authority.

## Documents

### `OBJECTIVE.md`

Owns the product constitution:

- product identity;
- system boundary;
- optimization objective;
- engineering principles;
- authority principles;
- capability/cost allocation;
- lifecycle invariants;
- execution/recovery philosophy;
- resumability;
- evaluation;
- governance;
- long-term direction.

It answers:

```text
WHAT are we building?
WHY are we building it?
WHAT are we optimizing?
WHAT must remain true?
```

### `RESEARCH_AND_SCOPE_MODEL.md`

Owns the external Research and Scope boundary:

- status of External Research;
- expected Research Handoff quality;
- Research Handoff as untrusted high-value input;
- structural import boundary;
- Scope Candidate vs Research Knowledge;
- material unknown handling;
- user-decision boundary;
- Planning finalization handoff;
- Accepted Scope creation;
- cross-Cycle Research handoff.

It answers:

```text
WHAT may Research prepare?
WHAT does Project Template trust?
WHEN does product Scope become authority?
```

### `PLANNING_MODEL.md`

Owns the Planning reasoning model:

```text
Planning
    ├─ Research Investigation & Finalization
    └─ Implementation Planning
```

It defines:

- why Planning is the strongest normal runtime reasoning stage;
- selective independent verification;
- material unknown classification;
- Scope finalization;
- implementation planning;
- Scope coverage;
- Phase/Task authority;
- context/path authority;
- verification/evidence design;
- repair policy;
- checkpoint/resume behavior;
- Planning revision boundaries.

It answers:

```text
WHAT must Planning decide?
WHAT must Planning verify?
WHAT authority may Planning create?
```

### `REFERENCE_ARCHITECTURE.md`

Owns the canonical architectural realization:

- environment boundaries;
- end-to-end control flow;
- Manager/Builder responsibilities;
- `Cycle -> Phase -> Task -> Attempt`;
- Task Gate and Phase Gate;
- local repair;
- durable failure evidence;
- Diagnosis;
- Recovery;
- issue lifecycle;
- Evaluation;
- closure and next-Cycle boundary;
- authority matrix;
- state-machine intent.

It answers:

```text
HOW should the constitution be realized architecturally?
```

### `DEVELOPMENT_PROMPT.md`

Owns instructions for an AI developing **Project Template itself**.

It requires development AI to:

- establish current repository truth;
- preserve the constitution;
- preserve Research/Planning boundaries;
- preserve existing good design;
- find root cause before patching;
- avoid architecture drift;
- validate negative paths;
- execute real verification;
- report constitution conflicts instead of editing constitution.

## Reading Order

For substantial Project Template development:

```text
README.md
    ↓
OBJECTIVE.md
    ↓
RESEARCH_AND_SCOPE_MODEL.md
    ↓
PLANNING_MODEL.md
    ↓
REFERENCE_ARCHITECTURE.md
    ↓
DEVELOPMENT_PROMPT.md
```

Then inspect only relevant runtime implementation, tests, configuration, migration, and documentation.

## Authority Boundary

These documents guide development of Project Template itself.

They are not:

- external Research output;
- Imported Research Package;
- Accepted Scope;
- Planning Package;
- Builder ticket;
- Task/Phase Gate evidence;
- runtime state;
- final Evaluation evidence.

Runtime authority remains in deterministic Workplan state and accepted/bound runtime contracts.

## Non-Duplication Rule

Each document owns one concern:

```text
README.md
    package map and ownership

OBJECTIVE.md
    product identity, goals, principles, invariants

RESEARCH_AND_SCOPE_MODEL.md
    Research input and Scope-authority boundary

PLANNING_MODEL.md
    Planning reasoning and authority synthesis

REFERENCE_ARCHITECTURE.md
    runtime/control-plane architecture

DEVELOPMENT_PROMPT.md
    instructions for AI developing Project Template
```

Cross-reference instead of copying whole sections between files.

A small amount of repeated invariant language is acceptable where needed to prevent ambiguity, but no file should become a second source of truth for another file's concern.
