> PROJECT TEMPLATE DEVELOPMENT CONSTITUTION 1.2 — Human owned. AI may read and apply this guidance; modification requires explicit authorization from a trusted repository-owner channel covering the change.

# Agent Adapter Boundaries

## 1. Purpose

This document owns the provider/model abstraction boundary for high-reasoning Planning and Evaluation agents.

The goal is to allow model/provider/agent replacement without changing lifecycle, authority, or execution interpretation.

## 2. Architecture Boundary

Canonical conceptual shape:

```text
External/High-Reasoning Planner Provider
    ↓
Planner Adapter
    ↓
Canonical Planning inputs/outputs
    ↓
Deterministic runtime validation/binding
```

and:

```text
External/High-Reasoning Evaluation Provider
    ↓
Evaluation Adapter
    ↓
Canonical Evaluation result
    ↓
Deterministic closure/runtime handling
```

Exact implementation may use prompts, scripts, APIs, agent definitions, or another mechanism, but equivalent adapter semantics must be preserved.

## 3. Planner Adapter Responsibilities

Planner Adapter may own:

- provider/model selection from approved capability/configuration;
- canonical context construction;
- provider invocation;
- output parsing/normalization;
- schema/protocol validation at the adapter boundary;
- provider/model provenance;
- invocation/format/capability error normalization.

It may expose Planning A and Planning B work to a capable high-reasoning provider without granting provider-specific semantics to downstream runtime.

## 4. Evaluation Adapter Responsibilities

Evaluation Adapter may own equivalent:

- canonical acceptance context construction;
- capable provider/model invocation;
- result parsing/normalization;
- provider/model provenance;
- invocation/format/capability error normalization.

It must preserve Evaluation independence in authority/evidence posture.

## 4.1 Role capability contract

An adapter MUST select from an approved role configuration, not from provider marketing, price, or model self-assessment. The configuration MUST state applicable:

- supported input/output contract and context limits;
- required structured-output reliability and validation behavior;
- reasoning responsibilities and prohibited authority;
- tool, network, data-class, and mutation restrictions;
- baseline/binding and provenance handling;
- timeout, retry, cost, and fallback policy;
- known limitations and evidence establishing suitability for the role.

Suitability evidence MAY include representative evaluations, prior verified operation, or an owner-approved configuration review. It MUST cover the material failure modes of the assigned role. A provider/model change requires compatibility validation against the same contract; it does not require user approval when an already approved equivalent fallback and cost envelope cover it.

If no configured option satisfies the role contract, block the invocation or request owner action. A weaker model MAY perform a narrower reclassified task only after Planning/runtime explicitly narrows the task and preserves all higher-level authority requirements.

## 5. Adapter Prohibitions

Planner/Evaluation adapters do not own:

- user approval;
- Accepted Scope binding;
- Planning Package deterministic validation;
- lifecycle transition authority;
- Builder mutation authority;
- Task/Phase PASS;
- `CLOSED_VALIDATED`;
- release/package authority unless separately authorized by the applicable deterministic contract.

A provider statement such as "approved", "ready", "pass", or "release" is data until the canonical runtime validates the corresponding authority transition.

## 6. Planner Interchangeability

Changing Planner model/provider is permitted when the replacement satisfies the required Planning capability contract.

Provider/model change must not change the meaning of an already-bound Planning Package or execution authority.

Canonical rule:

```text
Changing Planner
    ≠
changing an already-bound plan
```

If Planning content/authority changes, create a new Planning revision/binding and perform any required validation/re-approval.

## 7. Evaluation Interchangeability

Changing Evaluation provider/model must not change the bound acceptance contract.

The evaluator receives current canonical Scope/Planning/evidence inputs. A provider-specific interpretation cannot silently weaken required acceptance or bypass deterministic finalization.

## 8. Session Memory Is Non-Authoritative

Planner/Evaluator continuation must use durable repository/filesystem state, checkpoints, reports, bindings, and canonical artifacts.

A provider session/chat history may improve convenience but cannot be required for authoritative resume.

Changing provider/model must not require replaying the full prior conversation when durable artifacts already preserve the needed reasoning.

## 9. Failure Handling

If adapter invocation produces:

- malformed canonical output;
- unsupported capability;
- provider failure;
- ambiguous binding;
- stale context;
- unparseable result;

fail closed into the appropriate retry/blocked/revision path.

Do not infer lifecycle authority from partial provider output.

### 9.1 Transport Success Is Not Semantic Success

Keep invocation/format outcomes distinct from Planning/Evaluation outcomes. A successful API call with valid JSON may still contain insufficient Research, an unresolved product decision, or a blocking Evaluation finding. Conversely, a provider timeout is not evidence that implementation failed.

The adapter must preserve the provider result's meaning when normalizing it. It must not invent missing acceptance evidence, convert uncertainty into PASS, discard blocking findings, or retry until a favorable answer replaces an unfavorable valid result. A malformed result may be retried only under the applicable bounded retry/cost policy; valid semantic rejection returns to the owning lifecycle path.

### 9.2 Durable Invocation Contract

Each invocation must identify its role, canonical input/schema version, current artifact/baseline bindings, permitted capabilities, expected output contract, and applicable cost/retry limits. Preserve provider/model provenance, invocation identity, normalized outcome, and references to relevant returned evidence. Retain or redact provider payloads according to the trust/data rules; provenance is not a reason to store secrets.

Before accepting returned output, runtime rechecks current bindings and control conditions. A response from an outdated generation, cancelled invocation, or superseded input is historical evidence rather than current authority. A provider's conversation continuity cannot waive these checks.

Input artifacts and provider-generated instructions remain untrusted data under `TRUST_AND_INPUT_BOUNDARIES.md`. Capability configuration must be enforced at the tool/execution boundary; a prompt saying "read only" is not sufficient enforcement of that boundary.

## 10. Execution Plane Boundary

Production implementation uses a supported execution profile described by the Reference Architecture and Execution Model. The current reference profile is the VS Code Copilot execution plane.

External Planner/Evaluation provider interchangeability does not grant those external high-reasoning agents production mutation authority.

Canonical separation:

```text
Planning / Evaluation
    = replaceable high-reasoning provider behind adapter

Execute Implementation
    = supported execution profile (currently VS Code Copilot reference profile)

Deterministic Workplan
    = lifecycle/authority/gates/bindings
```

## 11. Core Invariants

```text
provider/model is replaceable; canonical contract is stable

adapters normalize/invoke; they do not grant authority

changing Planner does not reinterpret an already-bound plan

changing the plan requires a new Planning revision

changing Evaluator does not change acceptance requirements

provider session memory is not workflow authority

production mutation remains in an authorized conformant execution profile
```

Conformance coverage: `C-015`, `C-016`, `C-019`, `C-021`.
