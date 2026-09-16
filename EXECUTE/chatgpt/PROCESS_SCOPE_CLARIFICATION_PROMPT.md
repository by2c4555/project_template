# PROCESS CODEX SCOPE CLARIFICATION

Run Project Template v4.2.0 research in `SCOPE_CLARIFICATION` mode using `MASTER_RESEARCH_PROMPT.md`.

Required input:
- `EXECUTE/scope/SCOPE_CLARIFICATION_REQUIRED_Vx.md`
- referenced Codex Diagnosis
- current `project_details.md` / Research Vx
- user decisions

Codex has already isolated the technical problem and determined that a genuine product/scope decision is required.

Your job is to resolve only that scope ambiguity:
1. explain the decision in user/product terms;
2. collect the user's choice or clarify requirements;
3. preserve technical consequences supplied by Codex without inventing new ones;
4. update `project_details.md` and create Research Vx+1 when the authoritative scope changes/materially clarifies;
5. return the clarified scope to Codex.

Do not patch code.
Do not diagnose the implementation again.
Do not create the implementation plan.
