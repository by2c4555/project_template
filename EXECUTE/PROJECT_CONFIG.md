# Project Configuration

Static workflow policy for v4.0.1. Runtime state lives in `PROJECT_STATUS.md`.
Hard model/context requirements must not be silently overridden.

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

Provider-specific model names are not guessed by the template. Before execution, run `scripts/configure_models.py` with trusted documented capacities. It updates `EXECUTE/MODEL_BINDINGS.json` and pins `model:` in the three role agents. An unbound or undersized role is not runtime-ready.

## Context Isolation Policy

```yaml
context_isolation:
  task_is_fresh_subagent_invocation: true
  planner_transaction_is_fresh_subagent_invocation: true
  integration_gate_is_fresh_subagent_invocation: true
  retry_is_fresh_subagent_invocation: true
  conversation_history_authoritative: false
  cross_task_full_context_inheritance: false
  inter_agent_handoff: result_capsule_only
```

Invariant:
`1 Task = 1 execution contract = 1 isolated subagent invocation = 1 fresh context window.`

Disk artifacts are persistent memory. Model context is temporary working memory.

## Agent Routing Policy

```yaml
routing:
  user_entry_agent: ProjectManager
  planner_agent: Planner512K
  default_builder: Builder128K
  escalation_builder: Builder256K
  builders_may_spawn_subagents: false
  planner_may_spawn_subagents: false
  project_manager_may_spawn:
    - Planner512K
    - Builder128K
    - Builder256K
```

## Execution Policy

```yaml
execution:
  prefer_task_split_before_escalation: true
  stop_on_non_pass: true
  repair_attempts: 2
  same_approach_repeats: 1
  phase_auto_continue_on_pass: true
  fresh_context_per_retry: true
```

Builder256K remains an execution role, not an architecture role.

## Local Output Budget

```yaml
local_output_budget:
  max_command_output_chars_into_model: 12000
  max_search_results_into_model: 100
  max_log_excerpt_lines_into_model: 200
  max_diff_lines_into_model: 400
  max_test_failure_excerpt_lines_into_model: 250
```

Full raw output should remain in terminal or be persisted to an ignored/local file. Only summaries or focused excerpts should enter model context.

## Context Estimation Policy

```yaml
context_estimation:
  estimator: scripts/context_guard.py
  chars_per_token_estimate: 4
  include_task_contract: true
  include_listed_write_read_test_files: true
  expected_tool_output_reserve_tokens:
    Builder128K: 6000
    Builder256K: 12000
  decisions:
    within_target: PASS
    over_target_under_max: WARN
    over_max: SPLIT_REQUIRED
```

This is a conservative deterministic preflight, not a tokenizer-accurate measurement. It exists to block obviously oversized Task packs before their files are injected into model context.

## Interaction Policy

```yaml
interaction:
  task_completion_mode: auto
  phase_completion_mode: ask
  executor_escalation_mode: ask
```

The user authorizes at Phase boundaries. PASS may auto-route to the next Task, but never reuses the previous Task context.

## Planning Policy

```yaml
planning:
  require_project_details: true
  require_knowledge_validation: true
  require_plan_validation: true
  require_task_pack_validation: true
  architecture_critical_unknowns_block: true
  persist_blocking_questions: true
  checkpoint_transactions:
    - PT1_INPUT_KNOWLEDGE
    - PT2_ARCHITECTURE_PLAN
    - PT3_RISK_PHASES
    - PT4_TASK_COMPILATION
    - PT5_TASK_PACK_VALIDATION
```

## Knowledge Policy

```yaml
knowledge:
  execution_access: read_only
  planner_write_only: true
  require_provenance: true
```

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

`.env.user` is human-owned and must never be committed. `EXECUTE/.env.execute` must never contain secrets.

## Release Policy

```yaml
release:
  require_system_test: true
  require_package: true
  require_clean_install: true
  require_release_gate: true
```

## Default External I/O Policy

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
