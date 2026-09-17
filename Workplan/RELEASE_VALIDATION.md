# Release Validation — Project Template v5.3.1

This document is the authoritative release-validation specification and acceptance record for the v5.3.1 full release.

It distinguishes **required procedure** from **results actually observed**. A check is PASS only when the corresponding command was executed successfully against the actual candidate tree.

---

## 1. Verified baseline

Development baseline:

```text
repository: by2c4555/project_template
branch:     main
commit:     ec4e53921692c7ba3f73514de41ed5bc470b1ecb
version:    5.3.0
```

The supplied v5.3.0 baseline ZIP was previously verified against current `main` using the exact Git blob identity of the release integrity manifest.

All v5.3.1 changes were produced in an isolated working copy. Remote GitHub state was not modified.

---

## 2. Release intent

v5.3.1 is a **hardening patch**, not a workflow redesign.

Preserved invariants:

```text
schema = 6
Cycle -> Phase -> Task -> Attempt
Research -> Plan -> Manage -> Build
exact public command authority
human approval separation
Task Gate / Phase Gate authority
bounded Repair
reasoning-only Diagnosis / Recovery
Independent Evaluation
CLOSED_VALIDATED final state
```

Hardening scope:

1. VS Code Manager/Builder cost and capability separation.
2. High-quality External Research -> canonical ingest contract.
3. Safe v5.3.0 -> v5.3.1 patch migration.
4. Canonical documentation ownership and full-release tree cleanup.
5. Behavioral validation of the new boundaries.

---

## 3. Canonical v5.3.1 agent structure

Required workspace agents:

```text
.github/agents/manager.agent.md
.github/agents/builder.agent.md
```

Manager requirements:

- `name: ExecutionManager`;
- no `model:` field;
- tools: read/search/execute/agent;
- no production edit tool;
- `agents: ['Builder']` only;
- user-invocable.

Builder requirements:

- `name: Builder`;
- `model: 'Project Builder Local'`;
- read/search/edit/execute;
- no subagents;
- not user-invocable.

Removed legacy alias:

```text
.github/agents/builder100k.agent.md
```

must not exist in the canonical v5.3.1 release.

---

## 4. Canonical Research structure

Required Research sources of truth:

```text
Workplan/external_agent/RESEARCH_INSTRUCTION.md
Workplan/external_agent/RESEARCH_POTOCAL_PROMPT.md
Workplan/templates/PROJECT_DETAILS_TEMPLATE.md
Workplan/CHATGPT_PROJECT_INSTRUCTIONS.md
```

Obsolete duplicate paths must not exist:

```text
Workplan/external_agent/RESEARCH_PROMPT.md
Workplan/external_agent/EXTERNAL_RESEARCH_PROTOCOL.md
Workplan/docs/INGEST_PROJECT_DETAILS_TEMPLATE.md
Workplan/project_details.md
```

The protocol identifier remains:

```text
EXTERNAL_RESEARCH_PROTOCOL_V1
```

for deterministic ingest compatibility.

---

## 5. Full-release cleanliness

The packaged release must contain only repository material that participates in supported control, documentation, migration, testing, or runtime structure.

The release must not contain:

```text
.git/
__pycache__/
*.pyc
*.pyo
virtual environments
cache directories
editor-local state
temporary files
secrets/credentials
runtime-local Work/history/approval/ingest payloads
ZIPs nested inside the release
obsolete Research duplicates
obsolete Builder aliases
unrelated empty root src/test/docs/package placeholders
```

Runtime Workplan directories may retain `.gitkeep` sentinels where stable directory structure is useful.

---

## 6. Focused validation procedure

Before the release manifest is regenerated, run bounded suites independently so failures can be diagnosed without repeatedly invoking the whole E2E workflow.

Required commands:

```bash
PYTHONDONTWRITEBYTECODE=1 python Workplan/tests/run_v531_hardening.py
PYTHONDONTWRITEBYTECODE=1 python Workplan/tests/run_command_protocol.py
PYTHONDONTWRITEBYTECODE=1 python Workplan/tests/run_v53_invariants.py
PYTHONDONTWRITEBYTECODE=1 python Workplan/tests/run_scenarios.py
PYTHONDONTWRITEBYTECODE=1 python Workplan/tests/run_recovery_scenario.py
PYTHONDONTWRITEBYTECODE=1 python Workplan/tests/run_v531_acceptance.py
```

Observed on the final documentation/tree candidate before manifest refresh:

```text
V531_HARDENING_VALID: PASS
COMMAND_PROTOCOL_VALID: PASS
V53_INVARIANTS_VALID: PASS
SCENARIO_VALID: PASS
RECOVERY_SCENARIO_VALID: PASS
V531_FINAL_ACCEPTANCE_VALID: PASS
```

---

## 7. v5.3.1 hardening suite coverage

`run_v531_hardening.py` behaviorally checks:

### Agent/cost boundary

- Manager has no pinned model;
- Manager has no production edit capability;
- Manager can invoke only Builder;
- Builder pins `Project Builder Local`;
- Builder is not user-invocable;
- removed Builder100K agent does not exist.

### Research ingress

- canonical Research instruction/protocol files exist;
- obsolete Research prompt/protocol files do not exist;
- valid canonical Research handoff passes;
- missing protocol marker fails closed;
- missing required section fails closed;
- malformed `supporting_files` syntax fails closed.

### Compatibility

- already-accepted v5.3.0-style ingest remains immutable-digest revalidatable when strict new-Research shape is not being applied retroactively.

### Migration

- v5.3.0 -> v5.3.1 migration succeeds at a safe boundary;
- migration rejects active Work.

---

## 8. Real final-acceptance scenario

Required command:

```bash
PYTHONDONTWRITEBYTECODE=1 python Workplan/tests/run_v531_acceptance.py
```

The scenario is not a string/static test. It creates and validates a real isolated mock project Cycle:

```text
strict Research ingest
  -> Scope import
  -> approval-gated Planning
  -> two explicit Phases / two bounded Tasks
  -> calculator production implementation
  -> actual CLI verification
  -> Task Gate PASS
  -> Phase Gate PASS
  -> unittest implementation
  -> actual unittest execution
  -> Task Gate PASS
  -> Phase Gate PASS
  -> Independent Evaluation
  -> independent final behavior rechecks
  -> evaluation.py finalize PASS
  -> CLOSED_VALIDATED
  -> WORKPLAN_NEXT = EXECUTE_RESEARCH
```

Observed:

```text
V531_FINAL_ACCEPTANCE_VALID: PASS
```

---

## 9. Integrity generation

After all release files are stable:

```bash
python Workplan/scripts/integrity.py generate
```

Then check:

```bash
python Workplan/scripts/integrity.py check
```

Expected final manifest release-file count:

```text
102
```

Do not regenerate the manifest merely to hide unexpected local changes. Manifest generation is a release-construction step; later validation must only check it.

---

## 10. Structural validation

Required:

```bash
PYTHONDONTWRITEBYTECODE=1 python Workplan/scripts/validate.py
```

Expected:

```text
STRUCTURAL_VALID: PASS (v5.3.1 schema 6)
TEMPLATE_VALID: PASS (v5.3.1 structural)
```

Structural validation checks applicable:

- required canonical files;
- version/schema/config consistency;
- canonical Research/agent file names;
- absence of obsolete release files;
- Python syntax;
- release integrity manifest consistency;
- current operational docs/prompts for stale release headings/direct recovered-PASS behavior.

---

## 11. Authoritative full validation

Required final working-copy command:

```bash
PYTHONDONTWRITEBYTECODE=1 python Workplan/scripts/validate.py --full
```

Expected/observed suite set:

```text
command_protocol
v53_invariants
v531_hardening
v531_final_acceptance
normal_e2e
recovery_e2e
```

Final working-copy result:

```text
STRUCTURAL_VALID: PASS (v5.3.1 schema 6)
COMMAND_PROTOCOL_VALID: PASS
V53_INVARIANTS_VALID: PASS
V531_HARDENING_VALID: PASS
V531_FINAL_ACCEPTANCE_VALID: PASS
SCENARIO_VALID: PASS
RECOVERY_SCENARIO_VALID: PASS
TEMPLATE_VALID: PASS (v5.3.1 --full)
exit code: 0
wall time: 12.66 seconds (observed pre-package acceptance run)
```

A required suite timeout or non-zero exit makes the full validator FAIL.

---

## 12. Documentation/version consistency

Before packaging, verify all operational release surfaces describe one release:

```text
Workplan/VERSION
README.md
Workplan/README.md
Workplan/Objective_dev.md
Workplan/ENTRY_PROMPT.md
Workplan/CHATGPT_PROJECT_INSTRUCTIONS.md
Workplan/external_agent/*.md
.github/agents/*.md
Workplan/config/MODEL_CONFIG.ini
Workplan/config/MODEL_BINDINGS.json
Workplan/MIGRATION_V5_3_0_TO_V5_3_1.md
Workplan/CHANGELOG.md
Workplan/RELEASE_VALIDATION.md
```

Expected workflow version: `5.3.1`.

Expected state schema: `6`.

---

## 13. Full ZIP packaging

The user requested a **full repository ZIP**, not a changed-files patch.

Packaging procedure:

1. clean runtime/local artifacts;
2. preserve repository-relative paths;
3. include the complete canonical release tree;
4. exclude `.git/`, secrets, caches, venvs, bytecode, editor-local state, temp files, runtime-local Work payloads, and nested ZIP artifacts;
5. create a single top-level repository directory inside the archive;
6. compute SHA-256.

Final ZIP:

```text
project_template-v5.3.1-full.zip
```

Final checksum:

```text
SHA-256 recorded in the external delivery acceptance report after the final archive is created
bytes:   recorded in the external delivery acceptance report
```

---

## 14. Clean-room ZIP verification

After packaging, do not trust the working-copy result alone.

Required procedure:

```text
extract full ZIP into a fresh directory
  -> verify version/tree cleanliness
  -> run integrity check
  -> run structural validator
  -> run full validator
```

Clean-room result:

```text
recorded in the external delivery acceptance report after validating the final archive
wall time: recorded externally for the final archive
```

This verifies the artifact delivered to the user contains everything needed for release validation and does not depend on unshipped working-copy files.

---

## 15. Final acceptance matrix

| Criterion | Evidence | Result |
|---|---|---|
| Version/schema consistent | VERSION/state/config/validator | PASS |
| Research canonical files + strict ingest | hardening + acceptance suites | PASS |
| Manager/Builder cost boundary | static/behavioral hardening test | PASS |
| Exact command authority | command protocol suite | PASS |
| Core v5.3 invariants | v53 invariant suite | PASS |
| Normal end-to-end execution | normal E2E | PASS |
| Diagnosis/Recovery execution | Recovery E2E | PASS |
| Real final Evaluation closure | v531 final acceptance | PASS |
| Release integrity | generated manifest + check | PASS |
| Full working-copy validation | `validate.py --full` | PASS |
| Full ZIP clean-room validation | extracted artifact full validation | SEE EXTERNAL DELIVERY REPORT |
| Live VS Code local-Qwen subagent endpoint | requires user's VS Code/local model | ENVIRONMENT CHECK |

---

## 16. Known environment limitation

The release-validation environment does not contain the user's actual VS Code desktop runtime or local Qwen endpoint. Therefore it cannot prove a live machine-specific `ExecutionManager -> Builder -> Project Builder Local` invocation.

What the release validates deterministically:

- agent frontmatter/model/tool boundaries;
- Manager has no production edit tool;
- Builder pins the expected local alias;
- Workplan execution/routing/gates remain provider-neutral.

Machine smoke test after installation:

1. register the intended local model in VS Code as `Project Builder Local`;
2. select `ExecutionManager` and the desired paid/strong Manager model;
3. run one bounded implementation Task;
4. confirm the Builder subagent reports the local model and production edits occur only through Builder.

This is an environment integration check, not a known control-plane validation failure.

---

## 17. Final release rule

Do not publish or claim delivery PASS unless:

```text
focused suites PASS
integrity generated/check PASS
structural validation PASS
full working-copy validation PASS
full ZIP created
clean-room extracted ZIP validation PASS
checksum recorded
```

Repository state and executed validation are authority; a model statement is not.
