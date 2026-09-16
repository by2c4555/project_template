---
name: builder-task-execution
description: Isolated bounded execution kernel for Builder128K and Builder256K.
---

# Builder Task Execution

Execute exactly one active Task or one Integration Gate in this invocation.
The invocation itself is the context/recovery boundary.

## 1. Preflight Before Source Loading

Read only:
- `EXECUTE/PROJECT_STATUS.md`;
- active `TASK_NNN.md` metadata/contract;
- active `ISSUE_NNNN.md` only for retry/escalation.

Confirm active Task, dependency PASS state, Builder profile, Phase authorization, and non-completed status.

Run:
`python scripts/context_guard.py EXECUTE/tasks/<ACTIVE_TASK>.md`

Do this before reading Task-listed implementation files.

If preconditions fail: persist reason -> BLOCKED -> STOP.
If preflight is SPLIT_REQUIRED or CONTEXT_BLOCKED: persist -> STOP.
WARN may proceed only when runtime role floor is satisfied and the Task remains below the profile hard maximum.

## 2. Load Bounded Context

Load only:
- Task WRITE files;
- Task READ files;
- Task TEST files;
- execution-critical facts embedded in the Task;
- active Issue when resuming;
- smallest additional evidence justified by a verified failure.

Do not preload the entire Plan, Knowledge Base, repository tree, unrelated history, or unrelated Issues.

Any context expansion must follow:
`REQUEST -> JUSTIFY -> BUDGET CHECK -> LOAD`.

Material scope expansion -> `SCOPE_EXPANSION_REQUIRED` -> Issue -> BLOCKED -> STOP.

## 3. Baseline and Environment

Establish the smallest relevant baseline before edits.
Preserve unrelated user changes. Never use destructive reset behavior that can discard unrelated work.

Before external API/DB access, read the Task Environment contract and required env files only.
Never guess credentials, hosts, URLs, ports, tokens, or secret values.
Missing required value -> placeholder only when allowed -> WAITING_USER -> STOP before external access.
Production and DB writes are denied by default.

## 4. Implement

Implement only Task-defined behavior. Respect exact WRITE scope, verified facts, Must Preserve, acceptance criteria, and valid contracts.

Do not redesign architecture, change Knowledge/Plan, implement future Tasks, perform unrelated refactors, or silently broaden scope.

## 5. Bounded Tool Output

Tool output becomes model context, so treat output as a budgeted resource.

Default maximum brought into model context:
- command output: 12000 characters;
- search results: 100 entries;
- log excerpt: 200 lines;
- diff excerpt: 400 lines;
- test failure excerpt: 250 lines.

For large commands/tests/diffs:
`full output -> terminal or local file -> summary/focused excerpt -> model`.

Prefer filtered commands, targeted tests, `tail`/focused excerpts, and exact symbol searches.
Never dump a complete large build/test log merely because it is available.

## 6. Verify and Repair

Run exact Task verification first.
PASS -> Completion Fast Path; stop exploring.
FAIL -> capture concise evidence -> classify -> bounded repair.

Default maximum: 2 meaningful repair attempts.
Each attempt must add new verified evidence or a materially different corrective change.
No new evidence/action -> `NO_PROGRESS` -> terminate.

Instability signals include:
- REPEATED_EQUIVALENT_ACTION
- NO_PROGRESS
- SCOPE_DRIFT
- REPEATED_REGRESSION
- CONTRADICTED_VERIFIED_FACT
- EXCESSIVE_CONTEXT_EXPANSION
- REPAIR_LIMIT_REACHED

Repeated drift -> `EXECUTION_UNSTABLE` -> Issue -> BLOCKED -> STOP.

## 7. External I/O Guard

Bound external access. Avoid unbounded pagination, N+1 investigation, full resource enumeration, and unchanged retries.
Deterministic 400/401/403 failures are not retried unchanged. Transient 429/5xx/timeouts use only configured bounded retries.

## 8. Completion Fast Path

On sufficient PASS evidence:
1. persist Task result/history;
2. update compact project state;
3. return only the Result Capsule;
4. STOP.

Do not start the next Task, perform optional cleanup, or return full logs/diffs.

## 9. Result Capsule

Maximum intent: routing summary, not a transcript.

```yaml
result_capsule:
  unit: TASK_004
  status: PASS
  changed_files:
    - src/example.ts
  verification: PASS
  issue: none
  next_action: CONTINUE
```

For non-PASS include only the exact status, concise evidence location/summary, active Issue ID, and recommended next role/action.
Never include hidden reasoning, secrets, giant raw logs, or complete diffs.

## 10. Retry Isolation

A retry is always a new Builder invocation.
The next invocation may receive only persisted Task contract, failure capsule/Issue, minimal relevant evidence, and updated instructions.
Never require replay of the previous failed chat transcript.
