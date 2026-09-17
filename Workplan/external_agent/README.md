# External Agent Roles — v5.3.0

Normal users do **not** select role prompt files.

All External AI sessions bootstrap from:

```text
Workplan/ENTRY_PROMPT.md
```

The user then sends an exact public command such as `EXECUTE_PLANNING` or `EXECUTE_DIAGNOSIS`. `Workplan/scripts/command.py` validates durable lifecycle state and surface, determines INIT/RESUME, applies approval gates, and returns the machine-selected role constitution plus Action/Resume Ticket.

Files in this directory are semantic role constitutions. They never grant workflow authority by themselves.
