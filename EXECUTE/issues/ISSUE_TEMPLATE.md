---
issue_id: ISSUE_NNNN
status: OPEN

origin_task: TASK_NNN
origin_phase: PHASE_NN
origin_builder: Builder128K

classification: EXECUTOR_ESCALATION

safe_baseline: unknown
---

# ISSUE_NNNN — Title

## Problem

Concise verified problem.

## Verified Evidence

Only facts established during execution.

- evidence

## Last Confirmed Failure

Exact failing test, command, external result, or behavior.

Do not include giant raw logs.

## Attempts Ruled Out

- approach — reason

## Relevant Scope

Files/symbols/tests only.

- path

## Impact

Choose exactly one primary classification:

- LOCAL_REPAIR
- EXECUTOR_ESCALATION
- KNOWLEDGE_REVIEW_REQUIRED
- REPLAN_REQUIRED
- EXTERNAL_ACTION_REQUIRED

## Resume Package

Task:
`TASK_NNN`

Read:
- exact file/test
- exact file/test

Do not repeat:
- ruled-out approach

Recommended next role:
`Builder256K | Planner512K | User`

## Safe Resume Point

Describe current repository state and whether the failed Task change was reverted, partially preserved, or safely retained.

Never discard unrelated user work.

## Next Action

One concrete action.
