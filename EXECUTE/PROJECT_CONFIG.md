# Project Configuration — v4.3.2

## Controlled boundary

v4.3 controls only work after external scope handoff is manually handed into the VS Code repository. External Web AI is outside this runtime and remains a manual scope/product/evidence layer.

```text
External Research handoff
(project_details.md + useful docs/raw/*)
        │ manual copy
        ▼
Scope Snapshot (Python, SHA-256)
        │
════════ v4.3.2 controlled boundary ════════
Change Cycle -> Codex Planning -> Human Plan Approval
             -> Manager/Builder Execution
             -> Diagnosis -> Human Recovery Approval -> Recovery -> Human Resume
             -> Human Evaluation Start -> Codex Evaluation -> Machine Finalize
             -> CLOSED_VALIDATED
═══════════════════════════════════════════
        │ new external scope
        ▼
New Change Cycle (no inherited approval)
```

## Authority model

- **External scope layer:** WHAT / WHY / product decisions / next-version or post-validation debug scope.
- **Codex Planning:** repository research, HOW, architecture, immutable Plan/Task compilation; stops at PLAN_READY.
- **ProjectManager500K:** local orchestration only; cannot mutate authoritative workflow state directly.
- **Builder100K:** one bounded immutable Task; cannot mark PASS or dispatch future Tasks.
- **Codex Diagnosis:** root-cause analysis only; cannot repair in the same invocation.
- **Codex Recovery:** repair only after a human recovery approval.
- **Codex Evaluation:** one authorized read-only evaluation attempt.
- **Python control layer:** owns authoritative state transitions, integrity checks, counters, and transition ledger.
- **User/operator:** owns high-cost human gates.

## Fundamental invariants

1. `EXECUTE/control/STATE.json` is authoritative. Markdown status files are generated views.
2. Agents may produce artifacts/evidence; agents may not grant themselves authority.
3. Natural-language chat never counts as implementation approval, recovery approval, resume approval, or evaluation authorization.
4. Expensive phase boundaries require interactive human scripts.
5. Routine within-phase transitions use machine gates without user interaction.
6. Approval is bound to one exact Change Cycle, immutable Scope revision/digest, Planning version/revision, manifest, Task count, and SHA-256 package digest.
7. Scope Snapshot integrity failure or approved package mutation -> execution hard stop.
8. Task contracts are immutable; Task runtime status/counters live in machine state.
9. Ordinary Task dispatch is one-time. Local repair attempts are machine-counted.
10. Manager context accumulation is bounded by a dispatch batch; reaching the limit forces a fresh Manager conversation.
11. Builder failure beyond bounded repair -> Issue + hard stop.
12. Diagnosis and Recovery are separate invocations.
13. Recovery verification never authorizes resume by itself.
14. Evaluation authorization is one-attempt only; re-evaluation requires a new user gate.
15. A validated Cycle is immutable. New feature/version/post-validation debug scope always starts a new Cycle.
16. No approval/execution authority carries across a Cycle boundary.

## Human-operated gates

```text
PLAN_READY                         -> scripts/approve_plan.py
Manager batch limit                -> scripts/reset_manager_batch.py
IMPLEMENTATION_DEFECT diagnosis    -> scripts/approve_recovery.py
verified execution recovery        -> scripts/resume_execution.py
execution complete / re-evaluation -> scripts/start_evaluation.py
```

These scripts require an interactive TTY challenge and intentionally do not accept `--yes` or a static confirmation phrase.

## Machine gates

```text
scope capture/revision -> start_cycle.py / import_scope.py
planning interaction/package -> planning_gate.py
task dispatch/repair/pass/fail/completion -> execution_gate.py
diagnosis registration/routing -> diagnosis_gate.py
recovery verification -> recovery_gate.py
evaluation result/close or Issue creation -> finalize_evaluation.py
package/context/template integrity -> validate_v4.py / context_guard.py
bounded command output -> safe_exec.py
```

## Change-cycle semantics

One Cycle represents one externally scoped change until independently validated.

- Evaluation PASS/PASS_WITH_FINDINGS -> `CLOSED_VALIDATED`.
- A later feature/version/refactor/newly discovered bug supplied as new scope -> new Cycle.
- Evaluation failure before validation stays in the same Cycle through Diagnosis/Recovery/Replan/Re-evaluation.
- TASK/PLAN defect may create a new Planning Vx inside the same open Cycle; old approval is superseded and a new approval is mandatory.

## Root-cause classifications

Exactly one primary classification:

- `IMPLEMENTATION_DEFECT`
- `TASK_DEFECT`
- `PLAN_DEFECT`
- `EVALUATION_DEFECT`
- `SCOPE_AMBIGUITY`
- `EXTERNAL_BLOCKER`
- `UNKNOWN`

## Token-safety controls

- unresolved material decisions block Task expansion;
- external handoff is captured into immutable Scope Snapshots;
- exact approved Scope digest + approved-package digest checked on execution/recovery/evaluation transitions;
- Builder context preflight target/hard limit;
- machine-counted local repair budget;
- ordinary Task can be dispatched only once;
- Manager dispatch-batch context reset (default 10 Tasks);
- verbose command output stored in full logs while agent-visible output is bounded;
- no diagnosis+repair chain in a single invocation;
- no automatic re-evaluation loop.

## Model policy

```yaml
local_models:
  ProjectManager500K:
    minimum_context_tokens: 512000
  Builder100K:
    minimum_context_tokens: 102400
    controlled_target_tokens: 40000
    controlled_max_tokens: 52000
external_intelligence:
  environment: Codex
  recommended_model: GPT-6 Astra
```

## Safety scope

Interactive human gates are designed to prevent accidental agent flow and token/cost runaway in the normal tool workflow. They are not a security sandbox against a malicious process with full control of the user's local machine.
