> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.
# Planning Model

## 1. Purpose

Planning is the strongest normal reasoning stage inside Project Template runtime.

Planning exists to protect decision quality before lower-cost implementation begins.

Its responsibilities are intentionally broader than "write an implementation plan."

Canonical Planning:

```text
PLANNING
    ├─ A. Research Investigation & Finalization
    └─ B. Implementation Planning
```

These are logical sub-phases of one Planning authority.

Do not create additional public roles or lifecycle stages merely to represent these sub-phases unless a real deterministic authority requirement is established.

## 2. Why Planning Is the Finalizer

External Research can be deep and expensive, but Project Template does not control the external environment strongly enough to trust it as authority.

Planning is inside runtime and may be:

- selected by deterministic routing;
- bound to a specific repository baseline;
- given explicit context;
- checkpointed;
- resumed;
- constrained by Work authority;
- required to produce durable artifacts;
- validated before execution;
- prevented from granting itself deterministic PASS.

Therefore Planning is the correct semantic finalizer.

## 3. Planning Capability Principle

Planning should use the strongest suitable reasoning available for the project.

Planning reasoning budget should be spent on:

- ambiguity resolution;
- contradiction detection;
- material evidence verification;
- architecture;
- compatibility-sensitive decisions;
- acceptance completeness;
- authority synthesis;
- Task/Phase design.

Planning budget should not be wasted on:

- repeating well-supported low-risk Research;
- rereading irrelevant repository areas;
- regenerating evidence already durable and sufficient;
- routine source-code implementation.

## 4. Planning Inputs

Planning should receive applicable:

- Imported Research Package;
- Scope Candidate;
- Research Knowledge;
- current repository baseline;
- previous Completion Report/knowledge when relevant;
- current Planning revision issue when applicable;
- explicit user decisions;
- deterministic Work ticket/bindings.

Imported Research is not yet Accepted Scope.

## 5. Planning A — Research Investigation & Finalization

### 5.1 Objective

Convert:

```text
Imported Research Package
    +
current repository evidence
    +
required user decisions
```

into:

```text
Accepted Scope
    +
Finalized Research Knowledge
```

### 5.2 Required Reasoning

Planning should:

1. identify the material product objective;
2. identify required externally observable behavior;
3. identify acceptance expectations;
4. identify mandatory constraints and compatibility boundaries;
5. identify non-goals/exclusions;
6. inspect Research contradictions;
7. inspect missing material information;
8. identify stale/weak/inapplicable claims;
9. compare Research claims with current repository evidence;
10. investigate missing technical facts;
11. distinguish product decisions from technical decisions;
12. classify unresolved unknowns;
13. independently verify material claims;
14. resolve technical unknowns;
15. request user action only where product intent is genuinely unresolved;
16. produce durable finalization decisions;
17. finalize Accepted Scope;
18. finalize implementation-relevant Research Knowledge.

## 6. Claim Triage

Planning should not verify every Research statement equally.

Classify claims by materiality.

### HIGH materiality

Independent verification is normally required when a claim materially affects:

- architecture;
- public interfaces;
- backward compatibility;
- persistent data/schema;
- security/authorization;
- irreversible behavior;
- acceptance validity;
- platform/runtime support;
- major migration;
- major cost/risk;
- critical implementation feasibility.

### MEDIUM materiality

Verify when:

- evidence is weak;
- sources conflict;
- repository state changed;
- choice has meaningful integration impact.

### LOW materiality

May be reused when:

- evidence is sufficient;
- applicability is clear;
- error would not materially redirect implementation.

## 7. Unknown Classification

Every unresolved material unknown should become one of:

```text
USER_DECISION_REQUIRED
RESEARCH_RESOLVABLE
PLANNING_DECISION
EXTERNAL_BLOCKER
```

Planning must not leave important unknowns as invisible assumptions.

## 8. User Decision Boundary

Planning may choose technical HOW.

Planning may not invent material product WHAT / WHY.

If a product decision is unresolved:

```text
Planning checkpoint
    ↓
USER_ACTION_REQUIRED
    ↓
durable user decision
    ↓
Planning resumes
```

The requested user decision should be as focused as possible.

Do not ask the user to decide implementation details that Planning is supposed to own.

## 9. Research-Resolvable Unknowns

Planning may investigate:

- current repository behavior;
- library/framework capability;
- version compatibility;
- protocol constraints;
- external technical facts;
- feasibility;
- likely migration behavior.

Planning should use the smallest sufficient context/evidence chain.

## 10. Planning Decisions

Planning owns technical decisions that do not redefine product intent.

Examples:

- final architecture;
- internal module boundaries;
- interface design;
- data-model design;
- internal library selection;
- decomposition;
- dependency ordering;
- verification approach;
- authorized paths;
- Builder context;
- repair policy.

## 11. Finalization Output

Planning A should produce or update durable artifacts that represent:

```text
Accepted Scope
Finalized Research Knowledge
material decision record
remaining non-blocking uncertainty
evidence/provenance references
```

Exact file names and schemas belong to runtime implementation unless separately standardized.

Accepted Scope must be bindable and immutable for downstream authority.

## 12. Finalization Completion Criteria

Research Investigation & Finalization is complete only when:

- no unresolved material product decision remains;
- material contradictions are resolved;
- technical blockers are resolved or explicitly external;
- acceptance intent is sufficient;
- compatibility constraints are sufficient;
- Scope can be stated without material hidden assumptions;
- Planning can start implementation planning without redefining product intent.

## 13. Planning B — Implementation Planning

### 13.1 Objective

Convert:

```text
Accepted Scope
    +
Finalized Research Knowledge
    +
current repository state
```

into:

```text
Validated Planning Package
```

### 13.2 Planning Responsibilities

Planning owns applicable:

- final architecture;
- global constraints;
- interfaces;
- data model;
- technical decisions;
- known risks;
- Phase decomposition;
- Task decomposition;
- dependencies;
- authorized production paths;
- required read context;
- acceptance criteria mapping;
- verification;
- evidence requirements;
- repair policy.

## 14. Planning Package

The current Project Template implementation may represent Planning authority with artifacts such as:

```text
plan/IMPLEMENTATION_PLAN.md
plan/PHASES.json                    # when explicit phases are needed
tasks/TASK_INDEX.md
tasks/TASK_*.md
compiled/PROJECT_BRIEF.md
compiled/ARCHITECTURE.md
compiled/GLOBAL_CONSTRAINTS.md
compiled/INTERFACES.md
compiled/DATA_MODEL.md
compiled/DECISIONS.md
compiled/KNOWN_RISKS.md
```

This constitution owns the required concerns, not necessarily immutable filenames forever.

If implementation changes filenames/schema, it must preserve equivalent durable authority and migration consistency.

## 15. Scope Coverage

Every material Accepted Scope requirement must remain traceable through:

```text
Scope Requirement
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

Planning must detect orphaned Scope requirements.

No material requirement should disappear merely because it was difficult to decompose.

## 16. Phase Design

Planning should use Phases when they improve:

- dependency control;
- integration safety;
- verification boundaries;
- incremental delivery;
- recovery clarity.

A simple project may use an implicit phase.

Do not create Phases merely for ceremony.

## 17. Task Design

Tasks should be:

- explicit;
- bounded;
- independently understandable;
- path-authorized;
- context-limited;
- verifiable;
- small enough for a lower-cost Builder;
- large enough to produce meaningful progress.

A Task should state applicable:

- objective;
- phase;
- dependencies;
- authorized paths;
- required read context;
- acceptance;
- verification;
- evidence;
- repair budget/policy.

## 18. Authorized Path Design

Planning owns the production mutation boundary for a Task.

Authorized paths should be:

- minimal sufficient;
- explicit;
- compatible with task objective;
- immutable during an Attempt unless a higher authority revises the Task.

Recovery must not silently broaden them.

## 19. Builder Context Design

Builder read context should be selective.

Planning should provide:

- necessary Task contract;
- relevant interfaces/constraints;
- directly relevant code/docs;
- necessary evidence.

Do not default to whole-repository context.

Context expansion is read authority only.

## 20. Verification Design

Planning should define sufficient verification for each Task/Phase.

Verification may include:

- unit tests;
- integration tests;
- static checks;
- build/compile;
- CLI simulation;
- mock inputs;
- sample inputs;
- negative-path tests;
- migration checks;
- regression checks.

Verification must map to observable acceptance.

## 21. Evidence Design

Planning should define what evidence is needed for deterministic gates.

Evidence may include:

- command and exit result;
- test result;
- generated artifact;
- structured output;
- mutation manifest;
- relevant logs;
- before/after state;
- sample/mock results.

A Builder summary is not evidence by itself.

## 22. Repair Policy Design

Planning should define applicable repair limits/policy.

The system hard maximum for ordinary Task-local Repair Attempts remains 5.

Planning may choose a lower limit.

A structural or authority defect may escalate earlier.

## 23. Planning Checkpoints

Planning should preserve semantic progress through durable checkpoints.

Useful logical checkpoints include:

```text
RESEARCH_REVIEW_STARTED
MATERIAL_UNKNOWNS_CLASSIFIED
RESEARCH_FINALIZATION_COMPLETE
SCOPE_ACCEPTED
ARCHITECTURE_FINALIZED
TASK_GRAPH_FINALIZED
VERIFICATION_FINALIZED
PLANNING_PACKAGE_READY
```

Exact checkpoint names belong to implementation.

The purpose is resumability, not lifecycle proliferation.

## 24. Planning Resume

A fresh Planning session should be able to continue from durable:

- Imported Research Package;
- current repository baseline/bindings;
- prior finalization decisions;
- Accepted Scope if already accepted;
- Planning artifacts;
- checkpoints;
- revision issue/evidence when applicable.

Planning must not require replay of the external Research chat.

## 25. Planning Revision

A later diagnosis may prove:

- Task contract defective;
- Plan defective;
- architecture defective;
- Scope defective/ambiguous.

Planning revision must preserve:

- issue identity;
- previous authority;
- why revision is required;
- changed decisions;
- new bindings;
- supersession of stale authority.

Do not silently mutate bound Planning authority.

## 26. Scope Defect During Planning/Execution

If product Scope itself must change:

- Planning must not disguise it as a technical plan change.
- Execution agents must not rewrite Scope.
- Recovery must not rewrite Scope.

Route to the appropriate owner/user/external boundary.

A new/corrected Research Handoff may be required.

## 27. Cost Discipline

The cost strategy is:

```text
Research AI
    -> broad/deep preparation
    -> high throughput

Planning AI
    -> scarce strongest reasoning
    -> material verification
    -> final decisions
    -> authority synthesis
```

Planning should ask:

```text
Does redoing this Research materially reduce decision risk?
```

If no, reuse the Research.

If yes, verify the minimum sufficient evidence.

## 28. Planning Anti-Patterns

### Blind Trust

```text
Research said it
    ↓
Planning copies it
```

without material review.

### Blind Repetition

```text
Research did the work
    ↓
Planning discards it
    ↓
Planning researches everything again
```

### Premature Tasking

```text
Imported Research
    ↓
Tasks
```

before Scope finalization.

### Product Invention

Planning makes a product choice because asking the user is inconvenient.

### Over-Planning

Planning creates unnecessary Phase/Task/context complexity that does not improve execution quality.

### Planning as Production Editor

Planning directly performs routine production implementation instead of creating bounded Builder authority.

## 29. Planning Invariants

```text
Planning is the mandatory semantic finalizer.

Planning is the strongest normal runtime reasoning stage.

Planning Finalization precedes Accepted Scope authority.

Accepted Scope precedes production execution authority.

Planning reuses strong Research.

Planning selectively verifies material Research.

Planning owns technical HOW.

Planning does not invent unresolved material product WHAT / WHY.

Planning produces bounded authority suitable for lower-cost Builders.

Planning does not own deterministic PASS.
```
