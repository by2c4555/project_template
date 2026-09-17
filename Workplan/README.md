# Workplan v5.2.0 — Deterministic Human Command & Continuation Protocol

`Workplan/` is the durable control plane for AI-assisted development. v5.2 preserves the v5.1 deterministic control plane and adds one universal AI bootstrap plus exact human workflow commands so expensive or mutating work never starts from free-form language interpretation.

## 1. What this version is

There are only two normal work surfaces:

1. **External AI** — Research, Planning, Diagnosis, Recovery and independent Evaluation.
2. **VS Code Copilot Chat** — `@ExecutionManager` for bounded implementation.

Terminal/Python commands are control-plane mechanisms, not a third user work surface.

All AI surfaces bootstrap from:

```text
Workplan/ENTRY_PROMPT.md
```

Natural-language conversation is discussion only. Workflow execution requires an exact command.

## 2. Requirements and tools

- Python 3.x capable of running `Workplan/scripts/*.py`.
- External AI with repository/tool access for expensive reasoning stages.
- VS Code + GitHub Copilot Chat for local `@ExecutionManager` execution.
- A compatible low-cost Builder configured for bounded Task work.

No specific provider identity grants authority. Durable Workplan state and machine-issued tickets do.

## 3. Public command protocol

Use these exact tokens only:

| Command | Meaning |
|---|---|
| `WORKPLAN_STATUS` | Read bounded current status and allowed commands. |
| `WORKPLAN_NEXT` | Read the exact next surface/command without executing it. |
| `EXECUTE_RESEARCH` | Start a new Research handoff when no active cycle is running. |
| `EXECUTE_PLANNING` | INIT or RESUME Planning as determined by Workplan. |
| `EXECUTE_IMPLEMENTATION` | Start/resume/reconcile bounded implementation in VS Code. |
| `EXECUTE_DIAGNOSIS` | INIT or RESUME evidence-backed Diagnosis. |
| `EXECUTE_RECOVERY` | INIT or RESUME proven implementation-defect Recovery. |
| `EXECUTE_EVALUATION` | INIT or RESUME independent Evaluation. |
| `RESET_PLANNING` | Invalidate active Planning Work and restart from bound Scope; approval required. |
| `RESET_DIAGNOSIS` | Invalidate active Diagnosis Work; approval required. |
| `RESET_RECOVERY` | Invalidate active Recovery Work; approval required. |
| `RESET_EVALUATION` | Invalidate active Evaluation Work; approval required. |

Do not paraphrase execution commands. “Please continue planning” is discussion; `EXECUTE_PLANNING` is execution intent.

## 4. External Research setup

Open a fresh/appropriate External AI workspace with repository context and first tell it:

```text
Read and follow Workplan/ENTRY_PROMPT.md
```

Then send:

```text
EXECUTE_RESEARCH
```

Workplan selects `Workplan/external_agent/RESEARCH_PROMPT.md` as the role constitution. Continue product WHAT/WHY discussion until the handoff is ready. Expected output:

```text
project_details.md
docs/raw/<selected evidence>
```

`Objective_dev.md` is never user-project Research input.

Place the physical handoff in:

```text
Workplan/ingest/project_details.md
Workplan/ingest/docs/raw/*
```

Validate/import using the deterministic ingest/scope tools. The import transition will expose `EXECUTE_PLANNING` as the next command.

## 5. User Workflow

```text
External AI
  -> ENTRY_PROMPT.md
  -> EXECUTE_RESEARCH
  -> Workplan/ingest/
  -> deterministic ingest + Scope import
  -> EXECUTE_PLANNING
  -> PLAN_READY
  -> VS Code @ExecutionManager
  -> EXECUTE_IMPLEMENTATION
  -> bounded Tasks
  -> EXECUTE_DIAGNOSIS / EXECUTE_RECOVERY when routed
  -> return to EXECUTE_IMPLEMENTATION
  -> EXECUTE_EVALUATION
  -> Completion Report
  -> CLOSED_VALIDATED
  -> EXECUTE_RESEARCH for the next feature/version cycle
```

The user never selects Task IDs, generations, Cycle IDs, hashes or role prompt files.

## 6. Planning

On External AI, after bootstrap, send exactly:

```text
EXECUTE_PLANNING
```

Workplan determines:

- **INIT** — no compatible active Planning Work exists;
- **RESUME** — durable Planning Work exists;
- reconciliation needs — from durable Work metadata/checkpoints.

A fresh Planning cost envelope may require human approval. If approval is requested, the AI must stop and show the exact `approve.py` command. After approval, resend `EXECUTE_PLANNING`; Workplan then issues the bounded Planning ticket.

A provider/session change does not require a chat summary. Re-bootstrap with `ENTRY_PROMPT.md`, send `EXECUTE_PLANNING`, and Workplan resumes durable Work.

## 7. VS Code implementation

When `WORKPLAN_NEXT` says `VS_CODE / EXECUTE_IMPLEMENTATION`:

1. Open the project in VS Code.
2. Open Copilot Chat.
3. Select `@ExecutionManager`.
4. Send exactly:

```text
EXECUTE_IMPLEMENTATION
```

`@ExecutionManager` points to `Workplan/ENTRY_PROMPT.md`, submits the command with surface `VS_CODE`, and follows only deterministic execution actions. It never asks the user to choose the next Task and never invokes Builder without a machine-issued ticket.

## 8. Diagnosis and Recovery

If bounded implementation exceeds local repair limits, Workplan moves to Diagnosis and `WORKPLAN_NEXT` returns:

```text
NEXT SURFACE: EXTERNAL_AI
NEXT COMMAND: EXECUTE_DIAGNOSIS
```

Bootstrap the External AI from `ENTRY_PROMPT.md` and send that exact command. Diagnosis establishes root cause; it does not repair production code.

Only an evidence-backed `IMPLEMENTATION_DEFECT` routes to:

```text
EXECUTE_RECOVERY
```

After verified Recovery, Workplan normally returns to VS Code with `EXECUTE_IMPLEMENTATION`.

## 9. Evaluation and completion

After all approved Tasks pass, Workplan routes to:

```text
NEXT SURFACE: EXTERNAL_AI
NEXT COMMAND: EXECUTE_EVALUATION
```

Evaluation independently verifies actual behavior. PASS/PASS_WITH_FINDINGS requires a Completion Report bound to the exact Scope revision and digest. Successful completion produces `CLOSED_VALIDATED`.

## 10. Human approval UX

`Workplan/scripts/approve.py` remains the only human approval interface. AI must never run it.

Approval is a token/cost/rework circuit breaker, not routine bureaucracy. v5.2 approval challenges have a bounded lease. Wrong, stale or expired challenges cannot authorize later work.

Typical gated operations:

- a new material Planning cost envelope;
- `RESET_*` substantial invalidation;
- existing v5 risk gates for material expansion/rework.

Routine resume/reconciliation does not require approval merely because the provider/session changed.

## 11. Reset semantics

`RESET_*` means: invalidate only the active Work for that role and restart reasoning from the same authoritative inputs. It does **not** delete immutable Scope/history. Every public reset requires human approval.

Do not use reset to recover from an ordinary context/session interruption; send the matching `EXECUTE_*` command and let Workplan resume.

## 12. Resume / provider switch / machine transfer

For any interruption:

1. restore/open the repository;
2. make the AI read `Workplan/ENTRY_PROMPT.md`;
3. send `WORKPLAN_NEXT` if uncertain;
4. send the exact returned execution command.

Completed validated bounded units are not replayed merely because a session disappeared. At most the active bounded unit requires deterministic reconciliation/repetition.

## 13. System Workflow

```text
Human exact command
  -> ENTRY_PROMPT protocol adapter
  -> Workplan/scripts/command.py
  -> deterministic stage/surface validation
  -> INIT / RESUME / RESET gate
  -> approval when required
  -> machine-issued role/Task ticket
  -> bounded execution
  -> deterministic verification/state transition
  -> continuation projection
  -> exact next surface + exact next command
```

`STATE.json` remains internal authority. The command interface and continuation output are projections, not a second state database.

## 14. Recommended / tested reference stack

Capability requirements matter more than provider identity:

- **Research / Planning / Diagnosis / Recovery / Evaluation:** strong reasoning model with repository/tool access when needed.
- **ExecutionManager:** VS Code-capable agent that can run deterministic tools and delegate a Builder.
- **Builder:** low-cost coding model with sufficient context for one bounded immutable Task.

Reasoning strength and context size are different properties. Prefer selective retrieval and durable checkpoints over loading the whole repository.

Exact commercial model availability must be reverified when a release is prepared. Reference model identity is never workflow authority.

## 15. Worked examples

### Planning stopped by provider limit

New provider/session -> `ENTRY_PROMPT.md` -> `EXECUTE_PLANNING`. Workplan returns RESUME; no old-chat summary and normally no new approval.

### Wrong-stage command

If stage is PLANNING and the user sends `EXECUTE_EVALUATION`, Workplan returns `REJECTED`, the current stage and allowed commands. No workflow mutation occurs.

### Builder fails beyond local bound

VS Code stops at a deterministic handoff -> External AI -> `ENTRY_PROMPT.md` -> `EXECUTE_DIAGNOSIS`.

### User intentionally restarts Planning

Send `RESET_PLANNING` -> Workplan issues a bounded approval challenge -> human runs only the displayed `approve.py` command -> resend `RESET_PLANNING` -> active Planning Work is invalidated -> `EXECUTE_PLANNING` starts from the authoritative Scope.

### Approval expires

No expensive/reset action runs. Workplan clears the expired authorization while leaving the underlying lifecycle stage intact. Reissue the original command to request a new challenge if still desired.

### New cycle after closure

`WORKPLAN_NEXT` returns External AI / `EXECUTE_RESEARCH`. New Research output is placed into a clean `Workplan/ingest/`.

## 16. What users may edit

Users may edit their project files and prepare Research handoff under `Workplan/ingest/`. Normal users should not manually edit `Workplan/control/STATE.json`, Work metadata, tickets, digests or generated history.

## 17. Advanced tooling

Advanced users/agents may inspect `Workplan/scripts/tools/*.py`, manifests, projections and status output, but must not bypass the public command/approval authority rules when initiating normal workflow execution.
