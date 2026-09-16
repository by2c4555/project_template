# PROCESS EVALUATION

Run the Project Template v4.1.3 Research process in `EVALUATION_DRIVEN_RESEARCH` mode.

The latest Codex / GPT-6 Astra Evaluation is new evidence, not automatically authoritative project knowledge.

Use:

- current `EXECUTE/project_details.md`
- current `EXECUTE/docs/raw/**`
- current `EXECUTE/research/Research_Vx.md`
- latest `Evaluation_Vx.md`
- latest `RESEARCH_HANDOFF_Vx.md`, if present
- relevant test logs, runtime logs, screenshots/transcriptions, failed commands, security findings, performance evidence, and user decisions

Follow `MASTER_RESEARCH_PROMPT.md`.

For every material Evaluation finding:

1. identify the finding and evidence
2. classify its root knowledge impact
3. determine whether it is an implementation defect, planning defect, research gap, requirement gap, architecture uncertainty, test gap, security issue, performance issue, documentation issue, or external dependency change
4. research the correct expected behavior
5. ask the user only if a product/requirement decision is required
6. record a final disposition:
   - resolved by new evidence
   - resolved by user decision
   - corrected prior knowledge
   - still unresolved
   - rejected as not applicable
7. update authoritative knowledge only after resolution

Create the next Research version:

`Research Vx+1`

Update:

- `EXECUTE/project_details.md`
- `EXECUTE/docs/raw/**`

Create immutable:

- `EXECUTE/research/Research_Vx+1.md`

Preserve Evaluation Vx and all prior Research versions unchanged.

Do not patch source code.
Do not create the new Implementation Plan.
Do not automatically start Planning.

At completion, clearly state whether Planning Vx+1 is ready or blocked by unresolved research.
