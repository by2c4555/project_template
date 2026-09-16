# Planning & Compilation Compatibility Entry — v4.3.0

Use `EXECUTE/codex/IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md` as the canonical planning prompt.

This file exists only for compatibility with older operator habits. Do not use v4.2-style `PLAN_REVIEW -> AWAITING_USER_APPROVAL` semantics. v4.3 has a single `PLAN_READY` human boundary and only the interactive `scripts/approve_plan.py` can authorize implementation.
