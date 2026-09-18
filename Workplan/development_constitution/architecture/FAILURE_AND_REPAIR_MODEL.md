> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

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
