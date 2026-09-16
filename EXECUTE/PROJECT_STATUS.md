# Project Status

```yaml
workflow_version: "4.0.1"

project_status: ACTIVE
phase: INITIALIZE
stage: INPUT_VALIDATION
planning_transaction: PT1_INPUT_KNOWLEDGE

knowledge_revision: 0
plan_revision: 0

active_phase: none
phase_authorized: false

active_task: none
recommended_agent: Planner512K

active_issue: none

last_completed: none
latest_history: none
latest_result_capsule: none

next_action: >
  Invoke Planner512K as a fresh isolated subagent for PT1_INPUT_KNOWLEDGE.
```

This file is the compact global workflow router.
Disk artifacts are authoritative; chat history is not.
Do not place long logs, Plan content, Knowledge content, diffs, or secrets here.
