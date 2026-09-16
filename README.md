# Project Template v4.1.1
## Research → Plan → Approve → Execute → Evaluate → Repeat

Project Template v4.1.1 is a controlled engineering workflow that separates **research**, **planning**, **local implementation**, and **independent evaluation**.

If this is your first time using the template, follow **Quick Start** from top to bottom. Do not begin with the architecture sections.

---

# Quick Start

## What you need

- A ChatGPT Project for Research
- Codex with GPT-6 Astra for Planning and Evaluation
- VS Code for the local `ProjectManager500K` and `Builder100K` execution roles
- This repository/workspace

The complete loop is:

```text
1. Research         — ChatGPT Project
2. Planning         — Codex / GPT-6 Astra
3. User Approval    — you
4. Execution        — ProjectManager500K + Builder100K
5. Evaluation       — Codex / GPT-6 Astra
6. Route findings   — correction / replan / new research / finish
```

Do not skip the approval gate. Do not treat local execution completion as project validation.

---

# Step 0 — Prepare the workspace

Open this human-editable file in VS Code or any text editor:

```text
EXECUTE/MODEL_CONFIG.ini
```

Replace only the model/provider values and set each model's real documented context-window capacity:

```ini
[manager]
model = YOUR_MANAGER_MODEL
provider = YOUR_PROVIDER
context = 512000

[builder]
model = YOUR_BUILDER_MODEL
provider = YOUR_PROVIDER
context = 102400
```

The minimum accepted capacities are 512000 tokens for `ProjectManager500K` and 102400 tokens for `Builder100K`. Use the actual documented capacity when it is larger. Do not put API keys or secrets in this file.

Save the file, then run only:

```bash
python scripts/configure_models.py
python scripts/validate_v4.py
```

`configure_models.py` reads `EXECUTE/MODEL_CONFIG.ini`, validates the context floors, writes `EXECUTE/MODEL_BINDINGS.json`, and pins the provider-qualified model names into the VS Code agent files. The old CLI flags remain available as optional overrides for automation/CI, but normal users do not need them.

At this point, do **not** run `EXECUTE_PROJECT_PROMPT.md`. There is no approved plan yet.

---

# Step 1 — Research V1 in ChatGPT Project

## 1.1 Create the ChatGPT Project

Create a ChatGPT Project dedicated to this software project.

Copy the contents of:

```text
EXECUTE/chatgpt/PROJECT_INSTRUCTIONS.txt
```

into the ChatGPT Project Instructions.

Keep this file available in the Project as the research contract:

```text
EXECUTE/chatgpt/MASTER_RESEARCH_PROMPT.md
```

## 1.2 Start the initial research

Use:

```text
EXECUTE/chatgpt/START_RESEARCH_PROMPT.md
```

The Research phase may ask you questions when information required for Planning is missing.

## 1.3 Expected Research outputs

Research V1 must produce/update:

```text
EXECUTE/project_details.md
EXECUTE/docs/raw/00_RESEARCH_INDEX.md
EXECUTE/docs/raw/*.md
EXECUTE/research/Research_V1.md
```

Transfer the generated artifacts back into the repository using the same paths.

### Important

`EXECUTE/docs/raw/**` is the durable evidence layer. **Do not delete or clear it after Planning.** Later Research versions build on prior evidence and provenance.

## Stop condition

Research stops when planning-blocking knowledge gaps are resolved, or explicitly recorded as non-blocking unknowns.

Research does **not** create the Implementation Plan and does **not** start coding.

Next: Planning & Knowledge Compilation.

---

# Step 2 — Planning & Knowledge Compilation V1 in Codex

Open the repository/workspace in Codex using GPT-6 Astra.

Run the instructions in:

```text
EXECUTE/codex/PLANNING_AND_COMPILATION_PROMPT.md
```

Astra reads the Research artifacts, repository state, and relevant evidence, then creates the execution package for the local models.

## Expected Planning outputs

At minimum:

```text
EXECUTE/compiled/PROJECT_BRIEF.md
EXECUTE/compiled/ARCHITECTURE.md
EXECUTE/compiled/DECISIONS.md
EXECUTE/compiled/GLOBAL_CONSTRAINTS.md
EXECUTE/compiled/INTERFACES.md
EXECUTE/compiled/DATA_MODEL.md          # when applicable
EXECUTE/compiled/KNOWN_RISKS.md

EXECUTE/plan/IMPLEMENTATION_PLAN.md
EXECUTE/plan/PLANNING_STATUS.md

EXECUTE/tasks/TASK_INDEX.md
EXECUTE/tasks/TASK_NNN.md

EXECUTE/history/planning/Planning_V1/**
```

Planning must stop with:

```yaml
planning_status: AWAITING_USER_APPROVAL
execution_locked: true
```

Astra cannot approve its own plan.

---

# Step 3 — Review and approve the plan

Before approving, review at least:

```text
EXECUTE/compiled/ARCHITECTURE.md
EXECUTE/compiled/DECISIONS.md
EXECUTE/plan/IMPLEMENTATION_PLAN.md
EXECUTE/tasks/TASK_INDEX.md
```

If the plan is acceptable, approve and bind the exact Planning version to the new Execution version:

```bash
python scripts/approve_plan.py --planning Planning_V1 --execution Execution_V1
```

If approval succeeds, local implementation is unlocked.

If the plan is not acceptable, revise Planning instead of editing approved history silently.

---

# Step 4 — Execute locally in VS Code

Select/use `ProjectManager500K` as the user-facing local execution agent.

Run:

```text
EXECUTE_PROJECT_PROMPT.md
```

The Manager must read `EXECUTE/PROJECT_STATUS.md` first and may execute only the approved Planning version bound to the active Execution version.

The Manager dispatches one bounded Task per fresh `Builder100K` invocation.

Each Builder Task uses the context manifest defined by its Task file. Local models execute approved decisions; they are not responsible for rediscovering the project architecture.

## Expected Execution outputs

Execution state and evidence are recorded under:

```text
EXECUTE/execution/EXECUTION_STATE.md
EXECUTE/execution/EXECUTION_SUMMARY.md
EXECUTE/execution/evidence/**
```

## Stop condition

When all local Tasks pass, the Manager must stop at:

```text
AWAITING_EVALUATION
```

This means **Execution is complete**, not that the project has been independently validated.

Next: Evaluation.

---

# Step 5 — Evaluation V1 in Codex

Open the completed workspace in Codex using GPT-6 Astra.

Run:

```text
EXECUTE/codex/EVALUATION_PROMPT.md
```

Evaluation is independent and read-only with respect to the production implementation and approved planning artifacts. It may inspect code, run tests/build/static analysis, and compare the implementation against the Research and approved Planning package.

## Expected Evaluation outputs

```text
EXECUTE/evaluation/Evaluation_V1.md
EXECUTE/evaluation/RESEARCH_HANDOFF_V1.md     # when research is needed/useful
EXECUTE/history/evaluation/Evaluation_V1/**
```

Evaluation returns exactly one final status:

```text
PASS
PASS_WITH_FINDINGS
CORRECTION_REQUIRED
REPLAN_REQUIRED
RESEARCH_REQUIRED
```

---

# Step 6 — Route the Evaluation result

Use the Evaluation status to choose the next phase:

| Evaluation result | Next action |
|---|---|
| `PASS` | Project can be closed/validated according to your release process. |
| `PASS_WITH_FINDINGS` | Review findings and decide whether follow-up work is required. |
| `CORRECTION_REQUIRED` | Return to local Execution using the existing sound Research/Plan when appropriate. |
| `REPLAN_REQUIRED` | Create a new Planning Vx in Codex from the current Research. |
| `RESEARCH_REQUIRED` | Return to ChatGPT Project and create Research Vx+1. |

Never convert an evaluator finding directly into a permanent requirement without investigation when the issue indicates missing or uncertain knowledge.

---

# Step 7 — Research V2+ after Evaluation or a new issue

## Evaluation-driven Research

When Evaluation requests new research, use:

```text
EXECUTE/chatgpt/PROCESS_EVALUATION_PROMPT.md
```

Provide the relevant Evaluation report and Research handoff to the ChatGPT Project.

Research V2 updates the active project knowledge while preserving the previous Research history.

Typical chain:

```text
Research V1
  → Planning V1
  → Approval
  → Execution V1
  → Evaluation V1 = RESEARCH_REQUIRED
  → Research V2
  → Planning V2
  → Approval
  → Execution V2
  → Evaluation V2
```

## Issue-driven Research

For runtime errors, production issues, user feedback, compatibility changes, or other new observations that may change project knowledge, use:

```text
EXECUTE/chatgpt/PROCESS_ISSUE_PROMPT.md
```

Treat the issue as evidence first. Investigate it before promoting it into authoritative requirements or project knowledge.

---

# Where am I now?

If you open a project and do not remember the next step, read `EXECUTE/PROJECT_STATUS.md` and use this guide:

| Current state | What you do next |
|---|---|
| `RESEARCH` / `INPUT_REQUIRED` | Continue ChatGPT Research using the appropriate prompt in `EXECUTE/chatgpt/`. |
| `AWAITING_USER_APPROVAL` | Review the plan, then run `scripts/approve_plan.py` only if you approve it. |
| `EXECUTION` / `READY` or `IN_PROGRESS` | Run `EXECUTE_PROJECT_PROMPT.md` with `ProjectManager500K` in VS Code. |
| `AWAITING_EVALUATION` or Evaluation `REQUIRED` | Run `EXECUTE/codex/EVALUATION_PROMPT.md` in Codex/Astra. |
| Evaluation = `CORRECTION_REQUIRED` | Return to the authorized local correction path. |
| Evaluation = `REPLAN_REQUIRED` | Create the next Planning Vx in Codex/Astra. |
| Evaluation = `RESEARCH_REQUIRED` | Use `EXECUTE/chatgpt/PROCESS_EVALUATION_PROMPT.md` and create Research Vx+1. |
| Evaluation = `PASS` | Follow your release/closure process and preserve the evaluation history. |

---

# Which prompt do I use?

| Situation | Tool / environment | Prompt |
|---|---|---|
| Starting a new project | ChatGPT Project | `EXECUTE/chatgpt/START_RESEARCH_PROMPT.md` |
| Evaluation says more research is needed | ChatGPT Project | `EXECUTE/chatgpt/PROCESS_EVALUATION_PROMPT.md` |
| New error/issue/feedback may change knowledge | ChatGPT Project | `EXECUTE/chatgpt/PROCESS_ISSUE_PROMPT.md` |
| Research is ready and you need a plan | Codex / GPT-6 Astra | `EXECUTE/codex/PLANNING_AND_COMPILATION_PROMPT.md` |
| Approved plan is ready to implement | VS Code / ProjectManager500K | `EXECUTE_PROJECT_PROMPT.md` |
| Local execution finished | Codex / GPT-6 Astra | `EXECUTE/codex/EVALUATION_PROMPT.md` |

---

# Who owns which files?

| Layer | Primary owner | Purpose |
|---|---|---|
| `EXECUTE/project_details.md` | ChatGPT Research | Concise authoritative project requirements/context |
| `EXECUTE/docs/raw/**` | ChatGPT Research | Raw evidence, facts, provenance, limitations, research details |
| `EXECUTE/research/**` | ChatGPT Research | Immutable Research Vx records and handoff state |
| `EXECUTE/compiled/**` | Astra Planning | Distilled execution knowledge for local no-RAG models |
| `EXECUTE/reference/**` | Planning / controlled knowledge process | Durable indexed project knowledge with provenance where used |
| `EXECUTE/plan/**` | Astra Planning | Implementation plan and Planning state |
| `EXECUTE/tasks/**` | Astra Planning | Atomic self-contained Builder work packages |
| `EXECUTE/execution/**` | Local Manager/Builder | Execution state, summaries, and implementation evidence |
| `EXECUTE/evaluation/**` | Astra Evaluation | Independent Evaluation reports and Research handoffs |
| `EXECUTE/history/**` | Versioning process | Immutable Planning/Evaluation history |
| `EXECUTE/issues/**` | Issue workflow | Structured issue records when used |

---

# The three knowledge layers

The template intentionally keeps information at different abstraction levels.

```text
EXECUTE/docs/raw/**
    ↓
Evidence Layer
Detailed sources, facts, uncertainty, provenance

EXECUTE/reference/**
    ↓
Durable Knowledge Layer
Stable/normalized project knowledge with traceability

EXECUTE/compiled/**
    ↓
Execution Intelligence Layer
Compact Builder/Manager-oriented knowledge and constraints
```

Do not use `compiled/**` as a replacement for the original evidence. Do not delete `docs/raw/**` merely because Planning completed.

---

# Status model

These states are intentionally different:

```text
Task PASS
    ≠
Execution COMPLETE
    ≠
Project VALIDATED
```

Only independent Evaluation can produce the final validation result for an Execution version.

---

# Core architecture

```text
Research Vx — ChatGPT Project
    ↓
Planning & Knowledge Compilation Vx — Codex / GPT-6 Astra
    ↓
USER APPROVAL GATE
    ↓
Execution Vx — local ProjectManager500K + Builder100K
    ↓
Evaluation Vx — Codex / GPT-6 Astra
    ↓
PASS / correction / replan / Research Vx+1
```

The separation exists because local Manager/Builder models may have no RAG. Astra therefore compiles global reasoning into durable disk artifacts before execution.

`context window != project memory`

Disk artifacts are durable project memory. Each local Builder invocation is temporary working context.

---

# Workspace map

```text
EXECUTE/
├─ MODEL_CONFIG.ini                # human-editable Manager/Builder model settings
├─ MODEL_BINDINGS.json            # generated machine-readable bindings
├─ chatgpt/                       # Research prompt pack
│  ├─ PROJECT_INSTRUCTIONS.txt
│  ├─ MASTER_RESEARCH_PROMPT.md
│  ├─ START_RESEARCH_PROMPT.md
│  ├─ PROCESS_EVALUATION_PROMPT.md
│  └─ PROCESS_ISSUE_PROMPT.md
├─ project_details.md
├─ docs/raw/                      # durable research evidence; do not auto-delete
├─ research/                      # Research Vx artifacts / handoffs
├─ reference/                     # durable indexed knowledge where used
├─ codex/
│  ├─ PLANNING_AND_COMPILATION_PROMPT.md
│  └─ EVALUATION_PROMPT.md
├─ compiled/                      # distilled intelligence for local execution
├─ plan/                          # plan + approval state
├─ tasks/                         # atomic Builder tasks
├─ execution/                     # local execution state/evidence
├─ evaluation/                    # independent Evaluation reports
├─ issues/                        # structured issue workflow
└─ history/                       # immutable Planning/Evaluation history
```

---

# Safety rails

- ChatGPT Research does not implement code or create implementation Tasks.
- Astra Planning does not approve its own plan.
- Local Manager/Builder do not change approved architecture or requirements silently.
- Execution completion does not equal independent validation.
- Astra Evaluation does not silently fix production implementation while evaluating it.
- Approved and historical versions are not silently overwritten.
- Raw research evidence is preserved for provenance and future Research versions.

---

# Useful validation commands

Validate the template:

```bash
python scripts/validate_v4.py
```

Check a controlled Builder Task payload:

```bash
python scripts/context_guard.py EXECUTE/tasks/TASK_TEMPLATE.md
```

The context guard estimates only the controlled Task payload. It is not tokenizer-perfect and does not include all host/system/tool overhead.
