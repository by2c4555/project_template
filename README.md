# Project Template v4.1.2
## Research → Plan → Approve → Execute → Evaluate → Repeat

Project Template v4.1.2 is a controlled engineering workflow that separates **research**, **planning**, **local implementation**, and **independent evaluation**.

This README is usage-first. If you are new to the template, follow the setup and workflow sections from top to bottom. The architecture/reference sections are later in the file.

---

# 1. Required tools

Install or prepare these tools before starting the workflow.

| Tool | Required? | Used for |
|---|---:|---|
| **ChatGPT Project** | Yes | Research Vx, requirements clarification, processing evaluation findings/issues into new research |
| **Codex** with the project-designated high-capability model (**GPT-6 Astra** in this template) | Yes | Planning & Knowledge Compilation Vx and independent Evaluation Vx |
| **Visual Studio Code** | Yes | Local repository/workspace, terminal commands, and execution agents |
| **VS Code Chat / GitHub Copilot Chat custom-agent support** | Yes for local agent execution | Runs the workspace custom agents in `.github/agents/` such as `ProjectManager500K` and `Builder100K` |
| **Other Models / BYOK provider in VS Code** | Yes when using external/local runtime models | Supplies the Manager/Builder models; typical choices are **OpenRouter** or **Ollama** |
| **Python 3** | Yes | Runs `configure_models.py`, `validate_v4.py`, `approve_plan.py`, and `context_guard.py` |
| **Git** | Recommended | Version control, review, rollback, and preserving project history |

## Provider-specific requirements

### OpenRouter

You need an OpenRouter API key configured through VS Code's language-model provider setup. Do **not** store the API key in this repository or in `EXECUTE/MODEL_CONFIG.ini`.

### Ollama

You need Ollama installed and the desired local model already available. Current VS Code guidance prefers the official Ollama extension for local Ollama models rather than the deprecated built-in Ollama provider.

### GitHub Copilot account/plan

BYOK models can be used for VS Code chat without a Copilot plan, but some VS Code AI features such as semantic search, inline suggestions, or embeddings can still depend on GitHub Copilot services. The template itself primarily depends on chat/custom-agent execution plus normal file/terminal tools.

---

# 2. Workflow at a glance

Every numbered workflow step below states exactly which tool owns that phase.

```text
Step 1  Research V1
        Tool: ChatGPT Project
             ↓
Step 2  Planning & Knowledge Compilation V1
        Tool: Codex / GPT-6 Astra
             ↓
Step 3  User review + approval
        Tool: Human + terminal/Python
             ↓
Step 4  Local Execution V1
        Tool: VS Code Chat custom agent
              ProjectManager500K → Builder100K
             ↓
Step 5  Independent Evaluation V1
        Tool: Codex / GPT-6 Astra
             ↓
Step 6  Route result
        Tool depends on Evaluation status
             ↓
        PASS / correction / replan / Research V2+
```

A successful local build is **not** the end of the lifecycle. Execution must still go through independent Evaluation.

---


# 3. One-time project setup

This setup is separate from the Research/Planning/Execution lifecycle. Do it once for a new workstation/project checkout.

## Setup A — Extract/open the repository

**Tool:** File system + VS Code

1. Extract or clone this template.
2. Open the repository root in VS Code.
3. Confirm these paths exist:

```text
.github/agents/project-manager.agent.md
.github/agents/builder100k.agent.md
EXECUTE/
scripts/
```

Do not start `EXECUTE_PROJECT_PROMPT.md` yet. There is no approved plan at this point.

## Setup B — Make the Manager and Builder models available in VS Code

**Tool:** VS Code → Chat → Language Models

Open the VS Code language-model manager using either:

```text
Chat model picker
  → Manage Language Models
```

or Command Palette:

```text
Chat: Manage Language Models
```

Add/configure the provider you want to use for the local runtime models, for example OpenRouter or Ollama, and make the intended Manager and Builder models visible in the model picker.

### How to find the real model information

Do not guess model identifiers from a marketing/display name.

In **Manage Language Models**:

1. Find the exact model.
2. Hover the model name or context-size entry.
3. Record the values VS Code reports, especially:
   - **display/model name** used by VS Code;
   - **model ID**;
   - **vendor/provider**;
   - **context size**.

VS Code's model configuration JSON may sometimes show only the provider group, for example:

```json
{
  "name": "OpenRouter",
  "vendor": "openrouter",
  "apiKey": "${input:...}"
}
```

That confirms the provider/vendor, but it is **not** necessarily the per-model identifier. Use the Language Models editor details for the selected model.

### Why the template stores both model ID and VS Code model name

These are different concepts:

```text
model_id
  = provider/API identifier

vscode_model_name
  = model name registered/displayed by VS Code

vendor
  = VS Code provider/vendor identifier

qualified model name
  = "VS Code Model Name (vendor)"
```

The template records `model_id` for provenance, but pins the VS Code custom agent using the qualified VS Code model name.

## Setup C — Configure the local runtime bindings

**Tool:** Text editor + terminal

Open:

```text
EXECUTE/MODEL_CONFIG.ini
```

Fill in the exact values gathered from VS Code.

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

Use the **real documented/VS Code-reported context capacity** when it is larger than the minimum.

Minimum accepted capacities:

```text
ProjectManager500K : 512000 tokens
Builder100K        : 102400 tokens
```

Do not put API keys or secrets in this file.

Then run from the repository root:

```bash
python scripts/configure_models.py
python scripts/validate_v4.py
```

`configure_models.py`:

```text
MODEL_CONFIG.ini
    ↓
validate fields + context floors
    ↓
MODEL_BINDINGS.json
    ↓
pin "VS Code Model Name (vendor)" into .agent.md
```

If validation says `RUNTIME_READY: YES`, local runtime model setup is ready.

---


# Step 1 — Research V1

**Tool:** ChatGPT Project

**Do not use:** VS Code Manager/Builder or Codex Planning yet.

## 1.1 Create a ChatGPT Project

Create a ChatGPT Project dedicated to this software project.

Copy the contents of:

```text
EXECUTE/chatgpt/PROJECT_INSTRUCTIONS.txt
```

into the ChatGPT Project Instructions.

Keep this research contract available in the Project:

```text
EXECUTE/chatgpt/MASTER_RESEARCH_PROMPT.md
```

## 1.2 Start Research V1

Send/use:

```text
EXECUTE/chatgpt/START_RESEARCH_PROMPT.md
```

Research can ask questions when information required for Planning is missing.

## 1.3 Expected outputs

Transfer the generated artifacts back into the repository using these same paths:

```text
EXECUTE/project_details.md
EXECUTE/docs/raw/00_RESEARCH_INDEX.md
EXECUTE/docs/raw/*.md
EXECUTE/research/Research_V1.md
```

### Important: raw research is not temporary

`EXECUTE/docs/raw/**` is the durable evidence layer.

**Do not delete or clear it after Planning.** Later Research versions, Planning versions, and Evaluation investigations may need its evidence/provenance.

## Stop condition

Research stops when planning-blocking knowledge gaps are resolved or explicitly recorded as non-blocking unknowns.

Research does **not** create the Implementation Plan and does **not** start coding.

**Next tool:** Codex / GPT-6 Astra.

---

# Step 2 — Planning & Knowledge Compilation V1

**Tool:** Codex / GPT-6 Astra

**Input:** Repository + Research V1 artifacts

Run the instructions in:

```text
EXECUTE/codex/PLANNING_AND_COMPILATION_PROMPT.md
```

Codex/Astra reads the Research artifacts, repository state, evidence, and project constraints, then creates the execution package for the local no-RAG Manager/Builder runtime.

## Expected outputs

At minimum:

```text
EXECUTE/compiled/PROJECT_BRIEF.md
EXECUTE/compiled/ARCHITECTURE.md
EXECUTE/compiled/DECISIONS.md
EXECUTE/compiled/GLOBAL_CONSTRAINTS.md
EXECUTE/compiled/INTERFACES.md
EXECUTE/compiled/DATA_MODEL.md          # when applicable
EXECUTE/compiled/KNOWN_RISKS.md

EXECUTE/reference/KNOWLEDGE_INDEX.md

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

Codex/Astra cannot approve its own plan.

**Next tool:** Human review + terminal.

---

# Step 3 — Review and approve Planning V1

**Tool:** Human review + terminal/Python

Before approving, review at least:

```text
EXECUTE/compiled/ARCHITECTURE.md
EXECUTE/compiled/DECISIONS.md
EXECUTE/plan/IMPLEMENTATION_PLAN.md
EXECUTE/tasks/TASK_INDEX.md
```

If the plan is acceptable, bind the exact Planning version to the new Execution version:

```bash
python scripts/approve_plan.py --planning Planning_V1 --execution Execution_V1
```

If approval succeeds, local implementation is unlocked.

If the plan is not acceptable, return it to Planning instead of silently editing approved history.

Before starting Execution, you may run:

```bash
python scripts/validate_v4.py
```

Confirm the local model bindings are ready.

**Next tool:** VS Code Chat / `ProjectManager500K` custom agent.

---

# Step 4 — Local Execution V1

**Tool:** VS Code Chat custom-agent runtime

**User-facing agent:** `ProjectManager500K`

**Subagent:** `Builder100K`

The workspace custom agents are stored in:

```text
.github/agents/project-manager.agent.md
.github/agents/builder100k.agent.md
```

VS Code detects workspace custom-agent files in `.github/agents/`.

## 4.1 Select the Manager agent

Open VS Code Chat and select:

```text
ProjectManager500K
```

The Manager should already be pinned to the configured qualified runtime model by `configure_models.py`.

## 4.2 Start the approved execution

Run/use:

```text
EXECUTE_PROJECT_PROMPT.md
```

The Manager must read `EXECUTE/PROJECT_STATUS.md` first and may execute only the approved Planning version bound to the active Execution version.

The Manager dispatches one bounded Task per fresh `Builder100K` invocation.

```text
ProjectManager500K
      ↓
TASK_001 → fresh Builder100K
      ↓
TASK_002 → fresh Builder100K
      ↓
...
```

Local models execute approved decisions. They are not responsible for rediscovering or redesigning the global architecture.

## Expected outputs

```text
EXECUTE/execution/EXECUTION_STATE.md
EXECUTE/execution/EXECUTION_SUMMARY.md
EXECUTE/execution/evidence/**
```

## Stop condition

When all approved Tasks and integration verification pass, the Manager must stop at:

```text
AWAITING_EVALUATION
```

This means **Execution is complete**, not that the project is validated.

**Next tool:** Codex / GPT-6 Astra.

---

# Step 5 — Independent Evaluation V1

**Tool:** Codex / GPT-6 Astra

Open the completed workspace in Codex and run:

```text
EXECUTE/codex/EVALUATION_PROMPT.md
```

Evaluation is independent and read-only with respect to the production implementation and approved planning artifacts. It may inspect code, run tests/build/static analysis, and compare the implementation against Research and the approved Planning package.

## Expected outputs

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

**Next tool:** determined by the Evaluation result.

---

# Step 6 — Route the Evaluation result

Use this table instead of guessing the next tool.

| Evaluation result | Next tool | Action |
|---|---|---|
| `PASS` | Human/release process | Close or release according to your release process; preserve Evaluation history. |
| `PASS_WITH_FINDINGS` | Human/release process | Review findings and decide whether a follow-up lifecycle is required. |
| `CORRECTION_REQUIRED` | VS Code Manager/Builder | Return to the authorized local correction path using the existing sound Research/Plan when permitted by the evaluator. |
| `REPLAN_REQUIRED` | Codex / GPT-6 Astra | Create Planning Vx+1 from the current authoritative Research/evidence. |
| `RESEARCH_REQUIRED` | ChatGPT Project | Create Research Vx+1 using the evaluator handoff/findings. |

Never convert an evaluator finding directly into a permanent requirement when the finding indicates missing/uncertain knowledge. Investigate first.

---

# Step 7 — Research V2+ after Evaluation or a new issue

## Evaluation-driven Research

**Tool:** ChatGPT Project

When Evaluation requests new research, use:

```text
EXECUTE/chatgpt/PROCESS_EVALUATION_PROMPT.md
```

Provide the relevant Evaluation report and Research handoff to the ChatGPT Project.

Research V2 updates active project knowledge while preserving prior evidence/history.

Typical chain:

```text
Research V1          — ChatGPT Project
  ↓
Planning V1          — Codex / Astra
  ↓
Approval             — Human + terminal
  ↓
Execution V1         — VS Code Manager/Builder
  ↓
Evaluation V1        — Codex / Astra
  ↓ RESEARCH_REQUIRED
Research V2          — ChatGPT Project
  ↓
Planning V2          — Codex / Astra
  ↓
Approval
  ↓
Execution V2
  ↓
Evaluation V2
```

## Issue-driven Research

**Tool:** ChatGPT Project

For runtime errors, user feedback, compatibility changes, newly discovered constraints, or other observations that may change project knowledge, use:

```text
EXECUTE/chatgpt/PROCESS_ISSUE_PROMPT.md
```

Treat an issue as evidence first. Investigate it before promoting it into authoritative project requirements.

---

# Which tool do I use right now?

If you open a project and do not remember the next step, read:

```text
EXECUTE/PROJECT_STATUS.md
```

Then use this table:

| Current state | Tool to open | What to do |
|---|---|---|
| `RESEARCH` / `INPUT_REQUIRED` | ChatGPT Project | Continue Research with the appropriate prompt in `EXECUTE/chatgpt/`. |
| Research ready, no plan yet | Codex / Astra | Run `PLANNING_AND_COMPILATION_PROMPT.md`. |
| `AWAITING_USER_APPROVAL` | Human + terminal | Review plan and run `approve_plan.py` only if approved. |
| `EXECUTION` / `READY` / `IN_PROGRESS` | VS Code Chat → `ProjectManager500K` | Run/use `EXECUTE_PROJECT_PROMPT.md`. |
| `AWAITING_EVALUATION` or Evaluation `REQUIRED` | Codex / Astra | Run `EVALUATION_PROMPT.md`. |
| Evaluation = `CORRECTION_REQUIRED` | VS Code Manager/Builder | Follow the evaluator-authorized correction path. |
| Evaluation = `REPLAN_REQUIRED` | Codex / Astra | Create the next Planning Vx. |
| Evaluation = `RESEARCH_REQUIRED` | ChatGPT Project | Use `PROCESS_EVALUATION_PROMPT.md` and create Research Vx+1. |
| Evaluation = `PASS` | Human/release process | Preserve history and release/close according to your process. |

---

# Which prompt do I use?

| Situation | Tool/environment | Prompt/file |
|---|---|---|
| Start a new project's research | ChatGPT Project | `EXECUTE/chatgpt/START_RESEARCH_PROMPT.md` |
| Evaluation says more research is needed | ChatGPT Project | `EXECUTE/chatgpt/PROCESS_EVALUATION_PROMPT.md` |
| New error/issue/feedback may change knowledge | ChatGPT Project | `EXECUTE/chatgpt/PROCESS_ISSUE_PROMPT.md` |
| Research is ready and you need Planning | Codex / GPT-6 Astra | `EXECUTE/codex/PLANNING_AND_COMPILATION_PROMPT.md` |
| Plan is approved and implementation should start | VS Code Chat / `ProjectManager500K` | `EXECUTE_PROJECT_PROMPT.md` |
| Local execution finished | Codex / GPT-6 Astra | `EXECUTE/codex/EVALUATION_PROMPT.md` |

---

# Tool ownership rules

These boundaries are deliberate.

| Tool/role | Owns | Must not silently do |
|---|---|---|
| ChatGPT Project | Research, requirements clarification, Research Vx evidence | Implement production code or create the approved implementation plan |
| Codex / GPT-6 Astra Planning | Architecture, compilation, Tasks, Planning Vx | Approve its own plan or execute local production changes |
| Human | Approval/release decisions | Be bypassed by automatic Planning → Execution transition |
| VS Code `ProjectManager500K` | Orchestrate approved local Execution Vx | Redesign approved architecture/requirements |
| VS Code `Builder100K` | One bounded implementation Task | Own global architecture or future Tasks |
| Codex / GPT-6 Astra Evaluation | Independent verification and routing findings | Silently fix production implementation while evaluating |

---

# Who owns which files?

| Layer | Primary owner | Purpose |
|---|---|---|
| `EXECUTE/project_details.md` | ChatGPT Research | Concise authoritative project requirements/context |
| `EXECUTE/docs/raw/**` | ChatGPT Research | Raw evidence, facts, provenance, limitations, research details |
| `EXECUTE/research/**` | ChatGPT Research | Research Vx records and handoff state |
| `EXECUTE/reference/**` | Planning / controlled knowledge process | Durable indexed project knowledge with provenance |
| `EXECUTE/compiled/**` | Astra Planning | Distilled execution intelligence for local no-RAG models |
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

Do not use `compiled/**` as a replacement for original evidence. Do not delete `docs/raw/**` merely because Planning completed.

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
Research Vx
Tool: ChatGPT Project
    ↓
Planning & Knowledge Compilation Vx
Tool: Codex / GPT-6 Astra
    ↓
USER APPROVAL GATE
Tool: Human + terminal
    ↓
Execution Vx
Tool: VS Code Chat
      ProjectManager500K + Builder100K
    ↓
Evaluation Vx
Tool: Codex / GPT-6 Astra
    ↓
PASS / correction / replan / Research Vx+1
```

The separation exists because the local Manager/Builder runtime may have no RAG. Codex/Astra therefore compiles global reasoning into durable disk artifacts before execution.

```text
context window != project memory
```

Disk artifacts are durable project memory. Each local Builder invocation is temporary working context.

---

# Workspace map

```text
.github/
└─ agents/
   ├─ project-manager.agent.md      # VS Code custom agent: Manager
   └─ builder100k.agent.md          # VS Code custom agent: Builder

EXECUTE/
├─ MODEL_CONFIG.ini                 # human-editable runtime model identity/context
├─ MODEL_BINDINGS.json             # generated machine-readable bindings
├─ chatgpt/                         # ChatGPT Research prompt pack
│  ├─ PROJECT_INSTRUCTIONS.txt
│  ├─ MASTER_RESEARCH_PROMPT.md
│  ├─ START_RESEARCH_PROMPT.md
│  ├─ PROCESS_EVALUATION_PROMPT.md
│  └─ PROCESS_ISSUE_PROMPT.md
├─ project_details.md
├─ docs/raw/                        # durable Research evidence; never auto-clear
├─ research/                        # Research Vx artifacts / handoffs
├─ reference/                       # durable indexed knowledge
├─ codex/                           # Codex Planning/Evaluation prompts
│  ├─ PLANNING_AND_COMPILATION_PROMPT.md
│  └─ EVALUATION_PROMPT.md
├─ compiled/                        # distilled intelligence for local execution
├─ plan/                            # plan + approval state
├─ tasks/                           # atomic Builder Tasks
├─ execution/                       # local execution state/evidence
├─ evaluation/                      # independent Evaluation reports
├─ issues/                          # structured issue workflow
└─ history/                         # immutable Planning/Evaluation history
```

---

# Safety rails

- ChatGPT Research does not implement production code or create approved implementation Tasks.
- Codex/Astra Planning does not approve its own plan.
- Local Manager/Builder do not silently change approved architecture, scope, or requirements.
- Execution completion does not equal independent validation.
- Codex/Astra Evaluation does not silently fix production implementation while evaluating it.
- Approved and historical versions are not silently overwritten.
- Raw Research evidence is preserved for provenance and future Research versions.
- Provider credentials/API keys stay outside the repository configuration files.

---

# Useful commands

Configure the Manager/Builder bindings after editing `MODEL_CONFIG.ini`:

```bash
python scripts/configure_models.py
```

Validate the template/runtime setup:

```bash
python scripts/validate_v4.py
```

Approve an exact Planning version for an exact Execution version:

```bash
python scripts/approve_plan.py --planning Planning_V1 --execution Execution_V1
```

Check a controlled Builder Task payload:

```bash
python scripts/context_guard.py EXECUTE/tasks/TASK_TEMPLATE.md
```

The context guard estimates only the controlled Task payload. It is not tokenizer-perfect and does not include every host/system/tool overhead token.

---

# Common mistakes

## Mistake: starting in VS Code Manager before Research/Planning

Wrong:

```text
Open template → run ProjectManager500K immediately
```

Correct:

```text
Research → Planning → Human Approval → VS Code Execution
```

## Mistake: using OpenRouter API ID directly as the VS Code custom-agent model name

The API/provider `model_id` and the VS Code registered/display name can differ. Record both. The template pins the agent with:

```text
VS Code Model Name (vendor)
```

## Mistake: reading provider JSON and assuming it contains the selected model ID

A provider group such as:

```json
{
  "name": "OpenRouter",
  "vendor": "openrouter"
}
```

identifies the provider group, not necessarily the individual model. Inspect the model details in **Manage Language Models**.

## Mistake: deleting `EXECUTE/docs/raw/**` after Planning

Do not do this. `docs/raw/**` is the durable evidence/provenance layer used by future Planning, Evaluation, and Research versions.

## Mistake: treating `AWAITING_EVALUATION` as project completion

It means local Execution finished. The project still requires independent Evaluation.
