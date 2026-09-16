# Core Router

## 1. Direction

**DECISION:** implement a new product-owned Core Router. KRT proves many useful routing techniques and KiCad semantics, but it does not define the product architecture.

Conceptual product boundary:

```text
NativeRouterEngine
├── BoardState / derived routing world
├── RoutingPolicy + resolved hard rules
├── GeometryKernel
├── SpatialIndex
├── ConnectivityModel
├── SearchEngine(s)
├── NegotiationEngine
├── DrcEvaluator
├── Optimizer
├── BestStateHistory
└── Result / Evidence / Diagnostics
```

Candidate search implementations may change behind this boundary without changing KiCad/agent-facing contracts.

## 2. Geometry and spatial infrastructure

### Geometry kernel

Research recommends proven generic primitives instead of rewriting them:

- **Clipper2** — polygon boolean/offset operations; suitable for obstacle inflation, keepout union, free-space subtraction, envelope/corridor generation. Its studied README warned against relying on its triangulation as a critical dependency.
- **spade** — robust 2D Delaunay/CDT/Voronoi with precise predicates; candidate if Rust is chosen.

**RECOMMENDATION:** route algorithms query one shared geometry/legality service; they should not each implement collision math independently.

### Spatial index

`rstar` is the leading Rust R*-tree candidate in the research. Required router operations include insert/remove/update, region/intersection queries, nearest-neighbor, and layer-scoped queries. Incremental update is important for rip-up/reroute; full rebuild after every mutation is likely to scale poorly.

Specific dependencies remain recommendations until runtime/language is decided.

## 3. Search architecture and donor roles

| Capability | Strongest studied source(s) | Suggested treatment |
|---|---|---|
| octilinear/grid A* | KRT | selective reuse/adapt candidate |
| pose/orientation-aware search | KRT PoseRouter; KiCad PNS as reference | selective reuse/adapt |
| topology/navmesh/rubber-band | Topola | adapt/port concepts or code where appropriate |
| capacity/global planning | tscircuit; OpenROAD concepts | adapt/port |
| high-density search/repair | OpenROAD/TritonRoute; tscircuit | architecture reference/adapt |
| pin access/fanout | KRT, tscircuit, TritonRoute | adapt behind product model |
| multilayer/via search | KRT + industrial/reference donors | product model + selective reuse |
| rip-up/reroute | KRT; TritonRoute; Freerouting reference | project-owned negotiation layer |
| shove/walkaround | KiCad PNS/Freerouting behavior; Topola concepts | project-owned clean-room subsystem if required |
| differential pairs | KRT strongest permissive PCB donor | strong reuse/adapt candidate |
| bus/length/time matching | KRT; tscircuit metadata | higher-level optimization above connectivity |
| power/neck-down/plane workflows | KRT | study/reuse selectively; plane ownership unresolved |
| route simplification | tscircuit + KRT | post-route validated transaction |

The donor matrix is evidence for capability sourcing, not a mandate to implement every algorithm in V1.

## 4. Via model

Via transitions should be explicit graph/search actions with legality data including via type, layer span, drill/hole, pad diameter by layer, annular/clearance constraints, via-in-pad policy, stackup legality, local obstacle envelope, and cost.

**BLOCKING UNKNOWN:** V1 via technology (through only vs blind/buried/microvia/stacked/staggered). This can change state representation and search transitions.

## 5. Rip-up, negotiation, and protected objects

Recommended flow:

```text
route attempt
  -> failure evidence / frontier
  -> blocker attribution
  -> identity + mutation eligibility gate
  -> bounded rip-up set
  -> reroute impacted connections
  -> hard validation
  -> score
  -> accept or rollback
```

KRT provides progressive blocker/rip-up patterns; Freerouting demonstrates first-class rip-up eligibility/cost and undoable/best-state behaviors; TritonRoute demonstrates iterative search-and-repair. Raphael's eligibility semantics must remain product-owned because they depend on object-level protection.

## 6. Differential pairs and matched groups

Research recommends representing a differential pair as one constrained search object rather than two independent nets repaired afterward. Policy needs pair gap, per-layer width, skew tolerance, maximum uncoupled length, entry/exit heading, paired via geometry, synchronized transitions, and length/time objective.

Length/time matching is better layered after base connectivity stabilizes:

```text
connectivity route -> geometry stabilize -> measure -> matching optimizer -> DRC/connectivity revalidate
```

KRT evidence includes route length, via-barrel-aware length, propagation-time distinctions, buses, and meander/trombone matching.

## 7. Power and planes

KRT demonstrates wide power traces, neck-down near fine pitch, plane-related workflows, return-via controls, and current/resistance reporting. The research recommends separating power planning from signal routing and potentially separating `PlaneEngine` from detailed routing.

**BLOCKING UNKNOWN:** whether plane generation/fill is router-owned or delegated to KiCad.

## 8. Validation split inside routing

Full-board DRC at every expansion is too expensive; post-route-only validation is too late. Research recommends three conceptual levels:

```text
L0 Fast Search Feasibility   — incremental/coarse rejection
L1 Exact Commit Validation   — exact candidate copper before mutation acceptance
L2 Board-Level Verification  — complete connectivity/DRC/product invariants
```

Exact authority and KiCad-oracle mechanism are unresolved; see `05_VALIDATION_POLICY_SAFETY.md`.

## 9. Determinism and scoring

Scoring is product-owned. Hard-rule or ownership violations never become acceptable through lower route cost. Sources of nondeterminism to control include equal-cost queue ties, hash iteration order, net ordering, parallel candidate evaluation, random seeds, geometry tolerances, scoring ties, and rip-up victim selection.

**BLOCKING UNKNOWN:** required determinism level (semantic same result, stable accepted geometry, or byte-identical output).

## 10. V1 scope not yet locked

Push/shove, topology/navmesh, capacity/global routing, advanced differential pair depth, buses, length/time matching, power/plane depth, via stitching, and advanced via types are all technically evidenced but not all confirmed V1 requirements. Do not infer V1 scope from donor capability.
