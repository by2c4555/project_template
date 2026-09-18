> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Context and Cost Model

## 1. Purpose

Defines how Project Template minimizes token/model cost without reducing engineering quality.

## 2. Core Objective

```text
engineering quality / token / cost
```

## 3. Capability Allocation

```text
External Research
    -> broad/deep discovery

Planning
    -> scarce strongest reasoning
    -> finalization and authority synthesis

Manager
    -> local execution reasoning

Builder
    -> lower-cost bounded implementation

Deterministic software
    -> authority and validation
```

## 4. Selective Context

Do not load the whole repository by default.

Context should be task/reasoning specific.

## 5. Research Context

Research may be broad because it occurs outside runtime and should maximize useful preparation.

However the handoff should remain focused and structured.

## 6. Planning Context

Planning should receive:

- relevant Research;
- relevant current repository evidence;
- material prior knowledge;
- current authority/issue state.

Do not force Planning to reread irrelevant code or repeat sufficient evidence.

## 7. Builder Context

Builder context should be the smallest sufficient set:

- Task;
- constraints;
- interfaces;
- required code;
- required docs/evidence.

## 8. Context Expansion

Context expansion is read authority only.

It must not silently expand write authority or Scope.

## 9. Cost-Control Approval

User approvals stop the workflow before expensive downstream work when a material decision could invalidate it.

High-ROI boundaries:

```text
Scope Approval
Execution Approval
Material Change Re-Approval
```

## 10. Avoid Repeated Expensive Reasoning

Do not repeatedly pay for reasoning already preserved in durable:

- Research evidence;
- Planning decisions;
- Accepted Scope;
- architecture;
- Task contracts;
- Failure Records;
- checkpoints;
- Completion Knowledge Package.

## 11. Verification Cost

Prefer:

1. focused bounded tests;
2. negative-path tests for affected authority;
3. broader regression/release validation when appropriate.

Use mocks/samples/simulation where real external systems are unavailable, but do not replace real verification where real verification is possible.

## 12. Escalation Cost

Use strong external Diagnosis when materially necessary, not merely because a stronger model exists.

## 13. Approval Cost

Do not ask approval for routine work already within an approved envelope.

Approval spam has user and token cost.

## 14. Next-Version Cost Reuse

Completion Knowledge Package reduces future Research cost by preserving verified outcomes, decisions, and lessons.

It remains knowledge only; future Scope must still be re-established.

## 15. Core Invariants

```text
selective context

reuse durable reasoning

strong model for material judgment

cheap model for bounded implementation

deterministic software for authority

approval only at meaningful cost/authority boundaries
```
