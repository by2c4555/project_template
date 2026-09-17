# Resolution Knowledge Index

This index contains **verified reusable engineering lessons learned during execution/evaluation recovery**.

It is distinct from `EXECUTE/reference/KNOWLEDGE_INDEX.md`, which stores External-Agent-prepared project/requirement/architecture knowledge for the current planning package.

## Entry Schema

```yaml
resolution_id: RESOLUTION_NNNN
status: VERIFIED
source_type: EXECUTION_ISSUE | EVALUATION_FINDING
source_issue: ISSUE_NNNN | none
source_evaluation: Evaluation_Vx | none
source_finding: EVAL-NNN | none
source_task: TASK_NNN | none
area: concise component/area
symptom: concise searchable symptom
root_cause: concise root cause
tags: [tag1, tag2]
confidence: VERIFIED
artifact: EXECUTE/knowledge/resolutions/RESOLUTION_NNNN.md
```

## Verified Resolutions

None yet.

## Consumption Rules

- External Agent Planning must inspect this index before finalizing a plan.
- External Agent Evaluation must inspect relevant prior resolutions when designing targeted regression checks.
- ProjectManager500K should surface relevant entries to a Builder when a Task touches the same component/risk pattern.
- Read only relevant `RESOLUTION_*.md` files; do not preload the whole knowledge base.
- Never treat an unresolved Issue or unverified hypothesis as reusable knowledge.
