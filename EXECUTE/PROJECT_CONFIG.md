# Project Configuration

This file defines static workflow policy. It is not runtime state.

The hard model requirements are intentional and must not be silently overridden.

## Model Policy

```yaml
models:
  planner:
    minimum_context_tokens: 524288
    context_override_allowed: false
    controlled_context_target_tokens: 262144
    controlled_context_max_tokens: 307200

  builders:
    minimum_context_tokens: 131072
    context_override_allowed: false

    profiles:
      Builder128K:
        minimum_context_tokens: 131072
        controlled_context_target_tokens: 49152
        controlled_context_max_tokens: 65536

      Builder256K:
        minimum_context_tokens: 262144
        controlled_context_target_tokens: 98304
        controlled_context_max_tokens: 131072
```

Planner below 512K is unsupported.

Builder below 128K is unsupported.

Context requirements are capability floors, not targets for filling the entire window.

## Execution Policy

```yaml
execution:
  default_builder: Builder128K
  escalation_builder: Builder256K

  prefer_task_split_before_escalation: true

  stop_on_non_pass: true

  repair_attempts: 2
  same_approach_repeats: 1

  phase_auto_continue_on_pass: true
```

Builder256K is not an architecture role.

## Interaction Policy

```yaml
interaction:
  task_completion_mode: auto
  phase_completion_mode: ask
  executor_escalation_mode: ask
```

The user authorizes work at Phase boundaries rather than after every successful Task.

Escalation to a stronger Builder is visible to the user.

## Planning Policy

```yaml
planning:
  require_project_details: true
  require_knowledge_validation: true
  require_plan_validation: true
  require_task_pack_validation: true

  architecture_critical_unknowns_block: true
  persist_blocking_questions: true
```

## Knowledge Policy

```yaml
knowledge:
  execution_access: read_only
  planner_write_only: true
  require_provenance: true
```

Builder discoveries are recorded in Task history or Issues first.

Planner promotes durable verified facts into Knowledge.

## Environment Policy

```yaml
environment:
  user_env: ".env.user"
  execute_env: "EXECUTE/.env.execute"
  required_placeholder: "__REQUIRED__"

  production_access_default: false
  database_write_default: false

  never_guess_external_configuration: true
```

`.env.user` is human-owned and must never be committed.

`EXECUTE/.env.execute` must never contain secrets.

## Release Policy

```yaml
release:
  require_system_test: true
  require_package: true
  require_clean_install: true
  require_release_gate: true
```

A project is not COMPLETE until enabled release gates PASS.

## Default External I/O Policy

Task-specific values may be more restrictive.

```yaml
external_io_defaults:
  repeated_equivalent_calls: 2
  transient_retries_per_operation: 2

  api_pages: 3
  api_requests: 8
  api_items_per_page: 100

  db_queries: 8
  db_rows_per_query: 100
```

External access must be bounded and evidence-driven.
