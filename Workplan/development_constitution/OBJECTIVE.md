> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.
# Project Template Development Objective

## 1. Product Identity

Project Template is an **AI-assisted software-development control plane**.

Its purpose is to convert externally prepared product/research information into reliable software-development authority, then coordinate high-quality repository implementation, verification, recovery, and final acceptance.

Project Template runtime coordinates:

- Research Handoff import and structural validation;
- Research Investigation & Finalization by Planning;
- authoritative Scope finalization;
- architecture and implementation planning;
- bounded source-code implementation;
- CLI/tool execution;
- controlled file operations;
- software debugging and repair;
- verification and regression checking;
- recovery from failed implementation;
- independent final acceptance;
- durable cross-session continuation.

Project Template does **not** perform or govern the external user-facing Research conversation.

External Research may be performed by:

- ChatGPT;
- another web chat;
- another AI system;
- a human researcher;
- another preparation process.

Project Template may provide Research prompts, protocols, instructions, and templates to improve the quality and focus of that external work.

Those helper materials do not make Research a runtime lifecycle stage, Work item, Cycle, or source of runtime authority.

Project Template is not intended to become a general-purpose autonomous-agent framework.

Its architecture exists specifically to improve software-development quality, reliability, cost efficiency, auditability, and resumability.

## 2. System Boundary Principle

The constitutional boundary is:

```text
OUTSIDE PROJECT TEMPLATE RUNTIME
External Research
    ↓
Research Handoff
    ↓

PROJECT TEMPLATE RUNTIME
Research Import / Structural Validation
    ↓
Imported Research Package
    ↓
Planning
    ├─ Research Investigation & Finalization
    └─ Implementation Planning
    ↓
Execution
    ↓
Independent Evaluation
    ↓
CLOSED_VALIDATED
```

A Research Handoff is high-value input.

It is not Accepted Scope merely because it exists or passes structural validation.

Planning is the mandatory semantic finalizer.

## 3. Core Objective

Maximize:

```text
engineering quality / token / cost
```

while keeping workflow authority:

- deterministic;
- durable;
- auditable;
- bounded;
- resumable;
- provider-neutral;
- independently verifiable.

The intended capability allocation is:

```text
External Research AI
    -> maximize useful, focused information
    -> clarify user intent as far as practical
    -> perform broad repository/technical research
    -> collect evidence
    -> prepare candidate Scope and technical knowledge

Planning AI
    -> strongest normal runtime reasoning
    -> investigate missing material facts
    -> resolve contradictions
    -> selectively verify material claims
    -> finalize Research semantically
    -> finalize Accepted Scope
    -> create implementation authority

Manager
    -> local execution reasoning
    -> Task-local debugging
    -> bounded repair strategy

Builder
    -> lower-cost bounded implementation

Deterministic Workplan
    -> import integrity
    -> state
    -> routing
    -> tickets
    -> bindings
    -> gates
    -> retry limits
    -> validation
    -> closure

repository/filesystem state
    -> durable truth

chat/session state
    -> disposable context
```

## 4. Engineering Principles

Project Template development should preserve these principles:

1. Deterministic mechanisms before prompt complexity.
2. Durable repository state before conversational memory.
3. Bounded contracts before open-ended autonomy.
4. Use strong reasoning where wrong decisions have high downstream cost.
5. Use the lowest-cost capable Builder for routine implementation.
6. Executed verification before claimed completion.
7. Immutable execution bindings.
8. Explicit escalation instead of unbounded retries.
9. Resumability across sessions, models, providers, and machines.
10. Selective context instead of repository-wide context by default.
11. Negative-path validation for authority boundaries.
12. One source of truth per concern.
13. Preserve existing valid work before rewriting.
14. Fix root causes rather than accumulating compensating mechanisms.
15. Internal rigor may increase, but normal user workflow should become simpler.
16. External preparation must not be confused with runtime authority.
17. Research should maximize useful information, not authority.
18. Planning must finalize Research before implementation authority exists.
19. Planning should reuse strong Research rather than blindly repeat it.
20. Material Research claims should be independently verified when failure would materially affect architecture, compatibility, acceptance, security, irreversible behavior, or major cost/risk.
21. Planning must not invent unresolved material product requirements.
22. Technical choices that do not redefine product intent belong to Planning.
23. No runtime role may convert confidence into authority without deterministic acceptance/binding.

## 5. Authority Model

Workflow authority comes from deterministic Workplan state and accepted runtime contracts.

Authority does not come from:

- model capability;
- model price;
- provider identity;
- model confidence;
- chat context;
- prompt self-assertion;
- an external Research conversation;
- an imported Research Handoff by itself;
- a candidate architecture;
- an implementation summary;
- a model statement of PASS.

External Research material is **untrusted, high-value input**.

Structural import may prove that the handoff is readable, internally referential, and well-formed.

Structural import does not prove that Research is:

- semantically complete;
- correct;
- non-contradictory;
- current;
- sufficient for implementation authority.

Planning owns semantic finalization.

Deterministic software owns authority transitions and binding.

## 6. Canonical Software-Development Lifecycle

The normal Project Template runtime lifecycle is conceptually:

```text
IMPORT
    ↓
PLANNING
    ├─ Research Investigation & Finalization
    └─ Implementation Planning
    ↓
EXECUTION
    ↓
INDEPENDENT EVALUATION
    ↓
CLOSED_VALIDATED
```

External Research occurs before runtime ingress and is not a runtime lifecycle stage.

Diagnosis and Recovery are controlled exception paths.

They must not become alternative normal workflows or permanent loops.

## 7. Canonical Runtime Hierarchy

Execution authority remains organized as:

```text
Cycle -> Phase -> Task -> Attempt
```

Required invariants:

- no production Task authority exists before Accepted Scope and valid Planning authority;
- every Task belongs to exactly one Phase;
- each Builder dispatch creates a fresh Attempt;
- Attempt kinds include `INITIAL`, `REPAIR`, and `RECOVERY`;
- a simple project may use an implicit Phase when appropriate;
- normal users should not manually manage Phase, Task, Attempt, generation, ticket, or digest internals.

## 8. External Research Principle

External Research should do as much useful preparation as practical before handoff.

It should aim to produce:

- clear product objective;
- required behavior;
- observable acceptance expectations;
- mandatory constraints;
- compatibility requirements;
- non-goals;
- repository findings;
- current-system findings;
- interface/data/dependency findings;
- external technical evidence;
- feasibility findings;
- risks;
- candidate architecture options;
- preliminary interface/data-model ideas;
- candidate verification strategy;
- unresolved questions;
- evidence/source mapping.

The optimization target is:

```text
maximum useful information
/
minimum irrelevant context
```

Research may recommend conclusions.

Those conclusions remain non-authoritative until Planning finalizes them.

The active Project Template workflow must not depend on the external Research session remaining available.

## 9. Research Import Principle

Research import is an ingress, structure, integrity, and safety boundary.

It may validate applicable:

- required files;
- required fields/sections;
- syntax/schema;
- declared supporting files;
- path safety;
- digest/integrity;
- protocol compatibility;
- structurally invalid references.

Successful import produces:

```text
Imported Research Package
```

not:

```text
Accepted Scope
```

Semantic finalization requires Planning reasoning.

## 10. Planning Principle

Planning is the strongest normal reasoning stage inside Project Template runtime.

Planning has two mandatory logical responsibilities:

```text
A. Research Investigation & Finalization
B. Implementation Planning
```

These responsibilities should normally remain one Planning role/lifecycle authority rather than becoming extra roles merely for organizational convenience.

### 10.1 Research Investigation & Finalization

Planning must:

- inspect Imported Research;
- detect material gaps and contradictions;
- inspect current repository evidence as needed;
- investigate missing technical facts;
- identify stale/weak/inapplicable evidence;
- classify unresolved questions;
- selectively verify architecture-driving claims;
- distinguish product decisions from technical decisions;
- request user action when a material product decision cannot be safely inferred;
- finalize acceptance interpretation;
- produce Accepted Scope;
- produce Finalized Research Knowledge.

The intended division is:

```text
Research
    -> broad/deep preparation

Planning
    -> selective independent verification
    -> semantic finalization
    -> authoritative synthesis
```

### 10.2 Implementation Planning

Planning converts:

```text
Accepted Scope
    +
Finalized Research Knowledge
    +
current repository state
```

into durable execution authority.

Planning owns applicable:

- final architecture;
- constraints;
- interfaces;
- data model;
- decisions;
- risks;
- Phase decomposition;
- Task decomposition;
- dependencies;
- authorized production paths;
- Builder read context;
- acceptance criteria;
- verification;
- evidence requirements;
- repair policy.

Every material Scope requirement must remain traceable into implementation and acceptance.

Material Planning authority must not silently change after binding.

## 11. User Decision Principle

Planning may investigate technical unknowns.

Planning may make technical design decisions that do not redefine product intent.

Planning must not invent a missing material product requirement.

When a material product decision remains unresolved:

```text
Planning
    ↓
USER_ACTION_REQUIRED
    ↓
user decision
    ↓
Planning Finalization resumes
```

## 12. Selective Independent Verification Principle

Planning should independently verify Research claims when the claim materially affects:

- final architecture;
- public/compatibility-sensitive interfaces;
- schema or data migration;
- security/authorization boundaries;
- irreversible behavior;
- acceptance validity;
- major cost/risk;
- platform/runtime compatibility;
- critical implementation feasibility.

Planning should not spend scarce reasoning budget reproducing low-risk Research whose evidence is sufficient, current, and applicable.

## 13. Execution Environment Principle

Normal production implementation uses the **VS Code Copilot Agent execution environment**.

The supported execution architecture separates reasoning from mutation:

```text
Manager
    -> reasoning, coordination, local debugging, repair strategy

Builder
    -> bounded production implementation

Deterministic Workplan
    -> routing, authority, retry control, gates
```

This environment choice must not make workflow authority dependent on a specific model vendor.

## 14. Manager Capability Principle

Manager is the local software reasoning layer during execution.

Manager should have sufficient reasoning capability to:

- interpret compiler, test, and runtime failures;
- inspect failure evidence;
- debug Task-local software defects;
- identify likely root cause;
- design a bounded repair strategy;
- detect repeated or disproven strategies;
- determine whether the failure is still Task-local;
- recognize when escalation is required.

Manager is not the normal production editor.

Manager coordinates and reasons; Builder performs bounded repository mutation.

## 15. Builder Capability Principle

Builder is intentionally the lower-cost implementation worker.

Builder should receive Tasks that are:

- explicit;
- bounded;
- context-limited;
- path-limited;
- verifiable.

Typical Builder work includes:

- CLI operations;
- controlled file creation/modification/deletion;
- configuration edits;
- straightforward code implementation;
- implementation from an approved Task;
- application of a Manager-defined repair;
- declared verification commands;
- structured evidence capture.

Builder must not be relied on for open-ended debugging after its own failure.

A failed Builder must not autonomously enter an unrestricted:

```text
diagnose -> edit -> retry -> diagnose -> edit -> retry
```

loop.

## 16. Task and Phase Gate Authority

Only deterministic Task Gate logic may mark a Task PASS.

Only deterministic Phase Gate logic may mark a Phase PASS.

Manager and Builder may execute and coordinate work, but they do not own PASS authority.

Gate decisions should validate applicable:

- identity;
- generation;
- ticket;
- immutable bindings;
- verification result;
- evidence;
- mutation authority;
- current repository state.

A model statement never replaces gate evidence.

## 17. Local Debugging and Repair Principle

Ordinary Task-local software failures should first use:

```text
Builder failure
    ↓
durable failure evidence
    ↓
Manager local diagnosis
    ↓
Manager-defined repair strategy
    ↓
fresh Builder REPAIR Attempt
    ↓
Task Gate
```

Each failed Repair Attempt returns to Manager reasoning before another Repair Attempt is issued.

Local repair is bounded.

The system hard maximum is **5 local Repair Attempts for one Task failure chain**.

A structural failure, authority conflict, or clearly invalid repair boundary may escalate before the limit is exhausted.

No sixth local Repair Attempt is permitted for the same failure chain.

## 18. Durable Failure Principle

Every authoritative runtime failure must leave sufficient durable evidence for a fresh capable model/session to:

- diagnose;
- repair;
- recover;
- resume

without depending on the previous chat session.

Failure history must preserve applicable:

- original failure;
- Attempt history;
- verification results;
- Manager diagnoses;
- repair strategies;
- evidence;
- mutation information;
- authority bindings.

Failed strategies must not be silently overwritten.

External Research conversation failure is outside Project Template runtime authority.

Research Import and Planning Finalization failures are runtime boundary failures and must fail closed before production authority is created.

## 19. Escalation Principle

External strong reasoning is an exception path for failures that exceed local execution reasoning.

Escalation is appropriate when applicable:

- local repair is exhausted;
- failure is structural;
- Task authority is insufficient;
- Planning authority is defective;
- Accepted Scope appears defective;
- verification authority is defective;
- environment/tooling lies outside local authority;
- repeated strategies are disproven;
- correctness cannot be reliably determined.

Escalation should happen because materially stronger reasoning is needed, not merely because another model is available.

## 20. Diagnosis and Recovery Principle

External Diagnosis is reasoning-only.

It determines:

- what failed;
- root cause;
- affected authority;
- violated invariant/contract;
- blast radius;
- classification;
- correct recovery boundary.

External Recovery is reasoning-only.

It converts eligible Diagnosis results into a durable correction contract.

Production correction returns through:

```text
Manager
    ↓
Builder
    ↓
normal verification/evidence
    ↓
Task Gate / Phase Gate
```

Recovery must not directly mark implementation PASS.

Recovery must not silently broaden immutable Task authority.

Recovery must not manufacture new product Scope.

## 21. Issue Lifecycle Principle

Every escalated runtime issue must have a deterministic continuation and deterministic terminal disposition.

A resolved or superseded historical issue must not accidentally block later valid execution.

Issue handling must avoid:

- dangling issues;
- contradictory lifecycle/next-action state;
- permanent Diagnosis loops;
- stale blockers after approved authority replacement.

## 22. Context Principle

Context expansion is read authority only.

Additional context must never silently expand:

- Accepted Scope;
- Task objective;
- authorized write paths;
- repair authority.

Imported/Finalized Research may be read context.

Only accepted and bound contracts create runtime authority.

Builder context should remain selective and bounded.

## 23. Immutable Binding and Generation Principle

Work and Attempt authority must remain bound to the authority that existed when issued.

Resume must compare current authority with original bindings.

Original bindings must not be silently recalculated and overwritten.

Generation fencing must prevent stale sessions or agents from completing or mutating newer Work authority.

## 24. Resume Principle

Repository state is durable.

Chat/session state is disposable.

A fresh session, model, provider, or machine should be able to continue from durable:

- runtime state;
- Imported/Finalized Research artifacts where relevant;
- Accepted Scope;
- Planning authority;
- tickets;
- Attempts;
- checkpoints;
- failure evidence;
- bindings.

External Research chat history must not be required to resume an active runtime workflow.

## 25. Human Approval Principle

Human approval must remain:

- explicit;
- action-bound;
- subject-bound;
- state-bound;
- stale-safe;
- single-use where applicable.

AI must not grant its own human approval.

Approval mechanisms should exist only where genuine new cost, authority, or rework boundaries justify them.

Avoid duplicate approvals for the same already-approved envelope.

## 26. Independent Evaluation Principle

Independent Evaluation occurs after required execution gates pass.

Evaluation verifies actual repository outcomes against:

- Accepted Scope;
- Planning authority;
- gate evidence;
- current repository state.

Evaluation is review/acceptance, not production repair.

Final closure requires deterministic acceptance authority.

`CLOSED_VALIDATED` means the current Cycle satisfies its approved acceptance authority.

It does not claim perfection outside Scope.

## 27. Cross-Cycle Knowledge Principle

A completed Cycle may produce durable knowledge for future external Research.

Examples include:

- Completion Report;
- verified architectural outcomes;
- accepted decisions;
- non-blocking findings;
- lessons from repair/recovery.

Conceptually:

```text
CLOSED_VALIDATED
    ↓
Completion knowledge
    ↓
outside Project Template runtime
    ↓
future External Research
    ↓
new Research Handoff
    ↓
Import
    ↓
Planning Finalization
    ↓
new Accepted Scope
```

Previous Scope does not silently become new Scope authority.

Previous completion knowledge does not silently create a new Cycle.

## 28. Provider and Model Neutrality

Model selection affects capability and cost.

It does not grant workflow authority.

External Research may use any suitable provider or process.

Planning should use the strongest suitable reasoning available because it is the mandatory semantic finalizer and execution-authority synthesizer.

Core runtime authority remains provider-neutral.

## 29. User Experience Principle

Normal users should experience a simple flow:

```text
prepare Research externally
    ↓
supply Research Handoff
    ↓
Project Template imports it
    ↓
Planning finalizes Research
    ↓
only unresolved material product decisions return to user
    ↓
Planning creates implementation authority
    ↓
Execution
```

Users should not need to understand or manually manage:

- internal IDs;
- generation numbers;
- digests;
- ticket internals;
- mutation manifests;
- repair counters;
- checkpoint internals.

Internal rigor should reduce user burden.

## 30. Development Constitution Principle

`Workplan/development_constitution/` is human-owned development guidance for Project Template itself.

AI may read it.

AI must not edit, modify, rewrite, move, rename, or delete it.

If a future requirement conflicts with this constitution:

```text
AI reports constitution conflict
    ↓
AI proposes change outside protected area
    ↓
repository owner updates constitution explicitly
    ↓
AI rereads complete constitution
    ↓
development continues
```

## 31. Change Governance

A material Project Template change should consider:

- root cause;
- constitution impact;
- architecture impact;
- Research/Planning boundary impact;
- authority impact;
- token/cost impact;
- context impact;
- reliability impact;
- recovery/resume impact;
- compatibility/migration impact;
- test impact;
- documentation impact.

Do not add a new role, lifecycle stage, authority path, retry path, prompt, alias, or source of truth merely because it makes one local problem easier.

Do not make External Research authoritative merely to reduce Planning work.

Do not make Planning repeat all Research merely because Planning is stronger.

Preserve:

```text
Research = maximize useful information
Planning = maximize decision quality
```

## 32. Direction of Travel

Project Template should move toward:

- richer but focused external Research handoffs;
- less wasted Planning re-research;
- stronger Planning semantic finalization;
- stronger selective independent verification;
- clearer Scope authority;
- less model-managed workflow after Planning;
- more deterministic authority;
- less repeated expensive reasoning;
- more bounded low-cost implementation;
- stronger Manager-level local debugging;
- less broad context;
- more selective context;
- fewer duplicate sources of truth;
- fewer unnecessary roles/lifecycle states;
- stronger durable failure evidence;
- safer resume and recovery;
- simpler normal user operation;
- stronger independent acceptance;
- cleaner software-development boundaries.
