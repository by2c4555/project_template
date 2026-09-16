# CHATGPT Prompt Pack — Project Template v4.2.1

ChatGPT owns **scope intelligence and product evolution**, not technical incident recovery.

Use this folder for:

- initial project Research V1;
- next-version/feature Research based on a verified Project Completion Report;
- true scope/product clarification when Codex Diagnosis proves that implementation cannot proceed without a user/product decision.

## Setup once

Put the content of `PROJECT_INSTRUCTIONS.txt` into ChatGPT Project Instructions.
Keep `MASTER_RESEARCH_PROMPT.md` available as the governing research contract.

## Entry prompts

- `START_RESEARCH_PROMPT.md` — initial project scope research -> Research V1.
- `START_NEXT_VERSION_PROMPT.md` — use a verified `PROJECT_COMPLETION_REPORT_Vx.md` plus new user intent to define Research Vx+1 / a new feature/version scope.
- `PROCESS_SCOPE_CLARIFICATION_PROMPT.md` — process a Codex-produced `SCOPE_CLARIFICATION_REQUIRED_Vx.md` when a product/scope decision is genuinely required.

## Deliberately NOT handled here

Do not send ordinary runtime errors, failed Tasks, stack traces, or blocking Evaluation findings directly to ChatGPT.

Technical failures must first go through:

```text
Codex / External Agent
EXECUTE/codex/ISSUE_DIAGNOSIS_AND_RECOVERY_PROMPT.md
```

Only a proven `SCOPE_AMBIGUITY` returns to ChatGPT/User.

## Outputs

ChatGPT owns:

- `EXECUTE/project_details.md`
- `EXECUTE/docs/raw/**`
- `EXECUTE/research/Research_Vx.md`

Codex then owns repository-level technical preparation, planning, recovery, diagnosis, and evaluation.
