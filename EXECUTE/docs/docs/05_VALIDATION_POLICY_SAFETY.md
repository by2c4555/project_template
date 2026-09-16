# Validation, Policy, Authority, and Mutation Safety

## 1. Safety hierarchy

Raphael's acceptance model separates three questions:

1. **May this object/state be modified?** — identity, ownership, lock, freshness, authorization.
2. **Is the candidate legal?** — hard geometric/electrical/KiCad constraints.
3. **Is the legal candidate better?** — optimization score/quality.

A favorable score cannot override questions 1 or 2.

## 2. Validation execution state

**Required semantic:** `validator did not run` is not `board passed`.

The studies identify a weakness in KCAA's GUI DRC path: it can successfully open KiCad's DRC UI without returning machine-readable violation results. KRT provides stronger local patterns, including internal checks and a `kicad-cli pcb drc --refill-zones` oracle-style workflow, but final authority is still unresolved.

A hardened integration should distinguish at least:

```text
SUCCESS      validator ran and produced a result
FAILED       validator ran/failed or result rejected
UNAVAILABLE  validator/tool/runtime not available
```

Naming can change; preserving the distinction cannot.

## 3. Three validation levels

Research recommends:

```text
L0 — Fast Search Feasibility
     cheap/incremental rejection during search

L1 — Exact Commit Validation
     exact candidate copper/rules before accepting a ChangeSet

L2 — Board-Level Verification
     complete connectivity + DRC + project invariants
     and KiCad-native verification according to final authority policy
```

Internal fast legality is needed for performance, but internal checks alone should not automatically be treated as the final independent board authority.

## 4. Policy boundary

KRT `GridRouteConfig` contains a large set of useful physical/search knobs (width/clearance/vias/grid/layers/costs/rip-up/diff-pair/power/matching/etc.), but it mixes user intent, algorithm tuning, fallback behavior, physical constraints, and implementation-specific parameters.

A product-level policy should remain declarative and versioned:

```text
User configuration -----------+
                              -> RoutingPolicy
Optional AI strategy/policy --+       │
                                      ▼
                           policy/rule resolver
                                      │
                         engine-specific configuration
                         + per-net resolved rules
```

AI and users should not manipulate internal A* parameters unless those parameters are deliberately exposed as supported product policy.

## 5. Threshold ownership

Donor defaults such as decoupling distance, return-via distance, plane coverage percentage, switching-loop area, crosstalk ratio, width minima, or diff-pair skew are not universal product truth. Thresholds should resolve through product policy plus authoritative KiCad/project constraints.

Candidate hierarchy from research (not finalized):

```text
KiCad hard constraints
+ product AnalyzerPolicy defaults
+ project policy
+ net/interface class
+ per-net/per-rule override
+ waiver/suppression
-> ResolvedRulePolicy
```

**BLOCKING UNKNOWN:** exact precedence among KiCad rules, AnalyzerPolicy, RoutingPolicy, project config, net/object overrides, and waivers/suppressions.

## 6. Mutation safety evidence to preserve

KCAA demonstrates valuable system-level safeguards:

- protected mutation triggers a project snapshot and aborts if snapshot creation fails;
- project versions archive same-stem schematic/PCB/project files coherently;
- restore first archives current state;
- PCB writes use backup + temp file + atomic replace;
- dirty state triggers reload even after a failed tool call because partial mutation is possible.

KRT adds route-specific safeguards such as protected/locked-net filtering and an improvement gate capable of rejecting a worse route before live application.

These patterns should be generalized to every mutation entry point, including fully offline deterministic execution—not only AI/MCP calls.

## 7. Known destructive-edit risks

High-impact risks preserved from the source studies:

- missing/invalid `Edge.Cuts` or AABB-only boundary logic;
- no first-class object ownership/provenance;
- coordinate/tolerance-based deletion targeting the wrong object;
- incomplete lock semantics;
- simplified via spans and layer assumptions;
- live-board vs file-state freshness races;
- whole-file rewrite fidelity/version risks;
- GUI-only DRC mistaken for automated validation;
- direct LLM mutation beyond intended policy authority;
- secrets stored in plain local JSON in donor architecture;
- partial-apply placement/mutation;
- documentation claims drifting from source/tests.

## 8. AI authority

Optional AI may consume findings and propose policy/strategy. It must not obtain a privileged path around:

- BoardState freshness/identity;
- ownership and lock checks;
- KiCad hard rules;
- exact candidate validation;
- transaction/rollback;
- validation execution-state reporting.

This is an architecture invariant rather than an AI-provider choice.
