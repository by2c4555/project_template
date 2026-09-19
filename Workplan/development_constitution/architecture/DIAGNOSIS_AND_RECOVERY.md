> PROJECT TEMPLATE DEVELOPMENT CONSTITUTION 1.2 — Human owned. AI may read and apply this guidance; modification requires explicit authorization from a trusted repository-owner channel covering the change.

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

The Diagnosis Record must separate observed evidence from inferred cause. Include the failing authority/baseline, reproducible symptom or limitation, evidence references, leading hypothesis, relevant alternatives, and what would confirm or disprove the hypothesis. If the cause cannot be established, record `UNKNOWN` with a bounded evidence-gathering action; do not invent a root cause to make the record appear complete.

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

The contract must identify the issue and Diagnosis evidence, current Scope/Planning/generation and repository baseline, intended correction, authorized paths and side effects, verification criteria, stop/escalation conditions, and applicable repair/cost limits. Where rollback or compensation is relevant, state its feasibility and authority; do not assume reversal is always possible.

Runtime validates these bindings and the approved envelope before issuing a fresh Recovery Attempt. Producing a Recovery Contract is not permission to implement it.

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

That diagram applies to production correction. Other classifications return through their owning boundary:

| Corrected class | Required return |
|---|---|
| Implementation or bounded Task defect | Fresh authorized Attempt -> affected Task/Phase Gates |
| Planning or Scope defect | Successor revision under `L-054` -> applicable approvals/package validation -> affected execution/gates |
| Verification defect | Validate successor verification contract -> rerun affected checks -> affected gates |
| Evaluation defect | Validate successor Evaluation method/evidence -> new Evaluation attempt; no production edit solely to satisfy the old evaluator |
| Environment/tooling defect | Validate corrected environment/tool -> rerun only evidence invalidated by the defect -> owning gate/Evaluation |
| External blocker or `UNKNOWN` | Remain blocked until the named condition/evidence is independently resolved and current authority revalidates |

Runtime records the owning return boundary in the issue. Recovery completion cannot choose a later stage because it appears cheaper.

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

Each additional Diagnosis/Recovery round must name the new evidence, changed hypothesis, or revised authorized correction that justifies it. Repeating the same unsuccessful strategy against unchanged evidence is not progress. Preserve a stable issue lineage and cumulative effort/cost across new Attempts and provider changes; a reset must not erase exhaustion. Use the bound repair/escalation policy and explicit budget instead of inventing a new retry allowance.

Resolve an issue only when the correction has the required verification/gate evidence against the current baseline. A proposed fix, completed edit, provider success response, or superseded plan alone does not prove resolution. Supersession must reference the successor authority and preserve unresolved findings for its validation.

Conformance coverage: `C-011`, `C-012`, `C-013`, `C-016`, `C-019`.
