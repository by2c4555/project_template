# Changelog

## 5.0.0 — Workplan control plane

Breaking redesign from v4.4.0.

- Replaced top-level `EXECUTE/` + `scripts/` workflow surfaces with the `Workplan/` control plane.
- Added universal resume and cross-session/cross-machine continuation contracts.
- Added mapped resumable reasoning for Planning, Diagnosis, Recovery, and Evaluation.
- Added bounded Builder work checkpoints for interrupted Tasks.
- Replaced multiple human approval scripts with one challenge-based `approve.py` token-risk circuit breaker.
- Added AI-facing `approve_req.py` / `approve_res.py` isolation.
- Added minimal state projections; raw state is internal by default.
- Added `scripts/*.py`, `scripts/tools/*.py`, and `scripts/_core/` interface separation.
- Added required `USE_CASES/` coverage and behavioral validation scenarios.
- Preserved immutable scope/package integrity, bounded Builder repair, provider-neutral External Agents, independent Evaluation, Diagnosis/Recovery separation, reusable Resolution knowledge, and Completion Report cycle handoff.
