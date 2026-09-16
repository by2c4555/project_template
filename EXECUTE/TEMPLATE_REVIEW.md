---

task_id: TASK_NNN
title: "<Task Title>"
type: normal
status: PENDING
stage: pending

required_builder_profile: Builder64K
builder_profile_source: .github/agents/builder64k.agent.md

planned_context_tokens: 0
context_assessment: SAFE

depends_on: []

plan_refs: []
knowledge_refs: []
history_refs: []
issue_refs: []

## next_action_on_pass: RETURN_TO_PROJECT_MANAGER

# TASK_NNN — <Task Title>

## Objective

Define one bounded outcome for this task.

## Definition of Done

Describe the observable condition that means this task is complete.

---

## Plan References

List only the authoritative Plan IDs required by this task.

```text
REQ-...
ARCH-...
CONTRACT-...
NFR-...
```

Add a short local summary only when the reference alone is insufficient for execution.

---

## Knowledge References

List only the Knowledge IDs required by this task.

```text
API-...
DB-...
ENV-...
ARCHFACT-...
DECISION-...
```

The Builder must not scan the entire Knowledge Base.

---

## Dependencies

```yaml
depends_on:
  - TASK_...
```

All required dependencies must be `PASS` before execution begins.

---

## Builder / Context Contract

```yaml
required_builder_profile: Builder64K
builder_profile_source: .github/agents/builder64k.agent.md

planned_context_tokens: <estimate>
context_assessment: SAFE
```

The runtime context compatibility gate must pass before implementation context is loaded.

If the active executor is too small:

```text
BLOCKED
Reason: EXECUTOR_CONTEXT_TOO_SMALL
Escalation
```
