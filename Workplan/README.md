# Workplan v5.1.0 — Deterministic Control Plane & Capability-Based Work

`Workplan/` is the durable control plane for AI-assisted development. v5.1 moves workflow mechanics out of prompts and into deterministic capabilities while preserving v5 approval, integrity, diagnosis/recovery and independent evaluation invariants.

## User Workflow

There are only two normal work surfaces:

1. **External AI** — expensive Research, Planning, Diagnosis, Recovery and Evaluation reasoning.
2. **VS Code Copilot Chat** — local `@ExecutionManager`, which deterministically dispatches bounded Builder work.

The user should not invent stage-specific commands, select Task IDs, or manually invoke Builders.

### 1. Research

Use an external strong model to determine product **WHAT/WHY**, resolve product-scope unknowns and produce:

- `project_details.md`
- only useful declared supporting files

Research does not create implementation Tasks and does not read `Objective_dev.md` as project scope.

Copy the handoff into:

```text
Workplan/ingest/project_details.md
Workplan/ingest/docs/raw/*
```

Then validate/import:

```bash
python Workplan/scripts/tools/ingest.py check
python Workplan/scripts/tools/scope.py import
```

### 2. Planning / other external reasoning

The external agent uses one stable entry contract:

```bash
python Workplan/scripts/tools/external.py acquire --tool "<provider>" --model "<model>"
```

The role is derived from durable lifecycle state; wording such as **Continue Workplan.** only causes the agent to query state and never grants authority.

Planning must checkpoint bounded semantic units using the generation printed by its ticket. When finished:

```bash
python Workplan/scripts/tools/work.py complete --generation <N> --note "..."
python Workplan/scripts/tools/planning.py mark-ready
```

`mark-ready` revalidates ingest, validates the planning package, archives accepted Research input and switches the user to VS Code.

### 3. Execution in VS Code

Select `@ExecutionManager` and send:

```text
Continue Workplan.
```

The Manager queries:

```bash
python Workplan/scripts/tools/execution.py next
```

and follows only the returned action. For a new Task it runs `execution.py dispatch`; for an interrupted Task it runs `execution.py resume`. Both choose/bind the Task deterministically and return a bounded Builder ticket.

A Builder executes only that immutable Task. It checkpoints with its generation and may request bounded context by reason:

```bash
python Workplan/scripts/tools/work.py request-context --reason ARCHITECTURE
```

Context expansion never expands authority.

### 4. Failure / recovery

Local repair is bounded by each Task's `max_repairs`. When the limit is exceeded or a Task fails, state routes to Diagnosis. Diagnosis and Recovery are separate external Work roles. Recovery can only follow an evidence-backed `IMPLEMENTATION_DEFECT`.

### 5. Evaluation / completion

After all Tasks are PASS/PASS_RECOVERED, deterministic execution routes to Evaluation. Independent Evaluation verifies actual behavior against immutable Scope and contracts. A passing result requires a Completion Report containing the exact Scope revision and digest, then the Cycle becomes `CLOSED_VALIDATED`.

## System Workflow

```text
External Research
  -> untrusted Workplan/ingest/
  -> deterministic ingest receipt (package digest + canonical scope digest)
  -> immutable Scope history
  -> Planning capability / generation-fenced Work
  -> final ingest revalidation + planning integrity
  -> accepted ingest archive + PLAN_READY
  -> VS Code ExecutionManager
  -> deterministic next/dispatch/resume
  -> fresh bounded Builder + Task Ticket
  -> PASS / bounded repair / Diagnosis
  -> Recovery when proven implementation defect
  -> independent Evaluation
  -> Completion Report
  -> CLOSED_VALIDATED
```

## Authority boundaries

- `Workplan/control/STATE.json` is internal machine authority.
- `Workplan/control/ingest/*.json` are durable validation receipts.
- `Workplan/history/` stores immutable logical snapshots.
- `Workplan/archive/` preserves accepted original inbound packages.
- `Workplan/work/` stores resumable role Work, semantic checkpoints and evidence.
- Tickets are projections from current authority; stale Work generations are rejected.
- Provider/model identity is metadata only.

## Human commands

Normal human interactions are deliberately small:

```bash
python Workplan/scripts/resume.py
python Workplan/scripts/approve.py -- <challenge>
```

`approve.py` is the sole human approval surface and only exists for material token/cost/rework risk.

## Model guidance

Use the strongest available reasoning model for Planning/Diagnosis/Recovery/Evaluation when the uncertainty is material. Do not choose a weak model merely because it has a larger context window. Use low-cost models for Tasks whose scope, paths, acceptance criteria and verification are already bounded.

## Development reference

Maintainers and future agents evolving Project Template itself must read `Workplan/Objective_dev.md`. It is separate from user-project Research input.
