> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Project Template Development Prompt

## Purpose

This prompt is used only when an AI is developing, reviewing, diagnosing, or implementing changes to **Project Template itself**.

It is not a runtime prompt for a user project's:

- Research;
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
Workplan/development_constitution/OBJECTIVE.md
Workplan/development_constitution/REFERENCE_ARCHITECTURE.md
Workplan/VERSION
```

You may read and reason from every file under:

```text
Workplan/development_constitution/
```

You must not:

- edit;
- modify;
- rewrite;
- move;
- rename;
- delete;
- replace

any file in that directory.

This restriction applies even when a constitution change appears technically desirable.

If the constitution conflicts with the requested development:

```text
report CONSTITUTION_CHANGE_REQUIRED
    ↓
identify the exact conflict
    ↓
propose the required human change
    ↓
do not edit development_constitution/
    ↓
stop the affected architecture-changing work
```

The repository owner must update the constitution externally.

After the owner changes it, reread the complete constitution before continuing.

## 2. Establish Current Baseline

For substantial work, establish the current repository baseline once.

At minimum inspect:

```text
Workplan/VERSION
Workplan/development_constitution/OBJECTIVE.md
Workplan/development_constitution/REFERENCE_ARCHITECTURE.md
```

Then inspect only the implementation, tests, configuration, migration, and documentation relevant to the requested change.

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
affected architecture boundary
minimum robust correction
token/context impact
reliability impact
resume/recovery impact
compatibility impact
validation required
```

Do not implement a symptom-level workaround when the responsible mechanism can be corrected directly.

## 4. Preserve Existing Good Design

Do not rewrite working architecture from zero.

Classify material existing mechanisms as:

```text
KEEP
FIX
SIMPLIFY
EXTEND
REMOVE
```

Preserve anything that already satisfies the Development Objective and Reference Architecture.

Do not weaken an invariant merely to make obsolete implementation or tests pass.

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

A local defect must not silently redefine the architecture.

## 6. Software-Development Identity

Project Template is an AI-assisted **software-development control plane**.

Keep development focused on software engineering:

- Scope and requirement research;
- repository analysis;
- architecture/planning;
- source-code implementation;
- CLI/tool execution;
- controlled file operations;
- debugging;
- verification;
- repair/recovery;
- acceptance.

Do not generalize it into a general autonomous-agent platform unless the human owner first changes the Development Constitution.

## 7. Capability Allocation

Preserve the intended capability ladder:

```text
External strong reasoning
    -> Research
    -> Planning
    -> escalated Diagnosis
    -> Recovery reasoning
    -> Independent Evaluation

Manager
    -> execution coordination
    -> Task-local debugging
    -> failure analysis
    -> repair strategy
    -> Builder supervision

Builder
    -> low-cost bounded implementation
    -> CLI/file operations
    -> straightforward code changes
    -> Manager-defined Repair changes
    -> verification execution

Deterministic Workplan
    -> authority
    -> routing
    -> tickets
    -> bindings
    -> repair limits
    -> gates
    -> validation
    -> closure
```

Do not move difficult debugging responsibility to Builder merely because Builder can edit files.

Do not move routine implementation to expensive reasoning models merely because they are capable of editing code.

## 8. Builder Failure Rule

A failed Builder must not autonomously enter an open-ended debug/edit/retry loop.

The intended Task-local repair pattern is:

```text
Builder Attempt
    ↓
FAIL
    ↓
durable Failure Record
    ↓
Manager local diagnosis
    ↓
Manager-defined repair strategy
    ↓
fresh Builder REPAIR Attempt
    ↓
Task Gate
```

Repeat only within the approved bounded repair policy.

The hard local maximum is 5 Repair Attempts for one failure chain.

Structural or authority-level defects may escalate earlier.

## 9. Deterministic Authority Rule

Prefer deterministic software over prompt enforcement when a behavior is truly an authority invariant.

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

Prompts should explain behavior.

They should not become the sole source of execution authority.

Do not create deterministic machinery merely for cosmetic prompt preferences; use it where it protects a real authority, reliability, recovery, or validation boundary.

## 10. Context and Cost Discipline

Use selective context.

Do not load the whole repository by default.

Use strong models for reasoning that materially benefits from stronger reasoning.

Use low-cost models for bounded implementation.

Do not repeatedly pay for reasoning already preserved in durable:

- architecture;
- decisions;
- Task contracts;
- failure records;
- checkpoints;
- evidence.

## 11. Failure and Recovery Review

For a material failure, determine:

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

## 12. Constitution Conflict

If implementation pressure suggests changing:

- Project Template product identity;
- Research/Planning responsibility;
- VS Code execution boundary;
- Manager/Builder capability boundary;
- `Cycle -> Phase -> Task -> Attempt`;
- Task/Phase Gate authority;
- local repair philosophy;
- Diagnosis/Recovery separation;
- final Evaluation responsibility;
- durable-state philosophy;
- human ownership of this constitution;

do not silently change implementation to a different architecture.

Report:

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

Then stop the affected architecture-changing implementation.

## 13. Implementation Design

When no constitution change is required:

1. inspect current relevant implementation;
2. identify root cause;
3. preserve required invariants;
4. choose the simplest robust design;
5. prefer deterministic mechanisms over prompt complexity where authority requires it;
6. make the smallest coherent change;
7. update only relevant tests/docs/config/migration;
8. keep version consistency;
9. preserve resumability and provider neutrality.

## 14. Validation

Do not claim correctness because:

- the prompt looks correct;
- code appears reasonable;
- a model says PASS;
- a file exists.

Execute verification.

Prefer focused bounded suites first.

Test negative paths for authority boundaries.

Then execute broader release validation when appropriate.

Never report unexecuted validation as PASS.

## 15. Release Consistency

A new Project Template version must describe one coherent design across applicable:

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

Do not ship mixed-version behavior or stale canonical paths.

## 16. Development Result

For substantial Project Template changes, report:

```text
verified baseline
requested outcome
root cause
constitution impact
reference architecture impact
architecture change required: YES / NO
invariants preserved
files changed
behavior changed
tests actually executed
observed validation results
migration impact
known limitations
```

Do not claim the repository was updated when only a proposal or isolated candidate was created.

## Core Rule

```text
Do not make the constitution follow the latest patch.

Make each patch preserve the human-approved constitution.

When the constitution must change, the human changes it first.
```
