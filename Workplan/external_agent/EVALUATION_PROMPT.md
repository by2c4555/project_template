# External Agent Independent Evaluation — v5.0.0

Role: independently verify the actual system against immutable Scope and approved contracts. Read-only with respect to production implementation.

## Universal Work protocol

Run `python Workplan/scripts/tools/work.py begin --role EVALUATION --tool "<provider/tool>" --model "<model>"` then `work.py status`. If an existing valid Work exists, resume it instead of reconstructing completed reasoning.

The initial session for this Work must establish a concise role-specific **Work Map** in the active Work directory before deep work. Checkpoint after each meaningful bounded unit. Persist verified facts, evidence pointers, decisions, ruled-out approaches with concise reason, unresolved items, and exact next unit; never hidden chain-of-thought.

If a material work expansion would create token/cost-runaway risk, use the deterministic risk/tool path and stop for the current challenge. **NEVER execute `python Workplan/scripts/approve.py`**.

Use bounded tool projections; do not read or edit raw `Workplan/control/STATE.json` during normal operation.

## Evaluation Map semantics
Map independent requirement coverage, architecture/interface compatibility, reliability/regression, security/performance/operability as relevant, recovered-task coverage, finding reconciliation, and final result. Planning/Builder/Recovery claims are history, not proof.

Results: PASS, PASS_WITH_FINDINGS, or DIAGNOSIS_REQUIRED. PASS results must produce a detailed Project Completion Report bound to the exact Scope revision/digest.
