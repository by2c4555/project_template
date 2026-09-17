# Migration: Project Template v5.3.0 -> v5.3.1

v5.3.1 is a hardening patch. The durable workflow state schema remains **schema 6** and the canonical hierarchy remains `Cycle -> Phase -> Task -> Attempt`.

The patch changes two boundaries and cleans obsolete release scaffolding:

1. VS Code agent cost/capability policy: `ExecutionManager` uses the user-selected model and delegates production implementation to the pinned `Project Builder Local` Builder alias. The canonical files are `.github/agents/manager.agent.md` and `.github/agents/builder.agent.md`; the old Builder100K compatibility agent is removed.
2. New Research handoffs must satisfy `EXTERNAL_RESEARCH_PROTOCOL_V1`, `Workplan/external_agent/RESEARCH_INSTRUCTION.md`, `Workplan/external_agent/RESEARCH_POTOCAL_PROMPT.md`, and the canonical Project Details section contract.
3. Duplicate/obsolete Research template/protocol paths and unrelated empty root placeholders are removed from the full v5.3.1 release.

## Existing accepted Scope/ingest

Already-accepted v5.3.0 ingest packages remain valid by immutable package/scope digest. v5.3.1 revalidates those bound legacy packages using the legacy ingest shape so an active accepted Cycle is not invalidated solely by this patch.

Any **new** Research handoff created after migration must use the v5.3.1 protocol/template.

## State migration

Do not edit `STATE.json` manually. After installing the v5.3.1 release files, run:

```bash
python Workplan/scripts/migrate_v530_to_v531.py
```

The migration is allowed only when:

- current state is workflow `5.3.0`, schema `6`;
- `active_work` is null;
- `pending_approval` is null.

It changes only the workflow version/audit transition; it does not reinterpret Phase/Task/Attempt contracts.

If a Work is active, finish or use the authoritative reset/continuation path first. This prevents an old live agent session from crossing the release boundary unnoticed.

## VS Code local Builder binding

Register the intended local/low-cost implementation model in VS Code with the language-model display name:

```text
Project Builder Local
```

The tracked Builder custom agent pins that alias. The concrete provider/model may be Qwen2.5-Coder, another local model, or another low-cost model that satisfies the bounded Builder ticket; workflow authority remains provider-neutral.

ExecutionManager does not declare a model, so it uses the model selected by the user in the VS Code Chat model picker.

## Research handoff migration

Do not rewrite already-accepted Scope solely to satisfy the new template.

For the next Research cycle, start from:

```text
Workplan/templates/PROJECT_DETAILS_TEMPLATE.md
```

and follow:

```text
Workplan/external_agent/RESEARCH_INSTRUCTION.md
Workplan/external_agent/RESEARCH_POTOCAL_PROMPT.md
```

## Validation

After migration/configuration, regenerate the release manifest only for release construction, not as a way to hide local modifications. For a clean release candidate run:

```bash
python Workplan/scripts/integrity.py generate
python Workplan/scripts/validate.py --full
```
