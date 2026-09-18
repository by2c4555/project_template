# ChatGPT Project Instructions — Project Template v5.3.2

Use the current repository Workplan as workflow authority. Repository/filesystem state is durable; chat history, memory, and model confidence are not authority.

## Bootstrap

For substantial work:

1. read `Workplan/VERSION` once;
2. read `Workplan/ENTRY_PROMPT.md`;
3. use `WORKPLAN_NEXT` to determine the exact next surface/command;
4. follow only the machine-selected role/ticket;
5. do not reconstruct workflow state from prior chat.

Use current repository implementation over old conversation claims whenever they disagree.

## Research

When `WORKPLAN_NEXT` selects `EXECUTE_RESEARCH`:

1. execute the exact command on the `EXTERNAL_AI` surface;
2. follow `Workplan/external_agent/RESEARCH_INSTRUCTION.md`;
3. follow `Workplan/external_agent/RESEARCH_POTOCAL_PROMPT.md`;
4. use `Workplan/templates/PROJECT_DETAILS_TEMPLATE.md` as the canonical handoff shape;
5. write the handoff to `Workplan/ingest/project_details.md`;
6. place only declared supporting evidence under `Workplan/ingest/docs/raw/`;
7. resolve every material product-scope unknown before `READY_FOR_PLANNING` / `product_scope_unknowns: 0`;
8. run `python Workplan/scripts/tools/ingest.py check` and require actual `INGEST_VALID: PASS`.

Research defines product WHAT/WHY and acceptance authority. It must not create implementation Tasks, modify production code, or treat `Workplan/development_constitution/OBJECTIVE.md` as user-project Scope.

## Planning

Planning starts only when Workplan selects `EXECUTE_PLANNING` and required human approval has been granted by the human. Planning owns architecture, interfaces, Phases, Tasks, authorized paths, verification contracts, evidence requirements, and repair budgets within the approved Scope.

Never execute `approve.py` on behalf of the human.

## VS Code implementation

Use the workspace `ExecutionManager` custom agent for `EXECUTE_IMPLEMENTATION`.

- Manager model: selected by the user in the VS Code Chat model picker.
- Builder model: pinned by `.github/agents/builder.agent.md` to `Project Builder Local`.
- Manager has no production edit tool.
- Normal production implementation is delegated to Builder.
- Do not override Builder's model when invoking it.

Workplan, not either model, selects Phase/Task/Attempt and owns PASS/FAIL authority.

## Failure / recovery

On Task-local failure, Builder returns evidence and stops. ExecutionManager performs bounded local software debugging and supplies the Repair reason/strategy before Workplan issues a fresh Builder REPAIR Attempt. Local repair remains bounded (hard maximum 5); structural or exhausted failures route to External Diagnosis/Recovery. External Diagnosis and Recovery are reasoning-only; production correction returns through Builder and normal gates.

## Evaluation

When Workplan selects `EXECUTE_EVALUATION`, independently verify the current repository state against approved Scope/Planning authority and actual evidence. Do not accept Builder/Manager claims without durable evidence or required rechecks.

## Validation rule

Never claim a deterministic command, gate, test, migration, integrity check, or release validation passed unless it was actually executed successfully.
