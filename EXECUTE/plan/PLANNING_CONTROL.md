# Planning & Approval Control Contract — v4.3.2

`EXECUTE/control/STATE.json` is authoritative. Markdown status files are generated views.

## Core invariants

1. **Chat is feedback, never implementation authority.**
2. **No material decision -> no speculative Task/package expansion.**
3. `AWAITING_MATERIAL_FEEDBACK` and `PLAN_READY` are terminal states for the current Codex invocation.
4. The planning agent may call machine planning gates, but may never call human approval gates.
5. `approve_plan.py` is interactive-TTY only and binds approval to the exact Cycle, immutable Scope revision/digest, Planning revision, Task count, manifest, and SHA-256 package digest.
6. Task contracts are immutable after approval. Runtime Task state is stored only in `STATE.json`.
7. Any active Scope Snapshot or approved-package integrity failure blocks later Task dispatch. A material scope change requires a new Scope revision and invalidates/revises Planning authority.
8. Closed validated cycles are immutable; new external scope is captured as a fresh cycle-scoped Scope Snapshot with no inherited execution authority.

## Planning flow

Before Planning, `start_cycle.py` or `import_scope.py` must have captured the external handoff as the active immutable `SCOPE_NNN`. Planning records `based_on_scope_revision` + `based_on_scope_digest`.

```text
IN_PROGRESS
  ├─ material unknowns > 0 -> AWAITING_MATERIAL_FEEDBACK -> STOP
  │                           user chat -> resume/revise
  └─ material unknowns = 0 -> authorize-expansion
                              -> compile Plan/Tasks/compiled context
                              -> mark-plan-ready
                              -> PLAN_READY -> STOP
                                    ├─ chat feedback -> resume/revise
                                    └─ human runs approve_plan.py -> APPROVED
```

## Machine commands

```bash
python scripts/planning_gate.py status
python scripts/planning_gate.py hold-material-feedback --unknowns N
python scripts/planning_gate.py resume-feedback
python scripts/planning_gate.py begin-revision --reason "..."
python scripts/planning_gate.py set-material-zero
python scripts/planning_gate.py authorize-expansion
python scripts/planning_gate.py mark-plan-ready
```

## Human gate

```bash
python scripts/approve_plan.py
```

The approval script intentionally accepts no `--yes`, no static confirmation token, and no approval phrase from chat. It requires a live interactive terminal challenge.

This is an accidental-flow/token-runaway barrier, not a security boundary against a malicious process with full control of the user's local machine.
