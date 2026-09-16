# CHATGPT Prompt Pack — Project Template v4.1.2

This folder is used in the ChatGPT Project research workspace.

## Setup once

Put the content of `PROJECT_INSTRUCTIONS.txt` into ChatGPT Project Instructions.

Keep `MASTER_RESEARCH_PROMPT.md` available as the governing research contract.

## Entry prompts

Use only the entry prompt that matches the current case:

- `START_RESEARCH_PROMPT.md` — initial project research -> Research V1
- `PROCESS_EVALUATION_PROMPT.md` — Evaluation Vx / Research Handoff -> Research Vx+1
- `PROCESS_ISSUE_PROMPT.md` — error, bug, runtime issue, feedback, external change -> Research Vx+1 when knowledge changes

## Principle

Inputs from evaluation/issues are evidence first.

They must be investigated before becoming authoritative knowledge or requirements.

The ChatGPT Project outputs:

- `EXECUTE/project_details.md`
- `EXECUTE/docs/raw/**`
- `EXECUTE/research/Research_Vx.md`

The next phase is Codex / GPT-6 Astra Planning & Knowledge Compilation.
