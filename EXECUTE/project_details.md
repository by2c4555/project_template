# Project Details

Purpose: provide high-quality project source input for Planning.

Do not manually decompose the project into `TASK_NNN` files here unless a task boundary is itself a hard requirement.

Fill what is known. Mark unknowns explicitly instead of guessing.

## 1. Project Identity

```yaml
project_id: "__REQUIRED__"
project_name: "__REQUIRED__"
project_type: "__REQUIRED__"
repository_state: "new"
primary_language: "__REQUIRED__"
primary_framework: "none"
target_platforms: []
```

## 2. Project Summary

Describe what the system does, who/what uses it, its primary output/value, whether it is new/migration/extension/repair, and its most important technical boundary.

## 3. Goals

```text
GOAL-001:
GOAL-002:
```

## 4. Success Criteria

```text
SUCCESS-001:
SUCCESS-002:
```

## 5. Scope

### In Scope

```text
SCOPE-IN-001:
```

### Out of Scope

```text
SCOPE-OUT-001:
```

## 6. Functional Requirements

```text
REQ-001:
REQ-002:
```

## 7. Non-Functional Requirements

Consider performance, security, reliability, observability, compatibility, resource limits, latency/throughput, privacy, and maintainability.

```text
NFR-001:
```

## 8. Existing System / Repository

Describe important modules, verified working behavior, known broken behavior, and compatibility constraints.

## 9. Data

Describe entities, schemas/formats, lifecycle, retention, migrations, and expected scale.

## 10. Database

If applicable, describe database/version, schema constraints, read/write expectations, transactions, migration constraints, scale assumptions, and whether production access is allowed for automated tests.

Do not put credentials here.

## 11. APIs / External Services

Describe purpose, known endpoint family, auth method, request/response contract, pagination, rate limits, failure behavior, staging/test availability, and whether production access is prohibited.

Do not put secrets here.

## 12. Runtime / Platform / Dependencies

Describe supported OS/runtime versions, required libraries/tools, hardware/GPU/device requirements, packaging constraints, and deployment environment.

## 13. User Workflows

Describe critical end-to-end flows.

## 14. Error / Failure Expectations

Describe expected behavior for missing configuration, external failure, invalid input, partial work, and recovery.

## 15. Security / Access Constraints

Describe policy only. Actual credentials belong in `.env.user`.

## 16. Testing Expectations

Describe must-pass workflows, important regressions, required integration environments, realistic external-system validation, and unacceptable substitutions/mocking.

## 17. Packaging / Installation / Release

Describe expected deliverable, installation method, clean-install behavior, smoke test, and supported target environments.

## 18. Known Risks / Uncertainties

```text
RISK-001:
UNKNOWN-001:
```

## 19. Source Documents

List important files placed under `EXECUTE/docs/`.

## 20. Notes for Planning

Add information that materially affects architecture or task decomposition.

Do not include secrets.
