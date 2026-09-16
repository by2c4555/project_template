# Testing, Performance, Determinism, and Offline Operation

## 1. Test model synthesized from donor evidence

The studies support a layered validation strategy:

```text
L1 Algorithm unit tests
   small synthetic geometry, equations, invariants

L2 Golden PCB fixtures
   focused clean/defective boards

L3 KiCad parity/oracle tests
   compare product hard-validation interpretation with native DRC/ERC where applicable

L4 Donor parity tests
   adapted algorithm vs pinned donor vectors/behavior

L5 Broad corpus crash/regression
   parser/model robustness and false-positive regression

L6 Router/Analyzer integration
   connectivity, metrics, findings, ownership, rollback across routing attempts
```

Important unit properties include segment/polygon geometry, clearance envelopes, via/layer legality, deterministic tie-breaking, pin access, identity/protection, rollback, and connectivity preservation.

Router characterization should include simple/blocked corridors, via-required/multilayer detours, BGA escape, neck-down, protected vs rip-eligible obstacles, differential pair transitions, matching regions, and congestion.

Do not conflate “can parse many boards without crashing” with “engineering findings are correct.”

## 2. KRT test evidence

The reviewed KRT repository documents a broad suite covering full-board and single-ended routing, multilayer/vias, differential pairs, meander/length behavior, rule areas/keepouts, rule resolution, KiCad 9/10 net-format round-trip, rip/restore, obstacle-map parity, connectivity/DRC, stress boards, deterministic replay, and GUI/CLI parity infrastructure.

Documented commands include `python3 tests/run_all.py`, `--fast`, `--list`, name filters, and focused route/round-trip/rule-area tests. Rust build paths include `python build_router.py`, `--from-source`, and `cargo build --release`.

The studies also note a CI distinction: local test breadth is not the same as continuously enforced push/PR CI; some tests can self-skip without KiCad and such skips must not be counted as pass.

## 3. External validation

**RECOMMENDATION:** use KiCad native DRC/connectivity as an independent oracle where possible. Internal DRC is necessary but should not automatically be the only proof of board correctness.

Possible baseline comparisons include native Raphael routing against KRT, a FreeRouting executable, and selected tscircuit benchmarks. Compare completion, DRC violations, incomplete connections, runtime, memory, vias, trace length, bends, rip-up count, iterations, and repeatability—not a single aggregate score.

## 4. Performance evidence and limits

KRT's Rust hot path uses optimized A* structures, compact/hash-efficient state, optimized obstacle lookup, `mimalloc`, release/LTO tuning, and coarse Python/Rust calls rather than per-node FFI. Its README reported roughly 10× speedup over an earlier Python route path and example board-stage timings (including a sample 32-net route around 7 s). These are donor-reported values, **not independently reproduced product benchmarks**.

Likely non-Rust costs in that architecture include parsing/model construction, obstacle rasterization, rule/config resolution, orchestration/net ordering, rip-up bookkeeping, post-processing, writing, and validation. Product profiling must measure the end-to-end pipeline rather than only the search kernel.

No source study establishes product SLOs for maximum board area, net count, dense 8+ layer boards, worst-case memory, or deterministic latency.

## 5. Determinism

Research recommends first-class determinism for agent use and regression testing. Sources of instability include hash order, priority queue ties, net order, parallel evaluation, random seeds, floating tolerance, candidate score ties, and rip-up selection.

Candidate reproducibility contract from the research:

```text
same normalized BoardState
+ same RoutingPolicy
+ same engine version
+ same random seed
=> same accepted routing result
```

**BLOCKING UNKNOWN:** whether Raphael needs semantic equivalence, stable accepted geometry, or byte-identical KiCad output. Generated UUIDs make byte identity materially different from geometric repeatability.

## 6. Offline / AI independence

The donor evidence shows that board parsing, rule extraction, deterministic placement helpers, native routing primitives, geometry/via preflight, and local validation mechanisms can operate without cloud AI. MCP is a control wrapper in KCAA rather than an inherent dependency of deterministic routing.

**Architectural conclusion:** `AI = OFF` and external `Network = OFF` are technically feasible for the deterministic core. Local loopback/IPC to KiCad is not treated as an external cloud dependency.

**UNKNOWN:** whether every shipped product feature must formally support a network-off mode.

## 7. Acceptance targets still missing

No bundled source defines final numeric targets for board/layer/net scale, completion rate, final DRC/connectivity, runtime, memory, Analyzer false-positive/false-negative tolerance, or reproducibility. These must remain open inputs rather than borrowed from donor benchmark claims.
