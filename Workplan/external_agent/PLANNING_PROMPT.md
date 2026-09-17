# External Agent Planning — v5.0.0

Role: research the repository, remove material technical uncertainty once, and compile an execution-ready immutable package. Do not implement production code.

## Universal Work protocol

Run `python Workplan/scripts/tools/work.py begin --role PLANNING --tool "<provider/tool>" --model "<model>"` then `work.py status`. If an existing valid Work exists, resume it instead of reconstructing completed reasoning.

The initial session for this Work must establish a concise role-specific **Work Map** in the active Work directory before deep work. Checkpoint after each meaningful bounded unit. Persist verified facts, evidence pointers, decisions, ruled-out approaches with concise reason, unresolved items, and exact next unit; never hidden chain-of-thought.

If a material work expansion would create token/cost-runaway risk, use the deterministic risk/tool path and stop for the current challenge. **NEVER execute `python Workplan/scripts/approve.py`**.

Use bounded tool projections; do not read or edit raw `Workplan/control/STATE.json` during normal operation.

## Planning Map semantics
Stages/topics should cover only needed repository baseline, uncertainty/decisions, architecture synthesis, execution decomposition, and package compilation. Minor map refinement is allowed; material expansion requires the risk gate.

Product/scope ambiguity is user feedback, not token approval. Stop and request material feedback instead of inventing scope.
