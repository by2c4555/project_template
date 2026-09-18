# Release Validation — Project Template v5.3.2

This document is the authoritative release-validation specification and acceptance record for the v5.3.2 candidate.

A check is PASS only when the corresponding command was actually executed successfully against the candidate tree.

---

## 1. Verified baseline

Source of truth:

```text
repository: by2c4555/project_template
branch:     main
version:    5.3.1
verified:   2026-09-18
```

The supplied `Project Template v5.3.1.zip` working baseline was verified against current `main` by exact Git blob identity for:

```text
Workplan/VERSION
Workplan/Objective_dev.md
Workplan/README.md
README.md
```

Before any v5.3.2 edit, the baseline full validator was executed successfully:

```bash
PYTHONDONTWRITEBYTECODE=1 python Workplan/scripts/validate.py --full
```

Observed baseline result:

```text
STRUCTURAL_VALID: PASS (v5.3.1 schema 6)
COMMAND_PROTOCOL_VALID: PASS
V53_INVARIANTS_VALID: PASS
V531_HARDENING_VALID: PASS
V531_FINAL_ACCEPTANCE_VALID: PASS
SCENARIO_VALID: PASS
RECOVERY_SCENARIO_VALID: PASS
TEMPLATE_VALID: PASS (v5.3.1 --full)
```

All v5.3.2 changes were made only in an isolated working copy. Remote GitHub state was not modified.

---

## 2. Release intent

v5.3.2 is a **Development Constitution and architecture-alignment hardening release**.

It is not a schema or normal-lifecycle redesign.

Preserved invariants:

```text
schema = 6
Cycle -> Phase -> Task -> Attempt
Research -> Planning -> Execution -> Evaluation
exact public command authority
human approval separation
Task Gate / Phase Gate authority
bounded Repair
reasoning-only External Diagnosis / Recovery
Independent Evaluation
CLOSED_VALIDATED final state
```

Primary release goals:

1. Replace the monolithic `Workplan/Objective_dev.md` with a human-owned, AI-read-only Development Constitution package.
2. Separate development Objective, Reference Architecture, and new-version Development Prompt so each concern has one source of truth.
3. Make Project Template identity explicit as an AI-assisted software-development control plane.
4. Make Manager responsible for Task-local software debugging/Repair reasoning while Builder remains a low-cost bounded implementation worker.
5. Require an explicit Manager repair reason/strategy before a fresh Builder `REPAIR` Attempt.
6. Preserve durable local diagnosis/failure context for escalation.
7. Repair Diagnosis continuation so Plan/Task defects require a changed Planning Package and owner/external-resolution classes do not loop back into Diagnosis.
8. Add safe v5.3.1 -> v5.3.2 migration while preserving schema 6.
9. Remove obsolete release-specific test filenames and duplicate constitution authority.

---

## 3. Canonical Development Constitution

Required files:

```text
Workplan/development_constitution/README.md
Workplan/development_constitution/OBJECTIVE.md
Workplan/development_constitution/REFERENCE_ARCHITECTURE.md
Workplan/development_constitution/DEVELOPMENT_PROMPT.md
```

Every file must begin with exactly:

```text
> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.
```

Ownership:

```text
README.md
    package boundary and human ownership

OBJECTIVE.md
    product identity, goals, principles, invariants

REFERENCE_ARCHITECTURE.md
    canonical architecture and control flow

DEVELOPMENT_PROMPT.md
    guidance for AI developing Project Template itself
```

The obsolete path must not exist:

```text
Workplan/Objective_dev.md
```

No runtime role receives constitution mutation authority. Constitution updates are performed externally by the repository owner.

---

## 4. Manager / Builder boundary

Required Manager properties:

```text
.github/agents/manager.agent.md
name: ExecutionManager
no model field
no production edit tool
only Builder subagent
task-local software debugging / diagnosis
Repair strategy responsibility
```

Required Builder properties:

```text
.github/agents/builder.agent.md
name: Builder
model: Project Builder Local
not user-invocable
no subagents
bounded Task / Repair / Recovery implementation
no autonomous open-ended diagnose/edit/retry loop
```

Runtime repair behavior:

```text
Task Gate FAIL
    -> Manager diagnosis / explicit repair reason
    -> fresh Builder REPAIR Attempt
    -> Task Gate
```

The Task contract repair budget remains `0..5`, default `2`, hard maximum `5`.

Structural failures may escalate before budget exhaustion.

---

## 5. Migration

Required current patch migration:

```text
Workplan/MIGRATION_V5_3_1_TO_V5_3_2.md
Workplan/scripts/migrate_v531_to_v532.py
```

Migration requirements:

```text
from workflow_version = 5.3.1
to   workflow_version = 5.3.2
schema_version         = 6
active_work            = null
pending_approval       = null
```

The historical migration:

```text
Workplan/scripts/migrate_v530_to_v531.py
```

must remain usable as the first step of the supported chained upgrade:

```text
5.3.0 -> 5.3.1 -> 5.3.2
```

The historical script therefore performs self-contained post-write verification rather than calling the current-release `load_state()` after stopping at v5.3.1.

---

## 6. Canonical validation suites

Full validation must execute these bounded suites:

```text
Workplan/tests/run_command_protocol.py
Workplan/tests/run_v53_invariants.py
Workplan/tests/run_research_builder_hardening.py
Workplan/tests/run_constitution_hardening.py
Workplan/tests/run_issue_lifecycle.py
Workplan/tests/run_migration_regressions.py
Workplan/tests/run_final_acceptance.py
Workplan/tests/run_scenarios.py
Workplan/tests/run_recovery_scenario.py
```

Obsolete release-specific test filenames must not exist:

```text
Workplan/tests/run_v531_hardening.py
Workplan/tests/run_v531_acceptance.py
```

---

## 7. Targeted behavioral validation

Environment:

```text
Python 3.13.5
PYTHONDONTWRITEBYTECODE=1
```

The following candidate suites were executed individually before final manifest generation:

```text
COMMAND_PROTOCOL_VALID: PASS
V53_INVARIANTS_VALID: PASS
RESEARCH_BUILDER_HARDENING_VALID: PASS
CONSTITUTION_HARDENING_VALID: PASS
ISSUE_LIFECYCLE_VALID: PASS
MIGRATION_REGRESSIONS_VALID: PASS
FINAL_ACCEPTANCE_VALID: PASS
SCENARIO_VALID: PASS
RECOVERY_SCENARIO_VALID: PASS
```

These results verify the modified behavior independently of the release-manifest freshness check.

---

## 8. Structural/release validation procedure

After all release files are stable:

```bash
PYTHONDONTWRITEBYTECODE=1 python Workplan/scripts/integrity.py generate
PYTHONDONTWRITEBYTECODE=1 python Workplan/scripts/validate.py
PYTHONDONTWRITEBYTECODE=1 python Workplan/scripts/validate.py --full
```

Required final observations:

```text
STRUCTURAL_VALID: PASS (v5.3.2 schema 6)
TEMPLATE_VALID: PASS (v5.3.2 structural)
TEMPLATE_VALID: PASS (v5.3.2 --full)
```

Final candidate observations are recorded in Section 11 after execution.

---

## 9. Release cleanliness

The release must not contain:

```text
.git/
__pycache__/
*.pyc
virtual environments
cache directories
editor-local files
runtime Work/approval/history/ingest payloads
temporary files
ZIP artifacts
Workplan/Objective_dev.md
Workplan/tests/run_v531_hardening.py
Workplan/tests/run_v531_acceptance.py
```

Historical migration documentation/scripts are retained only where needed for supported upgrade chains.

The integrity manifest is deterministic and must match the final candidate tree exactly.

---

## 10. Packaging

The implementation delivery candidate must preserve repository-relative paths and contain only files that differ from v5.3.1, including deletions represented by the accompanying change summary rather than obsolete duplicate files.

The full repository itself is not modified remotely by this validation process.

---

## 11. Final candidate validation record

Final candidate validation was executed with:

```text
Python 3.13.5
PYTHONDONTWRITEBYTECODE=1
release_files: 108
```

Commands executed:

```bash
python Workplan/scripts/integrity.py generate
python Workplan/scripts/validate.py
python Workplan/scripts/validate.py --full
```

Observed results:

```text
RELEASE_INTEGRITY: PASS
STRUCTURAL_VALID: PASS (v5.3.2 schema 6)
TEMPLATE_VALID: PASS (v5.3.2 structural)
COMMAND_PROTOCOL_VALID: PASS
V53_INVARIANTS_VALID: PASS
RESEARCH_BUILDER_HARDENING_VALID: PASS
CONSTITUTION_HARDENING_VALID: PASS
ISSUE_LIFECYCLE_VALID: PASS
MIGRATION_REGRESSIONS_VALID: PASS
FINAL_ACCEPTANCE_VALID: PASS
SCENARIO_VALID: PASS
RECOVERY_SCENARIO_VALID: PASS
TEMPLATE_VALID: PASS (v5.3.2 --full)
```

The post-record rerun regenerated the release manifest and executed full validation again. It passed with the same v5.3.2 suite results. No release-tracked file may change after the final manifest/validation pass used for packaging.
