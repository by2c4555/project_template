> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Project Template Development Prompt

## Purpose

This prompt is used only when AI develops, reviews, diagnoses, or implements changes to **Project Template itself**.

It is not a runtime prompt.

## 1. Constitution Is Protected

Before substantial work read:

```text
Workplan/development_constitution/OBJECTIVE.md
Workplan/development_constitution/REFERENCE_ARCHITECTURE.md
```

Then read only relevant detailed architecture modules.

Also inspect:

```text
Workplan/VERSION
```

AI must not create, edit, modify, delete, rename, reformat, migrate, or auto-synchronize files under `Workplan/development_constitution/` unless the user explicitly authorizes modification of this protected area.

If conflict exists:

```text
CONSTITUTION_CHANGE_REQUIRED
```

Report exact conflict and propose changes separately.

## 2. Establish Current Baseline

Establish current repository truth once.

Inspect only relevant implementation/tests/config/docs after constitution review.

Do not repeatedly reload unchanged files.

## 3. Relevant Module Selection

Read only modules relevant to the requested change.

Examples:

### Research / Planning

- `RESEARCH_AND_SCOPE_MODEL.md`
- `PLANNING_MODEL.md`
- `architecture/USER_APPROVAL_AND_COST_CONTROL.md`
- `architecture/STATE_BINDING_AND_RESUME.md`

### Task Gate

- `architecture/AUTHORITY_MODEL.md`
- `architecture/TASK_AND_PHASE_GATES.md`
- `architecture/STATE_BINDING_AND_RESUME.md`

### Recovery

- `architecture/FAILURE_AND_REPAIR_MODEL.md`
- `architecture/DIAGNOSIS_AND_RECOVERY.md`
- `architecture/USER_APPROVAL_AND_COST_CONTROL.md`

### Closure

- `architecture/EVALUATION_CLOSURE_AND_NEXT_VERSION.md`
- `architecture/STATE_BINDING_AND_RESUME.md`

## 4. Understand Before Editing

Identify:

```text
requested outcome
current behavior
root cause
affected invariant
authority boundary
architecture boundary
minimum robust correction
token/cost impact
approval impact
resume/recovery impact
migration impact
validation required
```

## 5. Preserve Existing Good Design

Classify:

```text
KEEP
FIX
SIMPLIFY
EXTEND
REMOVE
```

Do not rewrite working architecture from zero.

## 6. Architecture Drift Guard

Do not add roles, lifecycle stages, authority paths, retry paths, prompts, aliases, or sources of truth merely because they simplify one patch.

## 7. Preserve Research Boundary

External Research remains outside runtime.

Research helper files must not create runtime Research Work or authority.

Normal runtime must not route to `EXECUTE_RESEARCH`.

## 8. Preserve Planning Boundary

Planning remains:

```text
Research Investigation & Finalization
+
Implementation Planning
```

Do not create Accepted Scope before valid Scope Approval.

Do not create `PLAN_READY` before valid Execution Approval.

## 9. Preserve User Approval Cost Control

Do not remove or bypass:

- Scope Approval;
- Execution Approval;
- material Change Re-Approval.

Do not add approval spam for routine bounded work.

## 10. Preserve Authority

Deterministic software owns:

- routing;
- bindings;
- generations;
- approvals validity;
- Task/Phase gates;
- closure.

## 11. Preserve Manager / Builder Boundary

Manager reasons.

Builder mutates within bounded authority.

Builder does not own open-ended debugging or PASS.

## 12. Preserve Repair Bound

No sixth ordinary Task-local Repair Attempt.

## 13. Preserve Closure Output

`CLOSED_VALIDATED` must produce a valid Completion Knowledge Package suitable as input to future external Research.

Do not make that package the next Scope automatically.

## 14. Deterministic Authority Rule

Use state/schema/contracts/tickets/bindings/generation/gates/validators/tests where a behavior is truly authoritative.

Prompts are not enough for authority invariants.

## 15. Context and Cost Discipline

Use selective context.

Reuse durable Research/Planning/evidence.

Use strong models only where material reasoning needs them.

Use lower-cost Builders for bounded implementation.

## 16. Failure and Recovery Review

For failure determine:

```text
what failed
expected vs actual
evidence
root cause
affected invariant
blast radius
local repair validity
correct continuation
approval impact
```

## 17. Validation

Do not claim correctness because code looks correct.

Execute focused tests, negative paths, then broader validation where appropriate.

For Research/Planning/Approval changes validate at minimum:

```text
Research is not runtime lifecycle
valid import creates Imported Research Package, not Accepted Scope
Planning A can detect missing/contradictory Research
Scope Approval is revision-bound
Accepted Scope requires valid Scope Approval
Planning B requires Accepted Scope
Execution Approval is revision-bound
PLAN_READY requires valid Execution Approval
material changes stale prior approval
routine local repair does not require duplicate approval
```

For execution/recovery changes validate:

```text
Task Gate and Phase Gate authority
stale generation rejection
authorized path enforcement
repair count <= 5
recovery cannot create Scope
material recovery expansion requires re-approval
```

For closure validate:

```text
Evaluation result is required
deterministic finalization is required
CLOSED_VALIDATED binds final repository baseline
Completion Knowledge Package is produced
Completion Knowledge Package is not next Scope
```

## 18. Simulation / Mock / Sample Validation

When external systems cannot be exercised directly use representative:

- valid Research Handoff;
- incomplete handoff;
- contradictory handoff;
- stale evidence;
- user decision blocker;
- valid Scope Approval;
- stale Scope Approval;
- valid Execution Approval;
- stale Execution Approval;
- recovery requiring re-approval;
- evaluation blocker;
- CLOSED_VALIDATED sample;
- next-version handoff sample.

## 19. Migration and Compatibility

Inspect legacy state such as:

- runtime `RESEARCH`;
- `EXECUTE_RESEARCH`;
- direct import → immutable Scope;
- missing approval state;
- prior Planning assumptions;
- existing Cycles;
- old closure output.

Do not silently reinterpret unsafe in-flight state.

## 20. Release Consistency

A release must be coherent across:

```text
VERSION
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

## 21. Packaging Protection

Before packaging normal implementation verify:

```text
Workplan/development_constitution/**
```

has no unintended create/modify/delete changes relative to the verified baseline.

Restore unintended protected-area changes before creating the implementation ZIP.

## 22. Development Result

Report:

```text
verified baseline
requested outcome
root cause
constitution impact
architecture impact
approval/cost impact
invariants preserved
files changed
tests executed
observed results
migration impact
known limitations
artifact
```

## Core Rule

```text
Research maximizes useful information.

Planning maximizes decision quality.

User approvals protect material cost/authority boundaries.

Deterministic software owns runtime authority.

Execution is bounded.

Recovery cannot self-expand authority.

CLOSED_VALIDATED produces next-version knowledge.

Do not make the constitution follow the latest patch.
```
