---
artifact_kind: PROJECT_DETAILS
artifact_status: INCOMPLETE
scope_title: TODO
baseline_ref: none
product_scope_unknowns: unknown
supporting_files: []
---

# Project Details

This file is the concise canonical external scope handoff for External Agent Planning.

Do not use it as a research diary or repository implementation plan. Keep only the **current confirmed truth** needed to understand what must be built, preserved, or verified.

A final handoff must use `artifact_status: READY_FOR_PLANNING` and `product_scope_unknowns: 0`. If material product/scope information is still unresolved, do not finalize this file.

## 1. Executive Handoff

What problem/change is being requested, why it matters, and what outcome is expected?

TODO

## 2. Current Baseline

Describe only verified baseline facts relevant to this scope.

For a new project, state that no prior validated baseline exists.

TODO

## 3. Change Summary / Delta

Summarize what is new or changed relative to the baseline.

- TODO

## 4. Requirements

Use stable requirement IDs when useful, for example `REQ-001`.

Mark importance when relevant (`MUST`, `SHOULD`, `OPTIONAL`).

- REQ-001 — TODO

## 5. Scope

### In Scope

- TODO

### Out of Scope / Non-Goals

- TODO

### Explicitly Unchanged

For an existing validated system, list behavior/subsystems that this scope does not intend to change.

- TODO

## 6. Constraints and Invariants

List only constraints that implementation must preserve or satisfy: compatibility, platform, protocol, security, performance, workflow, data, deployment, or other material boundaries.

- TODO

## 7. Confirmed Decisions

Product/scope decisions explicitly confirmed by the user.

- TODO

## 8. Implementation-Relevant Facts

Distilled facts/observations that materially affect technical planning. Distinguish provenance/classification.

Example:

```text
FACT-001
Classification: VERIFIED_FACT
Finding: ...
Evidence: EXECUTE/docs/raw/example.md
```

- TODO

## 9. External / Reference Findings

Summarize only findings that materially affect scope or implementation readiness. Point to `docs/raw/*` rather than copying large evidence here.

- TODO

## 10. Known Risks

Known external/product/integration risks that External Agent Planning should prioritize during repository research.

- TODO

## 11. Remaining Unknowns

### Product / Scope Unknowns

A final handoff must contain `NONE` here and `product_scope_unknowns: 0` in metadata.

- TODO

### Technical Unknowns for External Agent Planning

Repository/implementation questions that do not block the external scope handoff.

- TODO

## 12. Repository Investigation Targets

Questions External Agent Planning should answer during targeted repository research. Do not prescribe implementation unless it is itself a requirement.

- INV-001 — TODO

## 13. Success Criteria

Use observable/testable criteria and link them to requirements when useful.

- SC-001 -> REQ-001 — TODO

## 14. External Agent Context Map

Prioritize supporting evidence so External Agent Planning does not read all raw files by default.

### P0 — Read During Planning

- none

### P1 — Read When Relevant

- none

### P2 — Read Only If Needed

- none

## 15. Supporting Research Index

List the exact supporting files included in the metadata `supporting_files` field and what each is for.

- none
