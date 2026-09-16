# v4.3 Control Plane

This directory is the machine-governed control plane for the VS Code/Codex workflow.

## Authoritative files

- `STATE.json` — current workflow/cycle/scope/task/recovery/evaluation state.
- `TRANSITIONS.jsonl` — append-only transition audit ledger.
- `approvals/APPROVAL_xxxx.json` — immutable implementation approval records.
- `manifests/APPROVAL_xxxx_PACKAGE.json` — exact approved package SHA-256 manifests.
- `recovery_approvals/RECOVERY_APPROVAL_xxxx.json` — immutable broad-recovery approval records.

Do not hand-edit these files to advance the workflow. Use scripts in `scripts/`.

## State ownership

```text
Agent output/evidence
      ↓
Python validation/gate
      ↓
STATE.json transition
      ↓
TRANSITIONS.jsonl event
      ↓
Generated Markdown views
```

## Change Cycle

A Cycle is one externally scoped unit of change through independent validation.

```text
PLANNING
 -> EXECUTION
 -> EXECUTION_COMPLETE
 -> EVALUATION
 -> CLOSED_VALIDATED
```

Recovery/Replan states may interrupt the path before validation. A `CLOSED_VALIDATED` Cycle is immutable history. New external scope is captured as an immutable Scope Snapshot and creates the next Cycle.

## Approval scope

Implementation approval is not global. It is bound to:

```text
cycle_id
scope_revision
scope_digest
planning_version
planning_revision
package_digest
task_count
manifest_path
```

It cannot authorize another Cycle, another Scope revision, or another Planning revision.

## Runtime Task state

Approved `TASK_NNN.md` files are immutable contracts. Runtime state lives under the active Cycle's Execution object in `STATE.json`, including:

- status;
- dependencies;
- dispatch count;
- local repair count/budget;
- evidence path;
- recovery provenance.

## Human-operated high-cost gates

Human gates require an interactive TTY challenge. Agents must not call them:

- `approve_plan.py`
- `reset_manager_batch.py`
- `approve_recovery.py`
- `resume_execution.py`
- `start_evaluation.py`

## Threat model

The control plane is intended to stop accidental autonomous flow, stale approvals, retry loops, context accumulation, and high-cost phase transitions caused by model misunderstanding. It is not an OS sandbox and does not defend against a malicious process with unrestricted local-machine access.
