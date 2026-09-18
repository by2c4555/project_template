> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.
# Research and Scope Model

## 1. Purpose

This document defines the boundary between:

```text
External Research
    ↓
Research Handoff
    ↓
Project Template runtime
    ↓
Planning Finalization
    ↓
Accepted Scope
```

It exists because External Research is valuable but cannot be treated as trusted runtime authority.

## 2. External Research Is Outside Runtime

External Research may occur in:

- ChatGPT;
- another web chat;
- another external AI agent;
- a human research process;
- any other preparation environment.

Project Template cannot reliably control:

- whether the Research prompt is followed perfectly;
- whether the user answered every material question;
- whether sources are current;
- whether claims are correct;
- whether the Research AI omitted contradictions;
- whether confidence is calibrated;
- whether the external conversation remains available.

Therefore External Research is outside Workplan authority.

It is not:

- a lifecycle stage;
- a Work item;
- a Cycle;
- a runtime role;
- a resumable Workplan conversation;
- Scope authority.

## 3. Research Helper Material

Project Template may provide:

- Research instructions;
- Research protocols;
- prompts;
- Project Details templates;
- examples;
- recommended evidence format.

These are external preparation helpers.

They may strongly instruct Research to:

- clarify material product intent;
- ask the user when product choices are unresolved;
- research technical facts;
- inspect repository evidence;
- provide sources;
- identify uncertainty;
- avoid irrelevant context;
- produce a focused handoff.

Prompt adherence is useful but cannot be runtime authority.

## 4. Research Optimization Target

External Research should optimize for:

```text
maximum useful information
/
minimum irrelevant context
```

The Research AI should do as much expensive discovery as practical so scarce Planning capacity is spent on:

- semantic finalization;
- material verification;
- architectural judgment;
- execution-authority design.

Research should not intentionally leave obvious factual work for Planning merely because Planning is stronger.

## 5. Recommended Research Handoff Coverage

A strong handoff should contain applicable information in the following classes.

### 5.1 Product / Scope Candidate

- problem/objective;
- users/actors;
- required behavior;
- observable success;
- mandatory constraints;
- compatibility requirements;
- non-goals/exclusions;
- current-vs-desired behavior;
- unresolved product questions.

### 5.2 Repository / Existing-System Knowledge

- repository identity/baseline;
- current relevant behavior;
- relevant architecture;
- modules/files/components;
- interfaces;
- data model;
- dependencies;
- existing tests/validation;
- known technical constraints;
- likely change surfaces.

### 5.3 External Technical Knowledge

- official documentation findings;
- version/compatibility findings;
- platform/runtime constraints;
- feasibility evidence;
- migration considerations;
- relevant standards/protocol facts.

### 5.4 Design Candidates

Research may prepare non-authoritative candidates:

- architecture options;
- preliminary interface design;
- preliminary data-model design;
- trade-offs;
- risk analysis;
- candidate migration strategy;
- candidate verification strategy.

Research may recommend one candidate.

Planning owns final choice.

### 5.5 Evidence Map

Material claims should, where practical, preserve:

```text
claim
source / repository evidence
freshness/applicability
confidence / uncertainty
impact if wrong
suggested Planning verification need
```

The exact artifact schema belongs to runtime/protocol implementation.

## 6. Handoff Status

A Research Handoff is:

```text
high-value
possibly expensive to produce
focused
evidence-bearing
non-authoritative
```

It must be treated as untrusted input until runtime checks and Planning semantic finalization occur.

## 7. Structural Import Boundary

Project Template runtime begins at handoff import.

Deterministic import may validate:

- required files;
- required top-level fields/sections;
- syntax/schema;
- referenced support files;
- path safety;
- file integrity/digests;
- protocol/version compatibility;
- structurally malformed references;
- explicitly declared readiness fields where used.

Structural validation should not pretend to prove semantic correctness.

Successful import produces:

```text
Imported Research Package
```

not:

```text
Accepted Scope
```

## 8. Scope Candidate vs Research Knowledge

Imported information should be interpreted conceptually as:

```text
Imported Research Package
├─ Scope Candidate
└─ Research Knowledge
```

### Scope Candidate

Candidate statements about product WHAT / WHY, including:

- objective;
- required behavior;
- constraints;
- compatibility;
- acceptance;
- non-goals.

### Research Knowledge

Technical evidence and reasoning that may inform Planning, including:

- repository findings;
- external technical facts;
- architecture candidates;
- interface/data candidates;
- risks;
- verification candidates.

Neither class becomes runtime authority merely by import.

## 9. Semantic Finalization Belongs to Planning

Planning must inspect the Imported Research Package and determine whether it is semantically sufficient.

Planning may:

- accept supported findings;
- reject unsupported findings;
- correct technical conclusions;
- investigate missing facts;
- resolve contradictions;
- mark evidence stale/inapplicable;
- request a user decision;
- choose among design candidates;
- add technical findings discovered during finalization.

Planning must not silently invent a missing material product requirement.

## 10. Material Unknown Classification

Planning should classify unresolved unknowns into:

```text
USER_DECISION_REQUIRED
RESEARCH_RESOLVABLE
PLANNING_DECISION
EXTERNAL_BLOCKER
```

### 10.1 USER_DECISION_REQUIRED

A material product choice cannot safely be inferred.

Examples:

- mandatory platform support;
- externally visible behavior;
- required backward compatibility;
- destructive/non-destructive policy;
- business/domain constraint;
- required acceptance outcome.

Continuation:

```text
Planning pauses affected finalization
    ↓
USER_ACTION_REQUIRED
    ↓
user supplies decision
    ↓
Planning resumes
```

### 10.2 RESEARCH_RESOLVABLE

The missing answer is factual or technical and can be established from:

- repository evidence;
- authoritative external sources;
- controlled investigation.

Planning investigates it directly.

### 10.3 PLANNING_DECISION

The unknown is a technical design choice that does not redefine product intent.

Planning decides it.

Examples may include:

- internal library choice;
- internal decomposition;
- interface implementation detail;
- data structure choice;
- task sequencing.

### 10.4 EXTERNAL_BLOCKER

Correctness depends on information/environment/ownership unavailable to Planning.

The blocker must remain explicit.

Planning must not hide it behind assumptions.

## 11. Scope Acceptance

Planning Finalization produces Accepted Scope only when:

- material product intent is sufficiently clear;
- material contradictions are resolved;
- required user decisions are resolved;
- technical unknowns are resolved or safely bounded;
- acceptance intent is sufficiently clear;
- compatibility constraints are sufficiently clear;
- Planning can proceed without inventing product requirements.

Accepted Scope is then deterministically recorded/bound according to runtime implementation.

## 12. Scope Authority

After acceptance, Scope becomes the product authority for the active Cycle.

Scope authority must be:

- explicit;
- durable;
- immutable except through an authorized higher-level revision path;
- digest/binding safe where implementation uses digests;
- independent of external conversation state.

Imported Research remains evidence/knowledge.

It does not outrank Accepted Scope.

## 13. Scope Defect After Acceptance

If later evidence shows Accepted Scope is materially defective or ambiguous:

- Execution must not silently reinterpret it.
- Builder must not redefine it.
- Manager must not redefine it.
- Recovery must not manufacture new product Scope.

The issue must route to the appropriate Planning/owner boundary.

A corrected/new external handoff may be required when product intent itself must change.

## 14. Freshness and Applicability

Research evidence can become stale.

Planning should consider:

- repository revision;
- package/library version;
- documentation version;
- platform/runtime version;
- date-sensitive facts;
- changed product intent.

A claim that was correct during Research may no longer be applicable during Planning.

Freshness checking should be proportional to impact.

## 15. Research-to-Planning Efficiency Rule

Planning should reuse strong Research where:

- evidence is clear;
- source is suitable;
- applicability is current;
- impact is low/moderate;
- no contradiction exists.

Planning should independently verify where impact is material.

This avoids both failure modes:

```text
blind trust
    and
blind repetition
```

## 16. Cross-Cycle Boundary

A completed Cycle may produce durable knowledge that informs later external Research.

Canonical boundary:

```text
CLOSED_VALIDATED
    ↓
Completion Report / durable knowledge
    ↓
outside runtime
    ↓
new External Research
    ↓
new Research Handoff
    ↓
Import
    ↓
Planning Finalization
    ↓
new Accepted Scope
```

Previous Scope does not silently become the next Cycle's Scope.

Previous Research does not silently become current evidence.

## 17. Anti-Patterns

Do not implement:

### Research as Runtime Authority

```text
Research Handoff
    ↓
immediately immutable Scope
```

without Planning semantic finalization.

### Research as Runtime Lifecycle

```text
WORKPLAN_NEXT
    ↓
EXECUTE_RESEARCH
```

for the normal Project Template runtime path.

### Planning as Blind Compiler

```text
Imported Research
    ↓
Tasks
```

without semantic verification/finalization.

### Planning as Full Re-Research

```text
ignore Research
    ↓
rediscover everything
```

unless evidence proves the handoff unusable.

## 18. Core Invariants

```text
External Research is outside runtime.

Research Handoff is input, not authority.

Import proves structure/integrity, not semantic truth.

Planning is the mandatory semantic finalizer.

Accepted Scope is created only after Planning Finalization.

Planning may decide technical design.

Planning may not invent unresolved material product intent.

Active runtime must not depend on external Research chat history.
```
