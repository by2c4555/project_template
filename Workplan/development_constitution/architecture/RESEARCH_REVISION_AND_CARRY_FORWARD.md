> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Research Revision and Carry-Forward Model

## 1. Purpose

This document owns:

- transient Research ingest semantics;
- immutable consumed Research revision identity;
- Research sufficiency return path;
- predecessor/supersession lineage;
- durable Planning carry-forward knowledge;
- Research revision resume and delta reconciliation.

Lifecycle transitions remain owned by `RUNTIME_LIFECYCLE_AND_TRANSITIONS.md`.

## 2. Ingest Is a Transient Mailbox

`Workplan/ingest/` is a transient ingress mailbox.

It is not:

- durable Research storage;
- Planning memory;
- Accepted Scope;
- Planning authority;
- user-facing historical report storage.

A user placing/submitting a Research Handoff into ingest intentionally admits that content for Project Template processing. This is not semantic approval of the content.

## 3. Archive-on-Import Rule

After successful structural/trust validation:

```text
Research Handoff in ingest
    ↓
validate
    ↓
create immutable archived Research revision
    ↓
verify archived revision digest/identity
    ↓
bind runtime/Planning input to archived revision
    ↓
clear consumed package from ingest
```

Planning must not depend on the consumed package remaining in ingest.

Failed structural/trust import must not be promoted to an imported Research revision.

## 4. Research Revision Identity

Every successfully consumed Research Handoff must have durable identity equivalent to:

- Research revision ID;
- package digest;
- archive location/reference;
- import time;
- predecessor revision when applicable;
- revision reason / related report when applicable.

A corrected, expanded, or replacement Research Handoff is a **new Research revision**.

Existing Research identity must never be silently rebound to replacement bytes/content.

## 5. Research Sufficiency

Planning A owns semantic sufficiency judgment.

Canonical semantic outcomes:

```text
RESEARCH_SUFFICIENT
RESEARCH_REVISION_REQUIRED
```

`RESEARCH_REVISION_REQUIRED` applies when material missing, contradictory, stale, weak, or unavailable evidence prevents responsible and economical Scope finalization.

Planning may perform selective verification.

Planning should not absorb substantial missing broad/deep External Research merely to avoid returning Research for revision.

## 6. Research Revision Required Result

When Research is insufficient, Planning must preserve enough durable information for the next Research process to address the real gaps without discarding valid work.

The result must provide or durably reference applicable:

- source Research revision/digest;
- source Planning Work/revision;
- verified findings worth preserving;
- material gaps;
- contradictions;
- stale/unsupported claims;
- evidence required;
- focused questions for new Research;
- Planning decisions still safe to preserve as knowledge;
- work that should not be repeated;
- provenance/evidence references;
- latest safe Planning checkpoint.

The normal user-facing representation must be discoverable through `Workplan/reports/` as defined by `REPORTING_AND_HUMAN_REVIEW.md`.

## 7. Carry-Forward Planning Knowledge

Valid reasoning produced before Research revision should be preserved as durable Planning carry-forward knowledge.

Carry-forward knowledge is:

```text
KNOWLEDGE
```

not:

- Accepted Scope;
- Planning execution authority;
- approval;
- execution authority;
- deterministic PASS.

A later Planning revision may reuse carry-forward knowledge only while current evidence still supports it.

## 8. Research Revision Resume

When a replacement Research revision is imported:

1. create new immutable Research revision identity;
2. preserve prior Research/Planning history;
3. create explicit new Planning revision/binding;
4. reference predecessor Research revision/report/carry-forward knowledge;
5. reconcile new Research against the prior material gaps;
6. determine what remains valid, what changed, and what is superseded;
7. continue from the latest valid checkpoint where safe.

Do not silently change an existing Planning Work binding from one Research digest to another.

## 9. Delta Reconciliation

A new Research revision should normally be evaluated as a delta, not as a reason to replay the complete previous reasoning history.

Preferred context:

```text
new Research revision
+ predecessor Research Revision Required report
+ Planning carry-forward knowledge
+ selective old evidence when materially required
+ current repository evidence when materially required
```

Planning must explicitly determine:

- what changed;
- which previous gaps were resolved;
- which prior findings remain valid;
- which findings became stale or superseded;
- what still requires verification.

Provider/model/session changes do not justify discarding durable verified reasoning.

## 10. Awaiting Research

Research insufficiency is a normal controlled workflow outcome.

Equivalent lifecycle semantics:

```text
PLANNING_A
    ↓
RESEARCH_REVISION_REQUIRED
    ↓
persist report + carry-forward knowledge
    ↓
AWAITING_RESEARCH
    ↓
new Research revision imported
    ↓
new Planning revision
    ↓
PLANNING_A
```

No Accepted Scope or production execution authority may be created solely because Research is awaited.

## 11. Next-Version Reuse

Historical Research revisions, Research revision reports, carry-forward Planning knowledge, and Completion Knowledge Packages may reduce future Research/Planning cost.

They remain historical knowledge.

A future version still requires a separately initiated new Research Handoff, new semantic finalization, new Scope Approval, and new Planning authority.

## 12. Core Invariants

```text
ingest is transient

successful import archives immutable Research evidence

consumed Research is cleared from ingest

Research replacement creates a new revision

Research identity is never silently rebound

Planning may return materially insufficient Research before Scope creation

valid prior reasoning is preserved instead of discarded

Research revision resume uses durable state, not chat/provider memory

carry-forward knowledge is not authority

new Research/Planning authority is explicit
```
