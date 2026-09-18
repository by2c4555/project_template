# Migration: Project Template v5.3.1 -> v5.3.2

v5.3.2 is a constitution/architecture-alignment hardening patch. The durable workflow state schema remains **schema 6** and the canonical runtime hierarchy remains `Cycle -> Phase -> Task -> Attempt`.

## What changes

1. Project Template development authority moves from the single `Workplan/Objective_dev.md` file into the human-owned `Workplan/development_constitution/` package.
2. `Objective_dev.md` is removed; current documentation references `development_constitution/OBJECTIVE.md`.
3. `REFERENCE_ARCHITECTURE.md` becomes the canonical architectural interpretation of the Development Objective.
4. `DEVELOPMENT_PROMPT.md` becomes the entry guidance for AI used to develop Project Template itself.
5. Every constitution file declares on its first line that AI may read it but must not edit, modify, rewrite, move, rename, or delete it. Constitution updates are performed externally by the repository owner.
6. Manager/Builder documentation is tightened: Manager owns Task-local software debugging/repair reasoning; Builder executes bounded implementation and must return unexpected failures instead of inventing an autonomous repair loop.
7. Runtime schema and normal lifecycle are unchanged.

## Safe state migration

Do not edit `STATE.json` manually. After installing the v5.3.2 release files, run:

```bash
python Workplan/scripts/migrate_v531_to_v532.py
```

Migration is permitted only when:

- current workflow version is `5.3.1`;
- schema version is `6`;
- `active_work` is `null`;
- `pending_approval` is `null`.

The migration changes only workflow-version/state-sequence metadata. It does not rewrite Scope, Planning Package, Phase, Task, Attempt, evidence, or issue authority.

## Constitution migration

The canonical development files after migration are:

```text
Workplan/development_constitution/README.md
Workplan/development_constitution/OBJECTIVE.md
Workplan/development_constitution/REFERENCE_ARCHITECTURE.md
Workplan/development_constitution/DEVELOPMENT_PROMPT.md
```

`Workplan/Objective_dev.md` must not remain in the v5.3.2 release.

If a future requested version conflicts with the Development Constitution, AI reports the conflict and the repository owner updates the constitution externally before development continues.
