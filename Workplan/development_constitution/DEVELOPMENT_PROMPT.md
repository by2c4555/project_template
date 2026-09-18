> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.
# Project Template Development Prompt

## Purpose

This prompt is used only when an AI is developing, reviewing, diagnosing, or implementing changes to **Project Template itself**.

It is not a runtime prompt for a user project's:

- External Research;
- Planning;
- Manager;
- Builder;
- Diagnosis;
- Recovery;
- Evaluation.

Its purpose is to prevent Project Template architecture from drifting because of local fixes, new-version work, model preferences, or session-specific reasoning.

## 1. Constitution Is Read-Only

Before substantial Project Template development, read:

```text
Workplan/development_constitution/README.md
Workplan/development_constitution/OBJECTIVE.md
Workplan/development_constitution/RESEARCH_AND_SCOPE_MODEL.md
Workplan/development_constitution/PLANNING_MODEL.md
Workplan/development_constitution/REFERENCE_ARCHITECTURE.md
Workplan/VERSION
```

You may read and reason from every file under:

```text
Workplan/development_constitution/
```

You must not:

- create;
- edit;
- modify;
- rewrite;
- reformat;
- move;
- rename;
- delete;
- replace;
- migrate;
- automatically synchronize

any file in that directory.

If the constitution conflicts with requested development:

```text
report CONSTITUTION_CHANGE_REQUIRED
    ↓
identify exact conflict
    ↓
draft proposed change outside protected directory
    ↓
do not modify protected constitution
    ↓
complete unaffected authorized work
    ↓
stop affected architecture-changing work
```

The repository owner must explicitly update the constitution.

After owner changes it, reread the complete constitution before continuing.

## 2. Establish Current Baseline

For substantial work, establish current repository truth once.

At minimum inspect:

```text
Workplan/VERSION
complete Development Constitution
relevant runtime implementation
relevant tests/config/docs/migration
```

Use current repository state as implementation truth.

Do not repeatedly reload unchanged files.

Do not rely on old chat claims when repository state disagrees.

## 3. Understand the Change Before Editing

Before changing implementation, identify:

```text
requested outcome
current behavior
root cause / actual gap
affected invariant
affected authority boundary
affected architecture boundary
minimum robust correction
token/context impact
reliability impact
resume/recovery impact
compatibility/migration impact
validation required
```

Do not implement a symptom-level workaround when the responsible mechanism can be corrected directly.

## 4. Preserve Existing Good Design

Do not rewrite working architecture from zero.

Classify relevant mechanisms:

```text
KEEP
FIX
SIMPLIFY
EXTEND
REMOVE
```

Preserve anything that already satisfies the Development Objective and Reference Architecture.

Do not weaken an invariant merely to make obsolete implementation/tests pass.

## 5. Architecture Drift Guard

Do not introduce a new:

```text
role
lifecycle stage
authority path
retry path
prompt
model-specific authority
alias
state authority
source of truth
```

merely because it makes a local patch easier.

Prefer:

```text
fix existing mechanism
    before
simplify existing mechanism
    before
extend existing mechanism
    before
introduce new mechanism
```

A local defect must not silently redefine architecture.

## 6. Preserve External Research Boundary

External Research is outside Project Template runtime.

Project Template may ship:

- Research prompts;
- Research protocols;
- Research templates;
- examples.

These are external preparation helpers.

They must not become:

```text
runtime lifecycle authority
Research Work authority
Cycle authority
approval authority
resume authority
execution authority
```

Normal runtime routing must not require `EXECUTE_RESEARCH`.

A utility may display/export Research helper material only if doing so does not create runtime Research authority.

## 7. Preserve Import Semantics

Research Import is structural/integrity validation.

Do not equate:

```text
structurally valid Research Handoff
```

with:

```text
semantically final Accepted Scope
```

Successful import creates an Imported Research Package.

Planning semantic finalization creates Accepted Scope.

## 8. Preserve Planning as Mandatory Semantic Finalizer

Planning is the strongest normal runtime reasoning stage.

Do not reduce Planning to a Task compiler.

Planning must perform:

```text
A. Research Investigation & Finalization
B. Implementation Planning
```

Planning A must be able to:

- detect Research gaps/contradictions;
- inspect current repository evidence;
- investigate missing technical facts;
- classify unknowns;
- selectively verify material Research;
- request material product decisions from user;
- finalize Scope;
- finalize Research Knowledge.

Planning B must create applicable:

- architecture;
- interfaces;
- data model;
- constraints;
- Phases;
- Tasks;
- dependencies;
- paths/context;
- verification/evidence;
- repair policy.

No production execution authority may exist before Planning finalization is valid.

## 9. Do Not Waste Planning Capacity

Planning is expensive and constrained.

Research should carry broad/deep discovery work.

The design target is:

```text
Research = maximize useful information
Planning = maximize decision quality
```

Planning should independently verify the minimum sufficient evidence for material claims.

Do not force Planning to reproduce low-risk Research merely for ritual independence.

## 10. Preserve User Decision Boundary

Planning may decide technical HOW.

Planning must not invent unresolved material product WHAT / WHY.

When needed:

```text
material product unknown
    ↓
USER_ACTION_REQUIRED
    ↓
user response
    ↓
Planning Finalization resumes
```

Do not ask the user to decide technical details that Planning is responsible for.

## 11. Avoid Unnecessary Lifecycle Expansion

Research Investigation & Finalization and Implementation Planning are logical Planning sub-phases.

Do not create separate public lifecycle roles/stages for them unless deterministic authority, recovery, or resume requirements prove such separation necessary.

Prefer Planning checkpoints over lifecycle proliferation.

## 12. Preserve Capability Allocation

```text
External Research
    -> broad/deep preparation outside runtime

Planning
    -> strongest normal runtime reasoning
    -> semantic finalization
    -> implementation authority synthesis

Manager
    -> local execution reasoning/debugging

Builder
    -> lower-cost bounded implementation

Deterministic Workplan
    -> authority/state/routing/tickets/gates
```

Do not move open-ended debugging to Builder.

Do not move routine production implementation to Planning.

## 13. Builder Failure Rule

A failed Builder must not autonomously enter an open-ended debug/edit/retry loop.

Intended local repair:

```text
Builder Attempt
    ↓
FAIL
    ↓
durable Failure Record
    ↓
Manager diagnosis
    ↓
Manager-defined repair strategy
    ↓
fresh Builder REPAIR Attempt
    ↓
Task Gate
```

The hard local maximum is 5 Repair Attempts per Task failure chain.

Structural/authority failures may escalate earlier.

## 14. Deterministic Authority Rule

Prefer deterministic software over prompt enforcement when a behavior is an authority invariant.

Use applicable:

```text
state
schema
contract
ticket
binding
generation
gate
validator
counter
filesystem evidence
test
```

Prompts explain behavior.

They do not replace authority enforcement.

## 15. Context and Cost Discipline

Use selective context.

Do not load whole repository by default.

Do not repeatedly pay for reasoning already preserved in durable:

- Research evidence;
- finalization decisions;
- Accepted Scope;
- architecture;
- Task contracts;
- failure records;
- checkpoints;
- evidence.

## 16. Failure and Recovery Review

For a material runtime failure determine:

```text
what failed
where it failed
expected behavior
actual behavior
evidence
root cause
affected invariant
blast radius
whether local repair remains valid
whether prior strategies were disproven
correct continuation
```

Preserve previous valid work and failure history.

Do not restart from zero unless existing work is proven unusable.

## 17. Import and Planning Failure Rules

### Import Failure

```text
fail closed
    ↓
report structural/integrity defect
    ↓
do not create Accepted Scope
```

### Planning Finalization Blocker

```text
classify unknown
    ↓
resolve technically
or
request user action
or
preserve external blocker
```

Do not hide a blocker as an assumption.

## 18. Scope Defect Boundary

Accepted Scope exists only after Planning semantic finalization.

After acceptance:

- Builder must not rewrite it;
- Manager must not rewrite it;
- Recovery must not rewrite it;
- Evaluation must not rewrite it.

If later evidence shows Scope is materially defective, route to Planning/owner/external correction as appropriate.

## 19. Constitution Conflict

If implementation pressure suggests changing:

- Project Template product identity;
- External Research boundary;
- Planning-as-finalizer responsibility;
- Accepted Scope authority;
- VS Code execution boundary;
- Manager/Builder capability boundary;
- `Cycle -> Phase -> Task -> Attempt`;
- Task/Phase Gate authority;
- local repair philosophy;
- Diagnosis/Recovery separation;
- final Evaluation responsibility;
- durable-state philosophy;
- human ownership of constitution;

report:

```text
CONSTITUTION_CHANGE_REQUIRED

Current constitution:
...

Requested behavior:
...

Conflict:
...

Why existing architecture is insufficient:
...

Suggested human constitution change:
...

Implementation impact:
...

Compatibility/migration impact:
...
```

Do not modify protected constitution.

## 20. Implementation Design

When no constitution change is required:

1. inspect current relevant implementation;
2. identify root cause;
3. preserve required invariants;
4. choose simplest robust design;
5. prefer deterministic mechanisms where authority requires;
6. make smallest coherent change;
7. update relevant tests/docs/config/migration;
8. keep version consistency;
9. preserve resumability/provider neutrality.

For Research/Planning boundary work inspect applicable:

```text
root README / Quick Start
ENTRY_PROMPT / user entry instructions
command routing
WORKPLAN_NEXT
Research helper files
ingest/import
Planning acquisition
Planning checkpoints
Accepted Scope creation/binding
Planning Package validation
Cycle/authority creation
tests
migration/version docs
release validation
```

## 21. Validation

Do not claim correctness because:

- a prompt looks correct;
- code appears reasonable;
- a model says PASS;
- a file exists.

Execute verification.

Prefer focused suites first, then broader validation.

Test negative paths for authority boundaries.

For Research/Planning architecture validate at minimum:

```text
Research remains outside runtime lifecycle
Research helper files do not create runtime authority
invalid import fails closed
valid import creates Imported Research Package, not Accepted Scope
Planning can detect missing/contradictory Research
Planning can request user action for material product unknowns
Planning can investigate technical unknowns
Planning selectively verifies material Research
Planning Finalization creates/binds Accepted Scope
Implementation Planning cannot become PLAN_READY before Scope acceptance
execution cannot start without Accepted Scope + valid Planning Package
active runtime can resume without external Research chat history
```

Never report unexecuted validation as PASS.

## 22. Simulation / Mock / Sample Validation

When real external dependencies or user workflows cannot be exercised directly, use representative:

- mock Research Handoffs;
- incomplete handoffs;
- contradictory handoffs;
- stale evidence samples;
- valid handoffs;
- user-decision blockers;
- technical unknown samples;
- Planning revision samples.

Simulation must not replace real verification where real verification is available.

## 23. Migration and Compatibility

When migrating from old Research-as-runtime or immediate-Scope-import behavior, inspect:

- `RESEARCH` lifecycle state;
- Research Work records;
- `EXECUTE_RESEARCH`;
- bootstrap routing;
- old ingest-to-Scope behavior;
- existing Cycle records;
- Planning assumptions;
- old tests/docs.

Do not silently reinterpret unsafe in-flight state.

Prefer explicit migration or rejection boundaries.

## 24. Release Consistency

A release must describe one coherent design across applicable:

```text
VERSION
Development Constitution references
runtime
state/schema
agents
configuration
tests
documentation
migration
release validation
integrity metadata
```

Do not ship mixed behavior, such as:

```text
docs: Planning finalizes Research
runtime: import immediately creates immutable Scope
```

## 25. Packaging Protection

Before normal implementation packaging:

```text
Workplan/development_constitution/**
```

must have no create/modify/delete changes relative to the verified baseline unless the user explicitly authorized protected-area modification.

If unintended changes exist, restore baseline before producing the implementation package.

A constitution proposal must remain outside the implementation ZIP unless the user explicitly authorizes protected-area modification.

## 26. Development Result

For substantial changes report:

```text
verified baseline
requested outcome
root cause
constitution impact
reference architecture impact
Research boundary status
Planning Finalization status
Scope authority status
invariants preserved
files changed
behavior changed
tests actually executed
observed validation results
migration impact
known limitations
artifact
```

Do not claim repository modification when only a proposal/candidate was created.

## Core Rule

```text
External Research prepares the best handoff it can.

Planning is the strongest controlled reasoning stage.

Planning finalizes Research before Accepted Scope and implementation authority.

Research must not become runtime authority.

Planning must not blindly trust Research.

Planning must not blindly repeat Research.

Deterministic software owns authority transitions and PASS.
```
