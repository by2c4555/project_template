# Use Case 01 — External Research -> Validated Ingest

1. `WORKPLAN_NEXT` routes a new Cycle to `EXECUTE_RESEARCH` on `EXTERNAL_AI`.
2. The command result selects `Workplan/external_agent/RESEARCH_INSTRUCTION.md`, which requires `RESEARCH_POTOCAL_PROMPT.md` and `templates/PROJECT_DETAILS_TEMPLATE.md`.
3. External Research establishes product WHAT/WHY, resolves material product-scope unknowns, and builds the Source / Evidence Map.
4. Research writes `Workplan/ingest/project_details.md` plus only declared physical files under `Workplan/ingest/docs/raw/`.
5. Supporting metadata uses canonical logical `Workplan/docs/raw/*` paths.
6. `python Workplan/scripts/tools/ingest.py check` validates protocol marker, required sections, path safety, file presence, and package/scope digests.
7. Only `INGEST_VALID: PASS` permits Scope import. Planning must not begin from an unvalidated handoff.

Research ends at the ingest boundary; it does not create implementation Tasks or production code.
