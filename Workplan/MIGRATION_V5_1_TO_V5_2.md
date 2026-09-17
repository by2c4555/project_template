# Migration v5.1.0 -> v5.2.0

v5.2 preserves v5.1 durable state/Work/Task concepts but changes the normal human/AI entry protocol.

## User-visible changes

- Bootstrap every AI surface from `Workplan/ENTRY_PROMPT.md`.
- Replace free-form `Continue Workplan.` with exact public commands, especially `EXECUTE_IMPLEMENTATION` in VS Code.
- Normal users no longer select external role prompt files.
- `WORKPLAN_NEXT` is the canonical non-mutating way to discover the next surface/command.
- Public `RESET_*` commands are approval-gated explicit invalidations.
- Approval challenges expire after a bounded lease.

## State/schema

The shipped clean template uses workflow version `5.2.0` and state schema `5`. Existing in-flight v5.1 projects require an explicit migration tool/process before their state is treated as v5.2; do not hand-edit active state to change versions.
