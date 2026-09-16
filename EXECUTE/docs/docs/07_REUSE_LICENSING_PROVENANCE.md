# Donor Reuse, Licensing, and Provenance

> Engineering summary only; not legal advice. Distribution obligations depend on final product license, linkage, bundling, and dependency graph.

## 1. Reuse strategy

The current architecture is deliberately **product-owned + selective donor reuse**, not “fork one router/analyzer.”

Strong reuse targets are KiCad-specific integration/rules/validation and well-bounded algorithms. Product safety/identity/public contracts remain project-owned.

## 2. Router donor map

| Source | Main value | Studied license / reuse posture |
|---|---|---|
| KiCadRoutingTools | KiCad adapter/model/rules; grid/pose search; fanout; diff-pair; matching; route QA | MIT; direct/selective reuse candidate |
| tscircuit-autorouter | capacity/global/high-density pipeline, repair/simplification, fanout | MIT; direct/port/adapt candidate |
| Topola | topology/navmesh/rubber-band/Theta*-style concepts; Rust geometry use | MIT main project; inspect file-level licenses/assets |
| OpenROAD/TritonRoute | pin access, detailed routing, iterative search/repair, embedded DRC patterns | BSD-3-Clause; adaptation cost high due IC model |
| Clipper2 | polygon boolean/offset | Boost-1.0; direct dependency candidate |
| `rstar` | R*-tree spatial index | MIT OR Apache-2.0; direct dependency candidate |
| `spade` | robust Delaunay/CDT/Voronoi | MIT OR Apache-2.0; direct dependency candidate |
| FreeRouting | mature routing, rip-up, transaction/best-state concepts | GPLv3; reference-only for non-GPL core unless licensing changes |
| KiCad PNS/source | shove/walkaround/topology/diff-pair behavior/reference | GPLv3 context; reference-only unless obligations intentionally accepted |
| CopperRoute | derivative of FreeRouting; DRC feasibility evidence | GPL-3.0-only; reference-only for permissive core |
| libavoid/adaptagrams | object-avoiding connector routing | LGPL-2.1; optional isolated dependency/reference subject to distribution model |

## 3. Analyzer donor map

Observed top-level licenses in the research: `pcb-inspector` MIT; `kicad-happy` MIT; `kicad-tools` MIT; KRT MIT; `breakneck` MIT; `pcb-toolkit` MIT OR Apache-2.0; KiCad GPL-family and best treated as native authority/reference unless product licensing intentionally allows deeper reuse.

See `04_ANALYZER.md` for capability allocation.

## 4. Product-owned vs reusable

### Good direct/selective reuse candidates

- KiCad adapter/parser/rule-resolution code where it fits the canonical adapter.
- KRT search/fanout/diff-pair/matching components after deeper module-level review.
- tscircuit repair/simplification/capacity pieces with clean boundaries.
- generic geometry/spatial libraries.
- Analyzer algorithms/formulas behind product models/findings.
- donor tests/fixtures with compatible licensing.

### Better as adaptation/architecture reference

- tscircuit capacity/hypergraph architecture;
- Topola topology/navmesh approach;
- TritonRoute pin-access/search-repair architecture;
- KCAA project-level safety/lifecycle patterns.

### Keep product-owned

- canonical BoardState/BoardSnapshot;
- RoutingPolicy/AnalyzerPolicy and precedence;
- ElectricalIntent;
- object ownership/provenance;
- hard-constraint and ChangeSet/transaction contracts;
- candidate acceptance/best-state/scoring semantics;
- final FindingSet/result/evidence schemas;
- agent/MCP-facing stable API.

### Clean-room/reference-only candidates

If Raphael uses a non-GPL core, mature GPL implementations such as KiCad PNS shove or FreeRouting-specific central primitives should be treated as behavior/architecture references, not mechanically copied/translated.

## 5. Provenance record

Every donor-derived subsystem should record at least:

```yaml
source_repository: owner/repo
source_commit: <sha>
source_path: <path>
source_license: <license>
reuse_mode: direct | modified | ported | algorithm-adapted | reference-only
notice_required: true | false
local_module: <path>
reviewed_for_gpl_lineage: true | false
```

For adapted analyzers, also record semantic changes such as canonical input model, replaced thresholds/policy, stable object IDs, finding schema changes, and evidence/provenance output.

Suggested agent rule:

```text
PERMISSIVE_SOURCE:
  reuse/port only with recorded provenance and notice handling.

GPL_REFERENCE_SOURCE:
  inspect behavior/architecture;
  do not copy, translate, or mechanically port implementation text into a non-GPL core.
```

## 6. Known licensing unknowns

- final Core Router repository license;
- direct-copy vs port/reimplementation policy for permissive donors;
- complete transitive dependency and bundled-artifact audit;
- final repository/package/distribution model.

These are planning-relevant and must be resolved before broad donor code ingestion.
