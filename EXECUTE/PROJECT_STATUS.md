# Project Status

```yaml
workflow_version: "3.4.1"

project_status: ACTIVE
phase: INITIALIZE
stage: INPUT_VALIDATION

plan_revision: 0
knowledge_revision: 0

active_task: none
recommended_agent: none

active_issue: none
escalation: NONE

last_completed: none
latest_history: none

next_action: Validate project input, select the Planning model if required, and initialize/refine project knowledge.
```

## Rules

- This is the single global workflow router.
- Keep it small.
- Persist before and after every major stage.
- Detailed logs belong in Task history or Issues.
