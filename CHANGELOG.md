# Changelog

## v4.0.1 — Context Isolation Correction

v4.0.1 fixes the principal context-accumulation defect in v4.0.0.

### Changed

- ProjectManager is now the only user-facing agent and uses the VS Code `agent` tool to invoke named Planner/Builder custom agents as isolated subagents.
- Every Builder Task, retry, escalation, and Integration Gate requires a fresh subagent invocation.
- Planning is checkpointed into five transactions; every transaction uses a fresh Planner invocation.
- Planner and Builders have `agents: []` and cannot recursively spawn subagents.
- Tool surfaces are explicitly limited by role.
- Result Capsules replace transcript/log forwarding between agents.
- Added local command/search/log/diff output budgets.
- Added deterministic `scripts/context_guard.py` preflight for Task-listed context.
- Task template now declares context and output budgets.
- Validator now checks structural, architecture, and policy invariants rather than file presence only.
- Conversation history is explicitly non-authoritative; disk artifacts are persistent project memory.

### Runtime model note

The template enforces minimum documented capacities in policy/instructions:
- Planner512K >= 524288 tokens
- Builder128K >= 131072 tokens
- Builder256K >= 262144 tokens

Provider-specific model names are not guessed because identifiers vary by Copilot/provider configuration. Run `scripts/configure_models.py` with the exact model identifiers and trusted documented capacities. The script pins `model:` into each role agent and writes `EXECUTE/MODEL_BINDINGS.json`. Unknown/unbound capacity blocks execution.

### Breaking behavior

`PASS` may auto-continue workflow routing, but it never permits reuse of the prior Task context. A retry also starts fresh and receives only persisted Task/Issue evidence.
