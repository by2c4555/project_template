# Execute Project — Single Entry Point

Version: 3.4.1 Lean

This is the single user-facing entry point for the AI project workflow.

## Hard Rules

1. Read `EXECUTE/PROJECT_STATUS.md` first.
2. Do not rely on previous chat history as project state.
3. Load only the procedure and project context required for the current phase.
4. Persist major state transitions before continuing.
5. Never skip a failed or blocked gate.
6. Never execute a task with an undersized Builder/model context.
7. Never guess secrets, credentials, API URLs, database URLs, hosts, ports, or access tokens.
8. `EXECUTE/docs/` is raw source material and must not be rewritten by AI workflow.
9. `EXECUTE/reference/` is writable only during PLANNING or REPLANNING.
10. During normal EXECUTION, `EXECUTE/reference/` is read-only.
11. If user input is required, persist the requirement and stop.
12. If project state is COMPLETE, report completion and stop.

## Startup

If `EXECUTE/PROJECT_STATUS.md` is missing, create an INITIALIZE state before any other work.

Then read:

- `EXECUTE/PROJECT_CONFIG.md`
- `EXECUTE/PROJECT_STATUS.md`
- `.github/skills/project-orchestration/SKILL.md`

## Phase Routing

### INITIALIZE / KNOWLEDGE / PLANNING

Use the configured Planning model.

Required sequence:

```text
INPUT_VALIDATION
-> KNOWLEDGE_REFINEMENT
-> KNOWLEDGE_VALIDATION
-> IMPLEMENTATION_PLANNING
-> PLAN_VALIDATION
-> RISK_VALIDATION_DESIGN
-> TASK_GRAPH_DESIGN
-> CONTRACT_TEST_GENERATION
-> TASK_PACK_VALIDATION
-> EXECUTION_READY
```

Do not generate executable task work before the Plan passes validation.

### EXECUTION

Do not replay Planning.

Load only:

```text
PROJECT_STATUS
-> active Task metadata
-> required Builder Agent
-> Builder Skill
-> active Task
-> exact Knowledge/Plan/History/Issue refs
-> exact src/test Context Manifest
```

Do not load `project_details.md`, raw `docs/`, full `reference/`, full Plan, all tasks, all history, or all issues by default.

### REPLANNING

Stop normal Builder execution.

Use the configured Planning/Replanning model.

Load only the current Plan, source Issue, affected Knowledge IDs, selected evidence, affected Tasks, and relevant raw documents if needed.

Preserve completed work and replan only affected scope.

### WAITING_USER

Report the exact persisted `next_action` and stop.

### COMPLETE

Report completion and stop.

## Environment Safety Gate

If a task requires external API/database/service access:

1. read the task Environment Contract;
2. if root `.env.user` is missing, create only required keys with `__REQUIRED__`;
3. never invent values;
4. validate `.env.user`;
5. validate `EXECUTE/.env.execute`;
6. if required user configuration is missing or invalid:
   - persist `WAITING_USER`;
   - report exact variable names;
   - stop before external access.

`.env.user` is user-owned and never committed.

`EXECUTE/.env.execute` is workflow-owned, committed, and must contain no secrets.

## Resume Rule

After disconnect, model switch, context compaction, or a new chat:

```text
read PROJECT_STATUS
-> validate current incomplete artifact
-> resume current stage
```

Never restart from conversational memory alone.
