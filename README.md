# Project Template v4.2.0
## Research → Plan → Execute → Recover → Evaluate → Learn → Evolve

Project Template v4.2.0 is a controlled, restartable engineering workflow for projects that use:

- **ChatGPT Project** for product/scope research and future-version evolution;
- **Codex / GPT-6 Astra** as the external technical authority for repository research, planning, diagnosis, recovery, evaluation, and completion handoff;
- **VS Code custom agents** for deterministic local execution;
- optional **external recovery agents** that can temporarily take over the repository when a local Builder is blocked.

The major v4.2.0 change is that a project no longer has only a happy-path Research → Planning → Execution → Evaluation flow. It now has a durable **technical recovery and project-learning loop**.

The core principle is:

> **ChatGPT defines what should exist. Codex owns how it should exist and technical truth. Local agents execute it. Codex/external recovery resolves incidents. Codex independently evaluates the result. Verified lessons are persisted for future planning/execution/evaluation. A full Completion Report returns post-build truth to ChatGPT for the next version.**

Disk artifacts are authoritative. Chat history and agent memory are disposable.

---

# 1. Responsibility model

```text
ChatGPT
= WHAT / WHY / SCOPE / PRODUCT EVOLUTION

Codex
= HOW / REPOSITORY RESEARCH / PLAN / TASK / DIAGNOSIS / RECOVERY / EVALUATION

ProjectManager500K
= EXECUTION CONTROL / STATE / TASK DISPATCH / INCIDENT OPENING / SAFE RESUME

Builder100K
= ONE BOUNDED IMPLEMENTATION TASK

External Recovery Agent
= OPTIONAL TECHNICAL RESOLVER UNDER THE SAME RECOVERY CONTRACT

User
= IMPLEMENTATION APPROVAL / PRODUCT-SCOPE DECISIONS
```

After Codex begins technical preparation, normal runtime/build/test/evaluation problems do **not** go directly back to ChatGPT.

They go first to Codex Diagnosis.

ChatGPT re-enters the lifecycle mainly in two cases:

1. the current version is validated and a full `PROJECT_COMPLETION_REPORT_Vx.md` is used to define a new feature/version scope;
2. Codex Diagnosis proves a real `SCOPE_AMBIGUITY` that requires a user/product decision.

---

# 2. Required tools

| Tool | Required? | Primary use |
|---|---:|---|
| **ChatGPT Project** | Yes | Initial scope Research, next-version Research, true scope clarification |
| **Codex** with the project-designated high-capability model (**GPT-6 Astra** in this template) | Yes | Technical preparation, Planning, Diagnosis, Recovery, Evaluation, Completion Report |
| **Visual Studio Code** | Yes | Local repository/workspace and terminal |
| **VS Code Chat / GitHub Copilot Chat custom-agent support** | Yes for local execution | Runs `ProjectManager500K` and `Builder100K` |
| **Other Models / BYOK provider in VS Code** | Yes when using external/local runtime models | Supplies Manager/Builder models, e.g. OpenRouter or Ollama |
| **Python 3** | Yes | Configuration, validation, approval, context guard, recovery gate |
| **Git** | Strongly recommended | Baselines, diff review, rollback, audit history |

## Provider-specific notes

### OpenRouter

Configure the provider through VS Code's language-model setup. Do not store API keys in this repository or `EXECUTE/MODEL_CONFIG.ini`.

### Ollama

Install Ollama and make the intended model available to VS Code. Record the exact VS Code-visible model identity and documented context size.

### VS Code model identity

Use:

```text
Chat model picker
  -> Manage Language Models
```

or Command Palette:

```text
Chat: Manage Language Models
```

Record:

- provider/API `model_id`;
- `vscode_model_name`;
- `vendor`;
- context size.

The template stores both provider provenance and the VS Code qualified model name.

---

# 3. One-time local runtime setup

This setup is separate from the project lifecycle.

## Setup A — Open the project

Open the repository root in VS Code and confirm:

```text
.github/agents/project-manager.agent.md
.github/agents/builder100k.agent.md
EXECUTE/
scripts/
```

## Setup B — Configure local Manager/Builder models

Edit:

```text
EXECUTE/MODEL_CONFIG.ini
```

Example shape:

```ini
[manager]
model_id = YOUR_MANAGER_MODEL_ID
vscode_model_name = YOUR_MANAGER_VSCODE_MODEL_NAME
vendor = YOUR_MANAGER_VENDOR
context = 512000

[builder]
model_id = YOUR_BUILDER_MODEL_ID
vscode_model_name = YOUR_BUILDER_VSCODE_MODEL_NAME
vendor = YOUR_BUILDER_VENDOR
context = 102400
```

Minimum context floors:

```text
ProjectManager500K : 512000
Builder100K        : 102400
```

Then run:

```bash
python scripts/configure_models.py
python scripts/validate_v4.py
```

A clean template should report:

```text
TEMPLATE_VALID: PASS (v4.2.0)
```

`RUNTIME_READY` remains `NO` until real local model bindings are configured.

---

# 4. Lifecycle at a glance

```text
Step 1  Initial Scope Research
        Tool: ChatGPT Project
             ↓
Step 2  Technical Research + Planning
        Tool: Codex / GPT-6 Astra
        Loop: inspect repo -> ask user -> revise until material_unknowns = 0
             ↓
Step 3  Explicit Implementation Approval
        Tool: User + scripts/approve_plan.py
             ↓
Step 4  Local Execution
        Tool: VS Code ProjectManager500K -> fresh Builder100K per Task
             │
             ├── Task failure beyond bounded local repair
             │        ↓
             │    Issue + hard pause
             │        ↓
             │    Codex / External Recovery
             │        ↓
             │    PASS_RECOVERED + Resolution Knowledge
             │        ↓
             │    READY_TO_RESUME -> Local Manager continues
             │
             └── all Tasks complete
                      ↓
Step 5  Independent Evaluation
        Tool: Codex / GPT-6 Astra
             │
             ├── DIAGNOSIS_REQUIRED
             │       ↓
             │   Codex Diagnosis
             │       ↓
             │   repair / task revision / replan / re-evaluate / scope clarification
             │
             └── PASS / PASS_WITH_FINDINGS
                     ↓
Step 6  Full Project Completion Report
        Tool: Codex
             ↓
Step 7  New Feature / Version Scope
        Tool: ChatGPT Project + User
        Input: latest PROJECT_COMPLETION_REPORT_Vx.md
```

---

# 5. Step 1 — Initial Research V1

**Tool:** ChatGPT Project

Do not use the local Manager/Builder yet.

## 5.1 Configure ChatGPT Project

Copy:

```text
EXECUTE/chatgpt/PROJECT_INSTRUCTIONS.txt
```

into ChatGPT Project Instructions.

Keep available:

```text
EXECUTE/chatgpt/MASTER_RESEARCH_PROMPT.md
```

## 5.2 Start Research

Use:

```text
EXECUTE/chatgpt/START_RESEARCH_PROMPT.md
```

Expected outputs:

```text
EXECUTE/project_details.md
EXECUTE/docs/raw/**
EXECUTE/research/Research_V1.md
```

ChatGPT owns product/scope intelligence, not implementation architecture.

Research should define:

- intended outcome;
- in-scope behavior;
- non-goals;
- user-visible requirements;
- constraints;
- success intent;
- user decisions;
- known/unknown domain facts.

When scope is sufficiently defined for technical investigation, move to Codex.

---

# 6. Step 2 — Codex Technical Research & Planning

**Tool:** Codex / GPT-6 Astra

Use:

```text
EXECUTE/codex/IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md
```

Codex must inspect the real repository. It is not a one-shot text planner.

It owns:

- repository discovery;
- architecture investigation;
- dependency/interface/data analysis;
- compatibility and migration analysis;
- technical user clarification;
- material-unknown loop;
- context compilation;
- plan construction;
- atomic Task compilation;
- prior Resolution knowledge review.

## 6.1 Material unknown loop

While material decisions remain:

```text
planning_status: AWAITING_USER_FEEDBACK
```

Codex asks focused questions, records user decisions, researches again if necessary, and creates internal Planning revisions.

Do not send unresolved architecture/product-changing decisions to local agents.

## 6.2 Recovery knowledge consumption

Before finalizing a plan Codex must inspect:

```text
EXECUTE/knowledge/KNOWLEDGE_INDEX.md
```

and only relevant:

```text
EXECUTE/knowledge/resolutions/RESOLUTION_*.md
```

Verified lessons may become:

- global constraints;
- Task invariants;
- regression requirements;
- known failed approaches to avoid.

## 6.3 Planning output

Codex compiles at least:

```text
EXECUTE/reference/KNOWLEDGE_INDEX.md
EXECUTE/compiled/PROJECT_BRIEF.md
EXECUTE/compiled/ARCHITECTURE.md
EXECUTE/compiled/DECISIONS.md
EXECUTE/compiled/GLOBAL_CONSTRAINTS.md
EXECUTE/compiled/INTERFACES.md
EXECUTE/compiled/DATA_MODEL.md
EXECUTE/compiled/KNOWN_RISKS.md
EXECUTE/plan/IMPLEMENTATION_PLAN.md
EXECUTE/plan/PLANNING_STATUS.md
EXECUTE/tasks/TASK_INDEX.md
EXECUTE/tasks/TASK_NNN.md
EXECUTE/history/planning/**
```

## 6.4 Explicit approval request

When:

```text
material_unknowns: 0
```

Codex sets:

```yaml
planning_status: AWAITING_USER_APPROVAL
implementation_approval_requested: true
execution_locked: true
```

A complete plan is not permission to implement.

---

# 7. Step 3 — Explicit implementation approval

After the user explicitly authorizes implementation, run:

```bash
python scripts/approve_plan.py --planning Planning_V1 --execution Execution_V1
```

This binds exactly one Execution version to the approved Planning version and resets execution/recovery state for that execution cycle.

Expected transition:

```text
Planning_V1
AWAITING_USER_APPROVAL
        ↓ explicit user authorization
APPROVED
        ↓
Execution_V1 = READY
```

---

# 8. Step 4 — Local Execution

**Tool:** VS Code Chat custom agent `ProjectManager500K`

Use:

```text
EXECUTE_PROJECT_PROMPT.md
```

The Manager dispatches one fresh `Builder100K` invocation per Task.

```text
TASK_001 -> Builder100K -> STOP
TASK_002 -> new Builder100K -> STOP
TASK_003 -> new Builder100K -> STOP
```

No chat transcript is the execution state.

## 8.1 Normal Task success

Builder runs Task acceptance criteria and writes:

```text
EXECUTE/execution/evidence/TASK_NNN.md
```

A normal Task becomes:

```text
PASS
```

## 8.2 Bounded local repair

Builder may perform at most the Task-defined local repair budget, default:

```yaml
max_evidence_driven_repair_attempts: 2
```

This is only for bounded repairs inside the approved Task authority.

Builder is not an open-ended project recovery agent.

---

# 9. When a local Builder gets stuck

This is a major v4.2.0 workflow.

If Task verification still fails after bounded local repair:

```text
TASK_017
   ↓
Builder BLOCKED
   ↓
Manager creates ISSUE_0042
   ↓
Local execution pauses
```

The Manager must persist a state equivalent to:

```yaml
execution_status: PAUSED_FOR_EXTERNAL_REPAIR
active_task: TASK_017
active_issue: ISSUE_0042

recovery:
  status: REQUIRED
  owner: CODEX_OR_EXTERNAL_AGENT
  resume_authorized: false
```

The Manager must then STOP.

It must not dispatch `TASK_018`.

---

# 10. Issue artifact: what failed

Created under:

```text
EXECUTE/issues/ISSUE_NNNN.md
```

The Issue is a forensic handoff package. It should contain:

- origin Task/Execution;
- expected behavior;
- observed behavior;
- exact reproduction;
- failure signature;
- evidence pointers;
- relevant files/symbols/tests;
- attempts already made;
- approaches ruled out;
- affected/unaffected scope;
- safe repository baseline;
- recovery control state.

Large raw logs stay in:

```text
EXECUTE/execution/evidence/**
```

The Issue points to them.

The Issue does **not** decide the authoritative root cause.

---

# 11. How to invoke Codex / an External Agent for recovery

Use:

```text
EXECUTE/codex/ISSUE_DIAGNOSIS_AND_RECOVERY_PROMPT.md
```

A short invocation is enough:

```text
Use EXECUTE/codex/ISSUE_DIAGNOSIS_AND_RECOVERY_PROMPT.md
and recover the currently active blocked Issue.
Diagnose and repair the repository until the blocked Task passes
its original acceptance criteria. Persist all required Diagnosis,
Resolution Knowledge, verification, and recovery state artifacts.
Do not authorize Local Manager resume unless recovery verification fully passes.
```

Because disk state stores the active Issue/Task, you do not need to manually reconstruct the incident from chat history.

The same prompt contract may be used by:

- Codex;
- another external coding agent;
- a human-guided technical agent.

The resolver identity is less important than the durable output contract.

---

# 12. Diagnosis: why it failed

Recovery creates:

```text
EXECUTE/diagnostics/Diagnosis_Vx.md
```

and updates:

```text
EXECUTE/diagnostics/DIAGNOSIS_STATUS.md
```

Codex/external recovery classifies exactly one primary root cause:

```text
IMPLEMENTATION_DEFECT
TASK_DEFECT
PLAN_DEFECT
EVALUATION_DEFECT
SCOPE_AMBIGUITY
EXTERNAL_BLOCKER
UNKNOWN
```

## 12.1 IMPLEMENTATION_DEFECT

Approved scope/plan/task intent is sound; implementation is wrong.

Codex/external resolver may repair the repository directly while preserving approved contracts.

## 12.2 TASK_DEFECT

The compiled Task is defective/incomplete, but higher-level technical intent remains sound.

Codex revises/recompiles the affected Task set. Material plan change escalates to `PLAN_DEFECT`.

## 12.3 PLAN_DEFECT

The approved implementation strategy is materially wrong.

Return to:

```text
EXECUTE/codex/IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md
```

Create a new Planning Vx and obtain explicit implementation approval again.

## 12.4 EVALUATION_DEFECT

Used mainly for False Evaluation cases. The evaluator made an invalid/unsupported finding.

Do not modify correct production code just to satisfy the false finding.

## 12.5 SCOPE_AMBIGUITY

Technical investigation proves that a real user/product decision is missing.

Only this class normally returns to ChatGPT/User scope clarification.

## 12.6 EXTERNAL_BLOCKER

Credential, service, permission, external dependency, production action, or other outside condition blocks progress.

## 12.7 UNKNOWN

Not enough evidence for a safe correction. Remain blocked.

---

# 13. External repair authority

The ordinary Builder is intentionally narrow.

The external recovery agent may need to modify broader repository scope if the confirmed root cause crosses components.

That broader authority is allowed only when:

- Diagnosis confirms it is necessary;
- approved product scope remains unchanged;
- approved public/data/security contracts remain intact;
- the expanded change is documented;
- recovery verification covers the impact.

This allows a blocked Task to be repaired correctly without pretending that every cross-component defect fits inside the original Builder WRITE list.

---

# 14. Recovery verification

A repair is not complete because an error disappears.

For a local execution Issue, recovery must verify as applicable:

1. original failure no longer reproduces;
2. every applicable original Task acceptance criterion passes;
3. targeted regression checks pass;
4. affected integration/build/runtime/static checks pass;
5. approved invariants/contracts remain intact.

Allowed recovery result:

```text
RECOVERY_PASS
RECOVERY_FAIL
```

Partial success never unlocks execution.

---

# 15. PASS_RECOVERED

After successful external recovery the original blocked Task becomes:

```yaml
status: PASS_RECOVERED

recovery:
  issue: ISSUE_0042
  diagnosis: Diagnosis_V3
  resolution: RESOLUTION_0042
  resolver: CODEX_OR_EXTERNAL_AGENT
```

`PASS_RECOVERED` is intentionally different from ordinary `PASS`.

It tells final Evaluation:

> This area previously caused a material execution incident. Inspect its Issue/Diagnosis/Resolution and perform targeted regression verification.

---

# 16. Resolution Knowledge: how it was fixed

Every successfully resolved material execution Issue must create:

```text
EXECUTE/knowledge/resolutions/RESOLUTION_NNNN.md
```

The Resolution stores reusable engineering knowledge:

- symptoms;
- confirmed root cause;
- trigger conditions;
- incorrect assumptions;
- correct solution;
- files/components changed;
- verification;
- failed/rejected approaches;
- do-not-repeat/prevention rules;
- regression protection;
- future detection signals;
- applicability/tags;
- confidence.

Then update:

```text
EXECUTE/knowledge/KNOWLEDGE_INDEX.md
```

The durable chain is:

```text
ISSUE_NNNN
= what failed

Diagnosis_Vx
= why it failed / who owns correction

RESOLUTION_NNNN
= how it was correctly fixed and verified

KNOWLEDGE_INDEX
= what future agents should reuse
```

---

# 17. Safe resume after external recovery

Successful recovery must set disk state equivalent to:

```yaml
execution_status: READY_TO_RESUME
active_issue: none
last_resolved_issue: ISSUE_0042

recovery:
  status: VERIFIED
  diagnosis: Diagnosis_V3
  resolution: RESOLUTION_0042
  verification: PASS
  resume_authorized: true
  recovery_baseline: <verified baseline>
  next_task: TASK_018
```

Before Manager continues, run:

```bash
python scripts/recovery_gate.py
```

The gate checks that:

- execution is `READY_TO_RESUME`;
- resume is authorized in disk state;
- resolved Issue exists and is `RESOLVED`;
- original Task is `PASS_RECOVERED`;
- Diagnosis reference exists;
- Resolution reference exists;
- recovery verification passed;
- recovery baseline exists.

If the gate fails, local execution remains stopped.

The Manager must never resume merely because a user/agent says “fixed”.

---

# 18. Execution continues after recovery

Once `recovery_gate.py` passes:

```text
ISSUE_0042 RESOLVED
       ↓
TASK_017 PASS_RECOVERED
       ↓
READY_TO_RESUME
       ↓
ProjectManager500K rereads disk state
       ↓
TASK_018
```

This makes agent restarts safe. The original Builder can disappear completely; the next Manager session can reconstruct state from disk.

---

# 19. Step 5 — Independent Evaluation

When all approved Tasks are `PASS` or `PASS_RECOVERED`, Manager writes:

```text
EXECUTE/execution/EXECUTION_SUMMARY.md
```

and transitions to Evaluation.

Then use Codex with:

```text
EXECUTE/codex/EVALUATION_PROMPT.md
```

Evaluation is independent and read-only with respect to production implementation.

It must inspect:

- approved Research/Plan/Tasks;
- source/tests;
- execution evidence;
- recovered Tasks;
- Issues;
- Diagnoses;
- relevant Resolution knowledge.

Recovered Tasks are mandatory high-attention regression areas.

---

# 20. Evaluation results in v4.2.0

The evaluator chooses exactly one:

```text
PASS
PASS_WITH_FINDINGS
DIAGNOSIS_REQUIRED
```

v4.2.0 intentionally removes the old direct evaluator routing such as:

```text
Evaluation -> ChatGPT Research
```

A blocking finding is not assumed to prove what is wrong.

It first goes to Diagnosis.

---

# 21. Blocking Evaluation finding

Example:

```text
Evaluation_V1
     ↓
EVAL-004 blocking
     ↓
DIAGNOSIS_REQUIRED
     ↓
Codex Diagnosis
```

Run:

```text
EXECUTE/codex/ISSUE_DIAGNOSIS_AND_RECOVERY_PROMPT.md
```

in Evaluation-finding mode.

Diagnosis can determine:

```text
IMPLEMENTATION_DEFECT -> repair -> re-evaluate
TASK_DEFECT           -> task revision/execution -> re-evaluate
PLAN_DEFECT           -> Planning Vx+1 -> user approval -> execution -> re-evaluate
EVALUATION_DEFECT     -> Evaluation Review -> re-evaluate
SCOPE_AMBIGUITY       -> ChatGPT/User clarification -> replan -> execute -> re-evaluate
EXTERNAL_BLOCKER      -> external action
UNKNOWN               -> remain blocked / investigate
```

---

# 22. False Evaluation handling

This is a first-class v4.2.0 case.

Suppose Evaluation says:

```text
FAIL: API must return field X
```

but Diagnosis proves field X was never part of approved scope/Task/contract.

Classification:

```text
EVALUATION_DEFECT
```

Required behavior:

1. preserve the original `Evaluation_V1.md`;
2. create `Evaluation_Review_Vx.md`;
3. identify the invalid finding and authoritative evidence;
4. do not change correct production code;
5. run a new immutable Evaluation version.

This keeps evaluator mistakes separate from implementation defects.

---

# 23. True scope ambiguity during recovery

ChatGPT does not receive raw logs/errors by default.

Codex must first prove that the technical problem cannot be resolved without a product decision.

Then create:

```text
EXECUTE/scope/SCOPE_CLARIFICATION_REQUIRED_Vx.md
```

Example question:

```text
Does offline mode require write operations?

A. Read-only offline
B. Full offline editing
```

Codex includes why the choice changes architecture/behavior.

Then use ChatGPT Project with:

```text
EXECUTE/chatgpt/PROCESS_SCOPE_CLARIFICATION_PROMPT.md
```

ChatGPT/User resolves the product scope, updates Research if necessary, then returns the clarified scope to Codex.

---

# 24. Evaluation PASS requires a Full Completion Report

A passing Evaluation is not finished with a short validation summary.

For:

```text
PASS
PASS_WITH_FINDINGS
```

Codex must create:

```text
EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_Vx.md
```

using:

```text
EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_TEMPLATE.md
```

The Completion Report is the verified **post-implementation truth package**.

It should explain the actual final system in enough detail for future ChatGPT scope research to understand the current baseline without reconstructing implementation from old chat sessions.

Required content includes:

- original scope/goals;
- delivered capabilities;
- actual workflows;
- final architecture;
- repository/implementation map;
- interfaces/contracts;
- data/persistence model;
- dependencies/runtime environment;
- major technical decisions;
- differences from the approved plan;
- material execution/recovery history;
- verification summary;
- known limitations;
- technical debt;
- known risks;
- critical invariants;
- extension points;
- non-blocking findings;
- verified final baseline;
- context needed for future-version research.

Codex transfers facts, not product recommendations.

It should not decide which feature the user should build next.

---

# 25. Step 7 — New feature/version Research

When the user wants the next feature/version, create/continue a ChatGPT Project session and use:

```text
EXECUTE/chatgpt/START_NEXT_VERSION_PROMPT.md
```

Primary baseline input:

```text
latest EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_Vx.md
```

Then add the user's new intent.

ChatGPT should understand:

```text
what already exists
+ how the completed system behaves
+ critical invariants
+ limitations/debt/risks
+ extension boundaries
+ user's new desired scope
```

and create the next `Research_Vx`.

Then Codex performs new technical research/planning.

This closes the evolution loop:

```text
Completion Report V1
       ↓
ChatGPT Research V2
       ↓
Codex Planning V2
       ↓
Execution V2
       ↓
Recovery if needed
       ↓
Evaluation V2
       ↓
Completion Report V2
```

---

# 26. Two kinds of durable project memory

v4.2.0 deliberately separates **execution memory** from **engineering knowledge**.

## Execution memory

Stored mainly in:

```text
EXECUTE/PROJECT_STATUS.md
EXECUTE/execution/EXECUTION_STATE.md
EXECUTE/issues/**
```

Answers:

- where is execution now?
- which Task is blocked?
- which Issue is active?
- who owns recovery?
- may the Manager resume?
- what is the next Task?

## Engineering knowledge

Stored mainly in:

```text
EXECUTE/diagnostics/**
EXECUTE/knowledge/**
```

Answers:

- why did the problem happen?
- what correctly fixed it?
- what approaches failed?
- what should future agents avoid/reuse?
- what regression checks should be preserved?

Do not mix these purposes.

---

# 27. Knowledge base consumption

A knowledge base that is never consumed is just an archive.

v4.2.0 explicitly requires reuse.

## Codex Planning

Before finalizing future plans:

```text
KNOWLEDGE_INDEX
   ↓
identify relevant past resolution
   ↓
read only matching RESOLUTION_NNNN
   ↓
compile guardrail/test/invariant into new plan/tasks
```

## Local Manager

Before dispatching a Task touching a known risk area, surface only relevant verified resolution guidance.

## Codex Evaluation

Recovered Tasks and relevant prior resolutions drive targeted regression checks.

---

# 28. Status routing table

| Current disk state | Owner / next tool | Required action |
|---|---|---|
| Research input required | ChatGPT Project | `START_RESEARCH_PROMPT.md` |
| Planning / technical preparation | Codex | `IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md` |
| Awaiting user feedback | User + Codex | answer/revise inside same Planning Vx |
| Awaiting implementation approval | User | explicitly authorize, then `approve_plan.py` |
| Execution READY / IN_PROGRESS | ProjectManager500K | `EXECUTE_PROJECT_PROMPT.md` |
| Builder blocked | ProjectManager500K | create Issue, persist hard pause, STOP |
| `PAUSED_FOR_EXTERNAL_REPAIR` | Codex / external recovery agent | `ISSUE_DIAGNOSIS_AND_RECOVERY_PROMPT.md` |
| `READY_TO_RESUME` | ProjectManager500K | run `recovery_gate.py`, then resume |
| Execution complete | Codex | `EVALUATION_PROMPT.md` |
| Evaluation `DIAGNOSIS_REQUIRED` | Codex | Diagnosis/Recovery prompt in evaluation mode |
| Diagnosis `PLAN_DEFECT` | Codex | new Planning Vx + new user approval |
| Diagnosis `EVALUATION_DEFECT` | Codex | Evaluation Review + new Evaluation |
| Diagnosis `SCOPE_AMBIGUITY` | ChatGPT/User after Codex handoff | `PROCESS_SCOPE_CLARIFICATION_PROMPT.md` |
| Evaluation PASS/PASS_WITH_FINDINGS | Codex | full Completion Report |
| Validated version + new feature request | ChatGPT Project | `START_NEXT_VERSION_PROMPT.md` |

---

# 29. Key artifacts and their meanings

```text
Research_Vx
= what the product/version should accomplish

Planning_Vx
= how Codex intends to implement that scope

TASK_NNN
= one bounded local implementation contract

Execution Evidence
= what Builder actually did/tested

ISSUE_NNNN
= what failed and where the evidence is

Diagnosis_Vx
= why it failed and which authority owns the correction

RESOLUTION_NNNN
= how it was correctly fixed and verified

Resolution KNOWLEDGE_INDEX
= reusable lessons future agents should consider

Evaluation_Vx
= independent validation findings

Evaluation_Review_Vx
= correction of a false/defective evaluation finding

PROJECT_COMPLETION_REPORT_Vx
= full verified post-implementation system baseline for future scope evolution

SCOPE_CLARIFICATION_REQUIRED_Vx
= rare Codex handoff proving a genuine product decision is missing
```

---

# 30. Directory map

```text
project_template-v4.2.0/
│
├── .github/
│   ├── agents/
│   │   ├── project-manager.agent.md
│   │   └── builder100k.agent.md
│   └── skills/
│       └── builder-task-execution/
│           └── SKILL.md
│
├── EXECUTE/
│   ├── chatgpt/
│   │   ├── PROJECT_INSTRUCTIONS.txt
│   │   ├── MASTER_RESEARCH_PROMPT.md
│   │   ├── START_RESEARCH_PROMPT.md
│   │   ├── START_NEXT_VERSION_PROMPT.md
│   │   └── PROCESS_SCOPE_CLARIFICATION_PROMPT.md
│   │
│   ├── codex/
│   │   ├── IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md
│   │   ├── PLANNING_AND_COMPILATION_PROMPT.md
│   │   ├── ISSUE_DIAGNOSIS_AND_RECOVERY_PROMPT.md
│   │   └── EVALUATION_PROMPT.md
│   │
│   ├── compiled/
│   ├── plan/
│   ├── tasks/
│   │
│   ├── execution/
│   │   ├── EXECUTION_STATE.md
│   │   ├── EXECUTION_SUMMARY.md
│   │   └── evidence/
│   │
│   ├── issues/
│   │   ├── ISSUE_INDEX.md
│   │   └── ISSUE_TEMPLATE.md
│   │
│   ├── diagnostics/
│   │   ├── DIAGNOSIS_STATUS.md
│   │   └── DIAGNOSIS_TEMPLATE.md
│   │
│   ├── knowledge/
│   │   ├── KNOWLEDGE_INDEX.md
│   │   ├── resolutions/
│   │   │   └── RESOLUTION_TEMPLATE.md
│   │   ├── patterns/
│   │   └── decisions/
│   │
│   ├── evaluation/
│   │   ├── EVALUATION_STATUS.md
│   │   ├── EVALUATION_REPORT_TEMPLATE.md
│   │   ├── EVALUATION_REVIEW_TEMPLATE.md
│   │   └── PROJECT_COMPLETION_REPORT_TEMPLATE.md
│   │
│   ├── scope/
│   │   └── SCOPE_CLARIFICATION_REQUIRED_TEMPLATE.md
│   │
│   ├── reference/
│   │   └── KNOWLEDGE_INDEX.md
│   │
│   ├── research/
│   ├── docs/raw/
│   ├── history/
│   │   ├── planning/
│   │   ├── evaluation/
│   │   ├── diagnostics/
│   │   ├── recovery/
│   │   └── completion/
│   │
│   ├── PROJECT_STATUS.md
│   ├── PROJECT_CONFIG.md
│   ├── MODEL_CONFIG.ini
│   └── MODEL_BINDINGS.json
│
├── scripts/
│   ├── configure_models.py
│   ├── validate_v4.py
│   ├── approve_plan.py
│   ├── context_guard.py
│   └── recovery_gate.py
│
├── EXECUTE_PROJECT_PROMPT.md
├── README.md
├── CHANGELOG.md
└── VERSION
```

---

# 31. Why there are two Knowledge Index files

They intentionally represent different knowledge layers.

## `EXECUTE/reference/KNOWLEDGE_INDEX.md`

Codex-prepared knowledge for the current Planning package:

- scope facts;
- repository facts;
- architecture facts;
- user decisions;
- technical constraints.

## `EXECUTE/knowledge/KNOWLEDGE_INDEX.md`

Verified incident/recovery learning:

- known failure patterns;
- root causes;
- proven resolutions;
- do-not-repeat guidance;
- regression protection.

Do not merge them casually. One describes the planned/current system knowledge; the other records validated lessons from real failures.

---

# 32. Core safety/consistency invariants

1. **No approved plan, no local implementation.**
2. **No unresolved material unknowns before approval request.**
3. **One Task = one fresh Builder invocation.**
4. **Builder is bounded; open-ended repair belongs to external Recovery.**
5. **Task failure beyond repair budget creates a durable Issue and pauses execution.**
6. **No future Task while an Issue is active.**
7. **No resume without durable recovery verification.**
8. **Recovered Task remains visibly `PASS_RECOVERED`.**
9. **Every material successful recovery creates Resolution knowledge.**
10. **Technical failures go to Codex Diagnosis before any scope escalation.**
11. **False Evaluation is repaired as evaluation history, not by corrupting correct code.**
12. **Only true scope ambiguity returns to ChatGPT/User.**
13. **Evaluation is independent and read-only.**
14. **Evaluation PASS requires a Full Completion Report.**
15. **Future feature/version Research starts from the verified Completion Report, not old chat memory.**

---

# 33. Migration from v4.1.3

The conceptual changes are material enough that v4.2.0 should be treated as a new workflow version, not a small prompt patch.

Important differences:

```text
v4.1.3
Evaluation/Issue could route directly toward ChatGPT Research

v4.2.0
Issue/Evaluation blocking finding -> Codex Diagnosis first
```

```text
v4.1.3
Local Builder failure could stop without a complete standardized recovery/resume contract

v4.2.0
mandatory Issue -> Diagnosis -> Resolution -> Recovery Verification -> READY_TO_RESUME
```

```text
v4.1.3
PASS primarily produced Evaluation output

v4.2.0
PASS also requires a full post-implementation Project Completion Report for future ChatGPT scope evolution
```

```text
v4.1.3
project knowledge mainly came from Research/Planning

v4.2.0
verified execution failures become a durable reusable Resolution Knowledge Base
```

---

# 34. Recommended operating habit

At any moment, ask only:

```text
What does disk state say is the current lifecycle stage?
Who owns that stage?
Which exact prompt/agent is authorized now?
What artifact must be produced before the next stage unlocks?
```

Do not reconstruct workflow state from memory.

That discipline is what makes v4.2.0 restartable across ChatGPT sessions, Codex sessions, VS Code agent sessions, external recovery agents, and human intervention.
