# Changelog

## 5.2.0 — Deterministic Human Command & Continuation Protocol

- Added universal AI bootstrap `Workplan/ENTRY_PROMPT.md` across External AI and VS Code surfaces.
- Added exact public workflow commands and deterministic `Workplan/scripts/command.py` validation by lifecycle stage and surface.
- Separated natural-language discussion from workflow execution authority.
- Added deterministic INIT/RESUME selection for external reasoning Work; normal users no longer choose role prompt files.
- Replaced normal VS Code `Continue Workplan.` UX with exact `EXECUTE_IMPLEMENTATION` intent.
- Added `WORKPLAN_STATUS` and `WORKPLAN_NEXT` bounded projections for universal continuation/recovery.
- Added approval-gated `RESET_*` commands that invalidate only targeted active Work while preserving immutable Scope/history.
- Added bounded approval challenge expiry and explicit `EXPIRED` handling.
- Unified lifecycle handoffs around exact next surface/command projections.
- Added command-protocol executable validation and v5.1 -> v5.2 migration guidance.

## 5.1.0 — Deterministic Control Plane & Capability-Based Work

- Added explicit untrusted `Workplan/ingest/` boundary, deterministic validation receipts and separate package/scope digests.
- Added Planning ingest revalidation and accepted-input archive binding before `PLAN_READY`.
- Added generation-fenced Work ownership and stale mutation rejection.
- Added bounded Action/Resume Tickets and machine-computed reconciliation.
- Added progressive reason-based context requests that do not expand authority.
- Added stable external Work entry with role derived from lifecycle state.
- Added deterministic ExecutionManager routing, Task selection/dispatch/resume and machine-enforced repair limits.
- Preserved exact challenge approval binding, immutable Scope/package integrity, Diagnosis/Recovery separation, independent Evaluation and Completion Report closure.
- Reduced operational prompt burden to small semantic role constitutions after deterministic enforcement existed.
- Added v5.0 -> v5.1 migration guidance and expanded executable release validation.

## 5.0.0 — Workplan control plane

Introduced durable Workplan state, universal resumability, cross-machine continuation, mapped expensive reasoning, bounded Builder work, single challenge-based approval, independent Evaluation and Diagnosis/Recovery separation.
