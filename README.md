# Project Template v4.1.0
## External Intelligence + Local Controlled Execution + Independent Evaluation

v4.1 changes the architecture from a VS Code-centric planner/executor into a closed engineering loop designed for powerful external reasoning and no-RAG local execution.

## Core Loop

```text
Research Vx — ChatGPT Project
    ↓
Planning & Knowledge Compilation Vx — Codex / GPT-6 Astra
    ↓
USER APPROVAL GATE
    ↓
Execution Vx — local ProjectManager500K + Builder100K
    ↓
Evaluation Vx — Codex / GPT-6 Astra, independent/read-only
    ↓
PASS / correction / replan / Research Vx+1
```

The important separation is:

- Research determines what is known and required.
- Astra compiles global reasoning into durable execution knowledge.
- Local models execute decisions; they do not rediscover architecture.
- Astra evaluates the finished implementation independently.
- Evaluation findings can become the evidence for the next Research version.

## Why v4.1

Manager and Builder may be local models without RAG. v4.1 therefore preserves the value of the stronger external model by compiling its reasoning into disk artifacts: project brief, architecture, decisions, constraints, interfaces, risks, implementation plan, and self-contained Task context manifests.

`context window != project memory`. Disk artifacts are durable memory; each local Builder invocation is temporary working context.

## Roles

### ChatGPT Project — Research Intelligence
Produces/updates `project_details.md`, `docs/raw/**`, and Research Vx. After an Evaluation reports research gaps, ChatGPT Project performs Research Vx+1.

### Codex / GPT-6 Astra — Planning & Knowledge Compilation
Use `EXECUTE/codex/PLANNING_AND_COMPILATION_PROMPT.md`. Astra reasons globally and produces the execution package. It must stop at `AWAITING_USER_APPROVAL`; it cannot approve its own plan.

### ProjectManager500K — Local Execution Orchestrator
Runs in VS Code. It may orchestrate/decompose within approved intent but may not change project architecture or requirements. Minimum documented local context: 512000 tokens.

### Builder100K — Local Implementation Worker
One bounded Task per fresh invocation. Minimum documented local context: 102400 tokens. Default compiled payload target: 40000 tokens; hard controlled maximum: 52000 tokens.

### Codex / GPT-6 Astra — Independent Evaluator
Use `EXECUTE/codex/EVALUATION_PROMPT.md` after local execution completes. Evaluation is read-only and independently verifies requirements, architecture, behavior, tests, and risks.

## Status Semantics

`Task PASS` is not `Execution COMPLETE`, and `Execution COMPLETE` is not `Project VALIDATED`.

When all local Tasks pass, the Manager sets `evaluation_status: REQUIRED` and stops. Only Evaluation Vx can produce a validation result.

Evaluation result is exactly one of:
- `PASS`
- `PASS_WITH_FINDINGS`
- `CORRECTION_REQUIRED`
- `REPLAN_REQUIRED`
- `RESEARCH_REQUIRED`

## Version Chain

Example:

```text
Research V1
  → Planning V1 APPROVED
  → Execution V1 COMPLETE
  → Evaluation V1 RESEARCH_REQUIRED
  → Research V2
  → Planning V2 APPROVED
  → Execution V2 COMPLETE
  → Evaluation V2 PASS
```

Each new version keeps immutable history. Current aliases point to the active artifacts.

## Workspace

```text
EXECUTE/
├─ project_details.md
├─ docs/raw/                      # research source material
├─ research/                      # Research Vx + ChatGPT handoff
├─ codex/
│  ├─ PLANNING_AND_COMPILATION_PROMPT.md
│  └─ EVALUATION_PROMPT.md
├─ compiled/                      # distilled intelligence for local models
│  ├─ PROJECT_BRIEF.md
│  ├─ ARCHITECTURE.md
│  ├─ DECISIONS.md
│  ├─ GLOBAL_CONSTRAINTS.md
│  ├─ INTERFACES.md
│  ├─ DATA_MODEL.md
│  └─ KNOWN_RISKS.md
├─ plan/
│  ├─ IMPLEMENTATION_PLAN.md
│  └─ PLANNING_STATUS.md
├─ tasks/
│  ├─ TASK_INDEX.md
│  └─ TASK_NNN.md
├─ execution/
│  ├─ EXECUTION_STATE.md
│  ├─ EXECUTION_SUMMARY.md
│  └─ evidence/
├─ evaluation/
│  ├─ EVALUATION_STATUS.md
│  ├─ Evaluation_Vx.md
│  └─ RESEARCH_HANDOFF_Vx.md
└─ history/
   ├─ planning/
   └─ evaluation/
```

## Operating Procedure

1. **Research V1** — In ChatGPT Project, research manually until `project_details.md` and `docs/raw/**` are sufficient.
2. **Planning V1** — Open the workspace in Codex and run `EXECUTE/codex/PLANNING_AND_COMPILATION_PROMPT.md` with GPT-6 Astra.
3. **Review** — Astra sets `AWAITING_USER_APPROVAL`. Review plan, decisions, Tasks, and compiled knowledge.
4. **Approve** — Explicitly approve and bind the versions:

   ```bash
   python scripts/approve_plan.py --planning Planning_V1 --execution Execution_V1
   ```

   The script succeeds only when `PLANNING_STATUS.md` is `AWAITING_USER_APPROVAL`. No approval means no implementation.
5. **Execute locally** — In VS Code select `ProjectManager500K` and run `EXECUTE_PROJECT_PROMPT.md`. The Manager dispatches one fresh Builder100K per Task.
6. **Local execution complete** — The Manager stops at `AWAITING_EVALUATION`; it does not claim project validation.
7. **Evaluation V1** — In Codex run `EXECUTE/codex/EVALUATION_PROMPT.md` with GPT-6 Astra.
8. **Route findings** — Corrections return to Execution; plan defects return to new Planning; research/requirement gaps return to ChatGPT Project as Research V2.
9. Repeat until Evaluation Vx returns an acceptable validation result.

## Configure Local Models

Provider/model names are not guessed. Bind the two local roles explicitly:

```bash
python scripts/configure_models.py \
  --manager-model "<MODEL>" --manager-provider "<PROVIDER>" --manager-context 512000 \
  --builder-model "<MODEL>" --builder-provider "<PROVIDER>" --builder-context 102400
```

Use each model's actual documented capacity. The provider suffix is part of the execution contract.

## Validate Template

```bash
python scripts/validate_v4.py
python scripts/context_guard.py EXECUTE/tasks/TASK_TEMPLATE.md
```

The context guard estimates only controlled Task payload. It does not claim tokenizer-perfect measurement or include all VS Code host/system/tool overhead.
