# Execute Project

Use the `ProjectManager` custom agent as the only user-facing entry point.

Read `EXECUTE/PROJECT_STATUS.md` first and resume only from persisted project state.
Do not preload project details, Knowledge, Plan, Tasks, history, Issues, source files, or logs in the main chat.

ProjectManager must invoke Planner/Builder work through isolated custom subagents.
One Builder Task or Integration Gate equals one fresh subagent invocation.
One Planner transaction equals one fresh subagent invocation.

Never reconstruct authoritative project state from chat history.
