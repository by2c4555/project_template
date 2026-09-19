> PROJECT TEMPLATE DEVELOPMENT CONSTITUTION 1.2 — Human owned. AI may read and apply this guidance; modification requires explicit authorization from a trusted repository-owner channel covering the change.

# Project Template Development Constitution

Constitution package revision: **1.2 — 2026-09-19**

This package specifies the intended architecture and development rules for **Project Template itself**. It guides any capable coding agent, model, provider, or human. It does not create runtime authority for a user project, prove that a feature is implemented, or override a surrounding platform instruction.

## Start here

1. Identify the work mode: analysis, proposal, implementation, validation, migration, or release.
2. Read [GOVERNANCE_AND_TERMINOLOGY.md](GOVERNANCE_AND_TERMINOLOGY.md) and [OBJECTIVE.md](OBJECTIVE.md).
3. Use [REFERENCE_ARCHITECTURE.md](REFERENCE_ARCHITECTURE.md) to select the owning modules for the affected concerns.
4. For changes to Project Template, follow [DEVELOPMENT_PROMPT.md](DEVELOPMENT_PROMPT.md).
5. Use [CONFORMANCE.md](CONFORMANCE.md) to identify required evidence. Never infer implementation from specification prose.

For a small analysis or editorial task, the entry documents and the directly affected owner are sufficient. Read lifecycle, authority, trust, state, and approval owners whenever a change can affect those boundaries. Avoid loading unrelated modules.

## Package structure

| Document | Canonical responsibility |
|---|---|
| [GOVERNANCE_AND_TERMINOLOGY.md](GOVERNANCE_AND_TERMINOLOGY.md) | Package status, instruction precedence, normative language, terminology, profiles, and amendment rules |
| [OBJECTIVE.md](OBJECTIVE.md) | Product identity, optimization order, and stable invariants |
| [REFERENCE_ARCHITECTURE.md](REFERENCE_ARCHITECTURE.md) | Compact system map and concern ownership |
| [DEVELOPMENT_PROMPT.md](DEVELOPMENT_PROMPT.md) | Agent/model protocol for developing Project Template |
| [CONFORMANCE.md](CONFORMANCE.md) | Stable requirement-to-evidence registry and assurance levels |
| [RESEARCH_AND_SCOPE_MODEL.md](RESEARCH_AND_SCOPE_MODEL.md) | External Research through Accepted Scope |
| [PLANNING_MODEL.md](PLANNING_MODEL.md) | Planning A/B, task design, and Planning package quality |
| `architecture/*.md` | Detailed subsystem contracts listed by the Reference Architecture |

## Product flow

```text
Outside runtime: External Research -> Research Handoff

Runtime ingress: validate -> archive immutable revision -> clear exact consumed input
Pre-Cycle:       Planning A -> Scope Approval -> Accepted Scope
Active Cycle:    Planning B -> package validation -> Execution Approval -> PLAN_READY
Execution:       bounded Attempts -> Task/Phase Gates
Acceptance:      Independent Evaluation -> completion knowledge -> finalization
Terminal:        CLOSED_VALIDATED; no automatic next-version work
```

Exception paths include Research revision, focused user decisions, bounded Repair, Diagnosis, Recovery, material Change Approval, pause, block, cancel, and reconciliation. [RUNTIME_LIFECYCLE_AND_TRANSITIONS.md](architecture/RUNTIME_LIFECYCLE_AND_TRANSITIONS.md) is the only owner of transition semantics.

## Core use rule

Use the narrow canonical owner for the concern. Summaries and diagrams orient the reader; they do not create a competing rule. When implementation, tests, prompts, reports, or this constitution disagree, record the disagreement and use the conformance process. Do not weaken the intended contract merely to match existing code.

## Current package revision

Revision 1.2:

- establishes one authorization notice and trusted-owner boundary;
- separates portable core contracts from reference integrations;
- centralizes terminology, precedence, work modes, and package governance;
- completes missing lifecycle families for revision, recovery, re-evaluation, and termination;
- strengthens approval identity, state reconciliation, external-effect, privacy, and provider-capability rules;
- adds proportional assurance profiles and stable conformance mapping;
- removes point-in-time implementation status from the normative package;
- shortens the mandatory architecture reading path while preserving detailed subsystem contracts.

Prior revision notes are retained in [GOVERNANCE_AND_TERMINOLOGY.md](GOVERNANCE_AND_TERMINOLOGY.md). Runtime and release versions remain separate from constitution package revision.
