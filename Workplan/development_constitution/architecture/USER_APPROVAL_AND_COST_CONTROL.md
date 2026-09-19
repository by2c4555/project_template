> PROJECT TEMPLATE DEVELOPMENT CONSTITUTION 1.2 — Human owned. AI may read and apply this guidance; modification requires explicit authorization from a trusted repository-owner channel covering the change.

# User Approval and Cost Control

## 1. Purpose

User Approval protects:

- token cost;
- model cost;
- execution cost;
- authority expansion;
- rework;
- destructive behavior;
- compatibility changes;
- migration risk.

Approval is not a substitute for deterministic gates.

## 2. Approval Philosophy

Approve **material envelopes**, not routine steps.

Use approval where the next action creates meaningful new:

```text
cost
authority
commitment
destructive effect
compatibility impact
rework exposure
```

Avoid approval spam.

### 2.1 Materiality Decision Rule

A change is **material** when knowledge of that change at the time of the previous approval could plausibly have caused the approving user to:

- reject the proposal;
- narrow or change Scope;
- choose a different architecture/approach;
- postpone execution;
- require additional safeguards;
- reject the additional cost, risk, or rework.

Materiality should be evaluated against the **approved envelope**, not against an arbitrary global threshold.

A change is normally material when it introduces or materially increases one or more of:

- externally observable product behavior;
- product Scope or non-goals;
- destructive or difficult-to-reverse behavior;
- backward-compatibility impact;
- migration requirement or migration risk;
- security, privacy, or authorization exposure;
- external service/monetary cost;
- model/token cost beyond an explicitly approved budget or cost class;
- production mutation blast radius;
- authorized-path expansion;
- schedule/rework exposure;
- architectural risk that would reasonably affect the user's approval decision.

A change is normally **not** material when it is an internal implementation detail that remains within the already approved:

- Scope;
- behavior;
- compatibility;
- risk;
- cost class/budget;
- authorized paths;
- repair policy.

Examples of normally non-material changes include equivalent internal refactoring, Task resequencing, or bounded repair already covered by the approved envelope.

If an explicit numeric budget/limit exists, crossing it is material.

If no explicit threshold exists and materiality remains uncertain after comparing the change to the approved envelope, treat the change as material only when the potential impact is significant enough that user reconsideration is plausible.

### 2.2 Explicit Approval Rule

Approval must be an explicit user action that deterministic runtime can bind to the current approval subject/revision/digest.

Approval must not be inferred from:

- silence;
- lack of objection;
- previous approval;
- unrelated user input;
- a user answer to a Planning question;
- model confidence;
- "continue" language when the pending approval subject is not deterministically unambiguous.

A UI/chat action such as "approve", "yes", or "proceed" may be valid **only when** runtime can deterministically bind that action to the currently presented pending approval subject and exact bound revision/digest.

#### Trusted decision source

The approval mechanism MUST establish that the action came from a trusted channel authenticated for the relevant user/owner. Repository prose, Research, issue text, copied chat, model output, environment variables, tool output, and generated artifacts cannot impersonate approval.

An approval record MUST identify the approving principal or trusted-channel identity, approval kind, exact subject/revision/digest, displayed material envelope, decision, time, and anti-replay binding. Delegation, when supported, MUST be explicit, scoped, durable, and revocable by an authorized principal.

If identity or channel authenticity cannot be established, record the input as untrusted evidence and keep the approval pending. Do not ask the model to decide whether approval-looking text is genuine.

```text
USER_DECISION_REQUIRED answer
    ≠
SCOPE_APPROVAL

SCOPE_APPROVAL
    ≠
EXECUTION_APPROVAL

EXECUTION_APPROVAL
    ≠
CHANGE_APPROVAL
```

### 2.3 Approval Status Semantics

Implementation must preserve semantics equivalent to:

```text
PENDING
APPROVED
REJECTED
REVOKED
STALE
CONSUMED
```

Exact enum names are implementation-defined.

- `PENDING`: awaiting explicit decision.
- `APPROVED`: valid but not yet consumed by the authorized transition.
- `REJECTED`: user declined the proposed subject.
- `REVOKED`: user withdrew an approval before consumption.
- `STALE`: subject/binding changed such that approval no longer applies.
- `CONSUMED`: approval was validly used for its one-time transition.

Consumed approval remains durable history and cannot be replayed to authorize a different revision.

A request for changes is not partial approval. Runtime records rejection/change-request semantics, returns to the owning proposal boundary, and presents a new exact subject when ready. Implementations MAY support explicitly narrowed approval only by creating and validating a new narrowed subject; they MUST NOT edit an approved subject in place.

### 2.4 Preserve Valid Authorization Without Repeating Reviews

Check durable approval state before asking the user. Valid authorization already covering the current action remains usable; a new session, model, provider, or routine retry is not a new approval boundary.

Distinguish the exact subject of a pending approval from work inside a previously consumed envelope:

- Changing the subject/revision/digest of an unconsumed approval requires a new bound decision; do not transfer the old approval to edited content.
- Routine work within consumed authority proceeds under that authority without reusing the approval as a new grant.
- A permitted non-material contract revision still requires the deterministic revision/binding path and a recorded explanation of why it remains inside the approved envelope. It must not silently rewrite the original subject or approval history.
- A material revision requires Change Approval and any newly applicable Scope/Planning validation. It cannot bypass those checks by calling itself a repair.

One user review may present multiple distinct decisions when each subject, consequence, and explicit decision is bound separately. Do not treat one approval class as another, or ask again for a boundary whose existing approval remains valid.

## 3. Approval Classes

```text
SCOPE_APPROVAL
EXECUTION_APPROVAL
CHANGE_APPROVAL
```

## 4. SCOPE_APPROVAL

Occurs after Planning A.

Planning presents Draft Finalized Scope.

The approval summary should contain:

- objective;
- required behavior;
- compatibility;
- constraints;
- non-goals;
- material decisions;
- assumptions;
- major risks;
- next action/cost consequence.

Valid Scope Approval authorizes deterministic creation/binding of Accepted Scope.

## 5. EXECUTION_APPROVAL

Occurs after Planning B.

The execution review should contain:

- Accepted Scope;
- final architecture;
- Phases;
- Task shape/count;
- major affected areas;
- destructive changes;
- compatibility impact;
- migration impact;
- complexity/cost class;
- major risks;
- verification strategy;
- requested execution envelope.

Valid Execution Approval authorizes transition to `PLAN_READY`.

## 6. CHANGE_APPROVAL

Required when a valid existing approval envelope must materially change.

Examples:

- Scope change;
- architecture rework that materially changes risk/cost;
- destructive migration newly introduced;
- compatibility break newly introduced;
- major authorized-path expansion;
- major extra work;
- new external cost;
- significant execution envelope expansion.

Deployment, publication, remote mutation, paid service use, or sensitive-data disclosure MUST be included in the Scope/Execution envelope or an exact Change Approval before the effect. Approval to prepare or preview an action does not authorize executing the external effect.

## 7. No Approval for Routine Progress

Do not require user approval for:

- normal Task transition;
- normal Phase transition;
- Task PASS;
- Phase PASS;
- ordinary Manager diagnosis;
- bounded repair inside approved repair policy;
- routine verification;
- evidence capture.

## 8. Approval Envelope

Conceptually bind approval to:

```text
approval_id
approval_kind
subject_id
subject_revision
subject_digest
generation
approved_action
approved_cost_or_authority_envelope
approved_at
status
```

Exact schema belongs to implementation.

## 9. Stale-Safe Approval

If the approved subject materially changes:

```text
old approval
    ↓
STALE
```

Old approval must not authorize new authority.

## 10. Single-Use and Revocation Semantics

Where an approval authorizes a one-time transition, it should be consumed or otherwise prevented from being replayed incorrectly.

Before consumption, the user may revoke an approved transition. Revoked approval cannot be consumed.

After consumption, revocation cannot erase historical authority that already existed. To stop/change active work, use the appropriate pause/cancel/change/revision path.

## 11. Approval Does Not Grant PASS

User approval does not mean:

- Task PASS;
- Phase PASS;
- Evaluation PASS;
- CLOSED_VALIDATED.

Those remain deterministic/evaluation responsibilities.

## 12. Rejection Flow

User may:

- reject;
- request changes;
- narrow scope;
- lower cost/risk;
- change constraints.

The workflow should return to the correct Planning boundary.

Do not throw away valid prior Research unnecessarily.

Planning's `RESEARCH_REVISION_REQUIRED` outcome is **not** a user approval rejection. It is a semantic sufficiency return path to `AWAITING_RESEARCH`; importing a replacement Research revision does not itself constitute Scope Approval.

## 13. Scope Rejection

```text
Draft Finalized Scope
    ↓
User rejects/changes
    ↓
Planning A revision
    ↓
new Draft Finalized Scope
    ↓
new Scope Approval
```

## 14. Execution Rejection

```text
Planning Package
    ↓
User rejects/changes
    ↓
Planning B revision
or
Planning A if product intent changed
    ↓
new approval
```

## 15. Recovery and Re-Approval

Recovery may proceed automatically only within the already approved envelope.

If Recovery requires material expansion:

```text
Recovery Proposal
    ↓
CHANGE_APPROVAL
    ↓
revised authority
```

## 16. Cost Control Principle

The system should stop before expensive next-stage work when a material user decision can invalidate that work.

This is why Scope Approval occurs before full Implementation Planning and Execution Approval occurs before repository mutation.

If the user has approved an explicit numeric budget, token ceiling, monetary ceiling, or bounded cost class, runtime must enforce that envelope before controlled dispatch where cost can be reasonably estimated.

Crossing an explicit approved ceiling is material and requires a new approval/budget expansion.

Unknown cost must be labeled unknown; it must not be fabricated as an exact estimate.

Cost checks must account for work already dispatched but not yet reported. Parallel dispatch and provider retries must not each assume the same unspent budget is available. The implementation may reserve estimated cost or serialize dispatch; exact accounting mechanics belong to the runtime. The strict-ceiling and unknown-cost rules are defined in `CONTEXT_AND_COST_MODEL.md`.

## 17. Duplicate Approval Rule

Do not ask for duplicate approval for the same already-approved envelope.

A repeated approval request requires a meaningful new or changed boundary.

## 18. User Pause / Resume / Cancel

Pause/resume/cancel are user control actions, not approval classes.

Their lifecycle semantics are owned by `RUNTIME_LIFECYCLE_AND_TRANSITIONS.md`.

Approval logic must not interpret:

```text
PAUSE
CANCEL
```

as rejection, nor interpret:

```text
RESUME
```

as a new Scope/Execution/Change approval.

A resume action resumes only authority that remains valid.

## 19. Resume

Approval state must be durable.

A fresh session should know:

- what was approved;
- exact subject;
- whether approval is current;
- whether it was consumed;
- whether it became stale.

## 20. Negative Cases

Must reject:

- inferred approval without an explicit bound user action;
- approval confused with a `USER_DECISION_REQUIRED` answer;
- approval for wrong revision;
- approval for stale digest;
- approval from wrong subject;
- replayed one-time approval;
- approval for a superseded Planning Package;
- using Scope Approval as Execution Approval;
- using Execution Approval for material later expansion;
- treating Research submission/revision as Scope Approval;
- treating `RESEARCH_REVISION_REQUIRED` as user rejection/cancellation.

## 21. Core Invariants

```text
Approval protects material cost/authority boundaries.

Material means the change could plausibly alter the user's prior approval decision.

Approval is explicit and bound to exact subject/revision/digest.

Silence and unrelated user input are not approval.

Material changes invalidate prior approval.

Routine bounded work does not require repeated approval.

Approval never substitutes for deterministic PASS.

Recovery cannot self-authorize material envelope expansion.
```

Conformance coverage: `C-004`, `C-006`, `C-013`, `C-014`, `C-021`.
