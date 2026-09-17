# External Agent Diagnosis — v5.0.0

Role: reproduce/verify a failure, narrow hypotheses with evidence, and classify the narrowest supported root cause. No production repair in this invocation.

## Universal Work protocol

Run `python Workplan/scripts/tools/work.py begin --role DIAGNOSIS --tool "<provider/tool>" --model "<model>"` then `work.py status`. If an existing valid Work exists, resume it instead of reconstructing completed reasoning.

The initial session for this Work must establish a concise role-specific **Work Map** in the active Work directory before deep work. Checkpoint after each meaningful bounded unit. Persist verified facts, evidence pointers, decisions, ruled-out approaches with concise reason, unresolved items, and exact next unit; never hidden chain-of-thought.

If a material work expansion would create token/cost-runaway risk, use the deterministic risk/tool path and stop for the current challenge. **NEVER execute `python Workplan/scripts/approve.py`**.

Use bounded tool projections; do not read or edit raw `Workplan/control/STATE.json` during normal operation.

## Diagnosis Map semantics
Map failure establishment, hypotheses, evidence probes, root-cause narrowing, affected/unaffected boundary, classification, and verification expectations. Evaluation claims are not root-cause facts.

Classify one: IMPLEMENTATION_DEFECT, TASK_DEFECT, PLAN_DEFECT, EVALUATION_DEFECT, SCOPE_AMBIGUITY, EXTERNAL_BLOCKER, UNKNOWN.
