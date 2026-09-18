> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Planning Model

## 1. Purpose

Planning is the strongest normal reasoning stage inside Project Template runtime.

Canonical Planning:

```text
PLANNING
    ├─ A. Research Investigation & Finalization
    └─ B. Implementation Planning
```

These are logical sub-phases of one Planning authority.

## 2. Why Planning Is the Finalizer

External Research can be strong but is not runtime-controlled.

Planning can be:

- deterministically selected;
- bound to repository state;
- checkpointed;
- resumed;
- constrained by Work authority;
- required to produce durable artifacts;
- validated before execution.

Therefore Planning is the mandatory semantic finalizer.

## 3. Planning Cost Strategy

```text
Research = maximize useful information
Planning = maximize decision quality
```

Planning should not redo Research without material reason.

### 3.1 Semantic Responsibility Rule

Research may perform more total investigative work than Planning. This is intentional.

Planning does **not** need to reproduce Research in order to own semantic responsibility.

Planning must instead decide whether the available Research is sufficient for each material decision:

```text
Research produces information and evidence.

Planning judges sufficiency, resolves uncertainty,
verifies material claims when needed,
and owns the final semantic decision.
```

Planning may reuse Research conclusions when justified.

Planning must never treat Research confidence, volume, or recommendation as a substitute for Planning's own responsibility to determine whether the decision is safe to authorize.

## 4. Planning Inputs

Applicable inputs:

- Imported Research Package;
- Scope Candidate;
- Research Knowledge;
- current repository baseline;
- prior completion knowledge where relevant;
- user decisions;
- Planning revision issue/evidence;
- deterministic bindings.

## 5. Planning A — Research Investigation & Finalization

### 5.1 Early Decision-Blocker Triage

Before spending substantial strong-model reasoning on deep technical investigation, Planning should identify obvious material `USER_DECISION_REQUIRED` items.

If a user decision could materially invalidate or redirect expensive downstream investigation, Planning should request that focused decision early.

Do not ask low-value questions merely to avoid reasonable Planning decisions.

After blocker triage, Planning should:

1. identify material product objective;
2. identify observable required behavior;
3. identify acceptance expectations;
4. identify constraints and compatibility;
5. identify non-goals;
6. detect contradictions;
7. detect material omissions;
8. inspect current repository selectively;
9. identify stale/weak evidence;
10. investigate technical unknowns;
11. classify unresolved questions;
12. selectively verify material claims;
13. distinguish product decisions from technical choices;
14. request focused user decisions when required;
15. finalize acceptance interpretation;
16. produce Draft Finalized Scope;
17. produce Finalized Research Knowledge;
18. preserve material decision evidence.

## 6. Claim Materiality

### HIGH

Normally verify independently:

- architecture-driving claims;
- public interface compatibility;
- persistent data/schema;
- security/authorization;
- irreversible behavior;
- acceptance-critical claims;
- platform/runtime support;
- major migration;
- major cost/risk;
- critical feasibility.

### MEDIUM

Verify when evidence is weak, conflicting, stale, or integration-sensitive.

### LOW

Reuse when evidence is sufficient and error impact is low.

## 7. Unknown Handling

Planning classifies unresolved unknowns as:

```text
USER_DECISION_REQUIRED
RESEARCH_RESOLVABLE
PLANNING_DECISION
EXTERNAL_BLOCKER
```

No important unknown should remain an invisible assumption.

## 8. User Decision Boundary

Planning decides technical HOW.

Planning does not invent product WHAT/WHY.

User requests should be focused and only for material product decisions.

A user answer that resolves `USER_DECISION_REQUIRED` changes Planning input.

It does not by itself approve the resulting Draft Finalized Scope.

```text
USER_DECISION_REQUIRED answer
    ≠
SCOPE_APPROVAL
```

After incorporating the answer, Planning A must produce/revise the Draft Finalized Scope and present the normal bound Scope Approval transition.

## 9. Planning A Output

```text
Draft Finalized Scope
Finalized Research Knowledge
Material Decision Record
Remaining Non-Blocking Uncertainty
Evidence/Provenance References
```

## 10. Scope Approval Handoff

Planning A must produce a concise user-reviewable Scope Approval Summary before asking for approval.

It should contain:

- objective;
- required behavior;
- compatibility;
- constraints;
- non-goals;
- material Planning resolutions;
- assumptions;
- major risks;
- consequence of approval.

Planning A must not continue into expensive Implementation Planning if valid Scope Approval is required but missing.

## 11. Planning B — Implementation Planning

After Accepted Scope:

```text
Accepted Scope
    +
Finalized Research Knowledge
    +
current repository
```

Planning owns applicable:

- final architecture;
- interfaces;
- data model;
- global constraints;
- decisions;
- risks;
- Phase decomposition;
- Task decomposition;
- dependencies;
- authorized paths;
- Builder read context;
- acceptance mapping;
- verification;
- evidence requirements;
- repair policy.

## 12. Scope Coverage

Every material requirement must trace through:

```text
Accepted Scope
    ↓
Architecture / Constraint
    ↓
Phase / Task
    ↓
Verification
    ↓
Evidence
    ↓
Independent Evaluation
```

## 13. Phase Design

Use Phases where they improve dependency control, integration safety, verification boundaries, or recovery clarity.

A simple project may use an implicit Phase.

## 14. Task Design

Tasks should be:

- explicit;
- bounded;
- context-limited;
- path-limited;
- verifiable;
- suitable for a lower-cost Builder.

## 15. Authorized Path Design

Authorized paths must be minimal sufficient and bound to Task authority.

They must not silently expand during an Attempt.

## 16. Builder Context Design

Provide only necessary Task contracts, constraints, code, interfaces, and evidence.

Context expansion is read authority only.

## 17. Verification Design

Planning may define:

- unit tests;
- integration tests;
- build/compile;
- static checks;
- CLI simulation;
- mock input;
- sample input;
- negative-path tests;
- migration checks;
- regression checks.

Verification must map to acceptance.

## 18. Evidence Design

Evidence may include:

- command and exit result;
- test result;
- structured output;
- generated artifact;
- mutation manifest;
- relevant logs;
- before/after state;
- sample/mock results.

A Builder summary is not evidence by itself.

## 19. Repair Policy

Hard maximum for ordinary Task-local Repair Attempts:

```text
5
```

Planning may choose less.

Structural/authority defects may escalate earlier.

## 20. Planning B Output

Planning B produces:

```text
Candidate Planning Package
```

The exact artifact schema belongs to runtime implementation, but must preserve equivalent authority concerns.

Planning must not self-declare its own package runtime-valid.

### 20.1 Deterministic Planning Package Validation

Before execution approval, deterministic validation must establish applicable structural/binding/traceability readiness:

- required artifacts/fields exist;
- Accepted Scope binding matches;
- generation/repository binding matches;
- material Scope coverage is represented;
- Phase/Task graph references are valid;
- dependencies resolve;
- authorized paths are valid/bounded;
- verification/evidence contracts exist where required;
- blocking unknowns/issues are not silently omitted;
- integrity metadata/digests are valid.

Successful validation produces:

```text
Validated Planning Package
```

This validator does not judge architecture quality or replace Planning semantic responsibility.

Validation failure routes back to Planning B or the correct earlier boundary.

## 21. Execution Approval Handoff

Before `PLAN_READY`, Planning must produce a concise execution review:

- Accepted Scope;
- architecture;
- Phases;
- Task count/shape;
- major affected areas;
- destructive changes;
- compatibility impact;
- migration impact;
- execution complexity;
- important risks;
- verification strategy;
- requested execution envelope.

User Execution Approval must bind to the specific Planning revision/digest.

## 22. Planning Checkpoints

Useful logical checkpoints include:

```text
RESEARCH_REVIEW_STARTED
MATERIAL_UNKNOWNS_CLASSIFIED
RESEARCH_FINALIZATION_COMPLETE
SCOPE_APPROVAL_PENDING
SCOPE_ACCEPTED
ARCHITECTURE_FINALIZED
TASK_GRAPH_FINALIZED
VERIFICATION_FINALIZED
EXECUTION_APPROVAL_PENDING
PLANNING_PACKAGE_READY
```

Exact names belong to implementation.

## 23. Planning Resume

A fresh Planning session should continue from durable artifacts and checkpoints, not external chat replay.

## 24. Planning Revision

Revision must preserve:

- issue identity;
- previous authority;
- reason for revision;
- changed decisions;
- new bindings;
- supersession of stale authority;
- whether re-approval is required.

## 25. Anti-Patterns

Do not:

- blindly trust Research;
- blindly repeat all Research;
- create Tasks before Scope finalization/approval;
- invent product requirements;
- over-plan trivial work;
- use Planning as routine production editor.

## 26. Planning Invariants

```text
Planning is mandatory semantic finalizer.

Research is optimized for information production.

Planning is optimized for decision correctness.

Planning may reuse Research, but cannot delegate final semantic responsibility to Research.

Planning is strongest normal runtime reasoning.

Scope approval precedes Accepted Scope authority.

Accepted Scope precedes Implementation Planning authority.

Deterministic Planning Package validation precedes Execution approval.

Execution approval precedes PLAN_READY.

Planning reuses strong Research.

Planning selectively verifies material Research.

Planning owns technical HOW.

Planning does not own deterministic PASS.
```
