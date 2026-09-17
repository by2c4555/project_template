# Research Instruction — Project Template v5.3.1

This is the machine-selected Research role instruction for `EXECUTE_RESEARCH`.

## Authority

- Start only after `Workplan/scripts/command.py EXECUTE_RESEARCH --surface EXTERNAL_AI ...` returns `ACCEPTED`.
- `Workplan/ENTRY_PROMPT.md`, current repository state, the Research command result, and deterministic ingest validation are authoritative.
- This role does not approve Planning, create implementation Tasks, mutate production code, or choose execution authority.

## Required protocol

Follow all rules in:

`Workplan/external_agent/RESEARCH_POTOCAL_PROMPT.md`

Use:

`Workplan/templates/PROJECT_DETAILS_TEMPLATE.md`

as the canonical output shape.

## Required output

Produce:

- `Workplan/ingest/project_details.md`
- only necessary supporting files under `Workplan/ingest/docs/raw/`

The `project_details.md` control fields must include:

- `artifact_kind: PROJECT_DETAILS`
- `artifact_status: READY_FOR_PLANNING`
- `research_protocol: EXTERNAL_RESEARCH_PROTOCOL_V1`
- `product_scope_unknowns: 0`
- a valid inline `supporting_files: [...]` declaration

Supporting files are declared with logical `Workplan/docs/raw/...` paths even though physical ingest files are stored under `Workplan/ingest/docs/raw/`.

## Completion condition

Run:

```bash
python Workplan/scripts/tools/ingest.py check
```

Research is ready for Scope import only when the command actually reports `INGEST_VALID: PASS` and no material product-scope unknown remains.

Do not claim readiness from model confidence alone.
