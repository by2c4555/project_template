# v5.1.0 Release Validation

Baseline studied: `main` v5.0.0 commit `bd0f0a96f5375efdb2e5836867c86a54742414c8`.

Executed on the generated v5.1.0 release tree:

```bash
python Workplan/scripts/validate.py --full
```

Result:

```text
TEMPLATE_VALID: PASS (v5.1.0)
SCENARIO_VALID: PASS
```

The executable scenario verifies:

- explicit Research ingest and canonical Scope import;
- separate physical-package and logical-Scope digests;
- Planning entry ingest revalidation;
- provider handoff generation increment;
- stale generation mutation rejection;
- semantic checkpoint continuation;
- final Planning revalidation, accepted-input archive and ingest normalization;
- deterministic ExecutionManager next/dispatch without user-selected Task ID;
- interrupted Builder reacquisition and stale Builder fencing;
- machine-computed `RECONCILE_ACTIVE_UNIT` and CLEAN states;
- immutable Task evidence completion;
- deterministic transition to independent Evaluation;
- Completion Report exact Scope binding;
- `CLOSED_VALIDATED` final state;
- Python compilation and required v5.1 structural/constitution checks.

The shipped package is reset to clean `AWAITING_SCOPE` state (schema 4); test mutations occur only in temporary copies.
