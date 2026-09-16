# Project Template v4.0.1
## High-Context Controlled Workflow for VS Code Copilot Chat

This template is a strict AI-assisted software-development workflow designed around one lesson:

> Nominal model context is not the same as usable project context.

VS Code Copilot Chat, agent instructions, tools, conversation history, user prompts, project material, and tool output all compete for the same model context. v4 therefore stops trying to support very small executors and instead enforces high-context roles with bounded project context.


## v4.0.1 isolation correction

v4.0.1 changes the runtime architecture: **Task isolation now means physical context isolation.** ProjectManager invokes Planner and Builders as VS Code custom subagents, each of which receives a separate context window.

```text
Main Chat / ProjectManager
  -> Planner512K transaction (fresh context) -> bounded capsule
  -> Builder128K TASK_001 (fresh context) -> bounded capsule
  -> Builder128K TASK_002 (fresh context) -> bounded capsule
  -> Builder256K Integration Gate (fresh context) -> bounded capsule
```

Hard invariant:

> 1 Task = 1 execution contract = 1 isolated subagent invocation = 1 fresh context window.

A Phase may still auto-continue after PASS; only workflow state continues, not the previous model context. Planner is similarly checkpointed into five fresh-context transactions. See `CHANGELOG.md`.

### VS Code requirements for this release

Use a VS Code/Copilot build that supports custom-agent `tools`, `agents`, and subagent invocation. Keep ProjectManager as the user-facing agent. Planner/Builders are internal (`user-invocable: false`).

Provider-specific model names are intentionally not guessed because identifiers vary. Before testing, bind them explicitly:

```bash
python scripts/configure_models.py \
  --planner-model "<MODEL>" --planner-context 524288 \
  --builder128-model "<MODEL>" --builder128-context 131072 \
  --builder256-model "<MODEL>" --builder256-context 262144
```

Use the real documented capacity for each selected model, not merely the minimum shown above. The script rejects undersized bindings and pins `model:` into the role agent frontmatter.

### Preflight

Run:

```bash
python scripts/validate_v4.py
python scripts/context_guard.py EXECUTE/tasks/TASK_NNN.md
```

`context_guard.py` estimates controlled Task payload from the Task contract and its listed WRITE/READ/TEST files without injecting those files into model context. It is conservative and not tokenizer-accurate.

---

## 1. Hard model requirements

### Planner

- Minimum runtime context: **512K tokens**
- Planning/Replanning below 512K is unsupported.
- Preferred controlled project context: <= 250K
- Controlled hard target: <= 300K
- Remaining capacity is reserved for host/system instructions, tools, conversation, reasoning, and output.

If Planner context is unknown:

`PLANNER_CONTEXT_UNKNOWN -> WAITING_USER -> STOP`

If Planner context is below 512K:

`PLANNER_CONTEXT_TOO_SMALL -> WAITING_USER -> STOP`

No override is allowed.

### Builder128K

Default implementation executor.

- Minimum runtime context: **128K**
- Preferred controlled Task context: <= 48K
- Controlled hard target: <= 64K

If runtime context is below 128K:

`EXECUTOR_CONTEXT_TOO_SMALL -> STOP`

### Builder256K

Escalation and integration executor.

- Minimum runtime context: **256K**
- Preferred controlled Task context: <= 96K
- Controlled hard target: <= 128K

Use Builder256K for:
- Tasks that cannot be cleanly decomposed to Builder128K;
- Phase Integration Gates;
- bounded complex debugging;
- escalation from Builder128K.

Builder256K is still a Builder. It does not own architecture.

---

## 2. Core design

The workflow separates responsibilities aggressively:

```text
ProjectManager
    = lightweight routing, Phase authorization, isolated subagent invocation

Planner512K+
    = requirements interpretation, Knowledge, architecture,
      Implementation Plan, Phases, Task compilation, replanning

Builder128K
    = default bounded implementation

Builder256K
    = bounded escalation and integration

Planning Skill
    = reusable planning/replanning algorithm

Builder Skill
    = reusable execution/repair/integrity algorithm

Task
    = exact bounded execution contract + fresh context boundary
```

The most important responsibility rule is:

> Planner thinks globally. Builder executes locally.

A Builder must never be forced to rediscover project architecture from a broad repository scan.

---

## 3. Authority chain

```text
EXECUTE/project_details.md
    User intent and authoritative project requirements

EXECUTE/docs/
    Raw supporting source material

EXECUTE/reference/
    Curated project Knowledge

EXECUTE/plan/IMPLEMENTATION_PLAN.md
    Validated project-wide decisions

EXECUTE/tasks/TASK_NNN.md
    Bounded execution contract

src/ + test/
    Current implementation reality

Task history + Issues
    Execution evidence and contradictions
```

Chat history is never authoritative project memory.

Important information must be persisted to disk.

---

## 4. Workspace layout

```text
workspace/
├─ .env.user                       # local only; created only when needed
├─ .gitignore
├─ README.md
├─ VERSION
│
├─ src/
├─ test/
│  ├─ contract/
│  ├─ unit/
│  ├─ integration/
│  └─ regression/
├─ package/
├─ scripts/
│
├─ .github/
│  ├─ agents/
│  │  ├─ project-manager.agent.md
│  │  ├─ planner512k.agent.md
│  │  ├─ builder128k.agent.md
│  │  └─ builder256k.agent.md
│  └─ skills/
│     ├─ project-planning/
│     │  └─ SKILL.md
│     └─ builder-task-execution/
│        └─ SKILL.md
│
├─ EXECUTE/
│  ├─ .env.execute
│  ├─ PROJECT_CONFIG.md
│  ├─ PROJECT_STATUS.md
│  ├─ project_details.md
│  ├─ docs/
│  ├─ reference/
│  │  └─ KNOWLEDGE_INDEX.md
│  ├─ plan/
│  │  ├─ IMPLEMENTATION_PLAN.md
│  │  └─ revisions/
│  ├─ tasks/
│  │  ├─ TASK_INDEX.md
│  │  ├─ TASK_TEMPLATE.md
│  │  └─ history/
│  └─ issues/
│     ├─ ISSUE_INDEX.md
│     └─ ISSUE_TEMPLATE.md
│
└─ EXECUTE_PROJECT_PROMPT.md
```

`.github/` answers **how AI operates**.

`EXECUTE/` answers **what this project knows, decided, did, and must do next**.

`src/` and `test/` represent implementation reality.

---

## 5. Single entry point

The user starts/resumes with `EXECUTE_PROJECT_PROMPT.md`.

It intentionally contains almost no workflow logic. Its job is only to route to ProjectManager and force state-first behavior.

Do not turn the entry prompt into a second copy of the workflow.

---

## 6. Planning state machine

```text
INITIALIZE
    ↓
INPUT_VALIDATION
    ↓
KNOWLEDGE_REFINEMENT
    ↓
KNOWLEDGE_VALIDATION
    ↓
IMPLEMENTATION_PLANNING
    ↓
PLAN_VALIDATION
    ↓
RISK_DESIGN
    ↓
PHASE_DESIGN
    ↓
TASK_COMPILATION
    ↓
CONTRACT_TEST_DESIGN
    ↓
TASK_PACK_VALIDATION
    ↓
EXECUTION_READY
```

A failed stage blocks downstream stages.

### Hard planning invariants

```text
No sufficient project_details
→ No Knowledge completion.

No sufficient Knowledge
→ No Implementation Plan.

No validated Implementation Plan
→ No executable Tasks.

No validated Task Pack
→ No execution.

Planner below 512K
→ No Planning.
```

---

## 7. Mandatory project input

`EXECUTE/project_details.md` is required.

It should contain enough information to establish:
- project purpose;
- success criteria;
- scope and exclusions;
- critical workflows;
- functional requirements;
- important non-functional requirements;
- runtime/platform;
- database expectations;
- external systems;
- compatibility requirements;
- security constraints;
- packaging/deployment expectations;
- known risks.

It must not contain secrets.

If architecture-critical information is missing, Planner must not guess.

Planner must persist questions and stop.

---

## 8. Persistent questions

When information is missing, Planner may generate:

`EXECUTE/reference/OPEN_QUESTIONS.md`

This file is created only when needed.

Each question should record:
- stable question ID;
- status;
- blocking planning stage;
- exact question;
- why the answer affects architecture;
- where the user should persist the answer.

Important answers must ultimately be written to `project_details.md` or relevant source documents.

The final project truth must not live only in chat.

---

## 9. Knowledge refinement

Inputs:
- `project_details.md`;
- relevant raw files in `EXECUTE/docs/`;
- verified repository evidence when the project already exists.

Planner separates requirements from factual claims, normalizes terminology, and records provenance.

Recommended Knowledge statuses:

```text
USER_STATED
VERIFIED
INFERRED
UNKNOWN
DISPUTED
SUPERSEDED
```

Architecture-critical `UNKNOWN` or `DISPUTED` facts block Planning unless they can be safely resolved.

Do not create dozens of empty Knowledge files. Create only files that are useful for the current project.

Builders have read-only Knowledge access. Durable discoveries are first recorded in history or an Issue, then promoted by Planner if verified.

---

## 10. Implementation Plan

`EXECUTE/plan/IMPLEMENTATION_PLAN.md` is the authoritative current project decision document after it is validated.

It should define durable project-wide decisions such as:
- architecture;
- component responsibilities;
- contracts;
- schemas/data models;
- data/control flow;
- state lifecycle;
- error semantics;
- database strategy;
- external integration;
- security;
- performance;
- compatibility;
- runtime/deployment;
- test strategy;
- integration strategy;
- packaging/install;
- release criteria;
- critical assumptions and risk proofs.

The Plan must not become an execution diary.

---

## 11. Risk-first planning

Before producing the final Task graph, Planner asks:

> Which assumption, if wrong, invalidates the largest amount of downstream work?

Critical feasibility work should happen early.

Typical ordering:

```text
Foundation
→ Critical Risk Proof
→ Minimal Vertical Slice
→ Integration Gate
→ Feature Expansion
→ Integration Gate
→ ...
→ Release Chain
```

Do not postpone the first realistic integration test until project end.

---

## 12. Phase model

A Phase is the user authorization boundary.

A Task is the AI execution boundary.

```text
Phase
├─ Task
├─ Task
├─ Task
└─ Integration Gate
```

A typical Phase should contain approximately 3–8 bounded Tasks plus one Gate, but actual boundaries are determined by coherent milestones, not a fixed count.

The user approves one Phase at a time.

After approval, Tasks continue automatically while every Task returns `PASS`.

---

## 13. Phase execution contract

```text
User approves Phase
        ↓
phase_authorized = true
        ↓
TASK_001
        ↓ PASS
TASK_002
        ↓ PASS
TASK_003
        ↓ PASS
PHASE_GATE
        ↓ PASS
phase_authorized = false
        ↓
ask user before next Phase
```

Only `PASS` may auto-continue.

The following stop the Phase:

```text
PARTIAL
BLOCKED
WAITING_USER
EXECUTOR_CONTEXT_UNKNOWN
EXECUTOR_CONTEXT_TOO_SMALL
EXECUTION_UNSTABLE
KNOWLEDGE_REVIEW_REQUIRED
REPLAN_REQUIRED
EXTERNAL_ACTION_REQUIRED
```

On stop:

`phase_authorized = false`

---

## 14. Task compilation

Planner is an execution compiler, not only an architect.

```text
Validated Architecture
    ↓
Phase Graph
    ↓
Task Graph
    ↓
Bounded Execution Capsules
```

Default target is Builder128K.

For each Task:

```text
Can this safely fit Builder128K?
    YES → Builder128K

    NO
     ↓
Can it be cleanly split?
    YES → SPLIT

    NO → Builder256K
```

Do not use Builder256K merely to avoid clean decomposition.

A Task should represent one coherent independently verifiable behavior.

---

## 15. Task context design

Prefer exact context:

```text
WRITE:
src/auth/service.py
- AuthService.authenticate()

READ:
src/auth/models.py
- User
- AuthResult

TEST:
test/unit/auth/test_service.py
```

Avoid broad context such as:

```text
Read src/
Read all docs/
Read entire Knowledge Base
```

Planner should embed execution-critical facts directly into the Task.

Knowledge IDs remain for provenance but should not force routine large-file loading.

---

## 16. Contract tests

Stable specification-derived behavior should be protected by contract tests when practical.

```text
Requirement
→ Contract
→ Contract Test
→ Task
```

Planner owns the contract intent.

Builder may add:
- unit tests;
- integration tests;
- regression tests.

Builder must not weaken a valid contract test merely to obtain PASS.

---

## 17. Builder execution state machine

```text
Read Project Status
    ↓
Read active Task metadata
    ↓
Context Gate
    ↓
Dependency/Phase Gate
    ↓
Environment Gate if needed
    ↓
Load bounded Task context
    ↓
Establish relevant baseline
    ↓
Implement
    ↓
Verify
    ↓
PASS? ── YES → Finalize → return PASS → STOP
    │
    NO
    ↓
Collect evidence
    ↓
Bounded repair
    ↓
Verify
    ↓
still non-PASS
    ↓
Issue
    ↓
BLOCKED
    ↓
STOP
```

Builder never starts the next Task itself. ProjectManager decides Phase continuation.

---

## 18. Repair policy

Default maximum:

**2 meaningful repair attempts**

Each attempt must produce:
- new verified evidence; or
- a materially different corrective change.

Repeating the same failed operation without new evidence is not a repair attempt. It is execution instability.

The workflow intentionally stops early rather than allowing the model to accumulate confusion.

---

## 19. Execution Integrity Guard

Do not ask a model whether it "feels confused".

Detect observable behavior:

```text
REPEATED_EQUIVALENT_ACTION
NO_PROGRESS
SCOPE_DRIFT
REPEATED_REGRESSION
CONTRADICTED_VERIFIED_FACT
EXCESSIVE_CONTEXT_EXPANSION
REPAIR_LIMIT_REACHED
```

First recoverable drift:

```text
stop current approach
→ reread Goal / Facts / Acceptance
→ one bounded reorientation
```

Repeated drift:

```text
EXECUTION_UNSTABLE
→ create/update Issue
→ BLOCK Task
→ revoke Phase authorization
→ STOP
```

---

## 20. Progress invariant

Every meaningful execution loop must produce at least one of:

```text
new verified evidence
or
a state-changing corrective action
or
termination
```

If none occurs, stop.

This is the anti-loop rule underlying repair, external I/O, and debugging.

---

## 21. Regression guard

Before significant change, establish the relevant baseline when practical.

If a Task makes previously passing unrelated verification fail:
- do not build additional work on the regressed state;
- restore only the Task-local safe change when safe;
- preserve unrelated user work;
- record the failed attempt;
- repeated regression becomes `EXECUTION_UNSTABLE`.

Never use destructive repository reset behavior that may discard unrelated user changes.

---

## 22. Environment safety

### `.env.user`

Human-owned local configuration.

May contain:
- API base URLs;
- DB URLs;
- API keys;
- tokens;
- usernames/passwords;
- external service credentials.

Never commit it.

AI may create placeholders only when a Task actually requires them:

```dotenv
API_BASE_URL=__REQUIRED__
API_KEY=__REQUIRED__
```

AI must never invent real values.

Missing required configuration:

`WAITING_USER -> STOP before external access`

### `EXECUTE/.env.execute`

AI/workflow-owned non-secret controls.

Safe to commit.

It must never contain secrets.

Production access and DB writes are denied by default.

---

## 23. External I/O anti-loop

Database discovery should prefer:

```text
schema/metadata
→ aggregate/filter
→ candidate identifiers
→ bounded sample
→ exact rows
```

API discovery should prefer:

```text
metadata/list/filter
→ bounded page or batch
→ candidate IDs
→ exact resources
```

Avoid unbounded pagination, row-by-row enumeration, or N+1 investigation.

Deterministic errors such as 400/401/403 must not be retried unchanged.

Transient failures such as 429/5xx/timeouts may receive bounded retries according to project policy.

---

## 24. Issue model

An Issue is not merely an error note.

It is:

```text
Problem record
+ verified evidence
+ ruled-out approaches
+ safe resume point
+ escalation handoff package
```

Recommended classifications:

```text
LOCAL_REPAIR
EXECUTOR_ESCALATION
KNOWLEDGE_REVIEW_REQUIRED
REPLAN_REQUIRED
EXTERNAL_ACTION_REQUIRED
```

An Issue should remain concise. Do not dump complete tool logs or hidden reasoning.

Never store secrets.

---

## 25. Builder escalation

Default escalation:

```text
Builder128K
    ↓
Issue
    ↓
STOP PHASE
    ↓
User chooses
    ↓
Builder256K
```

Builder256K resumes from:
- active Task;
- Issue;
- safe baseline;
- selected relevant evidence;
- exact files/tests.

It should not replay the entire Builder128K history.

If Builder256K still cannot complete reliably, classify the reason before doing anything else.

Possible outcomes:

```text
TASK_TOO_LARGE
→ Planner splits/recompiles

KNOWLEDGE_REVIEW_REQUIRED
→ Planner reviews Knowledge

REPLAN_REQUIRED
→ Planner revises affected Plan

EXTERNAL_ACTION_REQUIRED
→ WAITING_USER
```

Do not automatically escalate forever.

---

## 26. Replanning

Replanning is continuation, not restart.

Planner loads only affected state:
- current Plan;
- active Issue;
- affected Knowledge;
- selected Task history;
- affected Tasks;
- repository evidence when required.

Preserve:
- completed Tasks;
- valid tests;
- verified Knowledge;
- valid architectural decisions;
- history.

If Knowledge is wrong, correct Knowledge first.

If Plan is affected:
- archive a meaningful prior Plan revision;
- revise only affected sections;
- invalidate affected pending Tasks;
- generate replacement/corrective Tasks;
- validate the affected Task graph;
- resume from the correct Phase point.

---

## 27. Release chain

Project completion requires the configured release chain:

```text
System Test
→ Package
→ Clean Install
→ Release Gate
→ COMPLETE
```

Passing unit tests alone must not mark the project complete when these gates are enabled.

---

## 28. Prompt minimization rules

v4 intentionally keeps instruction ownership narrow:

```text
Agent
= role, context requirement, authority, hard boundaries

Skill
= reusable algorithm

Task
= task-specific execution contract

PROJECT_CONFIG
= static project policy

PROJECT_STATUS
= current workflow routing state
```

Do not copy the same rule into every Agent, Skill, Task, and entry prompt.

Context margin exists to improve reliability, not to justify larger prompts.

---

## 29. Git policy

Track:
- `EXECUTE/**`
- `.github/agents/**`
- `.github/skills/**`

Never track:
- `.env.user`
- `.env.user.*`

Task history, Issues, Knowledge, and Plan revisions are intentional project memory and should normally be committed.

---

## 30. Development rules for future versions

When evolving this template, preserve these architectural invariants unless a future version intentionally changes the major architecture:

1. **State first**  
   Disk state outranks chat history.

2. **High-context floors are hard requirements**  
   Planner >= 512K, Builder >= 128K.

3. **Context floor is not a context target**  
   Keep controlled project/task context well below nominal model capacity.

4. **Planning owns ambiguity**  
   Builders do not fill planning gaps.

5. **Phase is the authorization boundary**  
   Do not reintroduce user confirmation after every successful micro-Task.

6. **Task is the execution isolation boundary**  
   Keep Tasks coherent, bounded, and verifiable.

7. **Non-PASS stops execution**  
   Do not silently continue through errors.

8. **Issues are resume packages**  
   They must support clean escalation without replaying the entire conversation.

9. **No unbounded repair loops**  
   Progress or stop.

10. **No secret leakage**  
    Keep credentials only in `.env.user` or approved external secret systems.

11. **No duplicated prompt architecture**  
    Add a rule only at the layer that owns it.

12. **Replanning is incremental**  
    Preserve verified work.

---

## 31. Anti-patterns

Do not reintroduce:

- Builder32K or Builder64K profiles;
- a giant all-in-one project prompt;
- broad always-on project instructions duplicating Agent/Skill rules;
- full Knowledge loading for ordinary Tasks;
- full Plan loading for ordinary Tasks;
- one Task spanning many unrelated subsystems;
- Builder-driven architecture redesign;
- automatic executor escalation without user visibility;
- retries without new evidence;
- external configuration guessing;
- hidden dependence on old chat messages.

---

## 32. Suggested future enhancements

Future versions may safely add:
- deterministic Task/Issue schema validators;
- context-estimation tooling;
- provider-specific runtime-context detection;
- automatic dependency validation;
- Task-Pack linting;
- contract traceability checks;
- repository-diff guards;
- host-native interactive Phase buttons;
- richer release gates.

Add these as deterministic tooling where possible rather than increasing prompt size.

---

## 33. v4 Constitution

The following rules should be treated as the shortest authoritative summary of the design:

```text
Planner < 512K
→ no Planning.

Builder < 128K
→ no Execution.

Missing or insufficient project details
→ ask User and STOP.

Insufficient Knowledge
→ no Plan.

Unvalidated Plan
→ no Tasks.

Unvalidated Task Pack
→ no Execution.

Builder does not design architecture.

Builder does not repair planning gaps.

Builder does not modify Knowledge or Plan.

PASS
→ may continue inside the authorized Phase.

Any non-PASS
→ stop the Phase.

Two meaningful failed repairs
→ Issue and STOP.

Missing external configuration
→ never guess.

Repeated no-progress behavior
→ Issue and STOP.

Chat history
→ never authoritative state.

Disk state
→ authoritative workflow state.

Planning defects
→ Planner.

Execution defects
→ Builder.

Knowledge/architecture contradictions
→ Planner review.

User approval
→ required at Phase boundaries and explicit escalation/replanning decisions.
```

This README is intentionally detailed because it is the architectural reference for maintaining and evolving v4 without accidentally returning to the prompt/context failure modes that motivated the redesign.


## Provider-qualified model binding

v4.0.1 requires provider-qualified model references for bound Planner/Builder roles so duplicate display names from different providers cannot be silently confused.

Configure model name, provider/vendor, and documented context separately:

```bash
python scripts/configure_models.py \
  --planner-model "Claude Opus 4.7" --planner-provider openrouter --planner-context 1048576 \
  --builder128-model "Qwen3 Coder Next" --builder128-provider openrouter --builder128-context 262144 \
  --builder256-model "Qwen3 Coder Next" --builder256-provider openrouter --builder256-context 262144
```

The script pins references such as:

```text
Claude Opus 4.7 (openrouter)
Qwen3 Coder Next (openrouter)
```

To force the Copilot copy of the same display model instead, use `--planner-provider copilot`, which produces `Claude Opus 4.7 (copilot)`.

Use the actual vendor identifier shown/used by VS Code. Do not infer it from the provider's friendly UI label.

Important limitation: if two same-name models are registered under the same vendor (for example multiple `customendpoint` groups), `Model Name (vendor)` may still be ambiguous. Prefer distinct vendor providers such as `openrouter` versus `copilot`, or verify the runtime-selected model through VS Code diagnostics.
