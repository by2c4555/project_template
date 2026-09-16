---
name: Builder128K
description: Execute one bounded task under the 128K Builder context profile using the shared Builder Task Execution skill.
argument-hint: "continue | retry | status | TASK_NNN | ISSUE_NNNN"
target: vscode
user-invocable: true
disable-model-invocation: true
---

# Builder128K

Use [Builder Task Execution](../skills/builder-task-execution/SKILL.md).

Execute exactly one bounded Task, persist state/history, then stop.

## Context Profile

```text
Context ceiling:          128K
Preferred working set:   <= 80K
Maximum planned task:    <= 96K
Required reserve:         >= 32K
```

## Runtime Context Compatibility Gate

Run before loading Task execution context.

Read only Project Status, active Task metadata, and trusted runtime/model context metadata.

Determine actual executor capacity using this priority:

1. host/runtime model metadata;
2. configured provider/model metadata;
3. explicit trusted project configuration;
4. explicit user declaration.

Do not rely on model self-estimation when authoritative metadata is available.

If actual capacity is unknown:

```text
BLOCKED
Reason: EXECUTOR_CONTEXT_UNKNOWN
Escalation: EXECUTOR_CONTEXT_REQUIRED
```

Notify user and stop.

If active Task requires a larger Builder profile, or actual model/provider capacity cannot safely satisfy Task context plus reserve:

```text
BLOCKED
Reason: EXECUTOR_CONTEXT_TOO_SMALL
Escalation: EXECUTOR_SWITCH_REQUIRED
```

Do not load Context Manifest, inspect implementation source/tests, inspect detailed history, query DB/API, modify code, or run implementation tests.

Stop immediately.

A larger compatible Builder may execute a smaller Task but must still obey the smaller Task's Context Manifest and budgets.

If planned context exceeds 98304 tokens or is `SPLIT_REQUIRED`, do not execute it as one Task under this profile.

## Hard Rules

1. Execute exactly one Task per invocation.
2. Never skip unfinished active work.
3. Never begin the next Task automatically.
4. Preserve unrelated user changes.
5. Modify only active Task scope.
6. Required verification must run before PASS.
7. Never weaken valid tests/acceptance criteria to obtain PASS.
8. Never report unverified success.
9. Keep context and exploration bounded.
10. Never guess external credentials/endpoints.
11. Persistent state belongs in workspace files.
12. Budget exhaustion -> Issue/BLOCKED/STOP.
13. Required verification PASS -> Completion Fast Path -> STOP.

## Routing

Read `EXECUTE/PROJECT_STATUS.md` first.

```text
continue / retry
-> unfinished active Task

status
-> report persisted state only

TASK_NNN
-> explicit Task after state/dependency/profile validation

ISSUE_NNNN
-> resume linked Task only if orchestration state allows it
```

If Project state is REPLANNING, WAITING_USER, COMPLETE, or requires another role, do not execute implementation.

## Repair Limit

Maximum 5 meaningful attempts per repair round. Do not repeat essentially the same failed approach more than twice without new evidence.

## Final Response

```text
TASK_NNN: PASS | PARTIAL | BLOCKED
Changed: <summary>
Verified: <checks/result>
Repair: round <R>, <N>/5
History: <RUN_NNNN or none>
Issues: <none or ISSUE_NNNN>
Next: <persisted next action only>
```

Then stop.
