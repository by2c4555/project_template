> PROJECT TEMPLATE DEVELOPMENT CONSTITUTION 1.2 — Human owned. AI may read and apply this guidance; modification requires explicit authorization from a trusted repository-owner channel covering the change.

# Runtime Lifecycle and Transitions

## 1. Purpose

This document owns the canonical lifecycle transition semantics of Project Template runtime.

It defines:

- where runtime begins and ends;
- when active development Cycle authority exists;
- when production execution authority exists;
- required transition preconditions;
- canonical state/stage and event vocabulary;
- Research revision/awaiting-Research loop;
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
AWAITING_RESEARCH
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

### 2.1 Canonical Stage / Condition Dictionary

The following names are normative conceptual meanings even when implementation persists equivalent fields rather than exact enum names:

| Name | Kind | Required meaning |
|---|---|---|
| `IMPORT` | stage | Research Handoff is being structurally/trust validated |
| `PLANNING_A` | stage | pre-Cycle Research sufficiency/finalization reasoning |
| `AWAITING_RESEARCH` | condition | no valid continuation to Scope finalization until a new Research revision is imported |
| `SCOPE_APPROVAL_PENDING` | condition | Draft Finalized Scope awaits bound user decision |
| `ACTIVE_CYCLE` | authority condition | Accepted Scope is bound; active development Cycle authority exists |
| `PLANNING_B` | stage | implementation Planning under Accepted Scope |
| `EXECUTION_APPROVAL_PENDING` | condition | Validated Planning Package awaits bound user decision |
| `PLAN_READY` | authority condition | production execution authority exists |
| `EXECUTION` | stage | production Task/Phase work is active |
| `EVALUATION` | stage | independent acceptance reasoning is eligible/active |
| `CLOSURE_PREPARATION` | stage | closure knowledge is being prepared/validated |
| `CLOSED_VALIDATED` | terminal authority state | successful runtime/Cycle has deterministically closed |
| `PAUSED` | control condition | new controlled dispatch is prohibited until valid resume |
| `BLOCKED` | control condition | required prerequisite/authority/evidence is unavailable |
| `CANCELLED` | terminal/control condition | further runtime/Cycle authority is terminated without successful closure |

### 2.2 Canonical Event Dictionary

Equivalent implementation events must preserve these meanings:

```text
IMPORT_ACCEPTED
IMPORT_REJECTED
RESEARCH_SUFFICIENT
RESEARCH_REVISION_REQUIRED
RESEARCH_REVISION_IMPORTED
SCOPE_APPROVED
SCOPE_REJECTED
SCOPE_REVOKED
PLANNING_PACKAGE_VALID
PLANNING_PACKAGE_INVALID
EXECUTION_APPROVED
EXECUTION_REJECTED
MATERIAL_CHANGE_IDENTIFIED
REVISION_AUTHORITY_VALIDATED
RECOVERY_AUTHORITY_VALIDATED
RECOVERY_VERIFIED
PAUSE_REQUESTED
RESUME_REQUESTED
CANCEL_REQUESTED
ALL_REQUIRED_PHASES_PASS
EVALUATION_ACCEPTED
EVALUATION_BLOCKING
FINALIZATION_PASS
FINALIZATION_FAIL
```

Model output may propose semantic events such as `RESEARCH_SUFFICIENT` or Evaluation findings. Deterministic runtime owns the actual lifecycle transition and must validate required bindings/preconditions.

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

### 3.1 Transition Evidence and Control Precedence

Each authority-changing transition must durably identify its triggering event, prior authority, checked prerequisites, resulting authority, and relevant artifact/approval bindings. A retry must recognize an already-completed transition instead of consuming approval twice or creating duplicate authority. Interrupted transitions use the reconciliation rules in `STATE_BINDING_AND_RESUME.md`.

Stage and control conditions are separate concepts. For example, Planning may be paused or execution may be blocked without losing the underlying stage. Do not resume from a control condition by guessing which stage comes next.

Before controlled dispatch or authoritative completion, runtime checks:

1. the runtime/Cycle is not cancelled or successfully closed;
2. no applicable pause or blocking condition prohibits the action;
3. the actor, generation, bindings, approvals, and remaining cost envelope are valid;
4. the stage-specific prerequisites hold.

Pause, cancellation, or supersession fences pending outputs: a late provider/Builder result may be retained as evidence, but must not advance authority under an invalid or suspended dispatch. Reconciliation determines whether it can be accepted after a valid resume. Cancellation is terminal for that runtime/Cycle; a later request creates new authority rather than resuming cancelled tickets.

When more than one control condition applies, the most restrictive effect governs dispatch. Clearing one condition does not clear another. Runtime MUST preserve the underlying stage plus every active control condition and its independently validated clear condition.

## 4. Canonical Lifecycle

```text
════════ OUTSIDE RUNTIME ════════

External Research
    ↓
Research Handoff

════════ RUNTIME INGRESS ════════

Import / Structural + Trust Validation
    ↓
Immutable Archived Research Revision
    ↓
consumed package cleared from ingest

════════ PRE-CYCLE RUNTIME ══════

Planning A
Research Investigation & Finalization
    │
    ├─ RESEARCH_REVISION_REQUIRED
    │      ↓
    │  persist report + carry-forward knowledge
    │      ↓
    │  AWAITING_RESEARCH
    │      ↓
    │  new Research Handoff
    │      ↓
    │  new archived Research revision
    │      ↓
    │  Planning A revision / delta reconciliation
    │
    └─ RESEARCH_SUFFICIENT
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

A successful import must durably create/verify an immutable archived Research revision, bind runtime input to that revision, and clear the consumed package from `Workplan/ingest/` before Planning depends on the input.

Ingest location is transport state, not durable Research identity.

## 6. Planning A / Pre-Cycle Runtime

Planning A occurs inside Project Template runtime but before active development Cycle authority.

Planning A may:

- inspect the current archived Research revision;
- assess semantic Research sufficiency;
- inspect current repository evidence;
- investigate technical unknowns;
- request focused user decisions;
- produce Draft Finalized Scope.

Planning A must not create executable Phase/Task/Builder authority.

### 6.1 Research Revision Transition

When Planning A determines that material missing, contradictory, stale, weak, or unavailable evidence prevents responsible Scope finalization:

```text
PLANNING_A
    ↓
RESEARCH_REVISION_REQUIRED
    ↓
persist Research Revision Required report
+ persist Planning carry-forward knowledge
+ preserve current Research/Planning history
    ↓
AWAITING_RESEARCH
```

`RESEARCH_REVISION_REQUIRED` is a normal controlled semantic outcome. It is not `SCOPE_REJECTED`, not user cancellation, and not an implementation failure.

While `AWAITING_RESEARCH`, runtime must not create Accepted Scope or begin Planning B.

A valid replacement Research Handoff must:

```text
create new Research revision identity
+ preserve predecessor lineage
+ archive/verify new input
+ clear consumed ingest package
+ create explicit new Planning revision/binding
+ reference prior carry-forward knowledge
    ↓
PLANNING_A
```

The prior Planning Work must not be silently rebound from the old Research digest to the new Research digest.

Detailed knowledge/revision semantics are owned by `RESEARCH_REVISION_AND_CARRY_FORWARD.md`.

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

Validation failure must route according to the defect source:

```text
Planning-package structural/design defect
    → PLANNING_B

Accepted Scope/product-intent defect
    → PLANNING_A / Scope revision boundary

Research evidence defect that prevents responsible Scope correction
    → RESEARCH_REVISION_REQUIRED → AWAITING_RESEARCH
```

Do not use an unspecified "earlier boundary" when the defect class is known.

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

### 12.1 Revision effect

A material revision MUST identify what authority changed and compute its downstream invalidation:

| Changed authority | Minimum effect |
|---|---|
| Research evidence before Scope acceptance | New Research/Planning A revision; no silent rebinding |
| Accepted Scope/product intent | Suspend affected execution; new Scope revision and Scope Approval; revise/revalidate Planning; new Execution Approval when the execution envelope changes |
| Planning design/package within unchanged Scope | New Planning revision, deterministic package validation, and Execution or Change Approval as materiality requires |
| Task/Recovery contract within approved envelope | New contract/generation; invalidate affected tickets and evidence; re-run affected gates |
| Cost/risk/path/external-effect envelope | Change Approval before expanded dispatch |

Previously completed Tasks remain historical PASS records. They are current only when impact analysis shows their authority, outputs, dependencies, and evidence remain valid under the successor revision. Otherwise affected Tasks return to an eligible unpassed state under new authority; history is never erased.

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

It must also identify the affected stage/dispatch boundary and the condition that would permit continuation. New evidence, a user answer, or an environment repair does not itself clear the block: runtime validates that the named condition is resolved and rechecks current authority before continuing. Unaffected work may continue only when its independence and authority are explicit.

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

## 19. Canonical Transition Matrix

This matrix is normative at the semantic level. Exact persisted enum/command names may differ, but implementation and agents must not invent competing lifecycle routes.

| ID | FROM | EVENT / PRECONDITION | TO / EFFECT |
|---|---|---|---|
| `L-001` | outside runtime | valid Research Handoff submitted | `IMPORT` |
| `L-002` | `IMPORT` | `IMPORT_ACCEPTED` after structural/trust validation | archive immutable Research revision, clear ingest, enter `PLANNING_A` |
| `L-003` | `IMPORT` | `IMPORT_REJECTED` | remain outside downstream Planning; persist rejection reason |
| `L-010` | `PLANNING_A` | `RESEARCH_REVISION_REQUIRED` | persist report/carry-forward → `AWAITING_RESEARCH` |
| `L-011` | `AWAITING_RESEARCH` | valid `RESEARCH_REVISION_IMPORTED` | new Research/Planning revision → `PLANNING_A` |
| `L-012` | `PLANNING_A` | `RESEARCH_SUFFICIENT` + Draft Finalized Scope | `SCOPE_APPROVAL_PENDING` |
| `L-020` | `SCOPE_APPROVAL_PENDING` | valid `SCOPE_APPROVED` | bind Accepted Scope → active Cycle / `PLANNING_B` |
| `L-021` | `SCOPE_APPROVAL_PENDING` | `SCOPE_REJECTED` / material user change | Planning A revision; no Accepted Scope from rejected subject |
| `L-030` | `PLANNING_B` | Candidate Planning Package produced | deterministic Planning Package Validation |
| `L-031` | Planning Package Validation | `PLANNING_PACKAGE_VALID` | `EXECUTION_APPROVAL_PENDING` |
| `L-032` | Planning Package Validation | package/design defect | `PLANNING_B` revision |
| `L-033` | Planning Package Validation | Scope/product-intent defect | Planning A / Scope revision boundary |
| `L-034` | Planning Package Validation | Research evidence defect preventing Scope correction | `AWAITING_RESEARCH` via Research revision path |
| `L-040` | `EXECUTION_APPROVAL_PENDING` | valid `EXECUTION_APPROVED` + current bindings/no blocker | `PLAN_READY` |
| `L-041` | `EXECUTION_APPROVAL_PENDING` | `EXECUTION_REJECTED` | Planning B revision, or Planning A if product intent changed |
| `L-050` | `PLAN_READY` | valid execution dispatch | `EXECUTION` |
| `L-051` | `EXECUTION` | bounded failure within authority | local Repair path |
| `L-052` | `EXECUTION` | material change / exhausted/structural issue | Diagnosis/Recovery/Planning/owner path; affected dispatch stops |
| `L-053` | non-terminal authority stage | `MATERIAL_CHANGE_IDENTIFIED` | stop affected dispatch; validated revision and bound Change Approval precede replacement authority |
| `L-054` | revision pending | `REVISION_AUTHORITY_VALIDATED` + applicable approval | publish successor revision/generation; invalidate affected downstream tickets/evidence; return to its owning stage |
| `L-055` | diagnosed recoverable issue | `RECOVERY_AUTHORITY_VALIDATED` | issue bounded Recovery contract/Attempt under unchanged or newly approved envelope |
| `L-056` | Recovery implementation/gates | `RECOVERY_VERIFIED` | return to the failed owning boundary: Task/Phase progression, Planning validation, or Evaluation eligibility |
| `L-060` | execution/gates | `ALL_REQUIRED_PHASES_PASS` + no blocker/current bindings | `EVALUATION` |
| `L-061` | `EVALUATION` | `EVALUATION_BLOCKING` | Diagnosis/Recovery/Planning as classified |
| `L-062` | `EVALUATION` | accepted Evaluation result | `CLOSURE_PREPARATION` |
| `L-063` | Diagnosis/Recovery after Evaluation blocker | correction passes applicable execution gates and bindings are current | start a new Evaluation attempt against the corrected baseline |
| `L-070` | `CLOSURE_PREPARATION` | `FINALIZATION_PASS` | `CLOSED_VALIDATED`; runtime ends |
| `L-071` | `CLOSURE_PREPARATION` | `FINALIZATION_FAIL` | remain unclosed; route to correct repair/blocked boundary |
| `L-080` | runnable controlled stage | `PAUSE_REQUESTED` | safe durable `PAUSED` equivalent; no new controlled dispatch |
| `L-081` | `PAUSED` | valid `RESUME_REQUESTED` after reconciliation | resume last valid authority/stage |
| `L-082` | non-terminal runtime | `CANCEL_REQUESTED` | `CANCELLED` equivalent; no successful closure |
| `L-084` | `CANCELLED` or `CLOSED_VALIDATED` | separately authenticated new external request plus new Handoff | create new runtime identity at `IMPORT`; prior authority remains historical only |
| `L-083` | pending unconsumed approval | approval revoked, stale, or rejected | prevent consumption; remain pending or return to the applicable proposal revision boundary |
| `L-090` | non-terminal stage | required prerequisite unavailable or unverifiable | retain stage and authority history; enter an explicit `BLOCKED` condition |
| `L-091` | blocked stage | recorded unblock condition resolved and current prerequisites revalidated | clear only the resolved block; resume the last valid stage if no other control condition prevents it |

Any transition not represented by this matrix or by an explicit subsystem exception contract must fail closed rather than be inferred from model prose.

## 20. No Implicit Transition Rule

When a required transition condition is:

- missing;
- stale;
- ambiguous;
- mismatched;
- unverifiable;
- unknown,

do not infer success.

Fail closed or enter an explicit blocked/pending condition.

## 21. Core Invariants

```text
External Research is outside runtime.

Import starts runtime, not Cycle authority.

Successful import archives immutable Research evidence, binds to archive, and clears consumed ingest input.

Material Research insufficiency routes to AWAITING_RESEARCH without creating Scope authority.

A replacement Research Handoff creates new Research/Planning revision identity; prior bindings are not silently rewritten.

Accepted Scope binding starts active development Cycle authority.

Validated Planning Package + valid EXECUTION_APPROVAL are required for PLAN_READY.

PLAN_READY starts production execution authority.

Models propose semantic outcomes; deterministic runtime validates and transitions.

The canonical transition matrix controls cross-agent interpretation.

User may pause or cancel controlled runtime work.

Material envelope changes require CHANGE_APPROVAL.

Evaluation is non-mutating acceptance.

Completion Knowledge Package exists before CLOSED_VALIDATED.

CLOSED_VALIDATED ends runtime.

Next-version Research never auto-starts.
```

Conformance coverage: `C-002`, `C-003`, `C-004`, `C-006`, `C-007`, `C-009`, `C-012`, `C-013`, `C-016`, `C-017`, `C-019`.
