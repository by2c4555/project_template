# Open Decisions and Research Gaps

This file is the primary guardrail against local agents filling planning-critical gaps with assumptions.

## Blocking unknowns

### BU-01 — KiCad platform/API contract

Finalize supported KiCad version(s) and authoritative mechanisms for live/file read/write, machine-readable DRC/ERC, zone refill/freshness, UUID/object identity, lock state, groups/properties, transactions/undo, plugin packaging, and OS behavior. Existing evidence mixes KiCad 9/10 parser compatibility, KiCad 10 CI, and KiCad 9 plugin metadata; these are not equivalent.

### BU-02 — Canonical BoardState/BoardSnapshot schema

Exact representation of geometry, stackup, connectivity, filled copper, rules/provenance, identity, freshness, locks, and ownership is not finalized.

### BU-03 — ChangeSet + object ownership persistence

Need stable identity/mutation preconditions and persistence of user/router ownership/protection. Exact categories/storage are unresolved.

### BU-04 — Core Router runtime/API

Rust-first is a strong research recommendation, not an accepted decision in the bundled evidence. Python/Rust/C++/hybrid boundary affects reuse and performance.

### BU-05 — Core Router repository boundary and license

Standalone repo vs module/monorepo and target license remain unresolved.

### BU-06 — Donor reuse policy

Decide when permissive code may be copied/adapted directly vs ported/reimplemented; keep GPL-reference handling explicit.

### BU-07 — Native Router V1 feature scope

Unresolved depth includes global/capacity planning, push/shove/walkaround, topology/navmesh, differential pairs, length/time matching, power/ground, via stitching, plane generation, and advanced via technologies.

### BU-08 — Analyzer runtime

Python vs Rust/C++/hybrid is unresolved and affects direct reuse of Python donors.

### BU-09 — ElectricalIntent contract

Authoritative sources/confidence for power rails, clocks, switching nodes, differential pairs, protocols/interfaces, decoupling, current expectations, ground/reference domains, connector/net roles remain unspecified.

### BU-10 — Analyzer authority/confidence

Need rules for observation/advisory/optimization/review/blocking findings, confidence/evidence, suppression/waiver, and native KiCad precedence.

### BU-11 — Policy precedence

Exact ordering across KiCad hard rules, RoutingPolicy, AnalyzerPolicy, project settings, net/interface/object overrides, and waivers/suppressions is unresolved.

### BU-12 — Machine-readable KiCad validation authority

Decide canonical board-level validator: `kicad-cli`, live API/IPC, report parser, other supported mechanism, or a defined combination. Also decide whether it is required or secondary.

### BU-13 — Determinism contract

Semantic equivalence vs stable geometry vs byte-identical output.

### BU-14 — Quantitative product acceptance

Need numeric limits/targets for board size, copper layers, nets/connections, completion, final DRC/connectivity, runtime, memory, Analyzer error tolerance, and reproducibility.

### BU-15 — Automated placement V1

Placement has partial donor evidence but is not sufficiently confirmed as first-release scope.

## Non-blocking unknowns

- exact scoring weights/search heuristics;
- final visualization technology;
- optional AI finding review in V1;
- deep EM simulation later;
- final benchmark corpus size after acceptance criteria exist;
- FreeRouting benchmark/fallback retention;
- final MCP role;
- exact donor commits pinned at implementation time;
- final CLI names/internal modules;
- complete transitive license inventory before distribution.

## Missing source studies explicitly referenced by project history

These study artifacts were **not physically present** in the raw bundle and must not be reconstructed as if their conclusions were available:

- KiCad 10 Platform / API / Integration Study;
- Analyzer Contract & Validation Authority Study;
- Native Router deep donor studies for KRT, tscircuit, Topola, OpenROAD/TritonRoute;
- Canonical BoardState + ChangeSet + Ownership Study;
- Electrical Intent / Schematic Semantics Study;
- Automated Placement Architecture Study;
- Product Benchmark / Performance / Acceptance Study.

If these files become available, add them as evidence and regenerate only affected canonical docs. Until then, this knowledge base preserves the gaps rather than inferring missing conclusions.

## Decisions that must not be silently inferred from recommendations

Do **not** assume any of the following are decided unless explicitly confirmed later:

- Rust-first router;
- standalone router repository;
- a particular repository license;
- direct code reuse from permissive donors;
- `rstar`/`spade`/Clipper2 as final dependencies;
- exact search/global/topology architecture;
- exact ownership metadata format;
- exact authority/precedence hierarchy;
- exact machine-readable KiCad DRC path;
- placement in V1;
- exact determinism or benchmark target.
