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

## 5. Generation Fencing and Concurrent Writer Control

Generation must prevent stale sessions/agents from completing or mutating newer Work authority.

Production mutation on the same active authority must be serialized, leased, generation-fenced, or otherwise conflict-detected so two sessions cannot both validly mutate as the current writer.

A stale writer must fail before authoritative completion and should be prevented from mutation where implementation can enforce that boundary.

Generation/lease recovery must not silently transfer authority without durable state.

## 6. Approval and Human-Control State

Approvals must be durable and stale-safe.

A fresh session should know:

- approval kind;
- subject;
- revision/digest;
- pending/approved/rejected/revoked/stale/consumed-equivalent status;
- whether an approval transition was already consumed.

Human-control state must also be durable enough to prevent accidental dispatch after pause/cancel.

A fresh session must be able to determine whether runtime/Cycle is:

- runnable;
- paused;
- blocked;
- cancelled/terminated;
- closed.

Exact persisted state names belong to implementation.

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

## 11. Repository Baseline and Replay Safety

A repository baseline must identify actual relevant content state.

A branch name alone is insufficient.

If the workspace contains uncommitted or generated changes, baseline identity must include an equivalent durable content digest/manifest or other mechanism that distinguishes the actual working state from the underlying commit.

Potentially non-idempotent commands or external side effects must not be blindly replayed after uncertain interruption.

## 12. Pause / Interrupted-Action Resume

If pause/cancel occurred while a command or tool action may have been in flight, resume must reconcile actual repository/external state before issuing new work.

Do not assume an interrupted command made no changes.

Where mutation state is uncertain:

```text
reconcile actual state
    ↓
record evidence
    ↓
validate authority/bindings
    ↓
only then resume
```

## 13. Evaluation/Closure Resume

A fresh session must determine:

- whether Evaluation completed;
- whether finalization completed;
- whether `CLOSED_VALIDATED` is valid;
- whether Completion Knowledge Package exists and matches final baseline.

## 14. Cross-Machine / Provider Resume

A new machine/model/provider should continue from durable repository state without requiring full conversation replay.

## 15. Core Invariants

```text
runtime ingress does not itself create active Cycle authority

Accepted Scope binding creates active development Cycle authority

PLAN_READY creates production execution authority

original bindings are immutable history

new authority creates new revision/generation

stale sessions cannot complete newer authority

concurrent production writers are serialized/fenced/conflict-detected

actual repository baseline includes relevant working-state identity

potentially non-idempotent actions are reconciled before replay

approval is revision-bound and revocation/staleness is durable

pause/cancel state prevents accidental dispatch after restart

interrupted mutation is reconciled before resume

closure package binding is part of closure truth

resume depends on durable state, not chat
```
