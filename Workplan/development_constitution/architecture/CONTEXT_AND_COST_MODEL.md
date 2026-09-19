> PROJECT TEMPLATE DEVELOPMENT CONSTITUTION 1.2 — Human owned. AI may read and apply this guidance; modification requires explicit authorization from a trusted repository-owner channel covering the change.

# Context and Cost Model

## 1. Purpose

Defines how Project Template reduces total development cost without weakening correctness, authority, or evidence.

## 2. Core Objective

First satisfy the authorized outcome, correctness requirements, and trust boundaries. Within those constraints, reduce total cost: model/tool spend, elapsed time, avoidable rework, repeated context, and user effort.

Token count alone is not a quality or efficiency measure. Report measured usage separately from estimates; do not invent savings or precise cost when measurement is unavailable.

## 3. Capability Allocation

```text
External Research
    -> broad/deep discovery

Planning
    -> capability sufficient for material semantic decisions
    -> finalization and authority synthesis

Manager
    -> local execution reasoning

Builder
    -> capability sufficient for bounded implementation

Deterministic software
    -> authority and validation
```

## 4. Selective Context

Do not load the whole repository by default.

Context should be task/reasoning specific.

A fresh agent needs the current objective, applicable authority and constraints, relevant baseline, next bounded action, expected evidence, and stop/escalation conditions. Supply these through existing contracts/checkpoints and precise references, not a duplicate document set or complete chat replay.

Expand context to resolve a named uncertainty or dependency. Reuse prior evidence only while its source, baseline, and applicability remain valid.

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
reserved cost of in-flight controlled actions
+
estimated next controlled action
>
approved ceiling

→ DO NOT DISPATCH
→ request budget/CHANGE_APPROVAL or reduce work within authority
```

Concurrent dispatch must share the same budget accounting; independent agents must not each spend the same remaining allowance. Reconcile reservations with observed usage when calls finish, including failed calls and retries. Preserve accounting across resume; keep a conservative reservation for an interrupted call with unknown consumption until reconciled. Planning/reasoning spend controlled by runtime also counts against its applicable budget.

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

After the required checks pass, repeat or broaden them only for changed inputs, a failure, an unresolved risk, or a release requirement. Record unavailable checks and their impact honestly; simulated results do not establish live integration success.

## 12. Model Capability Floor and Escalation Cost

Use strong external Diagnosis when materially necessary, not merely because a stronger model exists.

A lower-cost model may be used only when it satisfies the capability contract of the assigned role.

Role requirements describe needed reasoning, tools, context, and evidence handling, not a provider brand or price tier. A model's name, cost, or self-assessment does not establish capability. Reuse configured, validated role assignments and authorized fallbacks instead of requesting routine provider decisions from the user.

The observable capability and fallback contract is owned by `AGENT_ADAPTER_BOUNDARIES.md`. Context-window size alone does not establish suitability, and loading more context does not repair a missing reasoning/tool capability.

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

capability sufficient for material judgment

least costly suitable execution within the required capability floor

deterministic software for authority

approval only at meaningful cost/authority boundaries

explicit budgets are enforced before dispatch when applicable

cost never authorizes skipping correctness

role capability floors are not silently downgraded
```

Conformance coverage: `C-014`, `C-015`, `C-019`.
