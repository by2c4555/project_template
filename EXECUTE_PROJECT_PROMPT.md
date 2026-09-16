# Execute Approved Project — v4.1

Use `ProjectManager500K` as the only VS Code user-facing execution agent.

Read `EXECUTE/PROJECT_STATUS.md` first.
Do not perform planning locally.
Do not begin implementation unless a Planning Vx is explicitly APPROVED and Execution Vx is bound to that exact version.

Each Builder Task must run as one fresh `Builder100K` subagent invocation using its compiled context manifest.

When all Tasks pass, transition to `EVALUATION` / `REQUIRED` and STOP. Project validation must be performed externally with `EXECUTE/codex/EVALUATION_PROMPT.md` using Codex / GPT-6 Astra.
