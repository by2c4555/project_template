# External Agent Recovery — v5.0.0

Role: perform the minimum complete repair for one evidence-backed IMPLEMENTATION_DEFECT while preserving approved scope/contracts.

## Universal Work protocol

Run `python Workplan/scripts/tools/work.py begin --role RECOVERY --tool "<provider/tool>" --model "<model>"` then `work.py status`. If an existing valid Work exists, resume it instead of reconstructing completed reasoning.

The initial session for this Work must establish a concise role-specific **Work Map** in the active Work directory before deep work. Checkpoint after each meaningful bounded unit. Persist verified facts, evidence pointers, decisions, ruled-out approaches with concise reason, unresolved items, and exact next unit; never hidden chain-of-thought.

If a material work expansion would create token/cost-runaway risk, use the deterministic risk/tool path and stop for the current challenge. **NEVER execute `python Workplan/scripts/approve.py`**.

Use bounded tool projections; do not read or edit raw `Workplan/control/STATE.json` during normal operation.

## Recovery Map semantics
Map repair boundary, bounded change units, targeted verification, regression/integration verification, and Resolution knowledge. Verify working-tree/baseline state on resume because Recovery may modify production code.
