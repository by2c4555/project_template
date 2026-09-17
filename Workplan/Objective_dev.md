# Development Objective — Project Template v5.3.0

## Status

Development constitution for v5.3.0.

This document governs development of the Project Template itself.

It is **not** user-project scope and must never be treated as user Research, Scope, or product requirements.

---

## 1. Core objective

Maximize **engineering quality per token/cost**.

The architecture must intentionally allocate work so that:

- expensive models perform high-value reasoning;
- lower-cost models perform bounded implementation;
- deterministic software controls authority, state, routing, gates, validation, verification, recovery, integrity, and resumability.

Repository state is durable.

Chat history and individual model sessions are disposable.

---

## 2. Development principles

1. Deterministic mechanisms before prompt complexity.
2. Durable state before conversational memory.
3. Bounded contracts before open-ended autonomy.
4. Strong reasoning only where it materially improves quality.
5. Low-cost implementation wherever deterministic contracts make it safe.
6. Executable verification before claimed completion.
7. Immutable execution bindings.
8. Explicit escalation.
9. Resumability across sessions/providers.
10. Simplicity: no agent, prompt, state, file, abstraction, or command without measurable value.

---

## 3. Authority model

Authority is derived from deterministic Workplan state and approved contracts.

Authority is not derived from:

- model capability;
- model confidence;
- chat context;
- prose instruction alone;
- role self-assertion.

The authoritative system must be able to reject an otherwise capable model when state, binding, path, gate, approval, or generation is invalid.

---

## 4. Roles

### External Agent

Use for:

- Research;
- Planning;
- architecture;
- escalated Diagnosis;
- Recovery reasoning;
- Independent Evaluation.

External Agent is not the normal implementation worker.

External Diagnosis and Recovery are reasoning-only.

### Execution Manager

Runs in VS Code/Copilot Chat or equivalent environment.

Responsibilities:

- invoke deterministic Workplan routing;
- supervise Phase/Task execution;
- dispatch exact tickets;
- run/coordinate verification;
- request bounded repair;
- escalate when required;
- report the exact next public command.

The Manager does not own PASS/FAIL authority.

### Builder

Receives one bounded Task/Repair/Recovery Ticket.

Responsibilities:

- implement within authorized paths;
- execute required verification;
- produce structured evidence;
- checkpoint;
- report completion/failure;
- stop.

Builder does not own routing, retry policy, repair budget, or PASS authority.

### Workplan

Workplan owns:

- lifecycle;
- Cycle/Phase/Task/Attempt state;
- immutable bindings;
- dependency routing;
- tickets;
- generations;
- context grants;
- repair limits;
- approvals;
- gates;
- mutation reconciliation;
- integrity;
- resume;
- escalation;
- completion.

---

## 5. Hierarchy

Canonical hierarchy:

`Cycle -> Phase -> Task -> Attempt`

Every Task belongs to exactly one Phase.

A trivial project may deterministically use implicit `PHASE_001`.

User UX must not require manual Phase or Task selection.

---

## 6. Planning contract

Planning must define enough durable structure that routine execution requires minimal reasoning.

Planning Package must include or bind:

- project brief;
- architecture;
- global constraints;
- interfaces;
- data model;
- decisions;
- known risks;
- Phase contracts;
- Task contracts;
- verification expectations.

The package must pass deterministic validation before `PLAN_READY`.

---

## 7. Phase contract

Minimum Phase authority:

- `phase_id`
- objective
- dependencies
- architecture bindings
- interface bindings
- acceptance criteria
- verification
- required evidence

Phase contracts are immutable after Planning approval except through controlled plan revision.

---

## 8. Task contract

Minimum Task authority:

- `task_id`
- `phase_id`
- objective
- dependencies
- authorized production paths
- required context
- architecture bindings
- interface bindings
- acceptance criteria
- verification
- required evidence
- repair budget

Task contracts are immutable after Planning approval except through controlled plan revision.

---

## 9. Planning package integrity

`PLAN_READY` must bind:

- Scope digest;
- Planning Package digest;
- Phase digests;
- Task digests.

Execution must fail closed if a bound contract changes.

---

## 10. Deterministic routing

Workplan selects:

- next Phase;
- next Task;
- Attempt kind;
- ticket;
- continuation.

The user and Manager must not manually reorder authoritative execution.

---

## 11. Ticket authority

Every Builder Attempt requires a durable ticket bound to:

- Cycle;
- Phase;
- Task;
- Attempt;
- generation;
- state identity;
- Scope;
- Planning Package;
- Phase/Task digest;
- authorized paths;
- context grant;
- verification;
- evidence requirements.

---

## 12. Production mutation authority

Builder production mutations must be checked against the complete production-worktree mutation set.

Unauthorized create/modify/delete must fail the Task Gate.

Workplan-owned control-plane updates are separate from Builder production mutations.

Generated/cache/runtime-local paths must not create false production-authority results.

---

## 13. Verification and evidence

Required verification must execute.

Evidence must be structured and bound to:

- Attempt;
- Task;
- Phase;
- generation;
- ticket;
- verification result.

File existence or textual claims are not sufficient proof.

---

## 14. Task Gate

Workplan deterministically decides Task PASS.

Task Gate must verify identity, bindings, ticket, contract digest, verification, evidence, and production mutation authority.

The Manager may orchestrate checks but cannot decide PASS.

---

## 15. Phase Gate

After all Phase Tasks PASS, Workplan must verify required phase-level integration/regression evidence.

Next Phase cannot become eligible until Phase Gate PASS.

The Manager may orchestrate verification but cannot decide gate authority.

---

## 16. Local diagnosis

The Manager may perform bounded first-line diagnosis for ordinary Task-local implementation failures.

This is not permission to change Scope, Plan, architecture, interfaces, Task contract, authorized paths, or repair budget.

---

## 17. Repair budget

Default local repair budget: `2`.

Normal deterministic range: `0..5`.

Repair budget is assigned by Planning/risk policy, not by Manager or Builder discretion.

A repair may escalate before budget exhaustion when failure crosses a structural boundary.

---

## 18. Repair attempts

Every repair requires a fresh Repair Ticket and fresh Builder Attempt.

Repair history must preserve failed evidence and prevent blind repetition of disproven strategies where that information exists.

Repair attempts must pass the normal Task Gate.

---

## 19. Immediate escalation

Escalate without routine retry when the issue involves:

- Scope;
- architecture;
- interfaces;
- data model;
- invalid contracts;
- invalid dependencies;
- unauthorized required paths;
- deep unsupported root cause;
- repeated disproven strategy;
- environment/tooling outside Builder authority;
- verification contract defect;
- material high-risk condition.

---

## 20. External Diagnosis

External Diagnosis is reasoning-only.

It must produce a durable diagnosis containing:

- observed failure;
- evidence;
- affected component;
- root cause;
- violated contract;
- blast radius;
- classification;
- recovery boundary.

Recommended classifications:

`IMPLEMENTATION_DEFECT`, `TASK_DEFECT`, `PLAN_DEFECT`, `SCOPE_DEFECT`, `ENVIRONMENT_DEFECT`, `TOOLING_DEFECT`, `VERIFICATION_DEFECT`, `EXTERNAL_BLOCKER`, `UNKNOWN`.

---

## 21. External Recovery

External Recovery is reasoning-only.

It produces a Recovery Contract.

It must not directly implement production repair.

Recovery Contract binds:

- issue;
- objective;
- affected contracts;
- authorized paths;
- required changes;
- verification;
- regression verification;
- completion criteria.

Implementation occurs through a fresh Builder Attempt.

---

## 22. Recovery flow

Required flow:

`Diagnosis -> Recovery reasoning -> Recovery Contract -> Manager -> Recovery Ticket -> Builder -> Verification -> Task Gate -> Phase Gate`

Recovery cannot directly mark a Task PASS.

---

## 23. Model/provider neutrality

Workflow authority must not depend on named model/provider identities.

Logical roles should be capability-oriented.

Execution Manager may use VS Code/Copilot Chat.

Builder should normally use the lowest-cost model that satisfies the bounded ticket.

Auto model selection may be used where appropriate, but deterministic Workplan authority remains unchanged.

---

## 24. Context grants

Context expansion is read authority only.

A context grant must be durable and record:

- reason;
- paths/resources;
- work/attempt identity;
- generation;
- time;
- `authority_unchanged=true`.

Context expansion must never silently expand write authority.

---

## 25. Research/Scope boundary

User Research artifacts enter through explicit ingest validation.

`Objective_dev.md` must never be included as user product Scope.

Scope remains an immutable accepted product WHAT/WHY snapshot for the active Cycle.

---

## 26. Immutable bindings

Work/Attempt bindings must be persisted at creation.

Resume must compare current repository bindings against persisted originals.

Binding mismatch blocks execution.

Persisted bindings must never be silently recalculated and overwritten.

---

## 27. Generation fencing

Stale agents/sessions must not complete or mutate a newer Attempt.

Generation checks remain mandatory for checkpoint and completion authority.

---

## 28. Durable resume

Resume derives from repository state, tickets, checkpoints, evidence, and immutable bindings.

A new model/provider/session must be able to continue without replaying full chat history.

---

## 29. Semantic checkpoints

Persist verified decisions, evidence, and exact next bounded unit.

Do not persist hidden chain-of-thought.

---

## 30. Exact public commands

Public command authority is exact-token authority.

The runtime must not normalize authoritative input with trimming, case conversion, or free-intent interpretation.

For example, only:

`EXECUTE_PLANNING`

is authoritative.

Lowercase, whitespace-modified, or prose-wrapped variants must be rejected.

---

## 31. Human approval

Human approval remains explicit and deterministic.

Approval must be:

- action-bound;
- subject-bound;
- state-bound;
- time-bound;
- stale-safe;
- single-use.

AI cannot grant its own approval.

---

## 32. Independent Evaluation

Default External Independent Evaluation runs after all required Phase Gates PASS.

Do not pay for external evaluation after every Phase by default.

Risk policy may trigger phase-level external evaluation when justified.

Evaluation is reasoning/review, not production mutation.

---

## 33. Durable knowledge

Verified resolutions may become reusable knowledge.

Knowledge is advisory context, not execution authority.

A prior resolution cannot override current Scope, Plan, ticket, binding, gate, or state.

---

## 34. Root README

Root `README.md` is the primary normal-user guide.

It must explain current implemented behavior for:

- setup;
- required tools;
- VS Code;
- Copilot Chat;
- Execution Manager;
- Builder;
- External Agent;
- full workflow;
- ingest;
- repair/escalation/recovery;
- resume;
- approval;
- public commands;
- advanced documentation locations.

---

## 35. Documentation ownership

- root README: normal user;
- Workplan README: advanced operator;
- Objective_dev: development constitution;
- ENTRY_PROMPT: command/bootstrap interface;
- role files: role behavior;
- runtime/tests: executable authority.

Avoid duplicate sources of truth.

---

## 36. Simplicity constraint

Do not add roles, prompts, state, files, schemas, abstractions, or commands without measurable reliability, cost, auditability, or recovery value.

Prefer deterministic code to longer prompts.

Prefer one authoritative state to duplicated state.

---

## 37. Executable validation

v5.3 must behaviorally validate:

- exact public commands;
- wrong stage/surface;
- immutable bindings;
- generation;
- Phase/Task routing;
- production path authority;
- Task Gate;
- Phase Gate;
- repair/fresh attempts;
- immediate escalation;
- diagnosis/recovery separation;
- resume/reconciliation;
- context grants;
- approvals;
- final evaluation closure;
- release integrity.

String presence is not proof of a runtime invariant.

---

## 38. Full candidate validation

Release validation must execute:

`python Workplan/scripts/validate.py --full`

against the actual candidate tree.

The release report must identify exact revision/candidate and executed suites.

No unexecuted validation may be reported as PASS.

---

## 39. Release manifest

Integrity manifest must be deterministically generated.

It must exclude:

- `__pycache__/`;
- `*.pyc`;
- temp/cache files;
- virtual environments;
- secrets/credentials;
- editor-local artifacts;
- other defined runtime-local files.

A stale manifest must fail validation.

---

## 40. Release consistency

The following must describe one release:

- VERSION;
- Objective;
- root README;
- Workplan README;
- runtime version/schema;
- config;
- prompts;
- agents;
- use cases;
- tests;
- validation;
- migration;
- changelog;
- integrity manifest.

Mixed release labels are a defect.

---

## 41. Compatibility

Compatibility adapters may exist only when they do not create a second authority path.

Legacy model/context labels may be accepted temporarily as aliases, but runtime authority must use the v5.3 role/contract model.

---

## 42. State/schema migration

Material state-shape changes require schema version update and explicit migration documentation.

Do not silently reinterpret in-flight v5.2 execution attempts as v5.3 Attempts unless the equivalence is deterministically proven.

---

## 43. Change governance

A material future change to this constitution requires:

- owner/user agreement;
- runtime impact review;
- test updates;
- documentation updates;
- full validation;
- new development version when behavior materially changes.

---

## 44. Normal flow

```text
Research
  -> Ingest validation
  -> Scope
  -> Planning
  -> validated Planning Package
  -> Phase selection
  -> Task selection
  -> Task Ticket
  -> fresh Builder Attempt
  -> verification/evidence
  -> Task Gate

Task failure
  -> Manager bounded diagnosis
  -> Repair Ticket if authorized
  -> fresh Builder
  -> Task Gate
  -> escalation if unresolved/structural

Escalation
  -> External Diagnosis
  -> External Recovery reasoning
  -> Recovery Contract
  -> Manager
  -> Recovery Ticket
  -> fresh Builder
  -> Task Gate

All Phase Tasks PASS
  -> Phase Gate

All required Phases PASS
  -> External Independent Evaluation
  -> completion report
  -> CLOSED_VALIDATED
```

---

## 45. User-experience invariant

Internal control may become more rigorous, but normal operation must not become more complex for the user.

The user should not need to manually manage:

- Phase IDs;
- Task IDs;
- Attempt IDs;
- generation;
- digests;
- repair counters;
- ticket internals.

`WORKPLAN_NEXT` remains the universal authoritative continuation mechanism.

---

## 46. Direction of travel

v5.3 should move the system toward:

- less model-managed workflow;
- more deterministic workflow;
- less repeated expensive reasoning;
- more durable contracts;
- less broad context;
- more selective context;
- less autonomous repair;
- more evidence-bound repair;
- less prompt authority;
- more executable authority;
- less expensive-model implementation;
- more expensive-model high-value reasoning;
- less claimed completion;
- more proven completion.
