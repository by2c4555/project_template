> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Diagnosis and Recovery

## 1. Purpose

Defines escalated reasoning after local execution can no longer safely continue.

## 2. External Diagnosis

Diagnosis is reasoning-only.

`External` describes the reasoning environment/provider boundary. Diagnosis remains runtime-controlled work and does not own lifecycle authority.

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

Every classification must map to an explicit continuation.

| Classification | Canonical continuation |
|---|---|
| `IMPLEMENTATION_DEFECT` | Recovery/local correction under current higher-level authority when legal |
| `TASK_DEFECT` | Task contract/authority revision; Planning involvement when Task redesign is material |
| `PLAN_DEFECT` | Planning B revision; return to Planning A if product Scope/acceptance is implicated |
| `EVALUATION_DEFECT` | Correct/revise Evaluation method/evidence; do not mutate production merely to satisfy a defective evaluator |
| `SCOPE_DEFECT` | Planning A / owner boundary; revised Scope and new approval if material |
| `SCOPE_AMBIGUITY` | Focused user decision and Planning A finalization; new Scope approval as required |
| `ENVIRONMENT_DEFECT` | Environment correction or owner action; resume only after environment is validated |
| `TOOLING_DEFECT` | Tooling correction/replacement/owner action; do not reinterpret implementation as failed if tool is defective |
| `VERIFICATION_DEFECT` | Verification contract/reasoning revision through Planning as appropriate; rerun valid verification |
| `EXTERNAL_BLOCKER` | Explicit blocked state awaiting external/owner action |
| `UNKNOWN` | Remain blocked / gather bounded additional evidence / escalate; **no production continuation by guess** |

The deterministic continuation must preserve current authority history and identify whether re-approval is required.

## 6. External Recovery

Recovery is reasoning-only.

`External` describes where the reasoning may execute; deterministic Workplan still owns continuation, bindings, and authority transitions.

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

`UNKNOWN` must never mean "try arbitrary production changes until something works."
