> PROJECT TEMPLATE DEVELOPMENT CONSTITUTION 1.2 — Human owned. AI may read and apply this guidance; modification requires explicit authorization from a trusted repository-owner channel covering the change.

# Failure and Repair Model

## 1. Purpose

Defines Task-local failure handling and bounded repair.

## 2. Failure Evidence

Every authoritative failure must preserve applicable:

- failure identity;
- Task/Attempt identity;
- generation;
- observed failure;
- expected behavior;
- command/check;
- exit result;
- logs;
- verification evidence;
- mutation information;
- authority bindings;
- prior attempts;
- prior diagnoses;
- prior repair strategies.

## 3. Local Repair Flow

```text
Builder Attempt
    ↓ FAIL
Failure Record
    ↓
Manager diagnosis
    ↓
bounded repair strategy
    ↓
fresh REPAIR ticket
    ↓
fresh Builder REPAIR Attempt
    ↓
verification/evidence
    ↓
Task Gate
```

## 4. Hard Limit

Maximum ordinary Task-local Repair Attempts per failure chain:

```text
5
```

No sixth local repair.

The initial Attempt does not count as a Repair Attempt. The configured repair allowance may be smaller than five. Reserve/count each fresh authorized repair before dispatch; a failed, interrupted, or abandoned dispatched repair remains part of the same failure chain. Resume preserves that count.

An infrastructure retry with no new implementation attempt may use a separate bounded retry policy, but must retain its invocation/effect evidence and cost. It must not conceal additional edits or reset the local repair allowance.

## 5. Early Escalation

Escalate earlier when:

- authority is invalid;
- Task contract is defective;
- architecture is wrong;
- Scope is defective;
- environment/tooling is external;
- strategy is disproven;
- repair requires material envelope expansion.

## 6. Strategy History

Failed strategies must remain durable.

Do not silently repeat the same disproven strategy.

Each proposed repair must state the observed defect, a supported hypothesis, the bounded change, and the check that would disprove or confirm the hypothesis. A repeat is justified only by new evidence or a recorded transient cause. Repeated no-progress failures should escalate before the maximum.

Do not rerun a failed or flaky acceptance check until it happens to pass and then discard the failures. Establish the cause or follow a predefined repeat policy, retaining all outcomes.

## 7. Repair Authority

Local repair stays within:

- current Scope;
- current Task objective;
- authorized paths;
- approved cost/authority envelope.

If repair requires expansion, route to Diagnosis/Recovery and possibly User Re-Approval.

## 8. Successful Repair

A successful REPAIR Attempt returns to Task Gate.

Manager does not self-grant PASS.

## 9. Failure Chain Identity

Retries must belong to the same failure chain where appropriate so the hard limit cannot be bypassed by renaming the attempt.

Changing the Task name, model, provider, session, or worktree does not reset an unresolved failure chain. A materially revised Task/Recovery contract must reference the predecessor, describe the changed strategy and authority, and receive any required re-approval. It cannot authorize an unchanged sixth ordinary repair.

## 10. Core Invariants

```text
failure is durable
repair is bounded
each repair is a fresh Attempt
Manager reasons
Builder mutates
Task Gate decides PASS
no sixth local repair
```

Conformance coverage: `C-010`, `C-011`, `C-012`, `C-019`.
