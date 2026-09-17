# Use Case 11 — Exact Human Command Protocol

1. Any AI surface first reads `Workplan/ENTRY_PROMPT.md`.
2. Free-form discussion does not mutate Workplan.
3. The human sends an exact command such as `EXECUTE_PLANNING`.
4. The AI submits that exact token to `Workplan/scripts/command.py` with its current surface.
5. Wrong-stage/wrong-surface commands are rejected without reinterpretation.
6. Workplan deterministically chooses INIT/RESUME and any approval requirement.
7. Approval-required commands stop until the human uses `scripts/approve.py` before the challenge lease expires.
8. Normal resume after provider/session loss does not require a new approval.
9. `RESET_*` invalidates only targeted active Work and preserves immutable Scope/history.
10. `WORKPLAN_NEXT` supplies the exact next surface and command at every normal handoff.
