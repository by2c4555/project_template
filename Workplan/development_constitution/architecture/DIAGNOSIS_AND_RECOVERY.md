> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Diagnosis and Recovery

## 1. Purpose

Defines escalated reasoning after local execution can no longer safely continue.

## 2. External Diagnosis

Diagnosis is reasoning-only.

Inputs may include:

- Accepted Scope;
- Planning Package;
- repository state;
- Failure Record;
- Attempt history;
- Manager diagnosis history;
- verification evidence;
- mutation history;
- relevant logs/artifacts.

## 3. Diagnosis Output

Diagnosis determines:

```text
observed failure
root cause
affected component
violated invariant/contract
blast radius
classification
correct recovery boundary
```

## 4. Canonical Classifications

```text
IMPLEMENTATION_DEFECT
TASK_DEFECT
PLAN_DEFECT
EVALUATION_DEFECT
SCOPE_DEFECT
SCOPE_AMBIGUITY
ENVIRONMENT_DEFECT
TOOLING_DEFECT
VERIFICATION_DEFECT
EXTERNAL_BLOCKER
UNKNOWN
```

## 5. Deterministic Continuation

Every classification must map to a deterministic continuation.

Examples:

- `IMPLEMENTATION_DEFECT` → Recovery/local correction;
- `TASK_DEFECT` → Task authority revision;
- `PLAN_DEFECT` → Planning revision;
- `SCOPE_DEFECT` / `SCOPE_AMBIGUITY` → Planning/owner boundary;
- `ENVIRONMENT_DEFECT` → environment/owner action;
- `EXTERNAL_BLOCKER` → explicit blocked state.

## 6. External Recovery

Recovery is reasoning-only.

It converts eligible Diagnosis into a durable correction contract.

## 7. Recovery Flow

```text
Escalated Failure
    ↓
External Diagnosis
    ↓
Diagnosis Record
    ↓
External Recovery
    ↓
Recovery Contract
    ↓
Manager
    ↓
fresh RECOVERY Builder Attempt
    ↓
Verification / Evidence
    ↓
Task Gate / Phase Gate
```

## 8. Recovery Boundaries

Recovery cannot:

- directly mark Task PASS;
- directly mark Phase PASS;
- create new product Scope;
- silently broaden Task authority;
- silently expand authorized paths;
- bypass User Re-Approval for material expansion.

## 9. Material Change

If recovery requires:

- material Scope change;
- major architecture revision;
- destructive migration;
- compatibility break;
- major cost increase;
- major authority expansion,

route through Planning and `CHANGE_APPROVAL`.

## 10. Issue Lifecycle

Conceptually:

```text
OPEN
    ↓
AWAITING_DIAGNOSIS
    ↓
DIAGNOSED
    ↓
RECOVERY_READY
or
PLAN_REVISION_REQUIRED
or
OWNER_ACTION_REQUIRED
    ↓
IN_RECOVERY / revision
    ↓
RESOLVED / SUPERSEDED
```

Exact names belong to implementation.

## 11. No Permanent Loops

Diagnosis and Recovery must not become permanent retry loops.

Repeated failure must either:

- make progress;
- revise authority;
- request owner action;
- terminate as blocked.
