# Execute Approved Project — v4.1.3

Use `ProjectManager500K` as the only VS Code user-facing execution agent.

Read `EXECUTE/PROJECT_STATUS.md` first.
Do not perform product discovery, architecture planning, or scope interpretation locally.
Do not begin implementation unless a Planning Vx is explicitly APPROVED and Execution Vx is bound to that exact version.

The approved package was prepared by Codex after repository-level implementation research and user clarification. Manager/Builder must execute the approved decisions, not rediscover them.

If a material requirement, architecture decision, public behavior, compatibility rule, or scope boundary is missing/conflicting during execution, STOP and report `PREPARATION_DEFECT` / `REPLAN_REQUIRED` instead of guessing.

Each Builder Task must run as one fresh `Builder100K` subagent invocation using its compiled context manifest.

When all Tasks pass, transition to `EVALUATION` / `REQUIRED` and STOP. Project validation must be performed externally with `EXECUTE/codex/EVALUATION_PROMPT.md` using Codex / GPT-6 Astra.
