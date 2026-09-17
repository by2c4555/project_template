# Workplan Universal Entry Protocol — v5.3.0

This is the single AI bootstrap entrypoint for Project Template Workplan on every provider/surface.

## Authority

Natural-language conversation is discussion only. It never authorizes workflow execution, reset, role selection, Phase/Task/Attempt selection, approval, or state mutation.

Public workflow authority is an **exact literal token**. Do not trim, case-normalize, paraphrase, infer, or extract a command from prose.

## Exact public commands

- `WORKPLAN_STATUS`
- `WORKPLAN_NEXT`
- `EXECUTE_RESEARCH`
- `EXECUTE_PLANNING`
- `EXECUTE_IMPLEMENTATION`
- `EXECUTE_DIAGNOSIS`
- `EXECUTE_RECOVERY`
- `EXECUTE_EVALUATION`
- `RESET_PLANNING`
- `RESET_DIAGNOSIS`
- `RESET_RECOVERY`
- `RESET_EVALUATION`

## Required behavior

1. Submit the exact token to `Workplan/scripts/command.py`; never decide stage, role, INIT/RESUME, Phase, Task, Attempt, repair, or next surface yourself.
2. External AI uses `python Workplan/scripts/command.py <COMMAND> --surface EXTERNAL_AI --tool "<provider/tool>" --model "<model>"`.
3. VS Code uses `python Workplan/scripts/command.py <COMMAND> --surface VS_CODE --tool "vscode" --model "<model>"`.
4. On `REJECTED`, report the machine reason and allowed commands. Do not reinterpret intent.
5. On `APPROVAL_REQUIRED`, stop and show the exact human approval command. AI never executes `approve.py`.
6. After human approval, resubmit the original exact token; do not continue from conversational inference.
7. Accepted External-Agent commands return the machine-selected role constitution plus Action/Resume Ticket. Execute only that bounded Work.
8. Accepted `EXECUTE_IMPLEMENTATION` delegates routing to deterministic execution. Follow only the returned action and machine-issued Builder/Repair/Recovery Ticket.
9. After every bounded unit, failure, provider switch, or uncertainty, use `WORKPLAN_NEXT` rather than reconstructing state from chat.

## Durable-state rule

Repository state, immutable bindings, tickets, evidence, and checkpoints are authority. Chat/session/provider/process memory is disposable. Granted read context is supplementary and never expands production write authority.
