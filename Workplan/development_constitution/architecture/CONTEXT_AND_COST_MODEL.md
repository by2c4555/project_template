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

Because External Research is outside Project Template runtime, deterministic Workplan cannot guarantee enforcement of provider/token spend inside that external conversation.

When the user supplies a Research budget/constraint, Project Template Research prompts/protocols should carry that constraint forward clearly, but must not falsely claim runtime enforcement over an external provider/session.

## 6. Planning Context

Planning should receive:

- current archived Research revision;
- relevant Research;
- relevant current repository evidence;
- material prior knowledge;
- prior Research revision report/carry-forward knowledge when applicable;
- current authority/issue state.

Do not force Planning to reread irrelevant code or repeat sufficient evidence.

When a replacement Research revision is imported after `RESEARCH_REVISION_REQUIRED`, prefer delta reconciliation over full replay.

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

### 9.1 Explicit Budget / Ceiling Enforcement

When the user supplies an explicit:

- token budget;
- monetary budget;
- model-cost ceiling;
- tool/API ceiling;
- bounded cost class,

runtime-controlled dispatch must enforce the approved envelope when cost can be reasonably estimated.

Conceptually:

```text
consumed cost
+
estimated next controlled action
>
approved ceiling

→ DO NOT DISPATCH
→ request budget/CHANGE_APPROVAL or reduce work within authority
```

If exact provider cost is unavailable:

- record cost as unknown/estimated;
- do not fabricate exact usage;
- use conservative bounded estimates when possible;
- if a strict ceiling cannot be safely checked, fail closed/request user action rather than silently exceed it.

If measured/estimated consumption reaches or exceeds a strict ceiling during an active Cycle, runtime must stop **new controlled dispatch** at the next safe boundary. It need not pretend an already-running model/tool call can be retroactively cancelled.

### 9.2 Cost Is Not Correctness Authority

Cost optimization must not weaken required:

- Scope;
- verification;
- gates;
- security/authorization;
- evidence;
- acceptance.

The correct response to insufficient budget is to narrow/re-approve/block, not silently skip correctness requirements.

## 10. Avoid Repeated Expensive Reasoning

Do not repeatedly pay for reasoning already preserved in durable:

- archived Research revisions;
- Research revision reports;
- Planning carry-forward knowledge;
- Research evidence;
- Planning decisions;
- Accepted Scope;
- architecture;
- Task contracts;
- Failure Records;
- checkpoints;
- Completion Knowledge Package.

### 10.1 Research Revision Delta Rule

For a new Research revision following an insufficient predecessor, Planning should normally consume:

```text
new Research revision
+ predecessor Research Revision Required report
+ Planning carry-forward knowledge
+ selective predecessor evidence when materially needed
+ current repository evidence when materially needed
```

Planning should explicitly determine:

- what changed;
- which previous gaps are resolved;
- which prior findings remain valid;
- which findings are stale/superseded;
- what still requires verification.

Do not reload/reason over the complete prior Research/repository context merely because the provider/model changed. Provider/session memory is not a reason to discard durable verified reasoning.

## 11. Verification Cost

Prefer:

1. focused bounded tests;
2. negative-path tests for affected authority;
3. broader regression/release validation when appropriate.

Use mocks/samples/simulation where real external systems are unavailable, but do not replace real verification where real verification is possible.

## 12. Model Capability Floor and Escalation Cost

Use strong external Diagnosis when materially necessary, not merely because a stronger model exists.

A lower-cost model may be used only when it satisfies the capability contract of the assigned role.

Do not silently downgrade:

- Planning;
- material Diagnosis;
- Recovery;
- Independent Evaluation

to a model/runtime mode that cannot reliably satisfy the required reasoning contract merely to save cost.

If the configured capable model is unavailable and no approved equivalent fallback exists:

```text
BLOCK / request owner action / use approved fallback
```

rather than silently reducing decision quality.

## 13. Approval Cost

Do not ask approval for routine work already within an approved envelope.

Approval spam has user and token cost.

## 14. Next-Version Cost Reuse

Completion Knowledge Package reduces future Research cost by preserving verified outcomes, decisions, and lessons.

The same delta-reconciliation principle used for Research revisions may be used by a later separately initiated version to avoid rediscovering unchanged verified facts.

It remains knowledge only; future Research/Scope/Planning authority must still be re-established.

## 15. Core Invariants

```text
selective context

reuse durable reasoning

delta-reconcile Research revisions instead of replaying unchanged context

strong model for material judgment

cheap model for bounded implementation

deterministic software for authority

approval only at meaningful cost/authority boundaries

explicit budgets are enforced before dispatch when applicable

cost never authorizes skipping correctness

role capability floors are not silently downgraded
```
