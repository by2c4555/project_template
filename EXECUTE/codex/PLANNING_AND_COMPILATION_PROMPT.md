# Planning & Compilation Compatibility Entry — v4.3.2

Use `EXECUTE/codex/IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md` as the canonical planning prompt.

The active immutable Scope Snapshot referenced by `EXECUTE/control/STATE.json` is the product/scope authority for Planning. `Research_Vx` is not used in v4.3.2.

Do not use v4.2-style `PLAN_REVIEW -> AWAITING_USER_APPROVAL` semantics. v4.3 has a single `PLAN_READY` human boundary and only the interactive `scripts/approve_plan.py` can authorize implementation.
