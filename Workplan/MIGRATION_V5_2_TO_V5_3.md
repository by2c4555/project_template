# Migration: Project Template v5.2.0 -> v5.3.0

v5.3.0 changes workflow authority from schema 5 to schema 6 and introduces first-class `Phase` and `Attempt` state plus immutable Builder tickets and deterministic Task/Phase gates.

## Safety policy

**Do not silently upgrade in-flight v5.2 execution authority.** v5.2 active Builder/repair/recovery state does not contain enough information to prove equivalent v5.3 Phase/Attempt/ticket bindings.

Safe migration requires a quiescent boundary:

- preferred: finish/close the v5.2 cycle before switching the template; or
- explicitly reset/discard in-flight v5.2 execution and re-run Planning under v5.3.

The v5.3 state loader rejects workflow/schema mismatches with `MIGRATION_REQUIRED`; it does not guess old semantics.

## Planning packages

Existing `PLAN_READY` packages should be recompiled/revalidated under v5.3 before implementation. v5.3 expands package authority and gate semantics.

For a legacy/simple flat plan with no `PHASES.json`, v5.3 deterministically maps all Tasks to implicit `PHASE_001`. If an explicit multi-phase `PHASES.json` exists, every Task must declare `phase_id`.

Legacy Task contracts without `max_repairs` receive the v5.3 default of 2. Explicit values must be in `0..5`.

## Active Work

Do not reinterpret an old active Work as a v5.3 Attempt. v5.3 Builder execution requires a fresh Attempt and ticket with current Scope/Plan/Phase/Task digests. Recovery additionally requires a Recovery Contract digest.

Persisted v5.3 Work bindings are issue-time immutable. Resume compares rather than overwrites them.

## Builder naming

The logical runtime role is `Builder`. `Builder100K` may remain only as a compatibility alias for older local configuration; runtime authority must not depend on that model-sized name.

## Integrity

Regenerate the release manifest after applying the v5.3 files:

```bash
python Workplan/scripts/integrity.py generate
python Workplan/scripts/validate.py --full
```

Old manifests containing `__pycache__`, `*.pyc`, temp/cache/editor-local/runtime-local entries are invalid.

## Rollback

A repository that has begun v5.3 schema-6 execution should not be downgraded in place to v5.2 schema 5. Restore a known v5.2 repository/state snapshot or start a fresh v5.2 cycle instead of attempting to reinterpret v5.3 Attempts/Tickets as v5.2 state.
