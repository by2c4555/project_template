# Knowledge Index

## Canonical architecture in one view

```text
KiCad project / live board / supported project files
        │
        ▼
KiCad Adapter
  - acquire authoritative state
  - normalize KiCad semantics/rules
  - track freshness + identity
        │
        ▼
Canonical BoardState / BoardSnapshot
  - geometry + stackup + connectivity
  - exact board outline/cutouts
  - rules + rule provenance
  - object identity + lock/ownership state
        │
        ├──────────────► Analyzer
        │                 + ElectricalIntent
        │                 + AnalyzerPolicy
        │                 └─ Metrics + FindingSet + ExecutionStatus
        │
        ▼
RoutingPolicy + resolved hard rules
        │
        ▼
Product-owned Core Router
  - geometry/spatial index
  - search + negotiation
  - candidate scoring
  - best-state history
        │
        ▼
Router-neutral ChangeSet
        │
        ▼
Validation / safety gates
  - ownership/protection
  - exact candidate legality
  - board-level KiCad verification when required/available
        │
        ▼
KiCad Adapter apply transaction
  - commit or rollback
  - refresh / authoritative re-read
```

Optional AI is outside the deterministic correctness core. It may propose policy/strategy but does not bypass rules, ownership, validation, or mutation controls.

## Confirmed direction and requirements

1. **DECISION — Product-owned Core Router.** KiCadRoutingTools (KRT) is not the product routing architecture; it is primarily a KiCad integration/rules/validation/reference donor plus a possible selective algorithm donor.
2. **DECISION — Product-owned multi-donor Analyzer repository.** `pcb-inspector` is one donor, not the canonical Analyzer architecture/model; selected algorithms may be normalized behind product-owned contracts.
3. **REQUIREMENT — Valid `Edge.Cuts` before automated routing/placement.** Fallback rectangles/AABBs are not an equivalent authoritative board boundary.
4. **REQUIREMENT — Protect user work.** Automated mutation must distinguish protected/user objects from router-authorized/generated objects sufficiently to prevent silent destructive edits. Exact ownership categories/persistence are unresolved.
5. **CURRENT DIRECTION — Product-owned contracts.** Canonical BoardState, RoutingPolicy, ownership/provenance, ChangeSet, and Analyzer result boundaries should not expose donor-internal structures as permanent product APIs. Exact schemas remain unresolved.
6. **CURRENT DIRECTION — AI has no privileged geometry-mutation path.** Optional AI should operate through structured policy/strategy and remain subject to deterministic safety/validation boundaries.
7. **CURRENT DIRECTION — FreeRouting is not the primary future native router.** It may remain reference/benchmark/fallback only if explicitly retained.

## Core invariants

- Hard legality and protection override optimization score.
- `validation unavailable` is not `validation passed`.
- Router/Analyzer deterministic core must not require an LLM or cloud service.
- Router search consumes a prepared canonical request; it should not discover authoritative KiCad state opportunistically during search.
- Proposed mutation crosses a controlled ChangeSet/transaction boundary before KiCad state changes.
- Stable identity/provenance is required for safe selective mutation, rollback, findings, and later review.
- Board outline legality uses validated outline geometry, not only an axis-aligned bounding box.
- Donor code and donor contracts are separate concerns: code may be reused selectively without adopting donor architecture.

## Key unresolved items

The largest architecture blockers are: KiCad 10 API/authority contract; exact BoardState schema; ChangeSet/object-ownership persistence; router runtime/language/repository/license; V1 routing feature scope; Analyzer runtime; ElectricalIntent contract; Analyzer authority/confidence; policy precedence; machine-readable KiCad validation authority; determinism target; quantitative acceptance targets; and whether automated placement is V1.

See `08_OPEN_DECISIONS_AND_RESEARCH_GAPS.md` before planning around any of these.
