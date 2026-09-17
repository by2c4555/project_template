# Development Objective — Project Template v5.3.1

## Status

Development constitution for Project Template v5.3.1.

This file governs development of **Project Template itself**. It is not user-project Research, Scope, requirements, architecture, or implementation authority.

v5.3.1 is a hardening release. It preserves schema 6 and the v5.3 lifecycle while tightening:

1. Research quality before Scope/Planning;
2. VS Code Manager/Builder model-cost separation;
3. release/document/tree cleanliness;
4. patch migration and final-acceptance reproducibility.

No new workflow role is introduced.

---

## 1. Core objective

Maximize **engineering quality per token/cost** while keeping workflow authority deterministic, durable, auditable, resumable, and provider-neutral.

Architecture allocation:

```text
strong/paid model   -> high-value reasoning
local/low-cost model-> bounded implementation
deterministic code  -> authority/state/routing/gates/validation/recovery
repository state    -> durable truth
chat/session state  -> disposable context
```

---

## 2. Development principles

1. Deterministic mechanisms before prompt complexity.
2. Durable state before conversational memory.
3. Bounded contracts before open-ended autonomy.
4. Strong reasoning only where it materially improves quality.
5. Lowest-cost capable Builder for routine implementation.
6. Executed verification before claimed completion.
7. Immutable execution bindings.
8. Explicit escalation instead of unbounded retries.
9. Resumability across sessions/providers/machines.
10. Selective context rather than repository-wide context by default.
11. Negative-path validation for every authority boundary.
12. One source of truth per concern.
13. Release cleanliness: no obsolete alias, duplicate prompt/template, cache, or placeholder without measurable value.

---

## 3. Authority model

Authority comes from deterministic Workplan state and accepted contracts.

Authority does **not** come from:

- model capability;
- model price;
- model confidence;
- provider identity;
- chat context;
- prompt role self-assertion;
- a claimed PASS;
- an implementation summary.

The control plane must be able to reject a capable model when lifecycle stage, surface, ticket, generation, binding, authorized path, approval, evidence, or gate is invalid.

---

## 4. Canonical workflow

```text
Research
  -> deterministic ingest validation
  -> immutable Scope
  -> approval-gated Planning
  -> validated Planning Package
  -> deterministic Phase/Task routing
  -> bounded Builder Attempt
  -> verification/evidence
  -> Task Gate
  -> Phase Gate
  -> Independent Evaluation
  -> CLOSED_VALIDATED
```

Failure path:

```text
Task failure
  -> bounded local diagnosis
  -> Repair if permitted
  -> fresh Builder Attempt
  -> gate
  -> escalate if structural/exhausted
  -> External Diagnosis
  -> External Recovery reasoning
  -> Recovery Contract
  -> fresh Recovery Builder Attempt
  -> normal gates
```

---

## 5. Canonical hierarchy

Runtime hierarchy:

```text
Cycle -> Phase -> Task -> Attempt
```

Rules:

- every Task belongs to exactly one Phase;
- a trivial project may deterministically use implicit `PHASE_001`;
- every implementation dispatch creates a fresh Attempt;
- Attempt kind is `INITIAL`, `REPAIR`, or `RECOVERY`;
- normal user UX must not require manual selection of Phase/Task/Attempt/generation/digest/ticket internals.

---

## 6. External Agent role

External reasoning is used for:

- Research;
- Planning/architecture;
- escalated Diagnosis;
- Recovery reasoning;
- Independent Evaluation.

External Agent is not the normal production implementation worker.

External Diagnosis and Recovery are reasoning-only.

External Evaluation is review/acceptance, not repair.

---

## 7. Research role and ingress boundary

Research defines user-project **WHAT/WHY** and acceptance authority before Planning.

Canonical Research files:

```text
Workplan/external_agent/RESEARCH_INSTRUCTION.md
Workplan/external_agent/RESEARCH_POTOCAL_PROMPT.md
Workplan/templates/PROJECT_DETAILS_TEMPLATE.md
```

Canonical handoff:

```text
Workplan/ingest/project_details.md
Workplan/ingest/docs/raw/*
```

New v5.3.1 handoffs must declare:

```text
research_protocol: EXTERNAL_RESEARCH_PROTOCOL_V1
product_scope_unknowns: 0
```

`product_scope_unknowns: 0` is valid only when no unresolved question can materially alter product scope, architecture-driving constraints, acceptance criteria, mandatory interfaces, compatibility, security expectations, or another planning-critical boundary.

Research must preserve source/evidence mapping and distinguish facts, requirements, constraints, assumptions, and remaining non-blocking unknowns.

Research must not create implementation Tasks/Phases or modify production code.

---

## 8. Ingest authority

Research text is not accepted merely because a model says it is ready.

`Workplan/scripts/tools/ingest.py check` must deterministically validate applicable:

- artifact kind/status;
- protocol marker;
- canonical required sections;
- supporting-file list syntax;
- path safety;
- physical package presence;
- file digests;
- package/scope digest.

Only actual `INGEST_VALID: PASS` proves ingest package validity.

Existing already-accepted v5.3.0 ingest may use immutable-digest compatibility revalidation during patch migration. Compatibility must not create a second authority path for new Research.

---

## 9. Scope boundary

Accepted Scope is an immutable product WHAT/WHY snapshot for the active Cycle.

`Workplan/Objective_dev.md` must never be imported as user-project Scope.

Scope authority must remain bound by revision/digest through Planning, Work, resume, gates, Recovery, and Evaluation.

---

## 10. Planning role

Planning performs high-value technical reasoning after valid Scope and required human approval.

Planning owns:

- architecture;
- global constraints;
- interfaces;
- data model;
- decisions;
- known risks;
- Phase decomposition;
- Task decomposition;
- authorized production paths;
- required context;
- acceptance/verification contracts;
- evidence requirements;
- repair budgets.

Planning must define enough durable structure that routine execution does not repeatedly require expensive reasoning.

---

## 11. Planning Package integrity

`PLAN_READY` must bind:

- Scope digest;
- Planning Package digest;
- Phase digests;
- Task digests.

Material changes to bound Planning files after approval invalidate execution authority.

Execution must fail closed rather than silently rebinding to modified contracts.

---

## 12. Phase contract

Minimum Phase authority:

- `phase_id`;
- objective;
- dependencies;
- architecture bindings;
- interface bindings;
- acceptance criteria;
- verification;
- required evidence.

Phase dependencies must be valid and acyclic.

---

## 13. Task contract

Minimum Task authority:

- `task_id`;
- `phase_id`;
- objective;
- dependencies;
- authorized production paths;
- required read context;
- architecture bindings;
- interface bindings;
- acceptance criteria;
- verification;
- required evidence;
- repair budget.

Task contracts are immutable after Planning approval except through controlled revision/recovery mechanisms.

---

## 14. ExecutionManager role

ExecutionManager runs in VS Code/Copilot Chat or equivalent supported environment.

Canonical file:

```text
.github/agents/manager.agent.md
```

Responsibilities:

- invoke deterministic Workplan routing;
- supervise Phase/Task execution;
- execute only returned deterministic actions;
- delegate exact Builder tickets;
- run/coordinate verification as allowed;
- request bounded repair;
- perform bounded Task-local diagnosis where allowed;
- report exact next public command/surface;
- stop on external/human escalation.

ExecutionManager does **not** own PASS/FAIL authority.

---

## 15. Manager model boundary

`manager.agent.md` must not pin a model.

The Manager uses the model selected by the user in the VS Code Chat model picker.

This permits paid/strong reasoning where the user chooses it without hard-coding provider identity into Workplan.

The Manager must not override Builder's model during normal delegation.

---

## 16. Manager capability boundary

Manager must not have the normal production `edit` capability.

Expected tools:

```text
read
search
execute
agent
```

Manager may invoke only `Builder` as a normal subagent.

If production mutation is required, Manager delegates the machine-issued ticket instead of implementing directly.

---

## 17. Builder role

Canonical file:

```text
.github/agents/builder.agent.md
```

Builder receives one bounded Task/Repair/Recovery ticket.

Responsibilities:

- inspect granted context;
- implement within authorized paths;
- execute declared verification;
- produce required structured evidence/checkpoints;
- report completion/failure;
- stop.

Builder does not own routing, retry policy, repair budget, Scope/Plan changes, or PASS authority.

---

## 18. Builder model/cost boundary

Builder is pinned to:

```text
Project Builder Local
```

This is a machine-local VS Code model display alias, typically mapped to a low-cost/local coding model such as Qwen2.5-Coder.

The alias is cost/capability policy only. It grants no Workplan authority.

Normal implementation should use the lowest-cost model that reliably satisfies bounded tickets.

---

## 19. Deterministic routing

Workplan selects:

- lifecycle continuation;
- next Phase;
- next Task;
- Attempt kind;
- ticket;
- repair/recovery authority;
- next surface.

User, Manager, and Builder must not manually reorder authoritative execution.

---

## 20. Ticket authority

Every Builder Attempt requires a durable ticket bound to applicable:

- Cycle;
- Phase;
- Task;
- Attempt;
- Work;
- generation;
- state identity;
- Scope digest;
- Planning Package digest;
- Phase/Task digest;
- Recovery Contract digest;
- authorized paths;
- context grant;
- verification;
- evidence requirements.

Ticket authority is explicit and bounded.

---

## 21. Production mutation authority

Builder production mutations must be reconciled against the complete relevant production-worktree mutation set.

Unauthorized create/modify/delete must fail Task Gate.

Workplan control-plane updates are separate from production mutation authority.

Generated/cache/runtime-local paths must not create false production-authority results.

---

## 22. Verification and evidence

Required verification must execute.

Evidence must be structured and bound to current Attempt/Task/Phase/generation/ticket.

File existence and model prose are not sufficient proof.

Independent Evaluation must recheck acceptance-critical behavior instead of merely trusting prior model claims.

---

## 23. Task Gate

Only deterministic Task Gate marks a Task PASS.

Task Gate validates applicable:

- Task/Phase/Attempt identity;
- generation;
- completed Work;
- current ticket/digest;
- immutable bindings;
- Planning Package integrity;
- evidence identity;
- verification result;
- required artifact/digest evidence;
- mutation manifest;
- production path authority.

Manager may coordinate but cannot decide PASS.

---

## 24. Phase Gate

After all required Phase Tasks PASS, Workplan verifies Phase dependencies and declared integration/regression evidence.

Next dependent Phase cannot become eligible before Phase Gate PASS.

---

## 25. Local diagnosis

Manager may perform bounded first-line diagnosis for ordinary Task-local implementation failures.

This does not authorize changes to:

- Scope;
- Planning Package;
- architecture;
- interfaces;
- Task contract;
- authorized paths;
- repair budget.

---

## 26. Repair budget

Default local repair budget: `2`.

Supported deterministic range: `0..5`.

Repair budget belongs to Planning/risk policy, not Manager/Builder discretion.

A structural failure may escalate before budget exhaustion.

---

## 27. Repair Attempts

Every repair requires:

- fresh Attempt;
- fresh Repair Ticket;
- preserved parent-failure evidence;
- same Task authority unless a controlled higher-level decision changes it;
- normal Task Gate.

Do not blindly repeat disproven repair strategies when durable evidence exists.

---

## 28. Immediate escalation

Escalate without routine retry when failure crosses a structural boundary, including applicable:

- Scope defect;
- architecture/interface/data-model conflict;
- invalid contract/dependency;
- unauthorized required path;
- stale/invalid binding;
- verification contract defect;
- tooling/environment outside Builder authority;
- repeated disproven strategy;
- material high-risk uncertainty.

---

## 29. External Diagnosis

External Diagnosis is reasoning-only.

It should record:

- observed failure;
- evidence;
- affected component;
- root cause;
- violated invariant/contract;
- blast radius;
- classification;
- recovery boundary.

Recommended classifications:

```text
IMPLEMENTATION_DEFECT
TASK_DEFECT
PLAN_DEFECT
SCOPE_DEFECT
ENVIRONMENT_DEFECT
TOOLING_DEFECT
VERIFICATION_DEFECT
EXTERNAL_BLOCKER
UNKNOWN
```

---

## 30. External Recovery

External Recovery is reasoning-only and produces a durable Recovery Contract.

Recovery Contract binds applicable:

- issue;
- objective;
- affected contracts;
- authorized paths;
- required changes;
- verification;
- regression verification;
- completion criteria.

Implementation occurs through a fresh Builder Attempt.

Recovery cannot directly mark a Task PASS.

---

## 31. Recovery flow

Required flow:

```text
Diagnosis
  -> Recovery reasoning
  -> Recovery Contract
  -> Manager
  -> Recovery Ticket
  -> Builder
  -> verification/evidence
  -> Task Gate
  -> Phase Gate
```

---

## 32. Model/provider neutrality

Workflow authority must not depend on named provider/model identities.

Logical roles are capability-oriented.

Model selection affects cost/capability, not authority.

The repository may describe local model aliases required by its VS Code adapter, but a provider-specific identity must never override Workplan state/tickets/gates.

---

## 33. Context grants

Context expansion is read authority only.

A durable grant records:

- reason;
- paths/resources;
- Work/Attempt identity;
- generation;
- time;
- `authority_unchanged=true`.

Context expansion never silently expands write authority.

---

## 34. Immutable bindings

Work/Attempt bindings are persisted at creation.

Resume compares current repository bindings with persisted originals.

Mismatch blocks execution.

Persisted originals must never be silently recalculated and overwritten.

---

## 35. Generation fencing

Stale sessions/agents cannot complete or mutate a newer Attempt generation.

Generation checks remain mandatory for checkpoint and completion authority.

---

## 36. Durable resume

Resume derives from repository state, accepted contracts, tickets, checkpoints, evidence, and immutable bindings.

A new model/provider/session must be able to continue without replaying full chat history.

---

## 37. Semantic checkpoints

Persist verified decisions, outcomes, evidence, and exact next bounded unit.

Do not persist hidden chain-of-thought.

---

## 38. Exact public commands

Public command authority is exact-token authority.

Runtime must not normalize authoritative input with trimming, case conversion, or free-intent interpretation.

Only literal supported tokens are authoritative.

Wrong surface/stage must fail closed.

---

## 39. Human approval

Human approval is:

- action-bound;
- subject-bound;
- state-bound;
- time-bound;
- stale-safe;
- single-use.

AI cannot grant its own approval or execute the human approval command.

---

## 40. Independent Evaluation

Default External Independent Evaluation runs after required Phase Gates PASS.

Do not pay for external evaluation after every Phase by default.

Risk policy may require earlier evaluation where justified.

Evaluation independently verifies current outcomes against approved authority and actual evidence.

Only deterministic finalization may close the Cycle.

---

## 41. Durable knowledge

Verified resolutions may become reusable knowledge.

Knowledge is advisory context, not execution authority.

Prior knowledge cannot override current Scope, Plan, ticket, binding, gate, or state.

---

## 42. Documentation ownership

One source of truth per concern:

- root `README.md` — primary user/operator guide;
- `Workplan/README.md` — advanced control-plane reference;
- `Objective_dev.md` — Project Template development constitution;
- `ENTRY_PROMPT.md` — exact public command/bootstrap interface;
- `CHATGPT_PROJECT_INSTRUCTIONS.md` — compact ChatGPT Project bootstrap;
- `external_agent/RESEARCH_INSTRUCTION.md` — machine-selected Research role;
- `external_agent/RESEARCH_POTOCAL_PROMPT.md` — detailed Research protocol;
- `templates/PROJECT_DETAILS_TEMPLATE.md` — canonical Research output shape;
- other external role files — role-specific behavior;
- runtime/tests — executable authority/evidence;
- `RELEASE_VALIDATION.md` — release procedure + actual acceptance record.

Avoid duplicate prompts/templates that can drift.

---

## 43. Repository/release cleanliness

A release must not carry obsolete compatibility aliases, duplicate protocol files, obsolete input locations, cache artifacts, generated bytecode, editor-local state, secrets, or empty root placeholders with no authority/runtime/documentation purpose.

Runtime directories may remain as explicit Workplan structure when required for predictable repository layout and resume behavior.

User-project production directory structure must be created by actual project Planning/implementation rather than by unrelated template placeholders.

---

## 44. Executable validation

v5.3.1 must behaviorally validate at minimum:

- exact public commands;
- wrong surface/stage;
- Research strict ingress and negative cases;
- Manager/Builder agent model/tool boundary;
- immutable bindings;
- generation fencing;
- Phase/Task routing;
- production mutation authority;
- Task Gate;
- Phase Gate;
- fresh Repair Attempts;
- escalation;
- Diagnosis/Recovery separation;
- resume/reconciliation;
- context grants;
- approvals;
- migration safe boundary;
- final Evaluation closure;
- release integrity.

String presence alone is not proof of a runtime invariant.

---

## 45. Full candidate validation

Release validation must execute against the actual candidate tree:

```bash
python Workplan/scripts/integrity.py generate
python Workplan/scripts/validate.py --full
```

The report must identify baseline/candidate, commands actually run, observed results, known limitations, and package checksum.

No unexecuted validation may be reported as PASS.

---

## 46. Release manifest

Integrity manifest is generated deterministically.

It must exclude defined runtime/local artifacts, including applicable:

- `.git/`;
- `__pycache__/`;
- `*.pyc`/`*.pyo`;
- temp/cache files;
- virtual environments;
- secrets/credentials;
- editor-local artifacts;
- runtime Work/history/approval/ingest payloads;
- ZIP artifacts.

A stale manifest must fail validation.

---

## 47. Release consistency

The following must describe one release:

- `VERSION`;
- root README;
- Workplan README;
- Objective;
- runtime workflow/schema;
- config/model bindings;
- role instructions/protocols;
- agents;
- use cases;
- tests;
- validation;
- migration;
- changelog;
- integrity manifest.

Mixed release labels or stale canonical filenames are defects.

---

## 48. State/schema migration

Material state-shape change requires schema update and explicit migration.

v5.3.1 remains schema 6.

v5.3.0 -> v5.3.1 migration is permitted only at deterministic safe boundaries and must reject active Work where equivalence cannot be proven.

Do not silently reinterpret in-flight earlier execution attempts.

---

## 49. Change governance

A material future change requires:

- owner/user agreement;
- root-cause/architecture impact review;
- token/context/reliability/recovery impact review;
- runtime update where required;
- tests;
- docs/config/version consistency;
- full validation;
- new development version when behavior materially changes.

---

## 50. User-experience invariant

Internal control may become more rigorous, but normal operation must not become more complex for the user.

Users should primarily need:

```text
WORKPLAN_NEXT
EXECUTE_RESEARCH
EXECUTE_PLANNING
EXECUTE_IMPLEMENTATION
```

plus explicit commands only when Workplan routes to Diagnosis/Recovery/Evaluation/reset/approval.

Users should not manually manage internal identifiers or deterministic state machinery.

---

## 51. Direction of travel

Project Template should move toward:

- less model-managed workflow;
- more deterministic workflow;
- less repeated expensive reasoning;
- more local/low-cost bounded implementation;
- less broad context;
- more selective context;
- less prompt authority;
- more executable authority;
- less claimed completion;
- more proven completion;
- fewer duplicate files/roles/aliases;
- cleaner release trees;
- stronger Research input quality;
- safer resumability and migration.
