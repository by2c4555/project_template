> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Research and Scope Model

## 1. Purpose

This document owns the boundary:

```text
External Research
    ↓
Research Handoff
    ↓
Import
    ↓
Imported Research Package
    ↓
Planning Research Investigation & Finalization
    ↓
Draft Finalized Scope
    ↓
User Scope Approval
    ↓
Accepted Scope
```

## 2. External Research Is Outside Runtime

External Research may occur in any external environment.

Project Template cannot reliably control external prompt adherence, source quality, conversation completeness, user answers, or provider behavior.

Therefore External Research is not:

- a Workplan lifecycle stage;
- runtime Work;
- Cycle authority;
- Scope authority;
- durable runtime conversation state.

## 3. Research Helper Material

Project Template may provide prompts, protocols, templates, examples, and recommended handoff structure.

These improve handoff quality but do not create runtime authority.

## 4. Research Optimization Target

```text
maximum useful information
/
minimum irrelevant context
```

Research should perform broad/deep discovery so scarce Planning capacity is spent on finalization and material judgment.

## 5. Recommended Handoff Coverage

A strong handoff should include applicable:

### Product / Scope Candidate

- objective;
- users/actors;
- required behavior;
- observable success;
- constraints;
- compatibility;
- non-goals;
- unresolved product questions.

### Repository/System Knowledge

- relevant current behavior;
- architecture;
- modules/files;
- interfaces;
- data model;
- dependencies;
- tests;
- likely change surfaces.

### External Technical Knowledge

- official docs;
- version/compatibility;
- platform/runtime constraints;
- feasibility;
- migration considerations.

### Design Candidates

- architecture options;
- preliminary interfaces;
- preliminary data model;
- trade-offs;
- risks;
- candidate verification.

### Evidence Map

For material claims:

```text
claim
source/evidence
freshness/applicability
confidence/uncertainty
impact if wrong
suggested Planning verification need
```

## 6. Research Handoff Status

Research Handoff is:

```text
high-value
focused
evidence-bearing
possibly expensive
non-authoritative
```

## 7. Structural Import

Deterministic import may validate:

- required files;
- syntax/schema;
- required fields/sections;
- references;
- path safety;
- integrity/digests;
- protocol compatibility.

Successful import produces:

```text
Imported Research Package
```

not Accepted Scope.

## 8. Imported Research Package

Conceptually:

```text
Imported Research Package
├─ Scope Candidate
└─ Research Knowledge
```

Neither becomes authority merely by import.

## 9. Planning Semantic Finalization

Planning may:

- accept supported findings;
- reject unsupported findings;
- correct technical conclusions;
- inspect current repository evidence;
- investigate missing facts;
- resolve contradictions;
- identify stale evidence;
- request user decisions;
- select design candidates.

Planning must not invent missing material product requirements.

## 10. Unknown Classification

```text
USER_DECISION_REQUIRED
RESEARCH_RESOLVABLE
PLANNING_DECISION
EXTERNAL_BLOCKER
```

### USER_DECISION_REQUIRED

A material product choice cannot safely be inferred.

### RESEARCH_RESOLVABLE

A technical/factual answer can be established by investigation.

### PLANNING_DECISION

A technical design choice does not redefine product intent.

### EXTERNAL_BLOCKER

Required evidence/owner/environment is unavailable.

## 11. Draft Finalized Scope

Planning A produces a Draft Finalized Scope when:

- material intent is clear;
- contradictions are resolved;
- acceptance intent is clear;
- technical unknowns are resolved or bounded;
- required user decisions have been identified.

Draft Finalized Scope is not yet Accepted Scope authority.

## 12. User Scope Approval

The user reviews the finalized material Scope envelope.

Approval must be bound to the exact subject/revision/digest.

Only after valid approval does deterministic runtime establish Accepted Scope.

## 13. Accepted Scope

Accepted Scope is:

- explicit;
- durable;
- bound;
- stale-safe;
- authoritative for product WHAT/WHY during the active Cycle.

Imported Research remains knowledge/evidence and cannot override Accepted Scope.

## 14. Scope Defect After Acceptance

Execution, Manager, Builder, Recovery, and Evaluation must not silently rewrite Scope.

If Scope is materially defective:

```text
issue
    ↓
Planning / owner boundary
    ↓
focused correction / user decision
    ↓
new approval if material
```

A new external Research Handoff may be required if product intent itself changed.

## 15. Freshness

Planning should consider:

- repository revision;
- dependency version;
- documentation version;
- platform/runtime version;
- date-sensitive facts;
- changed product intent.

## 16. Efficiency Rule

Avoid both:

```text
blind trust
blind repetition
```

Reuse strong evidence.

Re-verify material claims.

## 17. Cross-Cycle Boundary

```text
CLOSED_VALIDATED
    ↓
Completion Knowledge Package
    ↓
outside runtime
    ↓
new External Research
    ↓
new Research Handoff
```

Completion Knowledge Package is not next Scope.

## 18. Core Invariants

```text
External Research is outside runtime.

Research Handoff is input, not authority.

Import proves structure/integrity, not semantic truth.

Planning finalizes semantics.

User Scope Approval authorizes finalized product Scope.

Accepted Scope exists only after valid approval/binding.

Runtime must not depend on external Research chat history.
```
