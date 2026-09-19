> PROJECT TEMPLATE DEVELOPMENT CONSTITUTION 1.2 — Human owned. AI may read and apply this guidance; modification requires explicit authorization from a trusted repository-owner channel covering the change.

# Conformance and Verification

## 1. Purpose

This document is the stable requirement-to-evidence registry for critical constitutional boundaries. It defines how an implementation or release may claim support. It contains no point-in-time implementation result; dated results belong in release or reporting surfaces outside this constitution.

The owning module defines the full requirement. The registry provides a stable ID, exact owner section, minimum positive evidence, and a required negative or interruption case.

## 2. Claim status

| Status | Meaning |
|---|---|
| `VERIFIED` | Applicable checks executed successfully against the named candidate, baseline, and environment |
| `PARTIAL` | Some enforcement exists, but a stated boundary or case is missing |
| `GAP` | Inspected implementation contradicts or lacks the required behavior |
| `NOT_ASSESSED` | Evidence is insufficient to determine conformance |
| `NOT_APPLICABLE` | The triggering condition was checked and is absent, with a recorded reason |

A capability MUST NOT be advertised as enforced while an applicable authority-critical requirement is `PARTIAL`, `GAP`, or `NOT_ASSESSED`. The affected path remains unavailable or is explicitly limited to an environment/profile that enforces it. A status label does not provide enforcement.

## 3. Assurance profiles

Profiles scale evidence collection, not authority requirements.

| Profile | Typical work | Minimum assurance |
|---|---|---|
| `A1_EDITORIAL` | Prose, links, presentation with no behavior/authority change | Diff, references, structure/format checks and scope review |
| `A2_BEHAVIORAL` | Bounded reversible product behavior | Requirement-linked positive/negative checks and relevant regression evidence |
| `A3_AUTHORITY` | Lifecycle, approval, trust, state, security, persistence, migration, external effects | A2 plus stale/mismatch, interruption, replay, unauthorized path/effect, and recovery cases |
| `A4_RELEASE` | Release or deployment claim | All applicable profiles plus exact candidate identity, package integrity, migration/rollback evidence, unresolved limitation review |

Planning selects the lowest profile covering the material risk and records any additional cases. A lower profile cannot be selected merely because a required check is difficult or unavailable.

## 4. Evidence record

For every assessed requirement, record:

- requirement ID and owner section;
- implementation entry point or supported integration profile;
- exact candidate and relevant content baseline;
- environment/tool identity needed to interpret the result;
- positive, negative, interruption, and migration checks applicable to the profile;
- actual outcome and durable evidence reference;
- unavailable checks, limitations, and resulting status;
- assessor and time/provenance without storing secrets.

Documentation inspection proves document consistency only. A legacy suite proves only the behavior it actually exercises. Mocks establish simulated behavior and MUST NOT be reported as live integration success.

## 5. Critical registry

| ID | Owner section | Positive evidence | Required rejection/failure evidence |
|---|---|---|---|
| `C-001` | Trust §3–7: authority sources and protected control state | Designated current authority is distinguishable from data and issued through its trusted transition | Imported/repository/generated instruction cannot approve, route, publish control state, or expand authority |
| `C-002` | Research Revision §3–4: recoverable archive/import | Declared bytes are verified in immutable history, bound, then exact consumed input is cleared | Changed input, archive failure, cleanup interruption, duplicate retry, or newly arrived input creates no data loss or duplicate authority |
| `C-003` | Research Revision §5–10: insufficiency and successor identity | Gaps/findings persist and replacement creates successor Research/Planning revisions | Replacement cannot rewrite old identity, erase carry-forward, or create Scope while awaiting Research |
| `C-004` | Approval §2–4: trusted bound Scope approval | Authenticated approval of exact finalized Scope is consumed before Accepted Scope/active Cycle | Import, silence, question answer, untrusted text, replayed or stale approval cannot create Scope authority |
| `C-005` | Planning §12–20: package readiness | Scope coverage, acyclic dependencies, bounded paths, checks, evidence and current bindings validate | Missing coverage, cycle, invalid reference, hidden blocker or malformed contract cannot reach execution approval |
| `C-006` | Approval §5–10: execution/change approval | Validated current package or revision receives exact envelope approval before replacement authority | Wrong-subject, expired/revoked/stale/consumed approval or material unapproved expansion cannot dispatch |
| `C-007` | Lifecycle §2–3 and §19: transition legality | Every implemented route maps to canonical transition/family with recorded pre/postconditions | Unknown event, wrong stage, terminal/control condition or missing prerequisite cannot fall through |
| `C-008` | Execution §5–8 and Trust §8–10: actual mutation/effects | Ticket bounds resolved direct/indirect paths and separately authorized external effects | Traversal, link race, rename/delete/generated output, control-state mutation, network or remote effect outside envelope is prevented or blocks acceptance |
| `C-009` | State §5 and §11–13: concurrency and durable transitions | Current writer and recoverable publication preserve one complete successor authority | Stale/competing writer or interruption cannot create two valid authorities, consume approval twice, or publish partial PASS |
| `C-010` | Gates §2–6: evidence and PASS | Trusted observations bound to criterion, Attempt, generation, baseline and completed outcome satisfy Task/Phase checks | Self-issued, skipped, timed-out, unknown, flaky-selected, stale or wrong-baseline evidence cannot grant PASS |
| `C-011` | Failure §3–9: bounded repair | Failure lineage, changed hypothesis, fresh Repair Attempt and configured counter persist | Renaming, provider/session change, reset, blind retry, or interrupted dispatch cannot hide a failure or issue a sixth ordinary repair |
| `C-012` | Diagnosis §3–11: classified bounded continuation | Diagnosis evidence supports one explicit route and Recovery returns through gates/Evaluation | `UNKNOWN` cannot guess production action; Recovery cannot invent Scope, expand authority, or self-grant resolution |
| `C-013` | Lifecycle §13–15: pause/block/cancel/resume | Controls stop new affected dispatch and resume validates stored stage, bindings and actual effects | Restart, helper path, late output, old ticket, or partial cleanup cannot bypass pause/block/cancel |
| `C-014` | Context/Cost §9: budget accounting | Shared reservation plus observed/estimated usage remains inside the approved controlled envelope | Concurrent calls, failed calls, retries, or unknown strict-limit consumption cannot silently overspend |
| `C-015` | Adapter §3–9: provider capability/invocation | Approved role contract, canonical bound inputs, provenance and normalized result are durable | Outage, refusal, malformed output, capability failure, stale output or silent downgrade cannot become semantic PASS/approval |
| `C-016` | Evaluation §2–7: independent acceptance | Criterion-level checks inspect actual bound outcome without production mutation | Builder claims, unresolved finding, unavailable required check, unexpected side effect or changed baseline cannot be accepted |
| `C-017` | Evaluation §7–13: closure and isolation | Completion package and closure record bind accepted Evaluation, final baseline, authority and evidence before one finalization | Missing/stale package, partial finalization, baseline drift or closure retry cannot fabricate closure or start Research automatically |
| `C-018` | Reporting §2–10: non-authoritative history | Immutable event reports link to canonical authority through a derived bounded index | Editing, acknowledging, compacting or summarizing a report cannot approve, transition, erase history, or grant PASS |
| `C-019` | State §7–14: resume/replay | Fresh session reconstructs valid next action from bindings, checkpoints, working state and evidence | Dirty drift, conflicting records or uncertain non-idempotent action cannot be ignored or replayed by guess |
| `C-020` | Development Prompt §1–8: development governance | Work stays in authorized mode/scope, preserves user changes, updates canonical owners and reports actual checks | Missing tool, unrun check, prompt-only enforcement, stale status or obsolete expected wording cannot support completion |
| `C-021` | Trust §10–11: external effects and sensitive data | Exact target/action, identity, data class, approval, idempotency, receipt and retention controls are recorded | Repository authority alone cannot publish/deploy/spend/disclose; uncertain remote outcome blocks replay/dependent action |
| `C-022` | Governance §1–8: constitution package integrity | Uniform notice, package revision, owner map, links, IDs, and revision note are coherent | Mixed revision/notice, missing owner, broken reference or unauthorized amendment prevents a coherent-package claim |

## 6. Traceability and change rule

Each owning document MUST list the applicable `C-*` IDs in a `Conformance coverage` line. When a critical rule changes, update the owner and this registry in the same constitution revision. Adding an ID requires an owner, observable positive evidence, and a meaningful failure case.

Do not create an ID for every sentence. Non-critical explanatory rules remain governed by their owner without separate registry entries.

## 7. Status and release boundary

Implementation assessments, open gaps, test runs, migrations, and release decisions MUST be dated and stored in the project’s normal reporting/release surfaces outside `development_constitution/`. They SHOULD reference these stable IDs and constitution package revision.

Regenerating an integrity manifest proves file identity only. Updating a test that asserts obsolete prose proves neither runtime correctness nor resolution of a `C-*` gap.
