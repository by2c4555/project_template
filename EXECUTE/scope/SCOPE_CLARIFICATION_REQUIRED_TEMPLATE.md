# Scope Clarification Required Vx

Use this artifact only when Codex/Diagnosis has proven that a **material product/scope decision** cannot be resolved from the active immutable Scope Snapshot or repository truth.

```yaml
artifact_kind: SCOPE_CLARIFICATION_REQUIRED
status: OPEN
cycle_id: CYCLE_NNN
current_scope_revision: SCOPE_NNN
current_scope_digest: sha256:...
origin: PLANNING | DIAGNOSIS
origin_artifact: path/to/source
```

## Material Gap

Describe the exact missing/ambiguous product or scope decision.

## Why It Blocks Technical Work

Explain which requirement, behavior, compatibility boundary, success criterion, or Task decomposition could change depending on the answer.

## What Is Already Known

Summarize verified scope/repository facts so External Research does not redo unrelated work.

## Requested External/User Resolution

State the smallest set of decisions or external facts needed.

## Return Path

Use External Research to update the cumulative handoff:

```text
EXECUTE/project_details.md
EXECUTE/docs/raw/*   # only if new evidence is useful
```

When the updated handoff is `READY_FOR_CODEX`, the user captures it with:

```bash
python scripts/import_scope.py --reason "<clarification resolved>"
```

This creates a new immutable `SCOPE_NNN`. Do not edit the old Scope Snapshot or Planning package in place.
