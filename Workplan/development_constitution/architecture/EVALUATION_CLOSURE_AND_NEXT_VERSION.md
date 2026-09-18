> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Evaluation, Closure, and Next Version

## 1. Purpose

Defines:

- Independent Evaluation;
- deterministic finalization;
- `CLOSED_VALIDATED`;
- Completion Knowledge Package;
- next-version Research handoff.

## 2. Evaluation Eligibility

Evaluation begins only after required Phase Gates PASS and blocking execution issues are resolved.

## 3. Evaluation Inputs

Applicable:

- Accepted Scope;
- Planning Package;
- Task/Phase gate evidence;
- current repository state;
- verification evidence;
- relevant issue/recovery history.

## 4. Evaluation Responsibilities

Independent Evaluation should:

- verify actual repository outcome;
- verify Scope satisfaction;
- verify Planning acceptance requirements;
- inspect sufficient evidence;
- run independent checks where appropriate;
- identify blocking vs non-blocking findings.

Evaluation is not production repair.

## 5. Evaluation Results

Canonical results may include:

```text
PASS
PASS_WITH_FINDINGS
DIAGNOSIS_REQUIRED
```

Exact runtime vocabulary should remain consistent with implementation.

## 6. Blocking Evaluation

```text
Evaluation blocker
    ↓
Failure Record
    ↓
External Diagnosis
    ↓
Recovery / Planning / Owner Action
    ↓
Execution/Gates when applicable
    ↓
Evaluation again
```

## 7. Deterministic Finalization

A model Evaluation result does not itself create `CLOSED_VALIDATED`.

Deterministic finalization verifies applicable:

- valid Evaluation result;
- required completion report;
- correct Scope/Planning bindings;
- current repository baseline;
- unresolved blocking issues;
- final required evidence.

## 8. CLOSED_VALIDATED Semantics

`CLOSED_VALIDATED` means:

- required Accepted Scope satisfied;
- required implementation completed;
- required Task/Phase Gates passed;
- Independent Evaluation accepted actual outcome;
- deterministic finalization completed;
- final repository baseline durably recorded;
- Completion Knowledge Package produced.

## 9. Completion Knowledge Package

Required purpose:

```text
Current Cycle closure
    ↓
durable reusable knowledge
    ↓
future External Research
```

Recommended contents:

### Completion Report

- what was implemented;
- what was verified;
- final acceptance result.

### Final Repository Baseline

- version;
- commit/revision identifier;
- Scope revision/digest;
- Planning revision/digest;
- Evaluation result;
- completion artifact digest where applicable.

### Verified Architecture State

- architecture actually implemented;
- interfaces;
- data model;
- important constraints.

### Scope Outcome

- requirement → implementation;
- requirement → verification;
- accepted result.

### Accepted Decisions

- material Planning decisions;
- trade-offs;
- rationale.

### Known Findings

- non-blocking findings;
- limitations;
- technical debt.

### Deferred Work

- explicitly deferred items;
- why deferred;
- dependencies/constraints.

### Repair / Recovery Lessons

- material failures;
- disproven strategies;
- successful correction patterns.

### Next-Version Research Seed

- suggested follow-up topics;
- compatibility watchpoints;
- unresolved opportunities;
- relevant evidence references.

## 10. Knowledge, Not Scope

Completion Knowledge Package is:

```text
KNOWLEDGE
```

not:

```text
NEXT SCOPE
```

A future version still requires:

```text
External Research
    ↓
new Research Handoff
    ↓
Planning Finalization
    ↓
User Scope Approval
    ↓
new Accepted Scope
```

## 11. Cross-Cycle Isolation

Previous:

- Scope;
- Planning Package;
- approvals;
- tickets;

must not silently become current Cycle authority.

They may remain durable historical evidence/knowledge.

## 12. Next-Version Flow

```text
CLOSED_VALIDATED
    ↓
Completion Knowledge Package
    ↓
outside runtime
    ↓
Next-Version External Research
    ↓
new Research Handoff
    ↓
next runtime import
```

## 13. Closure Resume

A fresh session must be able to determine whether closure completed and whether the Completion Knowledge Package is valid without replaying prior chat.

## 14. Core Invariants

```text
Evaluation is independent acceptance.

Evaluation does not repair production.

CLOSED_VALIDATED requires deterministic finalization.

Closure produces next-version knowledge.

Completion knowledge is not next Scope.

Future version begins through new Research + Planning finalization.
```
