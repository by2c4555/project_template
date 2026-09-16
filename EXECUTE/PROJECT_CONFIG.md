# Project Configuration

Version: 3.4.1 Lean

This file defines project-wide AI workflow policy. It is intended to be committed.

Do not store runtime state or secrets here.

## Quick Settings

Most users normally change only these:

```yaml
planning:
  model: "__SELECT__"
  replan_model: "SAME_AS_PLANNING"
  reuse_for_replanning: true

execution:
  builder_selection: "AUTO"

testing:
  generation_mode: "hybrid"
```

## Planning

- `model`: high-capability model used for project-wide planning. `__SELECT__` means the workflow must ask before Planning.
- `replan_model`: model used for replanning. `SAME_AS_PLANNING` reuses the configured Planning model.
- `reuse_for_replanning`: when `true`, do not ask again unless the model is unavailable or the user overrides it.

## Execution

`builder_selection` accepts:

```text
AUTO
Builder32K
Builder64K
Builder128K
Builder200K
Builder500K
```

`AUTO` means Planning selects the smallest safe Builder for each Task.

```yaml
execution:
  builder_selection: "AUTO"
  allow_larger_builder: true
  allow_smaller_builder: false
  require_runtime_context_check: true
```

A smaller Builder/model must never execute a task planned for a larger profile.

## Testing

```yaml
testing:
  generation_mode: "hybrid"
```

- `hybrid`: recommended; Planner creates stable contract tests and Builder creates implementation-specific tests.
- `contract_only`: Planner defines test contracts only.
- `full_tdd`: Planner creates as many stable executable tests as practical.

## Knowledge Base

```yaml
knowledge:
  execution_access: "read_only"
  planner_write_only: true
  require_provenance: true
  preserve_superseded_knowledge: true
```

Only Planning/Replanning may change `EXECUTE/reference/`.

## Repair

```yaml
repair:
  max_attempts_per_round: 5
  max_same_approach_repeats: 2
```

Five attempts are a maximum, not a target.

## Exploration Defaults

```yaml
exploration:
  default_search_rounds: 3
  default_additional_files: 6
  default_log_lines: 200
```

Task-specific budgets may be tighter or explicitly justified.

## External I/O Defaults

```yaml
external_io:
  repeated_equivalent_calls: 2
  transient_retries_per_operation: 2
```

These prevent DB/API loops. Task-specific request/query/page limits belong in each Task.

## Environment Safety

```yaml
environment:
  user_env: ".env.user"
  execute_env: "EXECUTE/.env.execute"
  missing_value_placeholder: "__REQUIRED__"
  production_access_default: false
  database_write_default: false
```

`.env.user` is human-owned and may contain credentials/endpoints. It is never committed.

`EXECUTE/.env.execute` is AI/workflow-owned and must remain secret-free.

## Release

```yaml
release:
  require_system_test: true
  require_package: true
  require_clean_install: true
  require_release_gate: true
```

Project COMPLETE requires every enabled release gate to PASS.
