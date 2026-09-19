> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

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

## 10. Execution Plane Boundary

Production implementation remains in the VS Code Copilot execution plane described by the Reference Architecture and Execution Model.

External Planner/Evaluation provider interchangeability does not grant those external high-reasoning agents production mutation authority.

Canonical separation:

```text
Planning / Evaluation
    = replaceable high-reasoning provider behind adapter

Execute Implementation
    = VS Code Copilot execution plane

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

production mutation remains in the authorized VS Code execution plane
```
