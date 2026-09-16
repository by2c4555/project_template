# Project Template v4.0.1

## AI-assisted development workflow for VS Code Copilot Chat

This template is for projects where one AI model plans the whole project and smaller bounded AI workers implement one task at a time.

The main idea is simple:

```text
You prepare project requirements
        ↓
ProjectManager starts the workflow
        ↓
Planner512K creates project knowledge, architecture, plan, phases, and tasks
        ↓
You authorize one Phase
        ↓
Builder128K / Builder256K executes each Task in a fresh context
        ↓
Integration Gate verifies the Phase
        ↓
You authorize the next Phase
```

You normally interact with **ProjectManager only**.

You do **not** manually switch between Planner and Builder agents for every step.

---

# Start Here

If this is your first time using the template, follow these steps in order.

## Step 1 — Prepare the project input

Before opening the execution workflow, fill in:

```text
EXECUTE/project_details.md
```

This is the main user-owned requirements file.

It should explain at least:

- what you are building;
- what success means;
- what is in scope and out of scope;
- important user/system workflows;
- functional requirements;
- architecture-relevant non-functional requirements;
- target runtime/platform;
- database or persistence requirements;
- external APIs/services;
- security constraints;
- packaging/deployment expectations;
- testing expectations;
- known risks or unknowns.

If something important is genuinely unknown, write:

```text
UNKNOWN
```

Do not guess.

You may also place supporting research or source documents in:

```text
EXECUTE/docs/
```

For example:

```text
EXECUTE/
├── project_details.md
└── docs/
    ├── API_RESEARCH.md
    ├── DATABASE_RESEARCH.md
    ├── SECURITY_RESEARCH.md
    └── vendor_specification.pdf
```

These documents may come from your own research, a ChatGPT Research Project, vendor documentation, previous project notes, or other trusted sources.

`project_details.md` is authoritative user intent.

`EXECUTE/docs/` is supporting raw source material.

---

## Step 2 — Choose models for the three roles

v4.0.1 has three internal AI roles:

```text
Planner512K
Builder128K
Builder256K
```

Minimum documented context sizes are:

```text
Planner512K  >= 524288 tokens
Builder128K  >= 131072 tokens
Builder256K  >= 262144 tokens
```

The template does not guess which provider you want to use.

Bind the exact model and provider before execution.

Example:

```bash
python scripts/configure_models.py \
  --planner-model "Claude Opus 4.7" --planner-provider openrouter --planner-context 1048576 \
  --builder128-model "Qwen3 Coder Next" --builder128-provider openrouter --builder128-context 262144 \
  --builder256-model "Qwen3 Coder Next" --builder256-provider openrouter --builder256-context 262144
```

Use the real model name, provider/vendor identifier, and documented context capacity available in your VS Code environment.

For example:

```text
Claude Opus 4.7 (openrouter)
Claude Opus 4.7 (copilot)
```

are treated as different bindings.

---

## Step 3 — Validate the workspace

Run:

```bash
python scripts/validate_v4.py
```

Do not begin planning if validation fails.

After model binding is correct and the workspace is structurally valid, the validator should report the template as ready.

For individual Tasks, the workflow may also use:

```bash
python scripts/context_guard.py EXECUTE/tasks/TASK_NNN.md
```

This estimates whether the bounded Task context fits its assigned Builder.

---

## Step 4 — Open the project in VS Code

Open the project folder in a VS Code/Copilot version that supports:

```text
custom agents
tools
agents
subagent invocation
```

The template depends on isolated subagent execution.

The user-facing agent is:

```text
ProjectManager
```

Planner512K, Builder128K, and Builder256K are internal agents.

---

## Step 5 — Start the workflow

In Copilot Chat:

1. Select the `ProjectManager` custom agent.
2. Start with `EXECUTE_PROJECT_PROMPT.md`.

That entry prompt tells ProjectManager to read:

```text
EXECUTE/PROJECT_STATUS.md
```

and resume from the persisted workflow state.

Do not paste the whole repository, all research documents, or the entire implementation plan into the main chat.

The system is intentionally designed so the main chat remains small.

---

# What Happens After You Start?

At a new project, the initial state is approximately:

```text
INITIALIZE
    ↓
PT1_INPUT_KNOWLEDGE
```

ProjectManager invokes a fresh Planner512K subagent.

The Planner then progresses through five isolated planning transactions.

```text
PT1_INPUT_KNOWLEDGE
    ↓
PT2_ARCHITECTURE_PLAN
    ↓
PT3_RISK_PHASES
    ↓
PT4_TASK_COMPILATION
    ↓
PT5_TASK_PACK_VALIDATION
    ↓
EXECUTION_READY
```

Each planning transaction receives a fresh context window.

The Planner uses the project input to create and maintain durable project state on disk.

Important outputs include:

```text
EXECUTE/reference/
EXECUTE/plan/IMPLEMENTATION_PLAN.md
EXECUTE/tasks/
EXECUTE/PROJECT_STATUS.md
```

The main chat does not need to remember the whole project.

Disk state is authoritative.

---

# When Does the User Need to Interact?

There are two common cases.

### 1. The Planner needs missing information

If architecture-critical information is missing, the workflow stops instead of guessing.

The Planner may create:

```text
EXECUTE/reference/OPEN_QUESTIONS.md
```

ProjectManager reports what information is required.

You answer the question and persist the important answer in:

```text
EXECUTE/project_details.md
```

or the appropriate supporting source document.

Then resume through ProjectManager.

### 2. A Phase is ready for execution

A Phase is the user authorization boundary.

Typical structure:

```text
Phase
├── TASK_001
├── TASK_002
├── TASK_003
└── Integration Gate
```

When you authorize the Phase:

```text
phase_authorized = true
```

ProjectManager executes its Tasks in dependency order.

You do not need to approve every successful Task.

---

# How Task Execution Works

The core invariant of v4.0.1 is:

> **1 Task = 1 execution contract = 1 isolated subagent invocation = 1 fresh context window.**

Example:

```text
ProjectManager
    ↓
Builder128K → TASK_001 → PASS
    ↓ fresh context
Builder128K → TASK_002 → PASS
    ↓ fresh context
Builder256K → TASK_003 → PASS
    ↓ fresh context
Builder256K → Integration Gate → PASS
```

A successful Task may allow ProjectManager to continue automatically inside the currently authorized Phase.

The previous Builder context is never reused for the next Task.

This is the main protection against context accumulation and scope drift.

---

# Builder128K vs Builder256K

`Builder128K` is the default implementation executor.

Use `Builder256K` when the work cannot safely fit the smaller Builder after reasonable Task decomposition.

Builder256K is also used for Phase Integration Gates.

The intended decision is:

```text
Can Task fit Builder128K?
    │
    ├─ YES → Builder128K
    │
    └─ NO
        ↓
Can Task be cleanly split?
    │
    ├─ YES → split it
    │
    └─ NO → Builder256K
```

Builder256K is not a Planner.

Builders do not redesign project architecture.

---

# What Happens When Something Fails?

Only `PASS` allows normal automatic continuation.

Statuses such as:

```text
PARTIAL
BLOCKED
WAITING_USER
EXECUTION_UNSTABLE
KNOWLEDGE_REVIEW_REQUIRED
REPLAN_REQUIRED
EXTERNAL_ACTION_REQUIRED
```

stop the current Phase.

The system then persists evidence to disk and reports the next valid action.

It does not silently keep retrying forever.

The default repair limit is two meaningful repair attempts.

After that, the problem should be recorded as an Issue and routed appropriately.

---

# What Is an Issue?

An Issue is a durable recovery package.

It should contain enough verified information for another isolated agent to continue without replaying the entire failed chat.

Conceptually:

```text
Issue
=
problem
+ verified evidence
+ approaches already ruled out
+ safe resume point
+ escalation information
```

Issues live under:

```text
EXECUTE/issues/
```

---

# Phase Completion

After all Tasks and the Integration Gate pass:

```text
Phase complete
    ↓
phase_authorized = false
    ↓
ProjectManager stops
    ↓
User authorizes the next Phase
```

The user approves Phases, not every micro-Task.

This keeps human control at meaningful checkpoints without forcing constant confirmation.

---

# Project Completion

When enabled by project policy, release completion may require:

```text
System Test
→ Package
→ Clean Install
→ Release Gate
→ COMPLETE
```

Passing unit tests alone does not necessarily mean the project is complete.

---

# Which Files Do I Actually Edit?

For normal use, the most important user-facing files are:

```text
EXECUTE/project_details.md
EXECUTE/docs/*
.env.user                  # only when external credentials/config are needed
```

You normally should not manually edit internal Planner/Builder instructions during project execution.

The workflow itself maintains files such as:

```text
EXECUTE/PROJECT_STATUS.md
EXECUTE/reference/*
EXECUTE/plan/*
EXECUTE/tasks/*
EXECUTE/issues/*
```

Review them when needed, but treat them as workflow state and project memory.

---

# Where Do Secrets Go?

Never put secrets in:

```text
project_details.md
EXECUTE/docs/
EXECUTE/.env.execute
Tasks
Issues
Plans
Knowledge files
```

Human-owned local credentials belong in:

```text
.env.user
```

and must not be committed.

If required external configuration is missing, the AI must stop and ask rather than inventing values.

---

# Mental Model

The easiest way to understand the system is:

```text
USER
  owns requirements and Phase authorization

ProjectManager
  owns routing

Planner512K
  owns global thinking

Builder128K / Builder256K
  own bounded implementation

Disk
  owns persistent project memory

Chat
  is temporary
```

Or even shorter:

> **Planner thinks globally. Builder executes locally. ProjectManager routes. Disk remembers. User authorizes.**

---

# Workspace Structure

```text
workspace/
├── README.md
├── EXECUTE_PROJECT_PROMPT.md
│
├── .github/
│   ├── agents/
│   │   ├── project-manager.agent.md
│   │   ├── planner512k.agent.md
│   │   ├── builder128k.agent.md
│   │   └── builder256k.agent.md
│   └── skills/
│       ├── project-planning/SKILL.md
│       └── builder-task-execution/SKILL.md
│
├── EXECUTE/
│   ├── PROJECT_CONFIG.md
│   ├── PROJECT_STATUS.md
│   ├── MODEL_BINDINGS.json
│   ├── project_details.md
│   ├── docs/
│   ├── reference/
│   ├── plan/
│   ├── tasks/
│   └── issues/
│
├── scripts/
│   ├── configure_models.py
│   ├── validate_v4.py
│   └── context_guard.py
│
├── src/
├── test/
└── package/
```

Think of the folders this way:

```text
.github/
= how the AI roles operate

EXECUTE/
= what the project knows, decided, is doing, and must do next

src/ + test/
= implementation reality
```

---

# Why v4.0.1 Uses Fresh Contexts

Large model context windows are not fully available to project content.

The same context is also consumed by:

```text
VS Code/Copilot system instructions
agent instructions
tools
conversation history
user prompts
project files
tool output
reasoning
model output
```

Therefore:

> nominal model context != usable project context

v4.0.1 does not try to keep one giant conversation alive.

Instead, it persists durable state to disk and starts fresh isolated subagents for bounded units of work.

That is why the workflow requires:

```text
Planner >= 512K
Builder >= 128K
```

while still keeping each actual planning or execution payload significantly below the model's nominal maximum.

---

# Core Safety and Reliability Rules

```text
Planner below 512K
→ no Planning.

Builder below 128K
→ no Execution.

Missing project details
→ ask User and STOP.

Insufficient Knowledge
→ no Plan.

Unvalidated Plan
→ no Tasks.

Unvalidated Task Pack
→ no Execution.

Builder does not design architecture.

Builder does not repair planning gaps.

Task execution always uses a fresh Builder context.

Planner transactions always use fresh Planner contexts.

PASS
→ may continue inside the authorized Phase.

Any non-PASS
→ stop the Phase.

Missing external configuration
→ never guess.

Repeated no-progress behavior
→ Issue and STOP.

Chat history
→ not authoritative.

Disk state
→ authoritative.
```

---

# Common Mistakes

Avoid these patterns:

```text
Selecting Planner512K as the main user-facing agent
→ Use ProjectManager instead.

Manually changing model in chat before every Task
→ Bind role models once; ProjectManager invokes the internal roles.

Pasting the whole repository into the chat
→ Let each Task define bounded context.

Putting research only in chat
→ Persist important material in project_details.md or EXECUTE/docs/.

Letting Builder make architecture decisions
→ Planning defects go back to Planner.

Approving every successful Task manually
→ Approve one Phase; successful Tasks continue automatically.

Retrying the same failure repeatedly
→ Produce new evidence, make a materially different repair, or stop.

Keeping important decisions only in conversation history
→ Persist them to disk.
```

---

# Quick Checklist

Before first run:

```text
[ ] Fill EXECUTE/project_details.md
[ ] Put useful supporting material in EXECUTE/docs/
[ ] Bind Planner512K model/provider/context
[ ] Bind Builder128K model/provider/context
[ ] Bind Builder256K model/provider/context
[ ] Run python scripts/validate_v4.py
[ ] Open project in compatible VS Code/Copilot
[ ] Select ProjectManager
[ ] Start with EXECUTE_PROJECT_PROMPT.md
```

During the project:

```text
[ ] Answer blocking Planner questions when requested
[ ] Persist important answers to disk
[ ] Authorize one Phase at a time
[ ] Let ProjectManager route Tasks automatically after PASS
[ ] Stop and review Issues when execution is non-PASS
```

---

# In One Sentence

**Prepare the requirements, bind and validate the models, start through ProjectManager, let Planner create bounded work, authorize one Phase, and let isolated Builders execute one fresh-context Task at a time.**
