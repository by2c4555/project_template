---
name: builder-task-execution
description: v4.2 bounded execution kernel for local Builder100K.
---

# Builder Task Execution v4.2

Execute exactly one Task per fresh invocation.

## 1. Gate

Read compact project/execution status, active Task metadata, global constraints, model binding, and only Manager-surfaced relevant recovery knowledge.

Confirm:
- approved Planning Vx binding;
- Task dependencies;
- execution state permits Builder work;
- no external-recovery pause is active.

Run `python scripts/context_guard.py <TASK_FILE>` before loading implementation files.

## 2. Load Compiled Context

Load only Task `mandatory` context first. `useful` context is optional and must remain within budget.

Never recursively load `docs/raw/**` or `knowledge/**` merely because they exist.

Context expansion requires:

`NEED -> JUSTIFICATION -> BUDGET -> LOAD`

Missing architectural/requirement knowledge is a Task-pack defect, not permission to invent.

## 3. Implement Within Contract

Honor objective, allowed files, required changes, invariants, decisions, must-preserve rules, out-of-scope list, acceptance criteria, and supplied verified prior-resolution guardrails.

Material contradiction/scope expansion -> persist evidence -> BLOCKED -> STOP.

## 4. Verify + Bounded Local Repair

Run exact Task verification first.

If it fails:

1. inspect evidence;
2. perform at most two evidence-driven repair attempts unless Task states a stricter limit;
3. never repeat an equivalent failed action without new evidence;
4. remain inside Task authority.

If verification still fails or safe repair requires wider authority:

- mark invocation `BLOCKED`/`FAIL`;
- persist the last confirmed failure;
- record attempts ruled out;
- return `external_recovery_required: true`;
- STOP.

Do not become an open-ended recovery agent.

## 5. Persist Evidence

Write `EXECUTE/execution/evidence/<TASK_ID>.md` containing concise reproducible evidence.

For failure include enough forensic information for Manager to create an Issue and for Codex/external recovery to isolate the problem.

## 6. Return Capsule and Stop

Success:

```yaml
result_capsule:
  task: TASK_NNN
  status: PASS
  evidence: EXECUTE/execution/evidence/TASK_NNN.md
  external_recovery_required: false
```

Failure:

```yaml
result_capsule:
  task: TASK_NNN
  status: BLOCKED
  evidence: EXECUTE/execution/evidence/TASK_NNN.md
  external_recovery_required: true
  last_confirmed_failure: <concise>
```

Never start the next Task. Disk artifacts are authoritative.
