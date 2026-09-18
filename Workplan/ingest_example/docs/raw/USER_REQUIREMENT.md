# Mock User Requirement — Research Handoff Simulation

This file is synthetic test evidence for Project Template v5.3.2 Research handoff validation. It is not a real product request.

Build a small local command-line notes application with these requirements:

- Target Python 3.11 or newer.
- Use only the Python standard library at runtime.
- No network access is required for normal operation.
- Support `notes add <text>` for non-empty note text and return a stable identifier.
- Support `notes list` and show all notes in deterministic identifier order.
- Support `notes delete <id>`.
- Deleting an unknown identifier must return a non-zero exit status with a clear error message.
- Notes must persist across separate command invocations using a local writable data file.
- GUI, web server/API, cloud synchronization, authentication, tagging, editing, import/export, and package-registry publishing are outside the requested scope.

For this mock validation, assume the target environment has Python 3.11+ and permits writing the local persistence file.
