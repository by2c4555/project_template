# Project Template Development Objective — v5.1.0

This file is the maintainer/development constitution for **Project Template itself**. It is not user-project scope and must never be treated as Research input for a user project.

## Purpose

Maximize engineering quality per token/cost by assigning work to the cheapest reliable authority:

- **Expensive models**: planning, architecture, diagnosis, recovery reasoning, independent evaluation.
- **Low-cost models**: bounded implementation under immutable Task contracts.
- **Deterministic software**: state, authority, gates, integrity, resume, routing, reconciliation and verification.

The design must amplify model intelligence rather than spend model intelligence remembering workflow mechanics.

## MUST invariants

1. `Workplan/` is the AI-development control plane; user-project files live outside it except thin platform adapters.
2. Durable repository state is authoritative; chat/session/provider/process/machine state is disposable.
3. Research input has an explicit untrusted boundary: `Workplan/ingest/`.
4. No Planning authority exists until deterministic ingest validation succeeds.
5. Ingest package identity and canonical logical Scope identity are distinct digests.
6. Planning revalidates its bound ingest at entry/resume and before `PLAN_READY`.
7. Accepted Research input is archived durably; archive and history have distinct responsibilities.
8. Scope and approved planning package integrity are immutable bindings for downstream work.
9. Work ownership is generation-fenced; stale generations cannot mutate Work.
10. Action/Resume Tickets are bounded deterministic projections, not a second authority database.
11. Resume computes reconciliation for mutating roles; it must not delegate workflow reconstruction to the model.
12. Semantic checkpoints persist verified facts/evidence/decisions and exact next bounded unit; never hidden chain-of-thought.
13. Context is granted progressively by reason and does not grant additional authority.
14. Manager routing is deterministic. The normal user does not select Task IDs or manually invoke Builders.
15. One fresh ordinary Builder executes one immutable Task at a time.
16. Builder repair attempts are machine-enforced and bounded.
17. Diagnosis determines evidence-backed root cause and does not repair production code.
18. Recovery performs the minimum complete proven repair for diagnosed implementation defects.
19. Evaluation is independent from Planning/Builder/Recovery claims and verifies actual behavior.
20. PASS/PASS_WITH_FINDINGS requires a Completion Report bound to exact Scope revision/digest.
21. There is a single human approval interface (`scripts/approve.py`), used only as a token/cost/rework circuit breaker.
22. Approval challenges remain bound to exact durable state and rotate/reject stale or wrong challenges.
23. Raw `STATE.json` is internal authority; normal agents consume bounded tools/projections.
24. Provider/model metadata is not authority and never substitutes for state bindings.
25. Cross-session and cross-machine continuation must not require prior chat history.
26. Prompt text must shrink only after equivalent deterministic capability exists and is tested.
27. Stable internal CLI/API contracts precede optional MCP/general-agent abstractions.
28. More capability should normally mean more deterministic software, not larger prompts.
29. README, runtime, use cases, validation and changelog must ship in sync.
30. Changes to these MUST invariants require explicit owner feedback and same-release updates to this constitution and verification.

## SHOULD principles

- Reason once; persist verified conclusions, evidence pointers, rejected approaches with concise reasons, unknowns and next work.
- Prefer bounded retrieval to broad context loading; minimum sufficient context is the goal, not minimum tokens at any cost.
- Treat context capacity and reasoning quality as separate concerns.
- Prefer the fewest new components consistent with clear ownership.
- Avoid OS/process locks when durable generation fencing provides the required safety.
- Avoid duplicate state, memory-summary files and prompt-only authority.
