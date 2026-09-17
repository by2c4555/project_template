# v5.2.0 Candidate Validation

Baseline studied: `main` v5.1.0 commit `d0ef7f3eccaf00bdfbd7b0a2d0e94c7a8782d360`.

This candidate adds the deterministic human command/continuation protocol without changing the repository remotely.

## Executed on the isolated candidate working copy

```text
python Workplan/tests/run_command_protocol.py
COMMAND_PROTOCOL_VALID: PASS
```

The command-protocol scenario verifies:

- unknown/free-form command tokens cannot start Workplan work;
- Research is accepted only as the bootstrap-stage execution command;
- Planning INIT requires a `NEW_COST_ENVELOPE` human approval;
- no Planning Work starts before approval;
- a granted Planning command starts bounded Work;
- provider/session re-entry becomes approval-free RESUME with a new generation;
- wrong-stage commands are rejected without reinterpretation;
- `RESET_PLANNING` is approval-gated and invalidates only active Planning Work;
- reset authorization is single-consumption;
- expired approval challenges return `EXPIRED`, clear pending authorization and preserve lifecycle stage;
- `WORKPLAN_NEXT` deterministically projects VS Code / `EXECUTE_IMPLEMENTATION` from `PLAN_READY`;
- wrong-surface commands are rejected.

All Python files materialized in the isolated candidate working copy were compiled successfully with `py_compile`.

## Full-repository validation pending after overlay

The delivery ZIP intentionally contains only changed/new repository-relative files. The environment could read current `main` through the GitHub connector but could not materialize a complete Git checkout through the runtime network. Therefore these checks were not executed on a complete overlaid repository in this session:

```text
python Workplan/scripts/validate.py --full
```

The updated `validate.py` is designed to run both `run_scenarios.py` and `run_command_protocol.py`. `run_scenarios.py` was updated for the v5.2 command/approval entry contract, but its complete execution requires the unchanged v5.1 implementation files from `main` to be present alongside the candidate.

`Workplan/FILE_SHA256SUMS.txt` is not included in this changed-files candidate because a trustworthy full-repository checksum regeneration requires the complete overlaid tree. Regenerate it only after applying the candidate to a clean v5.1.0 baseline and after full validation passes.
