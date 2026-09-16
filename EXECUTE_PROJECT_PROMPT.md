# Execute / Resume Approved Project — v4.2.0

Use `ProjectManager500K` as the only VS Code user-facing local execution agent.

Read first:

- `EXECUTE/PROJECT_STATUS.md`
- `EXECUTE/execution/EXECUTION_STATE.md`

## Start / Resume Rules

Do not perform product discovery, architecture planning, technical incident diagnosis, or scope interpretation locally.

Start ordinary implementation only when the exact Planning Vx is explicitly APPROVED and Execution Vx is bound to it.

Resume after an incident only when disk state proves:

- Issue = RESOLVED;
- blocked Task = PASS_RECOVERED;
- Diagnosis + Resolution artifacts exist;
- recovery verification = VERIFIED/PASS;
- execution status = READY_TO_RESUME;
- `resume_authorized: true`;
- recovery baseline + next Task are recorded.

Do not resume based only on a chat message saying an external agent fixed the problem.

## Failure Rule

If a Builder cannot complete a Task after bounded local repair:

1. Manager must open a durable `ISSUE_NNNN`;
2. pause local execution;
3. persist `resume_authorized: false`;
4. stop;
5. route to `EXECUTE/codex/ISSUE_DIAGNOSIS_AND_RECOVERY_PROMPT.md` using Codex or a compatible external recovery agent.

Do not send ordinary technical failures directly to ChatGPT.

## Completion Rule

When all Tasks are `PASS` or `PASS_RECOVERED`, persist the Execution Summary, transition to Evaluation, and STOP.

Project validation must be performed externally with:

`EXECUTE/codex/EVALUATION_PROMPT.md`

A passing Evaluation must also produce `PROJECT_COMPLETION_REPORT_Vx.md` before the version lifecycle is considered fully handed off for future development.
