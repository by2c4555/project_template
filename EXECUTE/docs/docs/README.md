# Raphael — Compact KiCad Layout Knowledge Base

**Generated from:** `KICAD_MCP_LAYOUT_RAW_KNOWLEDGE_2026-09-16.zip`  
**Knowledge date:** 2026-09-16  
**Purpose:** compact, source-grounded reference for local AI/agents working on Raphael.  
**Boundary:** this knowledge base is architecture/research context, not an implementation task plan.

## Why this version exists

The raw bundle contains 20 topic compilations plus four large research studies. Many concepts are repeated across files because each study restates BoardState, ownership, DRC, donor reuse, testing, and unknowns from its own angle. This edition normalizes those concepts into one canonical home and uses cross-references instead of repeating them.

## Evidence states

- **DECISION** — explicit current project direction in the available research record.
- **FACT** — directly supported by the bundled research evidence.
- **REQUIREMENT** — behavior the bundled research explicitly describes as required/intended; not automatically a settled implementation choice.
- **RECOMMENDATION** — research-derived proposal; not a project requirement until explicitly accepted.
- **INFERENCE** — interpretation of facts; useful, but not authoritative.
- **UNKNOWN** — unresolved information; do not guess.
- **BLOCKING UNKNOWN** — unresolved information that can materially change architecture, safety, compatibility, or planning.

When states conflict, prefer the latest explicit user decision. Never silently promote a recommendation to a decision.

## Minimal reading paths

For most local-agent work, start with `00_KNOWLEDGE_INDEX.md`, then load only the relevant canonical document:

| Task | Read |
|---|---|
| Understand product direction/scope | `01_PROJECT_CONTRACT.md` |
| KiCad I/O, live board, BoardState, ChangeSet, ownership | `02_KICAD_ADAPTER_AND_BOARDSTATE.md` |
| Router architecture/algorithms | `03_CORE_ROUTER.md` |
| Analyzer, ElectricalIntent, findings | `04_ANALYZER.md` |
| DRC, authority, policy, mutation safety | `05_VALIDATION_POLICY_SAFETY.md` |
| Tests, benchmarks, determinism, offline behavior | `06_TESTING_PERFORMANCE_DETERMINISM.md` |
| Donor reuse and licenses | `07_REUSE_LICENSING_PROVENANCE.md` |
| Before making architecture assumptions | `08_OPEN_DECISIONS_AND_RESEARCH_GAPS.md` |
| Trace a claim to raw source artifacts | `09_SOURCE_MAP.md` |

## Local-AI retrieval rule

Prefer targeted retrieval over loading every file. Treat `08_OPEN_DECISIONS_AND_RESEARCH_GAPS.md` as a mandatory guardrail before making architecture-sensitive conclusions. If a requested fact is not present here, consult the original research bundle rather than filling the gap from general knowledge.
