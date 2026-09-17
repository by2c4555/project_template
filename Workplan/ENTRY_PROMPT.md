# Workplan Universal Entry Protocol — v5.2.0

This is the single AI bootstrap entrypoint for Project Template Workplan, regardless of provider or surface.

## Authority

Natural-language conversation is **discussion only**. It never authorizes workflow execution, reset, role selection, Task selection, approval, or state mutation.

Workflow execution starts only from an exact public Workplan command. Do not paraphrase, infer, or substitute commands.

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

When the user sends an exact command:

1. Submit that exact command to the deterministic command interface. Do not decide stage, role, INIT/RESUME/RECONCILE, approval need, Task, or next surface yourself.
2. External AI uses:
   `python Workplan/scripts/command.py <COMMAND> --surface EXTERNAL_AI --tool "<provider/tool>" --model "<model>"`
3. VS Code Workplan agents use:
   `python Workplan/scripts/command.py <COMMAND> --surface VS_CODE --tool "vscode" --model "<model>"`
4. If the result is `REJECTED`, do not reinterpret the request. Report the machine reason and allowed commands.
5. If the result is `APPROVAL_REQUIRED`, stop. Display the exact human command. Never execute `Workplan/scripts/approve.py` for the user.
6. After the human grants approval, re-submit the original exact command. Do not continue from chat inference.
7. If an accepted external command returns a role constitution and Action/Resume Ticket, read the named constitution and execute only that ticket.
8. If `EXECUTE_IMPLEMENTATION` is accepted, follow only the deterministic execution machine entry and its issued Builder tickets. Re-query the public command after bounded units or a surface handoff.
9. At stage completion or uncertainty, use `WORKPLAN_NEXT`; never reconstruct workflow from conversation history.

## Discussion mode

Questions, design discussion, explanation, review, comparison, and hypothetical language do not start Workplan execution. Example: “How should Planning work?” is discussion. Only the exact token `EXECUTE_PLANNING` requests Planning execution.

## Durable-state rule

Repository Workplan state and machine-issued tickets are authoritative. Chat/session/provider/process state is disposable. Prior conversation may be supplementary context only when the current ticket permits it; it never changes Scope or authority.
