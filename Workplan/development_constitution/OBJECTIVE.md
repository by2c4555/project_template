> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Project Template Development Objective

## 1. Product Identity

Project Template is an **AI-assisted software-development control plane**.

Its purpose is to coordinate high-quality development of a software repository across:

- requirement and Scope research;
- repository and technical research;
- architecture and implementation planning;
- bounded source-code implementation;
- CLI/tool execution;
- controlled file operations;
- software debugging and repair;
- verification and regression checking;
- recovery from failed implementation;
- independent final acceptance;
- durable cross-session continuation.

Project Template is not intended to become a general-purpose autonomous-agent framework.

Its architecture exists specifically to improve software-development quality, reliability, cost efficiency, auditability, and resumability.

## 2. Core Objective

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

The intended allocation is:

```text
strong external reasoning
    -> high-value technical reasoning

reasoning-capable Manager
    -> local software debugging and repair reasoning

low-cost Builder
    -> bounded implementation

deterministic software
    -> authority, state, routing, gates, validation, recovery control

repository/filesystem state
    -> durable truth

chat/session state
    -> disposable context
```

## 3. Engineering Principles

Project Template development should preserve these principles:

1. Deterministic mechanisms before prompt complexity.
2. Durable repository state before conversational memory.
3. Bounded contracts before open-ended autonomy.
4. Strong reasoning only where it materially improves software quality.
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
15. Internal rigor may increase, but normal user workflow should become simpler rather than more complex.

## 4. Authority Model

Workflow authority comes from deterministic Workplan state and accepted contracts.

Authority does not come from:

- model capability;
- model price;
- provider identity;
- model confidence;
- chat context;
- prompt self-assertion;
- a model claim of PASS;
- an implementation summary.

A capable model may still be rejected when lifecycle stage, ticket, binding, generation, authorized path, approval, evidence, or gate authority is invalid.

Prompts guide model behavior.

Deterministic software owns execution authority.

## 5. Canonical Software-Development Lifecycle

The normal lifecycle is conceptually:

```text
Research
    ↓
Planning
    ↓
Execution
    ↓
Independent Evaluation
    ↓
CLOSED_VALIDATED
```

Diagnosis and Recovery are controlled exception paths.

They must not become alternative normal workflows or permanent loops.

## 6. Canonical Runtime Hierarchy

Execution authority remains organized as:

```text
Cycle -> Phase -> Task -> Attempt
```

Required invariants:

- every Task belongs to exactly one Phase;
- each Builder dispatch creates a fresh Attempt;
- Attempt kinds include `INITIAL`, `REPAIR`, and `RECOVERY`;
- a simple project may use an implicit Phase when appropriate;
- normal users should not manually manage Phase, Task, Attempt, generation, ticket, or digest internals.

## 7. Research and Scope Principle

Research owns product **WHAT / WHY**.

Research should establish trustworthy Scope and supporting knowledge before Planning.

Research may investigate:

- repository state;
- implementation feasibility;
- external technology;
- compatibility;
- preliminary architectural options.

Preliminary architecture produced during Research is **knowledge**, not final architecture authority.

Authoritative product Scope must remain explicit and immutable for the active Cycle after acceptance.

Research must not silently become implementation Planning.

## 8. Planning Principle

Planning is high-value technical reasoning.

Planning converts:

```text
approved Scope
    +
Research Knowledge
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

Material Planning authority must not silently change after approval.

## 9. Execution Environment Principle

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

## 10. Manager Capability Principle

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

Manager coordinates and reasons; Builder performs the bounded repository mutation.

## 11. Builder Capability Principle

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

## 12. Task and Phase Gate Authority

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

## 13. Local Debugging and Repair Principle

Ordinary Task-local software failures should first use the local capability ladder:

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

## 14. Durable Failure Principle

Every authoritative failure must leave sufficient durable evidence for a fresh capable model/session to:

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

## 15. Escalation Principle

External strong reasoning is an exception path for failures that exceed local execution reasoning.

Escalation is appropriate when applicable:

- local repair is exhausted;
- the failure is structural;
- Task authority is insufficient;
- Planning authority is defective;
- Scope authority is defective;
- verification authority is defective;
- environment/tooling lies outside local authority;
- repeated strategies are disproven;
- correctness cannot be reliably determined.

Escalation should happen because stronger reasoning is materially needed, not merely because another model is available.

## 16. Diagnosis and Recovery Principle

External Diagnosis is reasoning-only.

It determines:

- what failed;
- root cause;
- affected authority;
- violated invariant/contract;
- blast radius;
- correct recovery boundary.

External Recovery is reasoning-only.

It converts Diagnosis into a durable correction contract.

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

## 17. Issue Lifecycle Principle

Every escalated issue must have a deterministic continuation and a deterministic terminal disposition.

A resolved or superseded historical issue must not accidentally block later valid execution.

Issue handling must avoid:

- dangling issues;
- contradictory lifecycle/next-action state;
- permanent Diagnosis loops;
- stale blockers after approved authority replacement.

## 18. Context Principle

Context expansion is read authority only.

Additional context must never silently expand:

- Scope;
- Task objective;
- authorized write paths;
- repair authority.

Builder context should remain selective and bounded.

## 19. Immutable Binding and Generation Principle

Work and Attempt authority must remain bound to the authority that existed when issued.

Resume must compare current authority with original bindings.

Original bindings must not be silently recalculated and overwritten.

Generation fencing must prevent stale sessions or agents from completing or mutating newer Work authority.

## 20. Resume Principle

Repository state is durable.

Chat/session state is disposable.

A fresh session, model, provider, or machine should be able to continue from durable:

- state;
- Scope;
- Planning authority;
- tickets;
- Attempts;
- checkpoints;
- failure evidence;
- bindings.

Full conversation replay must not be required.

## 21. Human Approval Principle

Human approval must remain:

- explicit;
- action-bound;
- subject-bound;
- state-bound;
- stale-safe;
- single-use where applicable.

AI must not grant its own human approval.

Approval mechanisms should exist only where a genuine new cost, authority, or rework boundary justifies them.

Avoid duplicate approvals for the same already-approved envelope.

## 22. Independent Evaluation Principle

Independent Evaluation occurs after required execution gates pass.

Evaluation verifies actual repository outcomes against approved Scope and Planning authority.

Evaluation is review/acceptance, not production repair.

Final closure requires deterministic acceptance authority.

`CLOSED_VALIDATED` means the current Cycle satisfies its approved acceptance authority.

It does not claim perfection outside Scope.

## 23. Cross-Cycle Knowledge Principle

A completed Cycle may produce durable knowledge for future Research.

Examples include:

- Completion Report;
- verified architectural outcomes;
- accepted decisions;
- non-blocking findings;
- lessons from repair/recovery.

Previous knowledge may inform the next Cycle.

It must not silently become the new Cycle's Scope authority.

New Scope must be established explicitly.

## 24. Provider and Model Neutrality

Model selection affects capability and cost.

It does not grant workflow authority.

Project Template should describe capability classes rather than depend on vendor identity wherever practical.

The execution adapter may require a supported local model alias or environment-specific configuration without making core authority provider-specific.

## 25. User Experience Principle

Normal users should interact with a simple software-development flow.

Users should not need to understand or manually manage:

- internal IDs;
- generation numbers;
- digests;
- ticket internals;
- mutation manifests;
- repair counters;
- checkpoint internals.

Internal deterministic rigor should reduce user burden.

## 26. Development Constitution Principle

`Workplan/development_constitution/` is human-owned development guidance for Project Template itself.

AI may read it.

AI must not edit, modify, rewrite, move, rename, or delete it.

If a future Project Template requirement conflicts with this constitution:

```text
AI reports constitution conflict
    ↓
AI proposes change
    ↓
repository owner updates constitution externally
    ↓
AI rereads constitution
    ↓
development continues
```

The AI must not make the constitution follow its latest patch.

## 27. Change Governance

A material Project Template change should consider:

- root cause;
- constitution impact;
- architecture impact;
- token/cost impact;
- context impact;
- reliability impact;
- recovery/resume impact;
- compatibility/migration impact;
- test impact;
- documentation impact.

Do not add a new role, lifecycle stage, authority path, retry path, prompt, alias, or source of truth merely because it makes one local problem easier to implement.

Preserve working architecture unless a real architectural gap is established.

## 28. Direction of Travel

Project Template should move toward:

- less model-managed workflow;
- more deterministic authority;
- less repeated expensive reasoning;
- more bounded low-cost implementation;
- stronger Manager-level local debugging;
- less broad context;
- more selective context;
- fewer duplicate sources of truth;
- fewer unnecessary roles and lifecycle states;
- stronger durable failure evidence;
- safer resume and recovery;
- simpler normal user operation;
- stronger independent acceptance;
- cleaner software-development boundaries.
