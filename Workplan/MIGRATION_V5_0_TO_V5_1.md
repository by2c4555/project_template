# Migration v5.0 -> v5.1

v5.1 is a clean authority migration, not a dual-mode compatibility layer.

1. Finish or explicitly abandon any active v5.0 Work/Cycle before migration.
2. Replace runtime/control-plane files with v5.1 and reset the shipped template state to schema 4 / `AWAITING_SCOPE`.
3. Move future Research handoffs from `Workplan/project_details.md` + `Workplan/docs/raw/*` to `Workplan/ingest/project_details.md` + `Workplan/ingest/docs/raw/*`.
4. External roles enter through `scripts/tools/external.py acquire`; they no longer reconstruct the Universal Work protocol from prompts.
5. Work mutations require the current generation from the capability ticket.
6. Execution users invoke `@ExecutionManager` / `Continue Workplan.`; users do not supply Task IDs.
7. Do not maintain both v5.0 direct-root scope input and v5.1 ingest as competing authority locations.
