# Project Name

**Raphael**

**Document status:** Strict Review Draft  
**Last updated:** 2026-09-16  
**Document type:** `project_details.md`  
**Research basis:** `RESEARCH_PROMPT.md`, the bundled RAW KNOWLEDGE documents, and the current review draft previously titled `CODEX KICAD MCP Layout`.  
**Rename decision:** USER_STATED — the user requested that the project name be changed to **Raphael** on 2026-09-16.  
**Workspace boundary:** This document stops at research consolidation and requirements definition. It is not an implementation plan, task list, execution state, coding-agent instruction set, or project-management artifact.

**Strict authority rule:** This file treats only explicit user-stated decisions and requirements as authoritative. Repository findings, donor capabilities, recommendations, and architectural suggestions remain supporting evidence unless the user explicitly adopts them. Unresolved architecture-relevant information is marked `UNKNOWN` rather than inferred.

**Evidence-state convention used in this document:**

- **USER_STATED** — explicitly provided by the user in the project conversation or in user-authored project instructions.
- **DECISION** — an option explicitly selected as the current project direction in the available research record.
- **REQUIREMENT** — behavior or outcome the project must provide according to USER_STATED or DECISION evidence.
- **CONSTRAINT** — a limitation the future design must respect.
- **RESEARCH_EVIDENCE** — verified or cited repository/source evidence that informs requirements but is not itself a requirement.
- **RECOMMENDATION_ONLY** — a proposed direction that has not been adopted by the user.
- **UNKNOWN** — not yet established; downstream planning must not guess.
- **DISPUTED** — reliable evidence or requirements conflict.

---

## Purpose

Raphael is intended to become a KiCad-centered PCB layout automation system focused on deterministic, product-owned routing and analysis behavior, with safe and controlled board mutation.

The current authoritative project direction is:

1. **REQUIREMENT — Product-owned Core Router.** Raphael will implement a new Core Router owned by the project. KiCadRoutingTools may inform KiCad integration, validation, rule handling, tests, fixtures, and selectively approved algorithm reuse, but it must not define the product Core Router architecture.
2. **REQUIREMENT — Product-owned Analyzer.** Raphael will use a new product-owned Analyzer repository/architecture. `pcb-inspector` is one donor source, not the Analyzer foundation or canonical Analyzer model.
3. **REQUIREMENT — Canonical product contracts.** Raphael needs product-owned boundaries for canonical board state, routing policy, ownership/provenance, mutation/ChangeSet behavior, validation state, and Analyzer results.
4. **REQUIREMENT — Safe mutation.** Raphael must preserve user work through explicit ownership/protection semantics and controlled mutation. Automated mutation must not silently destroy protected user-created PCB objects.
5. **REQUIREMENT — Explicit validation state.** Raphael must distinguish validation passed, validation failed, and validation unavailable/not executed. Unavailable validation must not be treated as success.
6. **REQUIREMENT — Deterministic core independent from AI.** Core routing and deterministic Analyzer behavior must not require an LLM. Optional AI may participate only through constrained policy/strategy interfaces and must remain subject to the same hard rules, safety gates, ownership gates, validation gates, and mutation controls.

Raphael is not currently defined as a clone, fork, or wholesale adoption of any donor repository. Donor repositories are research evidence, reference implementations, possible sources of fixtures/tests, and potential direct-reuse candidates only where licensing and user approval later permit.

---

## Success Criteria

The following success criteria are authoritative at the current research/requirements level. Quantitative acceptance targets remain `UNKNOWN`.

1. Raphael has a project-owned Core Router with a stable public boundary that is not defined by KiCadRoutingTools internals.
2. Raphael has a product-owned Analyzer whose public board model, policy model, finding model, metrics, provenance, and execution-state contract are not defined by any single donor repository.
3. Automated routing must not proceed without an authoritative valid board boundary. Current accepted requirement: valid `Edge.Cuts` are mandatory before automated routing or automated placement.
4. Automated mutation must not silently modify, remove, or replace protected user work.
5. Proposed board mutations must cross an explicit controlled boundary such as a product-owned `ChangeSet` before application to KiCad.
6. Final acceptance of routing or mutation must not equate “validation did not run” with “validation passed”.
7. The system must preserve sufficient stable identity/provenance to support safe selective modification, rollback, diagnostics, Analyzer references, and later review.
8. Hard legality, ownership, and safety gates must take precedence over optimization quality or route-cost scoring.
9. Routing and deterministic analysis must be usable without an LLM as a correctness dependency.
10. Optional AI, if retained, must not directly generate arbitrary trace geometry or bypass product safety/mutation authority.

**UNKNOWN quantitative success criteria:**

- supported board size;
- supported copper-layer count;
- supported net count / connection count;
- required route completion rate;
- required final KiCad DRC/connectivity status;
- runtime / latency SLOs;
- memory limits;
- Analyzer precision, false-positive, and false-negative tolerances;
- deterministic reproducibility level;
- benchmark corpus size and pass thresholds;
- supported first-release board complexity.

---

## In Scope

The following items are in scope as current architectural/product-contract requirements or necessary research-definition areas:

- KiCad PCB/project ingestion sufficient to construct an authoritative routing and analysis snapshot;
- a canonical product-owned board-state boundary for router/analyzer use;
- KiCad routing-relevant rule interpretation to the extent defined by the final supported KiCad platform contract;
- a product-owned `RoutingPolicy` boundary separating user/AI intent from engine-specific tuning details;
- a new deterministic Core Router;
- route proposal generation and route evaluation behind project-owned interfaces;
- explicit ownership/protection semantics for user-created, imported, generated, temporary, and unknown-origin PCB objects;
- a product-owned mutation proposal boundary such as `ChangeSet`;
- safe KiCad mutation application, rejection, rollback/recovery, refresh, and state-freshness handling;
- deterministic Analyzer behavior for board/routing quality, geometry/connectivity findings, validation normalization, metrics, evidence, and execution status;
- product-owned Analyzer findings/metrics/provenance/execution-status concepts;
- use of KiCad and selected donor repositories as research evidence, validation references, fixtures, and possible reuse candidates where later approved;
- license/provenance tracking for any accepted direct reuse, port, or algorithm adaptation;
- testing expectations for geometry, rules, mutation safety, rollback/recovery, validation execution state, Analyzer result structure, determinism, and performance characterization.

**Conditionally in scope / not confirmed for V1:**

The following topics may remain relevant, but they are not currently confirmed as first-release requirements:

- automated component placement beyond boundary/safety implications;
- push/shove routing;
- blind/buried/microvia support;
- plane generation/fill inside the native router;
- topology/navmesh routing in the first release;
- high-density global/capacity routing in the first release;
- differential-pair depth beyond the final selected V1 scope;
- length/time matching beyond the final selected V1 scope;
- power/ground routing depth and via stitching;
- deep SI/PI/EM simulation;
- optional AI review of Analyzer findings;
- MCP as an external control interface.

---

## Out of Scope

The following are explicitly not current authoritative project directions:

- adopting KiCadRoutingTools wholesale as Raphael’s Core Router architecture;
- forking `pcb-inspector` and growing it into the complete Analyzer;
- treating KCAA `WorldModel`, KiCadRoutingTools `PCBData`, `pcb-inspector` `PcbBoard`, or ad-hoc tool dictionaries as the canonical cross-component board model;
- using FreeRouting as the primary future native routing engine;
- allowing AI to directly generate arbitrary trace coordinates and mutate a board outside Raphael’s structured policy/safety boundary;
- treating GUI-only DRC launch as sufficient automated validation;
- treating parser/file-format compatibility as proof of supported live KiCad plugin/API compatibility;
- silently treating unsupported, unavailable, stale, or failed validation as a passing result;
- silently using fallback AABB/default board rectangles as substitutes for valid authoritative board outlines in automated mutation;
- creating implementation phases, coding tasks, task dependency graphs, Builder/Subagent instructions, VS Code agent instructions, curated planner knowledge, `KNOWLEDGE_INDEX.md`, or execution-state files in this research workspace.

The following are not rejected forever, but are not yet confirmed as current V1 scope:

- full automated placement;
- advanced push/shove behavior;
- full differential pair / length tuning / time matching;
- native plane generation;
- deep engineering simulation;
- formal cloud-provider integration;
- a required database engine;
- a required MCP product interface.

---

## Critical User / System Workflows

These workflows describe product-contract intent only. They are not implementation plans.

### 1. KiCad State Acquisition

```text
KiCad project / live board / supported project files
    -> KiCad access layer
    -> canonical authoritative board snapshot
    -> freshness + identity + rule provenance recorded
```

**REQUIREMENT:** Routing and analysis must operate from an explicit canonical board snapshot rather than letting individual algorithms independently discover or mutate KiCad state.

**UNKNOWN:** The final source-of-truth mechanism among live `pcbnew`, KiCad IPC/kipy, `kicad-cli`, and direct file parsing/writing is not selected.

### 2. Routing Request

```text
Canonical Board State
+ resolved hard rules
+ RoutingPolicy
+ ownership/protection state
    -> Core Router
    -> route candidate / diagnostics
    -> ChangeSet candidate
    -> validation / acceptance gates
    -> KiCad apply transaction
    -> refresh / authoritative re-read or verification
```

**REQUIREMENT:** The Core Router must receive explicit board/rule/policy/protection input through a product-owned boundary. It must not use donor-internal data structures as Raphael’s public contract.

**UNKNOWN:** The exact schemas for `BoardState`, `RoutingPolicy`, and `ChangeSet` are not finalized.

### 3. Safe Selective Rip-Up / Reroute

```text
route failure or optimization opportunity
    -> identify blocking objects
    -> ownership / lock / permission gate
    -> bounded candidate mutation
    -> validate
    -> commit or reject / rollback
```

**REQUIREMENT:** Protected user work must not become rip-up eligible merely because removing it improves route cost or completion probability.

**UNKNOWN:** The persisted ownership/protection categories and how they map to KiCad UUIDs, locks, groups, properties, sidecar manifests, or other storage are not finalized.

### 4. Analyzer Run

```text
Canonical Board Snapshot
+ Electrical Intent where available
+ AnalyzerPolicy
    -> deterministic analyzers
    -> metrics + evidence + findings + execution status
    -> normalized FindingSet/report
```

**REQUIREMENT:** Analyzer results must use product-owned finding/metric/provenance/execution-state contracts rather than a single donor’s native result format.

**UNKNOWN:** Analyzer authority classes, confidence semantics, policy precedence, waiver/suppression rules, and electrical-intent confidence rules are not finalized.

### 5. Native Validation

```text
candidate board/change
    -> internal deterministic checks
    -> KiCad-native validation/oracle where required and available
    -> explicit execution state
    -> accept / reject / require review under final authority policy
```

**REQUIREMENT:** Validation execution state must be explicit. Supported states must distinguish at least successful execution, detected validation failure, and unavailable/not-executed validation.

**UNKNOWN:** The canonical machine-readable KiCad validation path is not selected.

### 6. User / AI Policy Control

```text
User configuration -----------+
                              -> validated product policy -> deterministic engines
Optional AI strategy/policy --+
```

**REQUIREMENT:** User settings and optional AI strategy must pass through constrained product-level policy. AI must not bypass ownership, hard-rule, validation, or mutation controls.

**UNKNOWN:** Whether MCP remains a product interface and which Agent Builder/local-agent contract applies are unresolved.

### 7. Rollback / Recovery

```text
mutation proposal
    -> apply attempt under transaction/recovery policy
    -> success: refresh/re-read/verify
    -> failure/rejection: rollback or restore to known safe state
```

**REQUIREMENT:** Failed, rejected, or partially applied mutations must have an explicit recovery path.

**UNKNOWN:** Whether Raphael can rely on KiCad-native undo/transaction behavior, project snapshots/backups, file restore, or another transaction mechanism is unresolved.

---

## Functional Requirements

### FR-001 — Product-Owned Core Router

**Status:** REQUIREMENT.

Raphael shall implement its own Core Router. KiCadRoutingTools shall not define the Core Router’s public architecture or product API.

KiCadRoutingTools may remain a research and reuse candidate for KiCad integration patterns, rule handling, validation/oracle behavior, tests, fixtures, and selectively approved internal algorithms.

### FR-002 — Product-Owned Analyzer

**Status:** REQUIREMENT.

Raphael shall develop a new product-owned Analyzer architecture/repository. `pcb-inspector` shall not be the canonical Analyzer foundation, board model, policy model, or complete engineering-analysis engine.

### FR-003 — Multi-Donor Analyzer Direction

**Status:** REQUIREMENT with unresolved implementation choices.

The Analyzer may integrate, port, or reimplement selected capabilities from multiple open-source donors behind Raphael-owned model, policy, metric, finding, provenance, and execution contracts.

**UNKNOWN:** The final direct-reuse set, reuse mode, licenses, and donor-specific acceptance rules are not selected.

### FR-004 — Canonical Board State

**Status:** REQUIREMENT.

Raphael shall use a canonical routing/analysis board state rather than treating KCAA `WorldModel`, KiCadRoutingTools `PCBData`, `pcb-inspector` `PcbBoard`, or ad-hoc dictionaries as the authoritative cross-component model.

**UNKNOWN:** The exact canonical schema is a blocking design decision.

### FR-005 — Routing Policy Boundary

**Status:** REQUIREMENT.

User and optional AI routing intent shall be expressed through a stable product-level `RoutingPolicy` or equivalent boundary rather than exposing a donor engine’s internal tuning/configuration structure as Raphael’s public contract.

**UNKNOWN:** The exact policy schema, validation rules, precedence rules, and allowed AI-authored policy edits are not finalized.

### FR-006 — Protected User Work

**Status:** REQUIREMENT.

Raphael shall explicitly distinguish mutation authority over existing/user-created objects from router-generated objects. Silent destructive modification of protected user work is not permitted.

**UNKNOWN:** The exact ownership categories and persistence mechanism are not finalized.

### FR-007 — Stable Object Identity / Provenance

**Status:** REQUIREMENT.

The mutation and analysis layers shall preserve sufficient stable object identity/provenance to support selective mutation, object-linked findings, rollback/recovery, suppression/waiver references, diagnostics, and later review.

**UNKNOWN:** The final KiCad-native and/or sidecar persistence mechanism is not selected.

### FR-008 — Valid Board Boundary

**Status:** REQUIREMENT.

Valid `Edge.Cuts` shall be required before automated routing or automated placement. Fallback AABB/default rectangles shall not be treated as equivalent authoritative board boundaries for automated mutation.

### FR-009 — Controlled Change Application

**Status:** REQUIREMENT.

Core Router and Analyzer components shall not directly perform opportunistic KiCad mutations during computation. Proposed modifications shall cross a controlled mutation boundary such as a product-owned `ChangeSet` before being applied to KiCad.

**UNKNOWN:** The exact `ChangeSet` schema is not finalized.

### FR-010 — Mutation Recovery

**Status:** REQUIREMENT.

The mutation layer shall provide a defined reject/rollback/recovery path for failed, rejected, or partially applied changes.

**UNKNOWN:** Exact integration with KiCad native undo/transaction facilities is unresolved.

### FR-011 — Explicit Validation Execution State

**Status:** REQUIREMENT.

Validation shall distinguish successful execution, detected validation failure, and validator/tool/service unavailability or non-execution. A failed, skipped, stale, unavailable, or non-machine-readable validator result shall not be normalized as a clean board.

### FR-012 — Deterministic Core Independence from LLM

**Status:** REQUIREMENT.

Core routing and deterministic Analyzer execution shall not require an LLM. Optional AI may consume results or generate constrained policy/strategy suggestions, but shall not be a correctness dependency for routing or deterministic analysis.

### FR-013 — Structured AI Authority

**Status:** REQUIREMENT.

When AI is enabled, it shall operate through constrained policy/strategy interfaces and shall remain subject to the same rules, ownership checks, validation gates, and mutation controls as non-AI automation.

### FR-014 — KiCad Rule Semantics

**Status:** REQUIREMENT with unresolved coverage.

Raphael shall account for KiCad routing-relevant rules to the extent defined by the final supported KiCad contract. This may include board rules, net classes, custom rules, keepouts/rule areas, stack/layer constraints, via rules, and zone/copper-fill freshness.

**UNKNOWN:** Exact supported-rule coverage and unsupported-rule reporting behavior are not finalized.

### FR-015 — Analyzer Finding Model

**Status:** REQUIREMENT.

The product Analyzer shall expose normalized findings/metrics with enough structure to support evidence, source/authority, object references, thresholds/units where applicable, execution provenance, and later suppression/waiver behavior.

**UNKNOWN:** The exact canonical schema and confidence/authority semantics are not finalized.

### FR-016 — KiCad Native Validation Integration

**Status:** REQUIREMENT with unresolved mechanism.

Raphael shall support programmatic KiCad-native validation/oracle behavior where the selected KiCad platform provides an acceptable machine-readable mechanism.

**UNKNOWN:** The exact mechanism and whether KiCad-native validation is mandatory, secondary, or unavailable for some supported workflows are not finalized.

### FR-017 — Donor Provenance

**Status:** REQUIREMENT.

Any accepted direct code reuse, modification, port, or algorithm adaptation shall preserve source provenance and license obligations at a granularity suitable for later technical and legal review.

**UNKNOWN:** The final reuse policy for permissively licensed code is not selected.

### FR-018 — Research/Planning Boundary Preservation

**Status:** REQUIREMENT for this workspace.

The research workspace shall not create or maintain implementation plans, coding tasks, task dependency graphs, Builder/Subagent instructions, VS Code agent instructions, curated planner reference knowledge, knowledge indexes, or execution-state files.

---

## Non-Functional Requirements

### Safety

- Protected user work must not be silently moved, removed, overwritten, or replaced.
- Hard legality, ownership, and validation gates take precedence over route quality or optimization scoring.
- Unsupported, stale, unavailable, or non-executed validation must remain visible.
- Partial-apply behavior must have explicit recovery semantics.
- Automated mutation must require sufficient identity/provenance to avoid targeting the wrong object.

### Determinism

Core routing and deterministic Analyzer behavior must not depend on nondeterministic LLM output for correctness.

**UNKNOWN:** The required determinism level is not selected. Candidate interpretations remain semantic-equivalent result, stable accepted geometry, or byte-identical output.

### Offline / Network Independence

Cloud AI must not be a correctness dependency of the deterministic routing/analysis core.

**UNKNOWN:** Whether the complete shipped product must guarantee a formal `Network = OFF` mode for all features is not selected.

### KiCad Fidelity

- Raphael must not knowingly treat unsupported KiCad routing rules as supported.
- Routing legality must not intentionally diverge from the selected KiCad authority without explicit unsupported-rule reporting.
- Board-outline handling must use authoritative geometry, not only AABB approximation.
- Live/file state freshness and zone-fill freshness must be explicit.

### Modularity

The following boundaries must remain independently replaceable at the product level, even if donor code is reused internally:

- KiCad integration/access;
- canonical board state;
- routing policy;
- Core Router;
- Analyzer/validation;
- mutation/ChangeSet application;
- optional AI/MCP orchestration.

### Maintainability / Provenance

- Reused or ported donor code must be traceable to repository, commit/tag, source path, license, and reuse mode.
- GPL-family/reference-only sources must not be mechanically copied into a non-GPL core unless the project later makes an explicit compatible licensing decision.
- Recommendations in RAW KNOWLEDGE documents must not be converted into implementation requirements without explicit user adoption.

### Performance

Performance must be characterized separately for parsing/model construction, geometry/indexing, routing search, validation, analysis, and KiCad application.

**UNKNOWN:** Numeric performance SLOs are not selected.

---

## Runtime and Target Platform

### KiCad

- **Product context:** KiCad PCB layout automation.
- **Research focus to date:** KiCad 10 is the primary version discussed in current project research.
- **UNKNOWN:** Whether KiCad 9 must also be supported.
- **UNKNOWN:** Exact KiCad 10 minor-version compatibility matrix.
- **UNKNOWN:** Which mechanisms are authoritative for each operation: live `pcbnew`, IPC/kipy, `kicad-cli`, direct file parsing/writing, or a hybrid.
- **UNKNOWN:** Whether parser/file-format compatibility is sufficient for any non-live workflows.

### Core Router Runtime

**UNKNOWN.** The project has decided to implement a product-owned Core Router, but it has not selected the final language/runtime/API boundary.

**RECOMMENDATION_ONLY:** Prior research recommends investigating Rust-first design. That recommendation is not yet an authoritative project decision.

### Analyzer Runtime

**UNKNOWN.** Python, Rust, C++, or a controlled hybrid model remain possible. The choice materially affects direct adaptation vs port/reimplementation of existing Python donor algorithms.

### Operating Systems

**UNKNOWN.** Donor evidence includes Windows/Linux/macOS patterns, but Raphael’s required support matrix has not been selected.

### Agent / MCP Runtime

- MCP is not required by the deterministic routing core according to current research evidence.
- **UNKNOWN:** Whether MCP remains an official product control interface.
- **UNKNOWN:** Target Agent Builder / local-agent integration contract where builder-specific planning is required.

---

## Existing System / Repository Constraints

### KCAA (`paul356/KiCad-AI-Assistant`)

**RESEARCH_EVIDENCE:** Studied evidence references commit `09adb6f095c3a57ce3ffa14fd6261afd0183842f`, package version `0.2.4`.

Relevant research value includes:

- deterministic routing prototype and geometry/search concepts;
- KiCad plugin lifecycle and local service patterns;
- KiCad query and rule extraction patterns;
- atomic file save/backup patterns;
- project snapshot/restore safety concepts;
- deterministic placement helpers;
- local MCP and provider integration patterns.

**CONSTRAINT:** KCAA must not be treated as Raphael’s final canonical BoardState, ownership model, board-boundary implementation, or automated DRC architecture unless later explicitly adopted and reconciled with product-owned contracts.

### KiCadRoutingTools (`drandyhaas/KiCadRoutingTools`)

**RESEARCH_EVIDENCE:** Studied evidence references commit `86013b2e8572c5d4f72fbc39e59cc48ff46180cc`.

Current authoritative treatment:

- Raphael’s Core Router is a new product implementation.
- KiCadRoutingTools is a primary research source for KiCad API/integration patterns, KiCad semantics, board ingestion, design-rule handling, validation/oracle patterns, tests/fixtures, and possible selective algorithm reuse.
- KiCadRoutingTools is not Raphael’s Core Router architecture.

### Analyzer Donors

**DECISION:** Raphael will create a product-owned Analyzer architecture/repository.

**DECISION:** `pcb-inspector` is a donor, not the Analyzer foundation.

Current donor set in research evidence includes:

- `takzen/pcb-inspector`;
- `aklofas/kicad-happy`;
- `rjwalters/kicad-tools`;
- `drandyhaas/KiCadRoutingTools`;
- `akiselev/pcb-toolkit`;
- `hatlabs/breakneck`;
- KiCad as an external/native authority.

**UNKNOWN:** Which donor capabilities will be directly reused, ported, reimplemented, or used only as reference.

### Native Router Donor Landscape

Current research sources include:

- KiCadRoutingTools;
- `tscircuit/tscircuit-autorouter`;
- Topola;
- OpenROAD/TritonRoute;
- Freerouting;
- KiCad PNS;
- generic geometry/index libraries such as Clipper2, `rstar`, and `spade`.

**UNKNOWN:** The final direct-reuse set and direct-dependency set are not selected.

### Licensing Constraint

**CONSTRAINT:** Architectural/reference study does not imply permission for direct source reuse.

**CONSTRAINT:** GPL-family router sources must remain reference-only unless the project later adopts a compatible licensing decision.

**UNKNOWN:** Raphael’s repository license(s) are not selected.

---

## Database / Persistence

No authoritative product database requirement has been established.

Potential persistent state may be needed for:

- object ownership/provenance;
- per-object or per-net protection state;
- policy overrides;
- Analyzer suppressions/waivers;
- donor-derived algorithm provenance;
- project snapshots / rollback metadata;
- benchmark/regression metadata.

**UNKNOWN:** Whether this state should be stored in KiCad-native UUIDs/groups/properties, `.kicad_pro`, sidecar manifests, another local file format, a local database, or a hybrid.

**UNKNOWN:** Whether any database engine is required at all.

---

## External APIs / Services

### KiCad Local Interfaces

Candidate local interfaces under research include:

- `pcbnew` / KiCad Action Plugin APIs;
- KiCad IPC / kipy;
- `kicad-cli`;
- `.kicad_pcb`, `.kicad_sch`, `.kicad_pro`, and `.kicad_dru` parsing/writing.

**UNKNOWN:** The final authoritative read/write/validate/mutate mechanism for each workflow is not selected.

### MCP

KCAA demonstrates MCP as a possible local structured control boundary.

**UNKNOWN:** Final product role of MCP. MCP is not currently an authoritative dependency of the deterministic core.

### AI Services

Cloud or local AI providers are optional to the deterministic architecture.

**REQUIREMENT:** No cloud or local AI provider may become a correctness dependency of Core Router or deterministic Analyzer execution.

**UNKNOWN:** Final supported AI providers, if any.

**UNKNOWN:** Credential storage and authorization model for optional AI providers.

---

## Security Constraints

1. Automated PCB mutation must be constrained by explicit ownership/protection policy.
2. AI must not gain mutation authority that bypasses the same hard rules, safety checks, and validation checks applied to user-driven automation.
3. Stable object identity must be sufficient to avoid destructive or selective modification of the wrong object.
4. Mutation failure must not leave silent partial state without a defined recovery path.
5. Secrets for optional AI providers must not be committed to the project repository.
6. Existing KCAA local JSON secret persistence is research evidence, not an accepted final credential-storage design.
7. Local network control interfaces, if retained, must not be assumed secure merely because they are local.
8. GPL/reference-only source material must be separated from permissive direct-reuse sources to reduce accidental license contamination during AI-assisted development.
9. Donor code provenance and required notices must be retained for accepted reuse.
10. Validation unavailability, unsupported rule coverage, stale board state, and partial mutation state must be surfaced rather than hidden.

**UNKNOWN security decisions:**

- final credential storage mechanism;
- local MCP authentication/authorization model;
- plugin process isolation model;
- external side-effect authorization model;
- signed update/package requirements;
- threat model for local service endpoints;
- user confirmation requirements for destructive or semi-destructive mutation.

---

## Packaging / Deployment / Installation

Current donor evidence demonstrates several possible packaging patterns, but no final Raphael deployment model is authoritative.

Known research evidence includes:

- KCAA packages a Python core and separate KiCad plugin ZIP;
- KiCadRoutingTools demonstrates Python/Rust components and KiCad PCM artifact patterns with native binaries in release workflow evidence.

**UNKNOWN project decisions:**

- monorepo vs multiple repositories;
- whether the Core Router is a standalone library, process, module, crate, service, or embedded component;
- Analyzer repository runtime/package format;
- KiCad PCM vs Action Plugin vs another integration package;
- bundled native binaries vs local build;
- Python runtime bundling strategy, if Python remains;
- Windows/Linux/macOS support matrix;
- installation/update mechanism;
- version compatibility policy between plugin, router, Analyzer, and KiCad;
- whether MCP or other local service components are packaged by default.

---

## Testing Expectations

Testing is expected to prove safety and behavior at product boundaries. Exact repository/runtime-specific commands remain `UNKNOWN` until runtime and packaging decisions are made.

Current required validation concerns:

- geometry correctness;
- KiCad rule-resolution correctness;
- canonical BoardState construction and freshness semantics;
- stable object identity and ownership behavior;
- protected-object mutation rejection;
- `ChangeSet` validation before application;
- transaction rollback/recovery behavior;
- route connectivity;
- route legality / DRC behavior;
- KiCad parser/writer/live-board compatibility according to the final platform contract;
- KiCad native-validation parity where applicable;
- explicit validation execution-state semantics;
- Analyzer finding evidence, metrics, object references, and execution status;
- regression coverage for donor-adapted algorithms;
- crash-safety across a PCB corpus;
- route/Analyzer integration consistency;
- deterministic behavior characterization;
- performance characterization by subsystem;
- license/provenance review for accepted reuse.

Research-derived test methods available for later adoption include:

- algorithm unit tests;
- small synthetic geometry tests;
- golden KiCad board fixtures;
- donor parity tests against pinned donor behavior;
- KiCad native-oracle parity tests;
- broad corpus regression/crash tests;
- routing stress fixtures;
- GUI/file/live-board parity tests;
- rollback and best-state tests;
- benchmark comparisons against donor/baseline routers.

**UNKNOWN:** Exact test commands, required coverage thresholds, benchmark corpus, pass/fail SLOs, CI matrix, and release acceptance gates are not selected.

---

## Release Expectations

Raphael is currently in research / requirements / architecture-definition state rather than release planning.

Before a release baseline can be defined, the project still needs explicit decisions on:

- supported KiCad version matrix;
- supported OS matrix;
- Core Router runtime and repository boundary;
- Analyzer runtime/package boundary;
- repository license(s);
- direct reuse policy for permissively licensed donor code;
- ownership/ChangeSet persistence contract;
- machine-readable KiCad validation mechanism;
- first-release router capability scope;
- whether automated placement is part of V1;
- quantitative acceptance targets.

**UNKNOWN:** Production release date, semantic-versioning policy, update channel, installer format, support policy, and backward-compatibility policy.

---

## Known Risks / Unknowns

### Blocking Unknowns

The following unknowns are blocking because guessing could cause incompatible architecture, destructive mutation behavior, wrong KiCad integration, invalid validation assumptions, licensing problems, or fundamentally wrong task decomposition.

#### BU-01 — KiCad Platform / API Contract

**UNKNOWN.** Raphael has not finalized which KiCad mechanisms are supported and authoritative for:

- reading/writing live board state;
- machine-readable DRC/ERC;
- zone refill/freshness;
- UUID/object identity;
- lock state;
- groups/properties;
- transactions/undo;
- plugin packaging;
- Windows/Linux/macOS behavior.

This blocks final KiCad Adapter, ChangeSet, validation, and packaging contracts.

#### BU-02 — Canonical BoardState Contract

**UNKNOWN.** The exact authoritative schema for board geometry, stackup, connectivity, rules, copper fill, identity, freshness, lock state, and provenance is not finalized.

#### BU-03 — ChangeSet / Ownership Persistence

**UNKNOWN.** The exact identity and persistence mechanism for categories such as `USER_PROTECTED`, `USER_EDITABLE`, `ROUTER_GENERATED`, `ROUTER_TEMPORARY`, `IMPORTED_UNKNOWN`, or equivalent categories remains unresolved.

#### BU-04 — Core Router Runtime / API

**UNKNOWN.** Raphael has decided to implement a product-owned Core Router, but has not selected its final language/runtime/API boundary. Rust-first remains a research recommendation, not an adopted decision.

#### BU-05 — Core Router Repository Boundary and License

**UNKNOWN.** Standalone repository vs module/monorepo and the repository license are unresolved.

#### BU-06 — Donor Reuse Policy

**UNKNOWN.** Raphael has not decided when permissively licensed donor code may be copied/adapted directly versus ported/reimplemented from algorithms/concepts.

#### BU-07 — Native Router V1 Capability Scope

**UNKNOWN.** Unresolved items include:

- single-net vs multi-net routing depth;
- global routing / capacity planning;
- push/shove/walkaround;
- topology/navmesh search;
- differential-pair scope;
- length/time matching;
- power/ground routing depth;
- via stitching;
- plane generation;
- through-via vs blind/buried/microvia support.

#### BU-08 — Analyzer Runtime

**UNKNOWN.** Python vs Rust/C++/hybrid remains unresolved.

#### BU-09 — Electrical Intent Contract

**UNKNOWN.** The authoritative source and confidence rules for power rails, clocks, switching nodes, differential pairs, interfaces/protocols, decoupling relationships, current expectations, connector roles, and related schematic semantics are not finalized.

#### BU-10 — Analyzer Authority / Confidence Contract

**UNKNOWN.** It remains unresolved which finding classes are observations, advisory findings, optimization costs, warnings requiring review, or hard blockers capable of aborting routing/application.

#### BU-11 — Policy Precedence

**UNKNOWN.** Precedence among KiCad hard rules, AnalyzerPolicy, RoutingPolicy, project configuration, per-net/per-object overrides, and suppression/waiver state is unresolved.

#### BU-12 — Machine-Readable KiCad Validation Authority

**UNKNOWN.** It remains unresolved whether `kicad-cli`, live KiCad APIs, IPC, report parsing, or another supported mechanism is the canonical board-level validation oracle.

#### BU-13 — Determinism Contract

**UNKNOWN.** Semantic same result vs stable accepted geometry vs byte-identical output remains unresolved.

#### BU-14 — Quantitative Product Acceptance Targets

**UNKNOWN.** Raphael lacks selected numeric targets for board size, layers, nets, completion rate, DRC, runtime, memory, Analyzer false positives/false negatives, and deterministic repeatability.

#### BU-15 — Automated Placement V1 Scope

**UNKNOWN.** Automated placement is not sufficiently confirmed as a V1 requirement. If included, placement-specific architecture and acceptance research remains necessary.

### Non-Blocking Unknowns

The following are important but currently less likely to block high-level project definition:

- exact scoring weights and search heuristics;
- exact internal crate/module names;
- visualization technology;
- whether optional AI finding review ships in V1;
- whether deep EM simulation is later integrated;
- final benchmark corpus size after minimum acceptance targets are selected;
- whether FreeRouting remains available only as benchmark/fallback;
- whether MCP remains an optional external interface;
- exact donor commits to pin at implementation time beyond studied evidence snapshots;
- full transitive dependency-license inventory before distribution.

### Known Risks

#### R-01 — KiCad Rule Fidelity

Internal routing legality may diverge from KiCad’s own rule engine if rule coverage, unsupported-rule reporting, or freshness handling is incomplete.

#### R-02 — Stale Live/File State

Mixing live KiCad state, direct file parsing, IPC, and CLI validation can produce freshness mismatches unless one canonical synchronization contract is defined.

#### R-03 — Object Identity / Destructive Mutation

Coordinate- or text-based matching can delete or modify the wrong object without stable identity and ownership semantics.

#### R-04 — Geometry Model Divergence

Different donors use different units, tolerances, grid approximations, and geometry representations. Combining them without one canonical geometry contract can produce inconsistent legality decisions.

#### R-05 — Algorithm Composition Complexity

Grid, pose, topology/navmesh, capacity/global planning, rip-up, and repair algorithms may have incompatible intermediate representations.

#### R-06 — GPL / Provenance Contamination

AI-assisted implementation could accidentally translate GPL implementation details into a core intended to use another license unless source/reuse boundaries are enforced.

#### R-07 — Analyzer False Authority

Heuristic, analytical, and native KiCad findings have different evidentiary strength. Treating them as equivalent can incorrectly block or approve routing.

#### R-08 — Partial Apply / Rollback Failure

Without atomic or well-defined transactional application, a mid-apply failure could leave the live board in an ambiguous state.

#### R-09 — Performance Scaling

Existing donor performance evidence does not establish Raphael’s product SLOs for large or dense multilayer boards.

#### R-10 — Scope Expansion

Attempting advanced routing, automated placement, SI/PI/EMC analysis, live editor integration, and AI orchestration in one first release could materially increase architecture and validation risk.

---

## Source Documents

This `project_details.md` is derived from the user-provided research instruction file and the available RAW KNOWLEDGE bundle. RAW KNOWLEDGE remains supporting evidence and must not be treated as automatically authoritative requirements.

| Source | Role in this document | Provenance / scope |
|---|---|---|
| `RESEARCH_PROMPT.md` | Governs workflow, evidence-state handling, document boundaries, and required `project_details.md` structure | User-provided project instruction, 2026-09-16 |
| `project_details.md` previous review draft | Base document revised into this strict draft and renamed to Raphael | Uploaded/generated draft dated 2026-09-16 |
| `KICAD_MCP_LAYOUT_RAW_KNOWLEDGE_2026-09-16.zip` | Bundled RAW KNOWLEDGE set and source studies | Uploaded research bundle dated 2026-09-16 |
| `docs/01_RESEARCH_SCOPE_AND_EVIDENCE_RULES.md` | Research/evidence-state guardrails | RAW KNOWLEDGE |
| `docs/02_CURRENT_PRODUCT_DIRECTION_RAW_KNOWLEDGE.md` | Consolidated current direction and separation of reuse/rewrite questions | RAW KNOWLEDGE |
| `docs/03_KICAD_INTEGRATION_RAW_KNOWLEDGE.md` | KiCad integration mechanisms, version/API uncertainty, live/file state issues | RAW KNOWLEDGE |
| `docs/04_BOARDSTATE_CHANGESET_OWNERSHIP_RAW_KNOWLEDGE.md` | BoardState, ChangeSet, ownership/protection evidence and gaps | RAW KNOWLEDGE |
| `docs/05_NATIVE_ROUTER_ARCHITECTURE_RAW_KNOWLEDGE.md` | Native router architecture findings and recommendations | RAW KNOWLEDGE, not implementation plan |
| `docs/06_ROUTING_DONOR_ALGORITHMS_RAW_KNOWLEDGE.md` | Routing donor algorithm landscape and feature-scope unknowns | RAW KNOWLEDGE |
| `docs/07_ANALYZER_ARCHITECTURE_RAW_KNOWLEDGE.md` | Analyzer repository decision and product-owned analyzer boundary | RAW KNOWLEDGE |
| `docs/08_ANALYZER_DONOR_FEATURE_MATRIX_RAW_KNOWLEDGE.md` | Analyzer donor capability matrix | RAW KNOWLEDGE |
| `docs/09_VALIDATION_DRC_AUTHORITY_RAW_KNOWLEDGE.md` | Validation/DRC authority and execution-state concerns | RAW KNOWLEDGE |
| `docs/10_POLICY_AUTHORITY_PRECEDENCE_RAW_KNOWLEDGE.md` | Policy precedence and authority unknowns | RAW KNOWLEDGE |
| `docs/11_TESTING_BENCHMARK_ACCEPTANCE_RAW_KNOWLEDGE.md` | Testing, benchmark, acceptance evidence and unknowns | RAW KNOWLEDGE |
| `docs/12_LICENSING_PROVENANCE_RAW_KNOWLEDGE.md` | License/provenance evidence and reuse constraints | RAW KNOWLEDGE |
| `docs/13_PERFORMANCE_DETERMINISM_OFFLINE_RAW_KNOWLEDGE.md` | Performance, determinism, and offline evidence | RAW KNOWLEDGE |
| `docs/14_SECURITY_AND_MUTATION_SAFETY_RAW_KNOWLEDGE.md` | Security and mutation-safety evidence | RAW KNOWLEDGE |
| `docs/15_PLACEMENT_RAW_KNOWLEDGE.md` | Placement-related evidence and Edge.Cuts implications | RAW KNOWLEDGE |
| `docs/16_ELECTRICAL_INTENT_RAW_KNOWLEDGE.md` | Electrical-intent evidence and limitations | RAW KNOWLEDGE |
| `docs/17_REPOSITORY_REUSE_MATRIX_RAW_KNOWLEDGE.md` | Repository reuse/adaptation matrix | RAW KNOWLEDGE; recommendations require user approval |
| `docs/18_BLOCKING_AND_NONBLOCKING_UNKNOWNS_RAW_KNOWLEDGE.md` | Consolidated blocking and non-blocking unknowns | RAW KNOWLEDGE |
| `docs/19_DECISIONS_AND_RECOMMENDATIONS_SEPARATION.md` | Guardrail separating decisions from recommendations | RAW KNOWLEDGE |
| `docs/20_SOURCE_ARTIFACT_COVERAGE_AND_MISSING_STUDIES.md` | Source coverage and missing-study notes | RAW KNOWLEDGE |
| `sources/KCAA_ARCHITECTURE_REUSE_STUDY.md` | KCAA architecture/reuse evidence | Source study; commit `09adb6f095c3a57ce3ffa14fd6261afd0183842f`, package `0.2.4` |
| `sources/KICAD_ROUTING_TOOLS_ARCHITECTURE_REUSE_STUDY.md` | KiCadRoutingTools evidence | Source study; commit `86013b2e8572c5d4f72fbc39e59cc48ff46180cc` |
| `sources/CORE_NATIVE_ROUTING_ARCHITECTURE_ALGORITHM_STUDY.md` | Router algorithm donor landscape | Source study dated 2026-09-16 |
| `sources/PCB_INSPECTOR_ANALYZER_REUSE_STUDY_REVISED.md` | Analyzer donor/reuse evidence | Source study; `pcb-inspector` reviewed at commit `1af4f84ec205295ed663d9e2427694a29a42e599` |

**Evidence priority:** Explicit user decisions outrank recommendations. Pinned source/tests at studied commits should be treated as stronger evidence than stale documentation claims. When evidence conflicts, the conflict must remain visible rather than silently resolved.

---

## User Decisions

The following decisions are currently treated as authoritative.

### UD-001 — Project Name Is Raphael

**USER_STATED / DECISION:** The project name is **Raphael**.

### UD-002 — Implement a New Core Router

**DECISION:** Raphael will implement its own Core Router. KiCadRoutingTools is not the architectural base of the Core Router.

### UD-003 — Use KiCadRoutingTools Primarily as Integration / Validation Evidence

**DECISION:** KiCadRoutingTools is a primary source for KiCad API/integration patterns, KiCad semantics, board ingestion, design-rule handling, validation/oracle patterns, tests/fixtures, and selective routing algorithm reuse where later approved.

### UD-004 — Build a New Product-Owned Analyzer Repository

**DECISION:** Raphael’s Analyzer will be a new product-owned repository/architecture that integrates or ports selected capabilities from multiple repositories.

### UD-005 — `pcb-inspector` Is a Donor, Not the Analyzer Foundation

**DECISION:** `pcb-inspector` will not define the canonical Analyzer board model, Analyzer policy, or complete engineering-analysis engine.

### UD-006 — Valid `Edge.Cuts` Are Mandatory for Automated Placement/Routing

**DECISION / REQUIREMENT:** Fallback board bounds must not silently replace a valid authoritative board outline for automated mutation.

### UD-007 — Protect User Work

**DECISION / REQUIREMENT:** Raphael must distinguish protected/user work from router-authorized/generated work sufficiently to prevent silent destructive automation.

**UNKNOWN:** Exact ownership categories and persistence implementation.

### UD-008 — Canonical Product Contracts Are Required

**DECISION / REQUIREMENT:** Raphael requires product-owned canonical boundaries for board state, routing policy, object ownership/provenance, mutation/ChangeSet behavior, validation state, and Analyzer results rather than exposing donor-internal structures as product APIs.

**UNKNOWN:** Exact schemas.

### UD-009 — AI Does Not Own Direct Geometry Mutation Authority

**DECISION / REQUIREMENT:** AI, if enabled, should generate or modify structured policy/strategy and remain subject to deterministic routing, safety, validation, and mutation boundaries. AI must not directly mutate board geometry outside those controls.

### UD-010 — FreeRouting Is Not the Primary Native Router

**DECISION:** FreeRouting may remain useful as a reference, benchmark, or optional fallback if explicitly retained, but it is not the intended primary future native routing engine.

### Decisions Still Needed

The following are intentionally not promoted to decisions:

1. Accept Rust-first Core Router runtime, or choose another runtime.
2. Use standalone Core Router repository, module, monorepo, or another boundary.
3. Choose Core Router repository license.
4. Permit direct source reuse from MIT/BSD/Boost/Apache donors, or prefer clean reimplementation/ports.
5. Target only KiCad 10, or also support KiCad 9.
6. Select required OS support: Windows, Linux, macOS.
7. Select through-via only for V1, or include blind/buried/microvias.
8. Decide KiCad-owned plane fill vs native router plane engine.
9. Define ownership/provenance persistence mechanism.
10. Define live-edit transaction/undo guarantee.
11. Select canonical machine-readable KiCad validation path.
12. Choose Analyzer runtime/language.
13. Define Analyzer finding authority/confidence model.
14. Define policy precedence and waiver/suppression model.
15. Decide whether automated placement is part of V1.
16. Select required determinism level.
17. Select quantitative acceptance/benchmark targets.
18. Decide final role of MCP.
19. Decide final Agent Builder / local-agent integration target if builder-specific planning is required.

---

_End of strict review draft._
