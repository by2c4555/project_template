# Project Template Development Objective — v5.2.0

This file is the development constitution for **Project Template itself**.

It defines the required architecture, authority boundaries, execution model, reliability rules, user-facing documentation contract, and development constraints for Project Template.

It is **not user-project scope** and must never be treated as Research input for a user project.

All implementation, documentation, configuration, prompts, tests, and future architectural changes must remain consistent with this file unless the owner explicitly approves a change to this constitution.

---

## 1. Core Objective

Project Template exists to maximize:

**engineering quality per token/cost**

The system must achieve this by assigning work to the correct authority:

* **External Agent** performs high-value reasoning.
* **Execution Manager** supervises bounded implementation inside VS Code.
* **Builder** performs bounded production implementation.
* **Deterministic Workplan software** owns workflow authority, state, routing, integrity, retry limits, verification gates, resume, and escalation.

The system must not depend on a model remembering workflow mechanics.

Difficult reasoning should be performed at the highest appropriate level once, converted into durable decisions and bounded contracts, and reused without repeatedly paying for the same reasoning.

Repository state is durable authority.

Chat history, model sessions, provider sessions, process state, and machine-local conversational context are disposable.

---

## 2. Architectural Roles

### 2.1 External Agent

The **External Agent** is the high-reasoning role.

Its responsibilities are limited to work that materially benefits from stronger reasoning:

* Research;
* Planning;
* Architecture;
* escalated Diagnosis;
* Recovery reasoning;
* independent Evaluation.

The External Agent must not perform routine production implementation.

Production code changes must normally return to the VS Code execution path after External Agent reasoning is complete.

The External Agent may inspect repository state, implementation, evidence, tests, and Workplan artifacts only as required by its current deterministic authority.

Provider or model identity does not grant authority.

Authority comes only from current Workplan state and machine-issued tickets.

---

### 2.2 Execution Manager

The **Execution Manager** operates inside:

**VS Code + GitHub Copilot Chat**

It is the supervisory layer for implementation.

Its responsibilities are:

* consume current deterministic execution state;
* execute the current Phase;
* supervise Task dispatch;
* supervise Builder execution;
* perform Task-level verification;
* perform Phase-level verification;
* perform bounded first-line diagnosis;
* request bounded repair execution;
* collect deterministic evidence;
* escalate when local authority or repair limits are exceeded.

The Execution Manager must not:

* arbitrarily select Tasks;
* reorder approved dependencies;
* broaden product Scope;
* redesign approved architecture;
* expand authorized paths without approved authority;
* increase or reset its own repair budget;
* bypass verification;
* bypass required External Agent escalation.

The Execution Manager is a technical supervisor.

It is not workflow authority.

---

### 2.3 Builder

The **Builder** is the bounded production implementation worker.

A Builder executes exactly one machine-issued:

* Task Ticket; or
* Repair Ticket.

Each ordinary Builder execution must be fresh and must not depend on conversational state from a previous Builder execution.

A Builder may:

* read granted context;
* modify authorized paths;
* implement the bounded objective;
* execute required verification;
* persist required checkpoints and evidence;
* report PASS or failure.

A Builder must not:

* choose its own Task;
* expand Task scope;
* redesign architecture;
* modify unauthorized paths;
* change dependencies;
* perform workflow routing;
* autonomously retry failed implementation;
* continue after required verification fails;
* perform broad diagnosis.

When required verification fails, the Builder must stop and return exact failure evidence to the Execution Manager.

Builder behavior is:

```text
execute
→ verify
→ report
```

not:

```text
execute
→ diagnose
→ repeatedly repair
```

---

### 2.4 Deterministic Workplan Software

Deterministic Workplan software is the workflow authority.

It owns:

* lifecycle state;
* Scope bindings;
* Planning bindings;
* Phase selection;
* Task selection;
* dependency routing;
* generation fencing;
* ticket issuance;
* repair counters;
* repair limits;
* approval gates;
* integrity validation;
* reconciliation;
* resume decisions;
* escalation routing;
* completion gates;
* authoritative continuation output.

AI roles must not reconstruct these decisions from conversation.

Any workflow decision that deterministic software can reliably perform must not be delegated to a model.

---

## 3. Execution Hierarchy

Implementation is organized as:

```text
Cycle
  → Phase
      → Task
          → Builder Attempt
```

### Cycle

A Cycle represents one authoritative product Scope and its complete Planning, implementation, recovery, and Evaluation lifecycle.

### Phase

A Phase represents a meaningful implementation or integration milestone.

A Phase contains one or more Tasks and has independent acceptance and verification requirements.

### Task

A Task is the smallest normal implementation contract issued to a Builder.

A Task must be sufficiently bounded for reliable execution without requiring the Builder to redesign the system.

### Builder Attempt

A Builder Attempt is one generation-fenced execution of one Task Ticket or Repair Ticket.

A failed attempt must not silently continue into another attempt.

Every new attempt requires new deterministic authority.

---

## 4. Planning Contract

Planning is performed by the External Agent.

Planning must preserve approved product Scope and convert it into an executable technical structure.

Planning must produce, where applicable:

1. architecture;
2. global constraints;
3. interfaces;
4. data model;
5. significant technical decisions;
6. known risks;
7. ordered implementation Phases;
8. bounded Tasks within each Phase;
9. deterministic verification requirements.

Implementation must be organized as:

```text
PHASE_N
  objective
  prerequisites
  dependencies
  architecture bindings
  phase acceptance criteria
  phase verification

  TASK_N
  TASK_N+1
  ...
```

Every Task must define at minimum:

* Task ID;
* Phase ID;
* objective;
* dependencies;
* authorized paths;
* required context;
* applicable architecture/interface bindings;
* acceptance criteria;
* verification commands or deterministic verification method;
* required evidence.

Tasks become immutable after approval of the Planning package.

Execution must not silently modify an approved Task contract.

Material changes to Scope, architecture, interfaces, Phase structure, Task authority, or dependency structure require deterministic escalation to the appropriate reasoning stage.

Planning must decompose work so routine Builder execution requires minimal independent architectural reasoning.

---

## 5. Phase and Task Routing

The normal user must not manually select:

* Phase IDs;
* Task IDs;
* Builder attempts;
* Work generations;
* internal role prompts.

The Execution Manager must not independently choose these either.

Workplan software determines the next eligible Phase and Task from durable state, dependencies, and verified results.

Only a machine-issued ticket grants execution authority.

---

## 6. Task Execution

For each Task:

```text
Workplan selects eligible Task
        ↓
Task Ticket
        ↓
Execution Manager
        ↓
Fresh Builder
        ↓
Implementation
        ↓
Task verification
   ┌────┴────┐
 PASS       FAIL
   │          │
 evidence    STOP
   │          │
   ▼          ▼
Manager     Manager
Task Gate   Diagnosis
```

A Task reaches PASS only when required deterministic verification and evidence requirements succeed.

A model statement that implementation is complete is not sufficient.

---

## 7. Task Gate

The Execution Manager must verify each Task before Workplan marks it PASS.

The Task Gate must confirm at minimum:

* the Task contract was respected;
* only authorized changes occurred;
* required verification passed;
* required evidence exists;
* relevant bindings remain valid;
* no unresolved Task-local failure remains.

Only after the Task Gate passes may Workplan advance.

---

## 8. Phase Gate

Passing all Tasks individually is not sufficient to complete a Phase.

After all Tasks in a Phase pass, the Execution Manager must perform the Phase Gate.

The Phase Gate verifies:

* Phase acceptance criteria;
* integration between Tasks;
* cross-Task interfaces;
* Phase-level invariants;
* required regression checks;
* required Phase-level behavior.

The next Phase must not start until the current Phase Gate passes.

This prevents individually successful Tasks from hiding integration defects.

---

## 9. First-Line Diagnosis

When Builder verification, Task Gate, or Phase Gate fails, the Execution Manager performs first-line diagnosis.

The Manager determines whether the failure is safely repairable inside existing approved authority.

Manager diagnosis may inspect:

* failure evidence;
* Task contract;
* Phase contract;
* relevant implementation;
* relevant interfaces;
* architecture bindings;
* prior verified repair knowledge.

Manager diagnosis must remain bounded.

It must not broaden Scope or approved architecture.

---

## 10. Manager Repair Budget

The default Manager diagnosis/repair limit is:

```text
5 rounds
```

The repair limit must be stored and enforced by deterministic configuration/state.

The Execution Manager must never increase, reset, or bypass this limit through model reasoning.

Each repair round must:

1. identify an evidence-backed bounded repair;
2. create or request a deterministic Repair Ticket;
3. start a fresh Builder execution;
4. perform required verification;
5. record the result.

A failed repair consumes one repair attempt.

A successful Builder repair does not produce PASS until the relevant Task Gate or Phase Gate succeeds.

Repair history must be durable enough to prevent repetition of an already disproven repair approach.

---

## 11. Immediate Escalation

The Execution Manager must not exhaust all repair rounds when evidence already shows that bounded local authority is insufficient.

Immediate escalation is required when the failure involves:

* product Scope uncertainty;
* incorrect approved architecture;
* incorrect interface contract;
* incorrect data model contract;
* required changes outside authorized paths;
* dependency structure requiring Planning change;
* unresolved root cause requiring deeper reasoning;
* repeated repair strategy already proven ineffective;
* repair risk outside Manager authority.

Workplan must route these cases directly to External Agent Diagnosis.

---

## 12. External Agent Diagnosis

External Agent Diagnosis performs evidence-backed root-cause analysis.

Diagnosis must determine:

* observed failure;
* verified evidence;
* affected component;
* root cause;
* violated contract or invariant;
* blast radius;
* defect classification;
* required recovery boundary.

Diagnosis must distinguish at least where applicable:

* implementation defect;
* Planning defect;
* Scope defect;
* environment/tooling defect;
* verification defect.

Diagnosis must not silently modify production code.

Diagnosis output must be durable and usable by a new session without prior chat history.

---

## 13. Recovery Reasoning

External Agent Recovery determines the minimum complete proven recovery for an evidence-backed defect.

Recovery must define:

* repair objective;
* affected contracts;
* authorized repair scope;
* required implementation changes;
* required verification;
* required regression coverage;
* completion conditions.

External Agent Recovery is a reasoning stage.

Normal production mutation returns to:

```text
External Agent Recovery
        ↓
Deterministic Recovery Contract
        ↓
Execution Manager
        ↓
Builder
        ↓
Verification
```

External Agent reasoning must not become an uncontrolled alternative implementation path.

---

## 14. Model Selection

Role authority and model identity are separate concerns.

### External Agent

Use a model with sufficient reasoning capability for:

* Research;
* Planning;
* Architecture;
* escalated Diagnosis;
* Recovery reasoning;
* independent Evaluation.

The architecture must remain provider-independent.

### Execution Manager

The normal Manager surface is:

**VS Code + GitHub Copilot Chat**

GitHub Copilot **Auto Model Selection** is the preferred default model-selection policy for the Execution Manager when available.

### Builder

Builder execution also occurs through the VS Code/Copilot agent workflow.

Builder work must be bounded sufficiently to allow routine implementation to use lower-cost model capacity when reliable.

The Builder model may change between Tasks or repair attempts.

Changing a model must never change:

* Task authority;
* write authority;
* Phase authority;
* repair budget;
* verification requirements;
* workflow state.

No commercial model name may become workflow authority.

---

## 15. Context Rules

Context must be granted progressively.

Every additional context grant must have a reason.

Additional context grants read access only and must never expand execution authority.

Each role should receive the minimum sufficient context required to perform current bounded work reliably.

Large context windows must not replace:

* Task decomposition;
* durable decisions;
* architecture contracts;
* checkpoints;
* deterministic state.

---

## 16. Research and Scope Boundary

`Workplan/ingest/` is the explicit untrusted Research handoff boundary.

No Planning authority exists until deterministic ingest validation succeeds.

Research package identity and canonical Scope identity must remain separate bindings.

Accepted Research input must be archived durably.

The resulting Scope is authoritative for downstream Planning and execution.

Changing Scope requires an explicit Scope revision.

`Workplan/Objective_dev.md` must never be treated as user-project Research input.

---

## 17. Integrity Bindings

Downstream work must remain bound to the exact authoritative inputs from which it was created.

The system must bind at minimum:

* Research ingest;
* Scope revision/digest;
* approved Planning package;
* Phase;
* Task contract;
* Work generation.

Planning must revalidate bound authoritative inputs:

* at entry;
* at resume;
* before `PLAN_READY`.

Execution must validate the approved Planning package before issuing implementation authority.

Resume must reject incompatible or modified authoritative bindings.

A Work item must never silently rebind itself to modified authoritative state.

---

## 18. Generation Fencing

Every mutating Work execution must use a generation identifier.

When Work is resumed or transferred to another model/session, a new generation is issued.

Older generations become stale.

A stale generation must never:

* mutate authoritative Work;
* checkpoint authoritative Work;
* complete Work;
* alter workflow state.

---

## 19. Resume and Reconciliation

Continuation across:

* model changes;
* provider changes;
* session loss;
* process restart;
* machine transfer;

must not require previous chat history.

Resume must derive the next action from durable repository state.

For mutating roles, Workplan must deterministically reconcile repository state before continuation.

The model must not reconstruct what probably happened.

Completed verified bounded units must not be repeated only because a session disappeared.

---

## 20. Semantic Checkpoints

Long-running reasoning or implementation work must persist semantic checkpoints when useful.

A checkpoint may contain:

* verified facts;
* evidence references;
* decisions;
* rejected approaches with concise reasons;
* unresolved unknowns;
* completed bounded unit;
* exact next bounded unit.

A checkpoint must not contain or require hidden chain-of-thought.

The purpose of checkpoints is to prevent repeated reasoning cost and make model sessions disposable.

---

## 21. Public Command Authority

`Workplan/ENTRY_PROMPT.md` is the single AI bootstrap entrypoint.

Natural-language conversation never grants:

* workflow execution;
* reset authority;
* role selection;
* Phase selection;
* Task selection;
* approval authority.

Mutating or expensive Workplan execution starts only through an exact recognized public command validated by deterministic software.

Public commands are exact protocol tokens.

Case changes, surrounding prose, substituted wording, or unintended whitespace must not silently become valid commands.

AI must never infer:

* INIT;
* RESUME;
* RECONCILE;
* RESET;
* current role;
* current Phase;
* current Task;
* approval requirement;
* next execution surface.

Deterministic Workplan software supplies these decisions.

---

## 22. Human Approval

There is one human approval interface:

```text
Workplan/scripts/approve.py
```

AI must never execute this approval command for the user.

Approval exists only as a token/cost/rework circuit breaker for material operations.

It must not become routine workflow bureaucracy.

Approval authorization must be:

* bound to exact durable state;
* bound to the requested action;
* time-limited;
* single-use;
* rejected when stale, incorrect, or expired.

Routine resume caused only by model, provider, process, session, or machine changes must not require repeated approval.

---

## 23. Independent Evaluation

Independent Evaluation is performed by the External Agent after every approved Phase passes.

Evaluation must verify actual repository behavior.

It must not rely solely on claims from:

* Planning;
* Execution Manager;
* Builder;
* Diagnosis;
* Recovery.

Evaluation must verify approved Scope and completion criteria.

`PASS` or `PASS_WITH_FINDINGS` requires a Completion Report bound to the exact Scope revision and digest.

Only successful deterministic completion may transition the Cycle to:

```text
CLOSED_VALIDATED
```

---

## 24. Knowledge Retention

Evidence-backed failures and successful non-trivial resolutions should become durable reusable knowledge when doing so prevents repeated reasoning cost.

Reusable knowledge should contain concise facts such as:

* failure signature;
* confirmed root cause;
* proven repair;
* verification evidence;
* applicability conditions.

Knowledge must not become another workflow authority database.

Current deterministic Workplan state remains authoritative.

---

## 25. Root README User Contract

The repository root:

```text
README.md
```

is the **primary user-facing entrypoint** for Project Template.

A new user must be able to understand, configure, and begin using the normal Project Template workflow from the root README without first reading internal Workplan implementation files.

The root README must clearly explain:

* what Project Template is;
* what problem it solves;
* required tools and prerequisites;
* installation or setup requirements;
* VS Code requirements;
* GitHub Copilot Chat requirements;
* required agent setup;
* model-selection behavior;
* configurable model settings;
* External Agent requirements;
* the complete normal user workflow;
* which tool/surface is used at each stage;
* how Research begins;
* how Research output enters `Workplan/ingest/`;
* how Planning begins;
* how Planning produces Phases and Tasks;
* how the user transitions to VS Code implementation;
* how Execution Manager and Builder interact;
* how Task failure is handled;
* how Manager diagnosis and bounded repair operate;
* when escalation to External Agent occurs;
* how Recovery returns to VS Code implementation;
* how Evaluation and final completion work;
* how interrupted work is resumed;
* how provider/model/session changes are handled;
* how human approval works when required;
* exact public commands that the normal user needs;
* where advanced/internal documentation is located.

The root README must describe the **actual executable behavior of the current release**.

It must not describe obsolete, intended, or hypothetical workflow behavior as if it were implemented.

Normal users must not need to understand:

* raw `STATE.json`;
* generations;
* internal digests;
* internal Work IDs;
* internal role prompt files;
* internal ticket schemas;
* implementation scripts;

in order to use the normal workflow.

These may be documented separately for maintainers or advanced users.

---

## 26. Documentation Responsibilities

Documentation responsibilities must remain distinct.

### `README.md`

Primary user guide.

Owns:

* prerequisites;
* setup;
* configuration;
* complete user flow;
* tool/surface transitions;
* normal commands;
* failure/recovery UX;
* resume UX.

### `Workplan/README.md`

Detailed Workplan operational and protocol reference.

It may document:

* internal workflow concepts;
* commands in greater detail;
* state transitions;
* advanced operation;
* maintainer/operator behavior.

It must not replace root `README.md` as the normal user entrypoint.

### `Workplan/Objective_dev.md`

Project Template development constitution.

It owns:

* architecture;
* role boundaries;
* invariants;
* development direction;
* release constraints.

It is not a normal user guide.

### `Workplan/ENTRY_PROMPT.md`

Universal AI bootstrap protocol.

It defines how an AI surface enters the deterministic Workplan command protocol.

It is protocol guidance and never workflow authority.

No other document may silently redefine responsibilities owned by these documents.

---

## 27. Simplicity Constraint

New:

* agents;
* prompts;
* state;
* files;
* schemas;
* commands;
* abstractions;

must provide measurable workflow value.

Prefer deterministic software over prompt complexity.

Do not create duplicate sources of truth.

Do not create a new workflow role when an existing role plus deterministic routing is sufficient.

Prompt text may shrink only after equivalent deterministic behavior exists and is tested.

More workflow capability should normally come from better deterministic contracts, routing, state, and verification rather than larger prompts.

---

## 28. Development Requirements

Development of Project Template must begin from the current authoritative repository implementation.

Before changing the architecture or runtime, development must inspect at minimum:

* `Workplan/VERSION`;
* `Workplan/Objective_dev.md`;
* root `README.md`;
* `Workplan/README.md`;
* relevant runtime code;
* relevant configuration;
* relevant tests;
* relevant use cases.

Current executable implementation is the factual baseline.

Historical chat, old uploaded files, and old assumptions must not override current repository state.

Changes must identify:

* the actual problem or root cause;
* affected and dependent files;
* affected invariants;
* authority changes;
* state/recovery implications;
* token/context implications;
* required verification.

Prefer the simplest robust design.

---

## 29. Validation Requirements

Every core invariant that can be deterministically tested should have an executable validation.

Documentation string presence is not proof that runtime behavior satisfies an invariant.

Validation must cover affected contracts, including where applicable:

* command authority;
* wrong-stage rejection;
* wrong-surface rejection;
* immutable bindings;
* generation fencing;
* Phase routing;
* Task routing;
* repair limits;
* immediate escalation;
* Task Gate behavior;
* Phase Gate behavior;
* resume;
* reconciliation;
* approval expiry/staleness;
* completion binding;
* release integrity.

A release must not be considered validated when required full-repository validation has not been executed successfully.

---

## 30. Release Consistency

The following must ship consistently in the same release:

* `Workplan/VERSION`;
* `Workplan/Objective_dev.md`;
* root `README.md`;
* `Workplan/README.md`;
* runtime implementation;
* configuration;
* prompts;
* use cases;
* tests;
* validation;
* migration documentation where required;
* changelog;
* release integrity metadata.

Any release that changes:

* user workflow;
* required tools;
* setup;
* configuration;
* model policy;
* public commands;
* execution surfaces;
* Manager behavior;
* Builder behavior;
* Phase/Task behavior;
* diagnosis;
* recovery;
* resume;
* approval;

must update root `README.md` in that same release.

Generated caches, secrets, credentials, temporary files, editor-local files, and runtime-local artifacts must never be included in release integrity manifests.

---

## 31. Constitution Change Rule

Changing a core invariant in this file requires:

1. explicit owner feedback;
2. same-release runtime changes where applicable;
3. corresponding deterministic validation;
4. required documentation updates;
5. full candidate validation.

Implementation must not silently redefine this constitution.

If current runtime and this constitution disagree, the mismatch is a release defect and must be resolved explicitly.

---

## 32. Required System Flow

The architectural baseline is:

```text
External Agent Research
        ↓
Research Handoff
        ↓
Workplan/ingest/
        ↓
Deterministic Ingest Validation
        ↓
Immutable Scope
        ↓
External Agent Planning + Architecture
        ↓
Ordered Phases
        ↓
Bounded Immutable Tasks
        ↓
PLAN_READY
        ↓
VS Code / GitHub Copilot Chat
        ↓
Execution Manager
        ↓
Deterministic Task Selection
        ↓
Fresh Builder
        ↓
Implementation
        ↓
Task Verification
   ┌────┴────┐
 PASS       FAIL
   │          │
   ▼          ▼
Task Gate   Manager Diagnosis
   │          │
   │      bounded repair
   │      maximum 5 rounds
   │          │
   │       unresolved
   │       or outside
   │       authority
   │          ↓
   │   External Agent Diagnosis
   │          ↓
   │   Recovery Reasoning
   │          ↓
   │   Recovery Contract
   │          ↓
   │   Execution Manager
   │          ↓
   │       Builder
   │          ↓
   └──── Verification
              ↓
      All Phase Tasks PASS
              ↓
           Phase Gate
        ┌─────┴─────┐
       PASS         FAIL
        │            │
    Next Phase    Diagnosis path
        │
        ↓
 All Phases PASS
        ↓
External Agent Independent Evaluation
        ↓
Completion Report
        ↓
CLOSED_VALIDATED
```

This flow is the architectural baseline for Project Template.

Any implementation that materially bypasses this flow is an architectural change and requires explicit owner approval.
