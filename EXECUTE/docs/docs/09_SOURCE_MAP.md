# Source and Provenance Map

## Physical source artifacts in the raw bundle

The compact knowledge base was derived only from source material physically present in `KICAD_MCP_LAYOUT_RAW_KNOWLEDGE_2026-09-16.zip` and its topic compilations.

| Source artifact | Primary evidence used here |
|---|---|
| `sources/KCAA_ARCHITECTURE_REUSE_STUDY.md` | KCAA KiCad access, local/offline behavior, project snapshots, atomic file mutation, placement helpers, current Edge.Cuts/AABB gaps, AI/MCP separation |
| `sources/KICAD_ROUTING_TOOLS_ARCHITECTURE_REUSE_STUDY.md` | KRT KiCad adapter/rules, live mutation, router capabilities, protection, validation/oracle, tests, performance, current “new Core Router” direction |
| `sources/CORE_NATIVE_ROUTING_ARCHITECTURE_ALGORITHM_STUDY.md` | donor routing landscape, geometry/spatial libraries, search/negotiation/DRC architecture, licensing split, provenance, router blockers |
| `sources/PCB_INSPECTOR_ANALYZER_REUSE_STUDY_REVISED.md` | new product-owned Analyzer decision, donor feature synthesis, Finding/registry concepts, electrical/engineering analysis gaps |
| `sources/RESEARCH_PROMPT.md` | evidence-state discipline and rule against promoting recommendations into decisions |

The raw bundle also contains `docs/01..20_*_RAW_KNOWLEDGE.md`, topic-normalized compilations derived from the same sources. This compact edition deduplicates those compilations; it does not add missing research conclusions.

## Important pinned evidence recorded in the raw bundle

- KCAA study: `paul356/KiCad-AI-Assistant`, commit `09adb6f095c3a57ce3ffa14fd6261afd0183842f`, package version `0.2.4`.
- KRT study: `drandyhaas/KiCadRoutingTools`, commit `86013b2e8572c5d4f72fbc39e59cc48ff46180cc`.
- Analyzer study records `pcb-inspector` at commit `1af4f84ec205295ed663d9e2427694a29a42e599` and additional multi-repository evidence.

Use pinned source/tests at the studied revisions as stronger evidence than stale donor documentation when the raw study identifies a conflict.

## Canonical-doc trace map

| Compact doc | Raw topic sources most directly condensed |
|---|---|
| `01_PROJECT_CONTRACT.md` | 02, 19 + cross-study decisions |
| `02_KICAD_ADAPTER_AND_BOARDSTATE.md` | 03, 04, 14, 15 |
| `03_CORE_ROUTER.md` | 05, 06, 09, 13, 17 |
| `04_ANALYZER.md` | 07, 08, 16, 17 |
| `05_VALIDATION_POLICY_SAFETY.md` | 09, 10, 14 |
| `06_TESTING_PERFORMANCE_DETERMINISM.md` | 11, 13 |
| `07_REUSE_LICENSING_PROVENANCE.md` | 12, 17, 19 |
| `08_OPEN_DECISIONS_AND_RESEARCH_GAPS.md` | 18, 20 + unresolved items throughout |

Raw topic numbers refer to the original `docs/NN_*.md` files in the ZIP.

## Evidence use rule for local agents

1. Prefer the compact canonical doc for routine retrieval.
2. If a conclusion changes architecture/safety/licensing, check its evidence state and `08_OPEN_DECISIONS_AND_RESEARCH_GAPS.md`.
3. If exact donor implementation behavior, source path, or citation is needed, return to the original research study rather than relying on this condensation.
4. If a claim is absent from both compact docs and raw evidence, label it `UNKNOWN` or explicitly use new research; do not synthesize it as an established fact.
