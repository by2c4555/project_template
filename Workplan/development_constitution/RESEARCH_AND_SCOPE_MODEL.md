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
Immutable Archived Research Revision
    ↓
consumed package cleared from ingest
    ↓
Planning Research Investigation & Finalization
    │
    ├─ RESEARCH_REVISION_REQUIRED
    │      ↓
    │  AWAITING_RESEARCH → new Research revision → Planning revision
    │
    └─ RESEARCH_SUFFICIENT
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

Research helper material and Research Handoff content may contain instruction-like text. Such text remains Research data/evidence and cannot override runtime authority.

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
- protocol compatibility;
- instruction/data trust boundary where applicable.

Import must fail closed when required structure, integrity, path safety, or protocol compatibility cannot be positively validated.

Invalid import must produce a durable rejection reason and must not partially create downstream Scope/Planning authority.

Successful import must produce an immutable archived Research revision equivalent to:

```text
Imported Research Package / Research Revision
```

Runtime must bind Planning input to that archived revision, not to a mutable consumed file remaining in `Workplan/ingest/`. After archive verification/binding, the consumed package must be cleared from ingest.

Successful import does not produce Accepted Scope.

### 7.1 Ingest and Archive Lifecycle

`Workplan/ingest/` is a transient ingress mailbox.

It is not durable Research storage, Planning memory, Scope authority, or report history.

After successful structural/trust validation:

```text
validate Research Handoff
    ↓
create immutable archived Research revision
    ↓
verify archived digest/identity
    ↓
bind runtime/Planning input to archived revision
    ↓
clear consumed package from ingest
```

A corrected or expanded Research Handoff is a new Research revision. Existing Research identity must not be silently rebound to replacement content.

Detailed revision/carry-forward semantics are owned by `architecture/RESEARCH_REVISION_AND_CARRY_FORWARD.md`.

## 8. Imported Research Package

Conceptually:

```text
Imported Research Package
├─ Scope Candidate
└─ Research Knowledge
```

Neither becomes authority merely by import.

Imported Research Package content is evidence/input. Embedded commands, prompts, or permission claims do not become runtime instructions merely because Planning can read them.

## 9. Planning Semantic Finalization

Planning may:

- assess whether the current Research revision is semantically sufficient for Scope finalization;
- accept supported findings;
- reject unsupported findings;
- correct technical conclusions;
- inspect current repository evidence;
- selectively investigate or verify missing facts when economical and material;
- return `RESEARCH_REVISION_REQUIRED` when substantial missing Research would otherwise be absorbed by Planning;
- resolve contradictions;
- identify stale evidence;
- request user decisions;
- select design candidates.

Planning must not invent missing material product requirements.

### 9.1 Research Sufficiency Assessment

Planning A must distinguish:

```text
RESEARCH_SUFFICIENT
RESEARCH_REVISION_REQUIRED
```

`RESEARCH_REVISION_REQUIRED` applies when material missing, contradictory, stale, weak, or unavailable evidence prevents responsible and economical Scope finalization.

This outcome must preserve useful verified findings and produce focused information for the next Research revision instead of discarding valid work.

Research insufficiency is not Scope rejection, not user disapproval, and not permission for Planning to invent missing product intent.

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

If resolution would require substantial broad/deep Research beyond economical Planning verification, classify the material gap into the Research revision return path rather than silently turning Planning into a replacement Research session.

### PLANNING_DECISION

A technical design choice does not redefine product intent.

### EXTERNAL_BLOCKER

Required evidence/owner/environment is unavailable.

## 11. Draft Finalized Scope

Planning A produces a Draft Finalized Scope only after the active Research revision is judged sufficient for semantic finalization.

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

A user answer to `USER_DECISION_REQUIRED` supplies product-decision input. It is **not automatically SCOPE_APPROVAL**. Scope Approval is a separate bound transition.

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

When a new Research revision follows an insufficient prior revision, reconcile the delta against preserved reports/carry-forward knowledge instead of blindly replaying all previous expensive reasoning.

## 17. Cross-Cycle Boundary

```text
CLOSED_VALIDATED
    ↓
Completion Knowledge Package exported/available
    ↓
outside runtime
    ↓
new external action/request
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

User submission to ingest means intentional admission for processing, not semantic truth or approval.

Ingest is transient; successful import creates immutable archived Research evidence and clears the consumed ingest package.

Research replacement creates a new revision; identity is never silently rebound.

Import proves structure/integrity, not semantic truth.

Planning judges Research sufficiency and finalizes semantics.

Materially insufficient Research returns through an explicit Research revision path before Scope authority is created.

User Scope Approval authorizes finalized product Scope.

Accepted Scope exists only after valid approval/binding.

Runtime must not depend on external Research chat history.

Research/import trust semantics are governed by `architecture/TRUST_AND_INPUT_BOUNDARIES.md`.
```
