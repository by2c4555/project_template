# External Agent Roles — Project Template v5.3.1

`Workplan/external_agent/` contains bounded reasoning-role instructions selected by deterministic Workplan commands. These files guide model behavior; they do **not** replace Workplan state, tickets, approvals, bindings, gates, or validation.

## Files

| File | Role | Purpose |
|---|---|---|
| `RESEARCH_INSTRUCTION.md` | Research | Compact machine-selected role instruction for `EXECUTE_RESEARCH`. |
| `RESEARCH_POTOCAL_PROMPT.md` | Research | Detailed external research protocol, evidence discipline, unknown-resolution rules, and canonical ingest contract. |
| `PLANNING_PROMPT.md` | Planning | Build the approved Planning Package after Research/Scope and human approval. |
| `DIAGNOSIS_PROMPT.md` | Diagnosis | Reasoning-only root-cause analysis for escalated failures. |
| `RECOVERY_PROMPT.md` | Recovery | Reasoning-only Recovery Contract generation. |
| `EVALUATION_PROMPT.md` | Evaluation | Independent final acceptance reasoning after required Phase Gates pass. |

## Research relationship

Research intentionally uses two files:

```text
RESEARCH_INSTRUCTION.md
        ↓
RESEARCH_POTOCAL_PROMPT.md
        ↓
PROJECT_DETAILS_TEMPLATE.md
        ↓
Workplan/ingest/project_details.md
        ↓
ingest.py check
```

`RESEARCH_INSTRUCTION.md` stays small enough to be returned directly by the public command router. `RESEARCH_POTOCAL_PROMPT.md` carries the detailed reusable research method so ChatGPT Project instructions and role prompts do not duplicate the full protocol every turn.

## Authority invariant

A role prompt may explain what to do, but only deterministic Workplan can authorize when that role may run, what state it is bound to, and whether resulting evidence passes.
