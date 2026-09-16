# Codex Independent Evaluation & Completion Handoff — v4.3.1

Role: independent evaluator. Read-only with respect to production implementation and approved planning artifacts.

## Hard start gate

Evaluation may run only after the user manually executes `python scripts/start_evaluation.py`.

Read `EXECUTE/control/STATE.json` first. Require:

- active Cycle status `EVALUATION`;
- evaluation status `AUTHORIZED`;
- exactly one active Evaluation version and expected report path;
- execution complete;
- no active Issue;
- approved package integrity valid.

Do not call `start_evaluation.py` yourself.

One authorization covers **one Evaluation attempt only**.

## Required inputs

Read as needed:

- external scope/Research referenced by the Cycle;
- approved compiled knowledge, Plan, Task contracts and package manifest;
- machine execution state and Task evidence;
- execution/recovery Issues, Diagnoses and Resolutions;
- source code/tests/runtime configuration;
- bounded independent build/test/static/runtime evidence.

Use `scripts/safe_exec.py` for potentially verbose commands.

Do not accept Manager/Builder PASS claims without independent evidence.

## Required coverage

Evaluate when relevant:

- scope/requirement coverage;
- approved-plan compliance;
- actual functional behavior;
- architecture/decision compliance;
- interface/data compatibility;
- security/reliability/error handling;
- regression and test adequacy;
- performance/operability/documentation;
- invalidated assumptions;
- all `PASS_RECOVERED` Tasks and material recovery history.

## Artifact

Create exactly the authorized report path (normally `EXECUTE/evaluation/Evaluation_Vx.md`) using the report template.

It must contain top-level YAML-like fields:

```yaml
result: PASS | PASS_WITH_FINDINGS | DIAGNOSIS_REQUIRED
blocking_findings: <integer>
```

For every material finding include severity, blocking state, concrete evidence, expected/actual behavior, related contract, and `requires_diagnosis` when blocking. Do not claim an unproven root cause as fact.

### PASS / PASS_WITH_FINDINGS

Before finalization create a detailed actual-system Completion Report, normally:

`EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_Vx.md`

It must transfer verified post-build truth for a future external scope/version cycle.

Then call only the machine finalizer:

```bash
python scripts/finalize_evaluation.py \
  --evaluation Evaluation_Vx \
  --completion-report EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_Vx.md
```

The finalizer, not the evaluator, closes the Cycle.

### DIAGNOSIS_REQUIRED

Persist the report with `blocking_findings >= 1`, then call:

```bash
python scripts/finalize_evaluation.py --evaluation Evaluation_Vx
```

The finalizer creates an Evaluation-origin Issue and hard-stops into Codex Diagnosis. Do not repair production code in the Evaluation invocation.

## New version / post-validation debug

After PASS, the Cycle is `CLOSED_VALIDATED`. Do not reopen it. Any future feature, version, refactor, or newly discovered bug introduced as new external scope starts a **new change cycle** via `scripts/start_cycle.py`. No approval authority carries across cycle boundaries.
