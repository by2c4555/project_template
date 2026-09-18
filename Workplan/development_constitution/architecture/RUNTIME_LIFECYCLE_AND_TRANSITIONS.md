> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Runtime Lifecycle and Transitions

## 1. Purpose

This document owns the canonical lifecycle transition semantics of Project Template runtime.

It defines:

- where runtime begins and ends;
- when active development Cycle authority exists;
- when production execution authority exists;
- required transition preconditions;
- deterministic transition ownership;
- pause/resume/cancel behavior;
- blocked and exception continuations;
- closure and next-version boundaries.

Other documents may summarize the lifecycle, but this file owns detailed transition semantics.

## 2. Conceptual Stage vs Persisted State

Architecture diagrams may use conceptual stage names such as:

```text
IMPORT
PLANNING_A
SCOPE_APPROVAL_PENDING
ACTIVE_CYCLE
PLANNING_B
EXECUTION_APPROVAL_PENDING
PLAN_READY
EXECUTION
EVALUATION
CLOSURE_PREPARATION
CLOSED_VALIDATED
PAUSED
BLOCKED
CANCELLED
```

Implementation does **not** have to persist each name as a separate enum value.

What is mandatory is that equivalent authority boundaries, preconditions, postconditions, and forbidden transitions are enforced deterministically.

Do not create extra persisted lifecycle states merely to mirror documentation wording.

## 3. Transition Authority

Deterministic Workplan owns lifecycle transitions.

No model may create a lifecycle transition merely by:

- saying the next stage is ready;
- producing a file;
- claiming validation;
- claiming approval;
- claiming PASS;
- inferring that a user probably wants to continue.

AI roles may produce candidate artifacts, reasoning, evidence, diagnoses, or recommendations.

Deterministic runtime decides whether transition preconditions are actually satisfied.

## 4. Canonical Lifecycle

```text
════════ OUTSIDE RUNTIME ════════

External Research
    ↓
Research Handoff

════════ RUNTIME INGRESS ════════

Import / Structural + Trust Validation
    ↓
Imported Research Package

════════ PRE-CYCLE RUNTIME ══════

Planning A
Research Investigation & Finalization
    ↓
Draft Finalized Scope
    ↓
SCOPE_APPROVAL_PENDING
    ↓
valid SCOPE_APPROVAL
    ↓
Accepted Scope binding

════════ ACTIVE DEVELOPMENT CYCLE ════════

Planning B
Implementation Planning
    ↓
Candidate Planning Package
    ↓
Deterministic Planning Package Validation
    ↓
Validated Planning Package
    ↓
EXECUTION_APPROVAL_PENDING
    ↓
valid EXECUTION_APPROVAL
    ↓
PLAN_READY

════════ PRODUCTION EXECUTION AUTHORITY ════════

Execution
    ↓
Task / Phase Gates
    ↓
Independent Evaluation

════════ CLOSURE PREPARATION ════════

Accepted Evaluation Result
    ↓
Completion Knowledge Package preparation
    ↓
Deterministic Finalization
    ↓
CLOSED_VALIDATED

════════ RUNTIME ENDS ════════

Completion Knowledge Package
    ↓
available for a future separately initiated
External Research process
```

## 5. Runtime Ingress

Runtime begins when a Research Handoff is submitted to the import boundary.

Runtime ingress does not imply:

- valid Research;
- Accepted Scope;
- active Cycle authority;
- Planning B authority;
- Builder authority;
- production mutation authority.

Invalid import must fail closed and remain outside downstream Planning authority.

## 6. Planning A / Pre-Cycle Runtime

Planning A occurs inside Project Template runtime but before active development Cycle authority.

Planning A may:

- inspect imported Research;
- inspect current repository evidence;
- investigate technical unknowns;
- request focused user decisions;
- produce Draft Finalized Scope.

Planning A must not create executable Phase/Task/Builder authority.

## 7. Scope Approval Transition

The transition to Accepted Scope requires:

```text
Planning A complete
+
Draft Finalized Scope exists
+
no unresolved blocking product decision
+
valid SCOPE_APPROVAL
+
current subject/revision/digest binding
```

Successful deterministic binding of Accepted Scope begins **active development Cycle authority**.

If approval is missing, rejected, revoked, stale, ambiguous, or bound to the wrong subject:

```text
DO NOT CREATE ACCEPTED SCOPE
DO NOT START ACTIVE CYCLE AUTHORITY
```

## 8. Planning B Transition

Planning B begins only after Accepted Scope exists.

Planning B produces a **Candidate Planning Package**.

Planning does not self-certify that its own package is runtime-valid.

The package must pass deterministic Planning Package Validation before it becomes a Validated Planning Package.

## 9. Planning Package Validation Transition

Deterministic Planning Package Validation checks applicable structural and authority-critical properties such as:

- required artifacts/fields exist;
- Accepted Scope binding matches;
- repository/generation binding matches;
- material Scope coverage is represented;
- required Phase/Task structure is valid;
- dependency references resolve;
- authorized paths are syntactically valid and bounded;
- required verification/evidence contracts exist;
- unresolved blocking items are not hidden;
- required digests/integrity metadata are valid.

This validation proves structural/binding/traceability readiness.

It does **not** replace Planning's semantic responsibility for architecture quality.

Validation failure returns to Planning B or the correct earlier authority boundary.

## 10. Execution Approval Transition

Transition to `PLAN_READY` requires:

```text
Accepted Scope
+
Validated Planning Package
+
valid EXECUTION_APPROVAL
+
current generation/bindings
+
no blocking issue
```

`PLAN_READY` begins production execution authority.

Before `PLAN_READY`:

- no production Builder mutation;
- no production Attempt dispatch;
- no Task PASS progression.

## 11. Execution Transition

During execution:

```text
eligible Phase
    ↓
eligible Task
    ↓
fresh Attempt
    ↓
Builder
    ↓
Verification / Evidence
    ↓
Task Gate
```

Phase Gate controls Phase progression.

Exception paths may route to local Repair, Diagnosis, Recovery, Planning revision, owner action, or Change Approval.

## 12. Material Change Transition

When current approved authority/cost/risk envelope must materially change:

```text
current work
    ↓
material change identified
    ↓
stop affected downstream dispatch
    ↓
produce revised proposal/authority
    ↓
CHANGE_APPROVAL
    ↓
new binding/revision/generation as required
```

Existing approval must not be stretched to cover materially different work.

## 13. User Control Actions

User control actions are distinct from approval classes.

Canonical semantics:

```text
PAUSE
RESUME
CANCEL
```

Exact command/UI names belong to implementation.

### PAUSE

A valid pause request must prevent new:

- Task dispatch;
- Repair dispatch;
- Recovery implementation dispatch;
- expensive reasoning dispatch controlled by runtime;
- transition into a later cost/authority stage.

Already-running external commands may not be instantaneously reversible.

Runtime must reach a safe durable boundary as soon as practical and record any uncertain/partial mutation.

### RESUME

Resume requires:

- durable state is readable;
- bindings are still current;
- required approvals are still valid or historically consumed as applicable;
- no unresolved safety/authority ambiguity;
- repository state is reconciled if an in-flight action was interrupted.

Resume never means "recompute authority from chat."

### CANCEL

Cancel terminates further execution authority for the affected runtime/Cycle.

Cancellation must:

- stop new production dispatch;
- preserve historical evidence;
- preserve actual repository state;
- record unresolved/partial mutation if applicable;
- invalidate or supersede pending execution authority as needed.

A cancelled active Cycle is **not** `CLOSED_VALIDATED`.

Where useful, implementation should produce a durable Cancellation Record containing:

- cancellation reason;
- last known repository baseline;
- completed vs incomplete work;
- outstanding risk/partial mutation;
- reusable findings.

## 14. Approval Revocation vs Cancellation

Revoking an approval before its transition is consumed prevents that transition.

Once an approval has been consumed to create historical authority, revocation does not erase history.

To stop or change already-created authority, use the appropriate:

- PAUSE;
- CANCEL;
- Planning revision;
- CHANGE_APPROVAL;
- superseding generation/binding.

## 15. Blocked State

When required external information, environment, permission, or owner action is unavailable:

```text
BLOCKED
```

or an implementation-equivalent condition must prevent invalid continuation.

Blocked work must preserve:

- reason;
- required next action;
- authority/binding context;
- evidence.

A blocked condition must not silently fall through into execution.

## 16. Evaluation Transition

Independent Evaluation becomes eligible only after:

- required Phase Gates PASS;
- no blocking issue remains;
- current Accepted Scope/Planning bindings match actual repository authority.

Evaluation has no production mutation authority.

## 17. Closure Preparation and Finalization

The correct closure order is:

```text
Independent Evaluation accepted
    ↓
Completion Knowledge Package prepared
    ↓
Deterministic Finalization validates:
    - Evaluation result
    - final repository baseline
    - Scope/Planning bindings
    - required evidence
    - required Completion Knowledge Package contents
    ↓
CLOSED_VALIDATED
```

`CLOSED_VALIDATED` must not be created before required closure knowledge exists and is valid.

## 18. Runtime End and Next Version

`CLOSED_VALIDATED` ends the current successful runtime/Cycle.

The Completion Knowledge Package is then available as external knowledge.

Project Template must **not automatically start next-version Research** merely because a Cycle closed.

A future Research process requires a new external action/request and eventually a new Research Handoff.

Previous Cycle authority must never silently become authority for the new version.

## 19. No Implicit Transition Rule

When a required transition condition is:

- missing;
- stale;
- ambiguous;
- mismatched;
- unverifiable;
- unknown,

do not infer success.

Fail closed or enter an explicit blocked/pending condition.

## 20. Core Invariants

```text
External Research is outside runtime.

Import starts runtime, not Cycle authority.

Accepted Scope binding starts active development Cycle authority.

Validated Planning Package + valid EXECUTION_APPROVAL are required for PLAN_READY.

PLAN_READY starts production execution authority.

Models propose; deterministic runtime transitions.

User may pause or cancel controlled runtime work.

Material envelope changes require CHANGE_APPROVAL.

Evaluation is non-mutating acceptance.

Completion Knowledge Package exists before CLOSED_VALIDATED.

CLOSED_VALIDATED ends runtime.

Next-version Research never auto-starts.
```
