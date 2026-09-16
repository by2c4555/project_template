# Analyzer

## 1. Direction

**DECISION:** build a new product-owned Analyzer repository. `pcb-inspector` becomes one donor among several, primarily for Finding/rule/report/native-validation concepts rather than its board model or high-level PCB heuristics.

Canonical flow:

```text
KiCad Adapter
  -> CanonicalBoardSnapshot
  + ElectricalIntent
  + AnalyzerPolicy
  -> deterministic analyzer primitives
  -> Metrics + Evidence + Findings + ExecutionStatus
  -> product-owned FindingSet/report
```

Each analysis run should operate on one normalized immutable snapshot. Donor rules should not independently reparse the board path and silently create inconsistent views.

## 2. Product-owned Analyzer contracts

Keep these stable even when algorithms are replaced:

- `CanonicalBoardSnapshot` / canonical PCB model;
- `ElectricalIntentModel`;
- `AnalyzerPolicy` and precedence;
- metrics schema;
- final `FindingSet` and stable finding/object identity;
- orchestration and execution-state semantics;
- evidence/provenance;
- suppression/waiver semantics;
- public API consumed by router/UI/optional AI.

A useful finding concept includes severity, category/rule ID, object/net/component/coordinate references, rationale, recommendation, evidence, and correlation. The product needs extensions for authority/source class, confidence, stable KiCad IDs, metric value/unit/threshold, suppression/waiver, analyzer/policy/input provenance, execution status, stable fingerprint, and separation of observation from repair proposal.

## 3. Donor capability map

| Donor | Best-supported role in the bundled research |
|---|---|
| `pcb-inspector` | Finding/Audit concepts, rule registry, KiCad DRC/ERC bridge and normalization, reporters, golden samples, deterministic-vs-AI separation |
| `kicad-happy` | richest studied deterministic PCB analyzer: filled copper, reference-plane coverage, EMC/return-path/PDN/decoupling/switching/clock/via-stitching/crosstalk-style checks |
| `kicad-tools` | geometry DRC, connectivity/routing-quality validation, placement checks, manufacturer-oriented checks |
| `KiCadRoutingTools` | route connectivity, DRC primitives, route/via metrics, propagation time, diff-pair/length matching, post-route QA |
| `pcb-toolkit` | impedance/differential impedance, via properties/parasitics, current capacity, PDN, thermal, crosstalk formulas; physics/calculator layer |
| `breakneck` | nearest ground-return-via spatial primitive |
| KiCad | native DRC/ERC and board semantics as external authority/reference |

## 4. What not to inherit from `pcb-inspector`

Its `PcbBoard` lacks enough board outline/mechanical geometry, full copper/stackup, rule/netclass/keepout data, route primitives, filled-zone topology, reference-plane relationships, courtyard/body information, and schematic semantics to be canonical.

Specific heuristics should not become product truth:

- **Return path:** midpoint-in-GND-polygon is too coarse. Use actual filled copper, route segmentation, reference-layer determination, void/gap crossings, layer transitions, nearest correct-domain return via, and stackup/electrical context.
- **Switching loop:** convex hull of a switching-named net is not physical loop reconstruction. Use schematic/electrical intent to identify real loop participants.
- **Differential pair:** name suffixes + straight-segment length are insufficient. Combine pair identity, exact connectivity, full geometry/vias, propagation delay, impedance, plane continuity, spacing/transitions, and protocol/policy tolerances.
- **Power width:** fixed minimum width is not engineering truth. Derive/validate with current expectation, copper thickness, temperature rise, layer context, plane contribution if modeled, and KiCad/netclass constraints.

## 5. ElectricalIntent

The research requires a product-owned ElectricalIntent model and rejects net-name/refdes inference as the primary semantic authority. Available evidence points to intent domains such as:

- power rails and load/current expectations;
- clocks/high-speed nets;
- differential interfaces/protocols;
- switching nodes/loops;
- decoupling relationships;
- ground/reference domains;
- connector/net roles.

Example composition for power/decoupling/PDN:

```text
Electrical intent
  -> identify IC power pins, caps, rails/load
Physical board
  -> cap-to-pin path/distance
  -> cap-to-ground-via distance
  -> plane/reference geometry
  -> current capacity
  -> target impedance / anti-resonance
  -> Metrics + Findings
```

**BLOCKING UNKNOWN:** authoritative intent sources, inference confidence, and precedence. The dedicated Electrical Intent study mentioned in project history is not present in the bundle.

## 6. Authority and execution semantics

Analyzer findings do not all have the same authority. Geometry/native DRC, deterministic heuristic, physics estimate, and optional AI advisory should be distinguishable. A failed or unavailable external validator must be represented explicitly rather than converted to a clean result.

**BLOCKING UNKNOWN:** which findings are observations/advisory/optimization costs/review warnings/hard blockers, and the exact confidence/evidence/waiver contract. See `05_VALIDATION_POLICY_SAFETY.md`.

## 7. Placement analysis

Available evidence supports placement collision/courtyard checks, nearest-free-position, HPWL/connectivity-based scoring, component grouping/classification, and placement DRC donors. However, exact board outline legality, fixed/locked components, richer mechanical constraints, orientation search, functional/thermal/high-speed grouping, and transaction semantics require further definition.

**UNKNOWN:** automated placement is not yet confirmed as V1 scope; the dedicated placement study is missing from the raw bundle.
