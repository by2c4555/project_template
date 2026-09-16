# Project Contract

## Goal

Raphael is a KiCad-centered PCB layout automation system with project-owned deterministic routing and analysis, explicit mutation safety, and optional AI orchestration separated from correctness-critical geometry and validation.

The product is not a fork/rebranding of any one donor project. Donors supply evidence, algorithms, KiCad integration knowledge, tests/fixtures, and reusable implementation candidates where licensing and project boundaries allow.

## Product boundaries

### In scope at architecture level

- KiCad PCB/project acquisition sufficient to construct authoritative routing/analysis state.
- Product-owned canonical board state/snapshot.
- KiCad design rules, net classes, relevant custom rules, keepouts/rule areas, and stack/layer constraints needed by routing/validation.
- Stable product `RoutingPolicy` boundary for user and optional AI intent.
- New deterministic Core Router.
- Search, candidate generation, route metrics, bounded optimization/negotiation, and controlled rip-up/reroute.
- Object identity, ownership/protection, and mutation authorization.
- Router-neutral ChangeSet and safe KiCad apply/rollback boundary.
- Deterministic Analyzer with geometry/connectivity/routing-quality/native-validation normalization and engineering findings.
- Product-owned metrics/findings/execution-status/provenance concepts.
- Regression fixtures and donor parity/compatibility evidence where licensing permits.

### Conditional / not confirmed for V1

- full automated component placement;
- push/shove routing;
- blind/buried/microvia support;
- router-owned plane generation/fill;
- topology/navmesh search in first release;
- global capacity planning in first release;
- deep SI/PI/EM simulation;
- optional AI review of findings.

### Current architecture exclusions / direction

- KiCadRoutingTools as the product Core Router architecture;
- `pcb-inspector` as the complete Analyzer foundation;
- KCAA `WorldModel`, KRT `PCBData`, `pcb-inspector` `PcbBoard`, or ad-hoc dictionaries as cross-component canonical state;
- FreeRouting as the primary future native engine;
- AI directly generating arbitrary trace geometry and mutating KiCad outside policy/safety boundaries;
- GUI-only DRC launch as an automated acceptance result;
- parser compatibility as proof of live KiCad plugin/API compatibility;
- validator/tool unavailability normalized to “pass.”

## Success conditions currently supported by the research record

1. Core Router and Analyzer expose stable project-owned contracts independent of donor internals.
2. Automated routing/placement hard-fails without valid authoritative `Edge.Cuts`.
3. Protected user work is not silently destroyed or moved.
4. LLM/cloud services are optional to deterministic routing/analysis correctness.
5. Validation records whether it executed; absence/failure of a validator is visible.
6. Object identity/provenance supports selective change, rollback, diagnostics, and findings tied to board objects.
7. Hard legality/safety is separate from optimization quality; a better score cannot legalize a forbidden mutation.

Quantitative success targets (board/layer/net limits, completion, DRC/connectivity thresholds, runtime/memory, Analyzer error tolerance, reproducibility) remain unresolved.

## Canonical workflows

### Routing

```text
BoardState + resolved hard rules + RoutingPolicy + ownership state
  -> Core Router
  -> candidate geometry + diagnostics
  -> ChangeSet candidate
  -> exact validation / acceptance gates
  -> transactional KiCad apply
  -> refresh / authoritative verification
```

### Selective rip-up/reroute

```text
route failure or optimization opportunity
  -> blocker attribution
  -> object identity + ownership/lock gate
  -> bounded eligible rip-up set
  -> reroute impacted connections
  -> validate
  -> commit or rollback
```

Protected objects never become removable merely because removal improves cost.

### Analyzer

```text
Canonical BoardSnapshot + ElectricalIntent (when available) + AnalyzerPolicy
  -> deterministic analyzers
  -> metrics + evidence + findings + execution status
  -> normalized FindingSet/report
```

### Optional AI/user control

```text
User configuration -----------+
                              -> validated product policy -> deterministic engines
Optional AI strategy/policy --+
```

Both control sources remain below the same hard-rule, ownership, validation, and transaction authority.

## Architecture ownership rule

The following are strategically product-owned even when implementation internals reuse permissive code: canonical board model; RoutingPolicy; AnalyzerPolicy; ElectricalIntent contract; ownership/protection; hard-constraint API; ChangeSet/transaction API; candidate acceptance; result/evidence/finding schemas; best-state/scoring semantics; and agent-facing public API.
