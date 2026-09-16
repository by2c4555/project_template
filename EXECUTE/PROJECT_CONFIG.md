# Project Configuration — v4.2.0

## Canonical Lifecycle

```text
Research Vx
  -> Codex Technical Preparation / Planning Vx
  -> User Implementation Approval
  -> Local Execution Vx
       -> Issue? Codex/External Recovery -> Resume
  -> Codex Evaluation Vx
       -> blocking finding? Codex Diagnosis -> repair/replan/re-evaluate/scope clarification
       -> PASS? Project Completion Report
  -> ChatGPT next-version scope research or close
```

The compact philosophy is:

> Research -> Plan -> Execute -> Recover -> Evaluate -> Learn -> Evolve

## Intelligence Roles

- **ChatGPT Project — Scope/Product Evolution:** WHAT, WHY, SCOPE, future feature/version Research, true product clarification.
- **Codex / GPT-6 Astra — Technical Truth:** repository research, architecture, Planning, Task compilation, Diagnosis, Recovery, Replan, independent Evaluation, Completion Report.
- **ProjectManager500K — Execution Control:** state-aware dispatch of approved Tasks; opens/records execution issues and pauses safely.
- **Builder100K — Implementation:** one bounded approved Task per fresh invocation, including only bounded local repair attempts.
- **External Recovery Agent — Optional:** may replace Codex for direct technical recovery if it obeys the same recovery artifact contract.
- **User — Authority:** implementation approval and product/scope decisions.

## Hard Authority Rules

1. No approved Planning Vx -> no local execution.
2. Planning review/feedback is not implementation approval.
3. Codex resolves material technical unknowns before requesting approval.
4. Execution is bound to one exact approved Planning Vx.
5. Local agents may not silently change approved architecture/intent/scope.
6. Builder failure beyond bounded repair -> mandatory Issue + hard execution pause.
7. Normal technical failures route to Codex Diagnosis/Recovery, not ChatGPT.
8. External repair may modify broader repository scope only when Diagnosis proves it is required and approved contracts are preserved.
9. A recovered Task becomes `PASS_RECOVERED`, not ordinary PASS.
10. No resume until recovery verification fully passes and `resume_authorized: true` is persisted.
11. Every material resolved execution Issue must produce durable Resolution knowledge.
12. Evaluation is read-only and may not silently fix production code.
13. Blocking Evaluation findings route to Codex Diagnosis; Evaluation does not assume its own finding is infallible.
14. `EVALUATION_DEFECT` must be handled by review + re-evaluation, not unnecessary code change.
15. Only proven `SCOPE_AMBIGUITY` returns to User/ChatGPT scope clarification.
16. Only Evaluation may validate the implementation iteration.
17. PASS/PASS_WITH_FINDINGS requires a full `PROJECT_COMPLETION_REPORT_Vx.md`.
18. Completion Report is the preferred verified baseline for ChatGPT next-version Research.
19. Historical Research/Planning/Issue/Diagnosis/Resolution/Evaluation artifacts are immutable records; current aliases/state may advance.
20. Disk artifacts are authoritative; chat memory is disposable.

## Local Execution State Machine

Primary states:

```text
LOCKED
READY
IN_PROGRESS
ISSUE_DETECTED
PAUSED_FOR_DIAGNOSIS
PAUSED_FOR_EXTERNAL_REPAIR
RECOVERY_VERIFICATION
READY_TO_RESUME
COMPLETE
AWAITING_EVALUATION
```

Normal Builder dispatch is forbidden while execution is paused for recovery.

## Root-Cause Classifications

Codex Diagnosis chooses exactly one primary classification:

- `IMPLEMENTATION_DEFECT`
- `TASK_DEFECT`
- `PLAN_DEFECT`
- `EVALUATION_DEFECT`
- `SCOPE_AMBIGUITY`
- `EXTERNAL_BLOCKER`
- `UNKNOWN`

## Evaluation Results

Exactly one:

- `PASS`
- `PASS_WITH_FINDINGS`
- `DIAGNOSIS_REQUIRED`

## Recovery Knowledge

```text
ISSUE = what failed
DIAGNOSIS = why it failed / who owns correction
RESOLUTION = how it was correctly fixed + verified
KNOWLEDGE INDEX = what future agents should reuse
```

## Model Policy

```yaml
local_models:
  ProjectManager500K:
    minimum_context_tokens: 512000
  Builder100K:
    minimum_context_tokens: 102400
    controlled_target_tokens: 40000
    controlled_max_tokens: 52000
external_intelligence:
  environment: Codex
  recommended_model: GPT-6 Astra
  responsibilities:
    - implementation_research
    - planning
    - task_compilation
    - diagnosis
    - recovery
    - evaluation
    - completion_handoff
```

## No-RAG Local Policy

Local models receive compiled knowledge, Task context manifests, explicitly surfaced relevant Resolution knowledge, repository files named by Tasks, and persisted execution evidence. Missing material knowledge is surfaced as a preparation/recovery defect rather than guessed.

## Environment Safety

Never guess credentials or external configuration. Production access and destructive operations require explicit approved authority.
