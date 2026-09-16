---
name: builder-task-execution
description: v4.1 bounded execution kernel for local Builder100K.
---

# Builder Task Execution v4.1

Execute exactly one Task per fresh invocation.

## 1. Gate
Read compact project status, active Task metadata, global constraints, model binding, and active Issue only if applicable. Confirm approved Planning Vx binding and Task dependencies.

Run `python scripts/context_guard.py <TASK_FILE>` before loading implementation files.

## 2. Load the Compiled Context Manifest
Load only `mandatory` Task context first. `useful` context is optional and must remain within budget. Never recursively load `docs/raw/` merely because it exists.

Context expansion requires: `NEED -> JUSTIFICATION -> BUDGET -> LOAD`.
Missing architectural/requirement knowledge is a Task-pack defect, not permission to invent.

## 3. Implement Within Contract
Honor objective, allowed files, required changes, invariants, architecture/decision references, must-preserve rules, out-of-scope list, and acceptance criteria.

Material contradiction or scope expansion -> persist evidence -> BLOCKED/REPLAN_REQUIRED -> STOP.

## 4. Verify
Run exact Task verification first. If it fails, perform at most two evidence-driven repair attempts unless the Task states a stricter limit. Do not repeat equivalent failed actions without new evidence.

## 5. Persist Evidence
Write `EXECUTE/execution/evidence/<TASK_ID>.md` with concise reproducible evidence. Update Task result and execution state only as permitted.

## 6. Return Capsule and Stop
Never start the next Task. Return only compact routing data. Disk artifacts are authoritative.
