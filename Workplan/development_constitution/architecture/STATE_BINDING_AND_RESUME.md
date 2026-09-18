> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# State, Binding, and Resume

## 1. Purpose

Defines durable state, immutable bindings, generation fencing, checkpoints, and cross-session continuation.

## 2. Durable Truth

Repository/filesystem state is durable truth.

Chat/session context is disposable.

### 2.1 Runtime / Cycle / Execution State Boundary

The following boundaries must remain distinct:

```text
Research Handoff enters Import
    ↓
runtime exists

Accepted Scope is created and bound
    ↓
active development Cycle authority exists

valid Planning Package + valid EXECUTION_APPROVAL
    ↓
PLAN_READY
    ↓
production execution authority exists
```

Planning A therefore runs inside runtime before active development Cycle authority.

A provisional Cycle ID or pre-Cycle record may exist earlier for bookkeeping, logging, or checkpointing, but it must not authorize:

- Phase creation as executable authority;
- Task issuance;
- Builder mutation;
- production Attempt issuance;
- execution PASS progression.

### 2.2 Active Cycle Binding

When Accepted Scope is created, the active Cycle must be durably associated with at least the applicable:

- Cycle identity;
- Accepted Scope revision/digest;
- repository baseline used for Scope acceptance;
- generation;
- Scope Approval identity/binding.

When `PLAN_READY` is later established, execution authority must additionally bind the applicable:

- Planning Package revision/digest;
- Execution Approval identity/binding;
- current generation.

Exact schema belongs to implementation.

## 3. Binding Principle

Work authority must remain bound to the authority that existed when issued.

Applicable bindings may include:

- Cycle;
- Scope revision/digest;
- Planning revision/digest;
- approval revision/digest;
- Phase;
- Task;
- Attempt;
- Recovery contract;
- generation.

## 4. No Silent Rebinding

Resume must compare current authority with original bindings.

Do not silently recalculate and overwrite original bindings.

## 5. Generation Fencing

Generation must prevent stale sessions/agents from completing or mutating newer Work authority.

## 6. Approval State

Approvals must be durable and stale-safe.

A fresh session should know:

- approval kind;
- subject;
- revision/digest;
- current/stale/consumed status.

## 7. Planning Checkpoints

Planning should preserve progress through durable checkpoints rather than depending on chat memory.

## 8. Attempt History

Every Builder dispatch creates a durable Attempt record.

Failed Attempts remain historical evidence.

## 9. Failure Resume

A fresh capable model should be able to diagnose from:

- Failure Record;
- Attempt history;
- prior Manager diagnoses;
- prior repair strategies;
- verification evidence;
- mutation evidence;
- authority bindings.

## 10. Issue Resume

Escalated issue state must preserve deterministic next action.

No dangling issue should require reconstructing meaning from conversation history.

## 11. Evaluation/Closure Resume

A fresh session must determine:

- whether Evaluation completed;
- whether finalization completed;
- whether `CLOSED_VALIDATED` is valid;
- whether Completion Knowledge Package exists and matches final baseline.

## 12. Cross-Machine / Provider Resume

A new machine/model/provider should continue from durable repository state without requiring full conversation replay.

## 13. Core Invariants

```text
runtime ingress does not itself create active Cycle authority

Accepted Scope binding creates active development Cycle authority

PLAN_READY creates production execution authority

original bindings are immutable history

new authority creates new revision/generation

stale sessions cannot complete newer authority

approval is revision-bound

resume depends on durable state, not chat
```
