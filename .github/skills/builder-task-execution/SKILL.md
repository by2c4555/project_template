---
name: builder-task-execution
description: Execute exactly one bounded task with strict context, exploration, external-I/O, repair, environment, history, issue, and completion controls.
user-invocable: false
disable-model-invocation: false
---

# Builder Task Execution

The selected Builder agent owns context profile and hard executor policy. This skill owns the shared Task procedure.

## Minimal Loading Order

```text
EXECUTE/PROJECT_STATUS.md
-> active Task metadata
-> selected Builder agent
-> runtime context compatibility gate
-> active Task
-> exact Knowledge refs
-> exact Plan refs if needed
-> selected history Summary/Run if needed
-> linked Issue if needed
-> exact src/test Context Manifest
```

Do not load `project_details.md`, raw `docs/`, all reference files, the full Plan by default, all Tasks/history/issues, or the whole repository.

## Preflight

Before implementation:

1. confirm exact active Task;
2. confirm dependencies PASS;
3. confirm runtime/model context compatibility;
4. confirm Task Context Budget is SAFE;
5. preserve unrelated repository changes;
6. perform Environment Safety Gate when external access is required;
7. load only the Context Manifest.

## Environment Safety Gate

If the Task requires external access:

1. read Task Environment Contract;
2. validate root `.env.user`;
3. validate `EXECUTE/.env.execute`;
4. never invent missing values;
5. do not make external requests until required values pass validation.

If `.env.user` is missing, create only required keys using `__REQUIRED__`, persist `WAITING_USER`, report exact variable names, and stop.

Never persist secret values into project state, Tasks, history, Issues, reference, logs, or final responses.

Production access and DB write access require explicit policy permission.

## Evidence-First Exploration

Every discovery action must directly support required context, implementation, required verification, blocker diagnosis, or state/history update.

Stop discovery once sufficient evidence exists. Do not search merely for confidence.

## Batch Operations

Prefer bounded batch operations over repeated equivalent calls.

Avoid reading many files one-by-one when search can identify relevant files, N+1 DB queries, resource-by-resource API calls when batch/list/filter exists, rerunning unchanged passing tests, or repeatedly reading unchanged files.

## Database Exploration

Prefer:

```text
schema/metadata
-> aggregate/filter
-> candidate keys
-> bounded sample
-> exact affected rows
```

Avoid row-by-row enumeration, unbounded SELECT, open-ended pagination, and repeated equivalent queries.

## API Exploration

Prefer:

```text
metadata/list/filter
-> bounded page/batch
-> candidate resources
-> exact resource only when needed
```

Avoid guessed endpoints, request-by-request enumeration, open-ended pagination, and unchanged credential retries.

Transient retries count against Task retry budget. Deterministic failures such as 400/401/403 must not be retried unchanged without evidence that state changed.

## Implementation

Modify only active Task scope. Use `src/` for product code and `test/` for tests unless the repository explicitly requires otherwise.

Do not implement future Tasks, broaden architecture, or modify `EXECUTE/reference/`.

If verified execution evidence contradicts project knowledge, create/update an Issue with `KNOWLEDGE_REVIEW_REQUIRED` and stop normal execution.

## Verification

Run the Task Verification Matrix.

`PASS` requires all required acceptance criteria and checks to pass.

Do not weaken valid tests/requirements to obtain PASS. Never report unverified success.

## Repair

Maximum:

```text
5 meaningful repair attempts per repair round
```

A meaningful attempt requires evidence -> meaningful intervention -> verification.

Do not repeat essentially the same failed approach more than twice without new evidence.

## Budget Exhaustion

If exploration, external-I/O, or repair budget is exhausted:

1. stop further actions of that class;
2. create/update an Issue;
3. record bounded evidence and remaining uncertainty;
4. set Task BLOCKED;
5. persist Task/history/project state;
6. return control;
7. stop.

Never silently increase budget.

## Task History

Every meaningful Task execution creates one immutable:

```text
EXECUTE/tasks/history/TASK_NNN/RUN_NNNN.md
```

Maintain:

```text
EXECUTE/tasks/history/TASK_NNN/SUMMARY.md
```

Keep both concise. Read Summary before detailed old Runs.

Do not write hidden reasoning or giant raw logs.

## Issues

Issue impact:

```text
LOCAL_REPAIR
CORRECTIVE_TASK
KNOWLEDGE_REVIEW_REQUIRED
REPLAN_REQUIRED
EXTERNAL_ACTION_REQUIRED
EXECUTOR_SWITCH_REQUIRED
```

Issue evidence does not override Plan/Task requirements.

## Completion Fast Path

Once required verification passes:

1. enter FINALIZE immediately;
2. stop exploration;
3. stop optional DB/API work;
4. stop optional refactoring;
5. do not rerun passing checks unless state changed after them;
6. batch required Task/history/project-state writes when possible;
7. signal `task_complete` when the harness supports it;
8. stop.

FINALIZE is terminal.

## Result States

```text
PASS
PARTIAL
BLOCKED
```

Only PASS normally satisfies downstream dependencies.
