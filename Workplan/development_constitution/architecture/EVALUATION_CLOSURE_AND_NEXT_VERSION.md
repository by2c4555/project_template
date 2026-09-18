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

### 4.1 Independence Semantics

Independent Evaluation is independent in **authority and evidence posture**.

The evaluator:

- has no production mutation authority;
- does not treat Builder/Manager self-claims as sufficient proof;
- evaluates actual repository state and bound evidence;
- evaluates against current Accepted Scope and Planning acceptance contracts;
- may run independent read-only or verification checks when authorized;
- must not weaken acceptance merely because implementation already consumed cost.

A different model/provider may improve independence, but is not required by the Constitution.

The same underlying model may perform Evaluation only when invoked as a separate evaluation role/context with no production mutation authority and with current bound evidence.

## 5. Evaluation Results

Canonical results may include:

```text
PASS
PASS_WITH_FINDINGS
DIAGNOSIS_REQUIRED
```

Exact runtime vocabulary should remain consistent with implementation.

`PASS_WITH_FINDINGS` is valid only when every finding is demonstrably non-blocking relative to Accepted Scope and required acceptance contracts.

If a finding could invalidate required behavior, compatibility, evidence, security, migration safety, or acceptance, the result must not be `PASS_WITH_FINDINGS`; it must route to Diagnosis/Recovery/Planning as appropriate.

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

## 7. Closure Preparation and Deterministic Finalization

A model Evaluation result does not itself create `CLOSED_VALIDATED`.

After an accepted Evaluation result, the required Completion Knowledge Package core information must be prepared.

Deterministic finalization then verifies applicable:

- valid Evaluation result;
- required Completion Knowledge Package contents;
- required completion report;
- correct Scope/Planning bindings;
- current repository baseline;
- unresolved blocking issues;
- final required evidence.

Only then may deterministic runtime establish `CLOSED_VALIDATED`.

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

The Completion Knowledge Package is a **required closure artifact**.

Its exact file layout may vary, but deterministic finalization must verify that the required core information is present or durably referenced.

### 9.1 Required Core Contents

Every `CLOSED_VALIDATED` Cycle must provide:

#### Completion Report

- what was implemented;
- what was verified;
- final acceptance result.

#### Final Repository Baseline

- version;
- commit/revision identifier;
- Scope revision/digest;
- Planning revision/digest;
- Evaluation result;
- completion artifact digest where applicable.

#### Verified Architecture State

- architecture actually implemented, or a durable reference to the canonical verified architecture state;
- externally relevant interfaces;
- persistent data-model state where applicable;
- important active constraints.

#### Scope Outcome

- material requirement → implementation outcome;
- material requirement → verification/evidence;
- accepted result.

#### Accepted Decisions

- material Planning decisions;
- important trade-offs;
- rationale needed for future Research/Planning.

#### Known Limitations and Deferred Work

- known non-blocking limitations;
- technical debt relevant to future work;
- explicitly deferred items;
- why they were deferred;
- relevant dependency/constraint.

If none exist, the package must say so explicitly rather than silently omit the section.

#### Next-Version Research Seed

- suggested follow-up topics;
- compatibility watchpoints;
- unresolved opportunities;
- relevant evidence references.

If no follow-up topic is known, the package must explicitly state that no specific next-version seed is currently identified.

### 9.2 Conditional Contents

Include when applicable:

#### Repair / Recovery Lessons

Required when material Repair/Recovery occurred:

- material failures;
- disproven strategies;
- successful correction patterns;
- lessons likely to prevent repeated cost.

#### Compatibility / Migration Findings

Required when the Cycle changed or materially investigated:

- compatibility boundaries;
- migration behavior;
- deprecated behavior;
- rollout/rollback implications.

#### Non-Blocking Evaluation Findings

Required when Evaluation returns `PASS_WITH_FINDINGS` or equivalent:

- finding;
- impact;
- evidence;
- recommended future attention.

#### External Dependency / Tooling Findings

Include when external services, toolchains, providers, or environment constraints materially affected implementation or verification.

### 9.3 Explicit Empty-State Rule

Required sections must not disappear merely because there is nothing to report.

Use an explicit empty state such as:

```text
NONE
[]
Not applicable
```

so future Research can distinguish:

```text
checked and absent
```

from:

```text
forgotten or unavailable
```

### 9.4 Finalization Rule

Deterministic finalization must not establish `CLOSED_VALIDATED` if required Completion Knowledge Package core information is missing, stale against the final repository baseline, or bound to the wrong Scope/Planning authority.

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
Completion Knowledge Package exported/available
    ↓
RUNTIME ENDS
    ↓
(no automatic next-version work)
    ↓
new external user/research action
    ↓
Next-Version External Research
    ↓
new Research Handoff
    ↓
next runtime import
```

Project Template must not automatically spend model/token/tool cost on next-version Research merely because the previous Cycle closed.

## 13. Closure Resume

A fresh session must be able to determine whether closure completed and whether the Completion Knowledge Package is valid without replaying prior chat.

## 14. Core Invariants

```text
Evaluation is independent acceptance.

Evaluation does not repair production.

CLOSED_VALIDATED requires deterministic finalization.

Closure produces next-version knowledge.

Completion knowledge is not next Scope.

Future version begins through a separately initiated new Research + Planning finalization.

Evaluation is independent in authority and evidence posture.

Required closure knowledge exists before CLOSED_VALIDATED.

Next-version Research does not auto-start.
```
