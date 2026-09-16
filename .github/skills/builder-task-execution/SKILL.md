---
name: builder-task-execution
description: Shared bounded execution kernel for Builder128K and Builder256K.
---

# Builder Task Execution

Use this procedure only after the active Builder has passed its Context Gate.

Execute exactly one active Task.

## 1. Preflight

Read:
- `EXECUTE/PROJECT_STATUS.md`;
- the active `TASK_NNN.md`.

When resuming escalation, also read the active `ISSUE_NNNN.md`.

Confirm:
- Task is the active Task;
- Task dependencies are PASS;
- required Builder profile matches;
- Phase is authorized when executing a normal Phase Task;
- Task is not already superseded or completed.

Do not load unrelated project context.

If any precondition is invalid:
- persist the exact reason;
- return BLOCKED;
- STOP.

---

## 2. Load Bounded Context

Load only:
- Task-listed WRITE files;
- Task-listed READ files;
- Task-listed tests;
- execution-critical facts embedded in the Task;
- the active Issue when resuming one;
- the smallest additional evidence required by a verified failure.

Do not preload:
- entire Implementation Plan;
- entire Knowledge Base;
- unrelated Task history;
- unrelated Issues;
- broad repository trees.

Context expansion requires evidence.

If the required scope materially exceeds the Task contract:
- `SCOPE_EXPANSION_REQUIRED`;
- create/update Issue;
- BLOCKED;
- STOP.

---

## 3. Dependency and Baseline Gate

Verify dependency state from persisted project data.

Before code changes, establish the smallest useful relevant baseline.

Examples:
- focused existing test;
- current function behavior;
- current integration check.

Preserve unrelated user changes.

Never use destructive repository-reset behavior that may discard unrelated work.

---

## 4. Environment Gate

Run this gate before any external API/DB access.

Read:
- Task Environment section;
- `.env.user` only when required;
- `EXECUTE/.env.execute`.

Never guess:
- API keys;
- tokens;
- passwords;
- URLs;
- DB URLs;
- hosts;
- ports;
- credentials.

If a required value is missing, the workflow may create only the required placeholder such as:

`KEY=__REQUIRED__`

Then:
- set WAITING_USER;
- state exact missing variable names without values;
- STOP before external access.

Production access is denied by default.

Database writes are denied by default.

Never expose secret values in history, Issues, logs, or responses.

---

## 5. Implement

Implement only the Task-defined behavior.

Respect:
- exact WRITE scope;
- verified Task facts;
- Must Preserve requirements;
- acceptance criteria;
- existing valid contracts.

Do not:
- redesign architecture;
- reinterpret project requirements;
- modify Knowledge;
- modify the Plan;
- implement future Tasks;
- perform unrelated refactors;
- broaden scope silently.

---

## 6. Verify

Run the exact Task verification first.

On PASS:
- use the Completion Fast Path;
- do not continue exploring;
- do not perform optional refactors;
- do not rerun already-sufficient checks without reason.

On FAIL:
- capture concise failure evidence;
- classify before changing more code.

---

## 7. Repair

Default maximum:

2 meaningful repair attempts.

Each attempt must produce at least one:
- new verified evidence;
- materially different corrective change.

A repeated equivalent failed action without new evidence is not valid progress.

Repair sequence:

failure evidence
→ bounded hypothesis
→ corrective change
→ verification

Do not repeat approaches already ruled out unless new evidence justifies them.

---

## 8. Progress Invariant

Every meaningful execution loop must produce at least one:

- new verified evidence;
- state-changing corrective action;
- termination.

If none occurs:
- `NO_PROGRESS`;
- do not continue the loop.

---

## 9. Execution Integrity Guard

Observable instability signals:

- `REPEATED_EQUIVALENT_ACTION`
- `NO_PROGRESS`
- `SCOPE_DRIFT`
- `REPEATED_REGRESSION`
- `CONTRADICTED_VERIFIED_FACT`
- `EXCESSIVE_CONTEXT_EXPANSION`
- `REPAIR_LIMIT_REACHED`

First recoverable drift:
1. stop the current approach;
2. reread Task Goal, Verified Facts, Must Preserve, Acceptance, and latest failure;
3. perform at most one bounded reorientation.

If drift repeats without new evidence:
- `EXECUTION_UNSTABLE`;
- create/update Issue;
- BLOCKED;
- STOP.

---

## 10. Regression Guard

If a change causes previously passing unrelated verification to fail:
- do not build further work on the regressed state;
- restore only the Task-local change when safe;
- preserve unrelated user work;
- record the failed attempt.

Repeated regression:
- `EXECUTION_UNSTABLE`;
- Issue;
- STOP.

---

## 11. External I/O Guard

Use bounded external access.

Database:
schema/metadata
→ filter/aggregate
→ candidate identifiers
→ bounded rows
→ exact affected records

API:
metadata/list/filter
→ bounded page/batch
→ candidate IDs
→ exact resources

Avoid:
- unbounded pagination;
- N+1 investigation;
- resource-by-resource enumeration without a bound;
- repeated equivalent calls.

Deterministic failures such as 400/401/403 must not be retried unchanged.

Transient failures such as 429/5xx/timeouts may use only configured bounded retries.

---

## 12. Completion Fast Path

When required verification passes:

1. persist Task result;
2. append bounded Task history;
3. update `EXECUTE/PROJECT_STATUS.md`;
4. return PASS to ProjectManager;
5. STOP.

Do not start the next Task.

Do not perform extra exploration after sufficient PASS evidence exists.

---

## 13. Non-PASS Finalization

When reliable completion is not possible:

1. preserve the safest practical repository state;
2. create/update an Issue when meaningful;
3. record:
   - verified problem;
   - exact failing evidence;
   - approaches ruled out;
   - relevant files/tests;
   - safe resume point;
   - recommended next role;
4. update Task status;
5. revoke Phase continuation through persisted state;
6. return the exact status;
7. STOP.

Never dump hidden reasoning or giant raw logs.

Never store secrets.
