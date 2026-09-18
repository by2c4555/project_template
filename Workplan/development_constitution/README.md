> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Project Template Development Constitution

## Purpose

`Workplan/development_constitution/` defines the human-owned development constitution for **Project Template itself**.

These documents exist to keep Project Template development stable across AI sessions, models, providers, and future versions. They define what Project Template is intended to become, the architecture it must preserve, and how an AI used for Project Template development must reason before changing the implementation.

This directory is **not runtime authority for a user project** and is **not a runtime system prompt** for Research, Planning, Manager, Builder, Diagnosis, Recovery, or Evaluation.

## Ownership

The entire directory is:

```text
HUMAN OWNED
AI READABLE
AI NON-MUTABLE
```

An AI may:

- read these files;
- use them as development guidance;
- compare implementation against them;
- report conflicts;
- propose a constitution change outside this directory.

An AI must not:

- edit;
- modify;
- rewrite;
- move;
- rename;
- delete;
- replace

any file under:

```text
Workplan/development_constitution/
```

If a new Project Template requirement conflicts with this constitution, the AI must report the conflict. The repository owner updates the constitution externally, after which the AI rereads the updated constitution before continuing.

## Documents

### `OBJECTIVE.md`

Defines the Project Template development constitution:

- product identity;
- core objective;
- engineering principles;
- authority principles;
- model/cost philosophy;
- non-negotiable invariants;
- failure/recovery philosophy;
- user-experience principles;
- resumability;
- change governance;
- long-term direction.

It answers:

```text
WHAT are we building?
WHY are we building it?
WHAT are we optimizing?
WHAT must remain true?
```

### `REFERENCE_ARCHITECTURE.md`

Defines the canonical architectural interpretation of `OBJECTIVE.md`.

It owns:

- environment boundaries;
- Research/Planning boundary;
- Manager/Builder responsibilities;
- execution flow;
- Task/Phase gates;
- local repair;
- durable failure evidence;
- Diagnosis/Recovery;
- Evaluation/closure;
- cross-Cycle handoff.

It answers:

```text
HOW should the constitution be realized architecturally?
```

### `DEVELOPMENT_PROMPT.md`

Defines how an AI used to develop a **new Project Template version** must work from this constitution.

It is not used by normal Project Template runtime agents.

It tells development AI to:

- establish the current repository baseline;
- read the constitution before substantial work;
- preserve existing good design;
- find root cause before patching;
- avoid architecture drift;
- identify constitution conflicts instead of editing the constitution;
- validate actual behavior before claiming completion.

## Authority Boundary

These files guide **development of Project Template itself**.

They are not:

- user-project Scope;
- Research output;
- Planning Package authority;
- Builder ticket authority;
- Task Gate evidence;
- Phase Gate evidence;
- runtime state;
- final Evaluation evidence.

Normal runtime authority remains in deterministic Workplan state, approved contracts, tickets, bindings, gates, evidence, and executable validation.

## Non-Duplication Rule

Each document owns one concern:

```text
README.md
    package boundary and ownership

OBJECTIVE.md
    identity, goals, principles, invariants

REFERENCE_ARCHITECTURE.md
    architecture and workflow boundaries

DEVELOPMENT_PROMPT.md
    instructions for AI developing Project Template
```

Do not copy the full Objective into the Architecture.

Do not copy the full Architecture into the Development Prompt.

Do not turn this README into another Objective.

## Update Rule

The Development Constitution is changed only by the repository owner outside the AI development workflow.

Correct flow:

```text
AI identifies constitution conflict
        ↓
AI reports conflict / proposes change
        ↓
AI does not edit this directory
        ↓
Repository owner updates constitution externally
        ↓
AI rereads all constitution files
        ↓
Development continues against the new constitution
```
