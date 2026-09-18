> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Authority Model

## 1. Purpose

This document defines who owns which runtime decisions and what cannot create authority.

## 2. Authority Classes

```text
Product Authority
Planning Authority
Execution Mutation Authority
Routing Authority
Gate Authority
Approval Authority
Recovery Authority
Evaluation Authority
Closure Authority
```

## 3. Product Authority

Product WHAT/WHY becomes authoritative only as Accepted Scope after:

```text
Planning semantic finalization
    +
valid User Scope Approval
    +
deterministic binding
```

External Research does not own Product Authority.

## 4. Planning Authority

Planning owns:

- final architecture;
- constraints;
- interfaces;
- data model;
- Phase/Task design;
- dependencies;
- authorized paths;
- read context;
- verification/evidence design;
- repair policy.

Planning authority becomes execution-usable only after valid Execution Approval and deterministic binding.

## 5. Mutation Authority

Builder may mutate production only under current valid bounded ticket authority.

Builder capability does not expand mutation authority.

## 6. Routing Authority

Deterministic Workplan owns:

- lifecycle continuation;
- eligible Phase;
- eligible Task;
- Attempt kind;
- issue continuation;
- Evaluation eligibility.

## 7. Gate Authority

Task Gate owns Task PASS.

Phase Gate owns Phase PASS.

No AI role may self-grant these states.

## 8. Approval Authority

The user owns material approval decisions.

AI may explain and recommend but must not self-approve user approval boundaries.

## 9. Recovery Authority

Recovery may design corrections within valid higher-level authority.

Recovery cannot:

- create new product Scope;
- directly mark PASS;
- silently expand Task authority;
- bypass required re-approval.

## 10. Evaluation Authority

Independent Evaluation determines acceptance findings.

Deterministic finalization owns `CLOSED_VALIDATED`.

## 11. Non-Authority Sources

The following do not create authority by themselves:

- model capability;
- model confidence;
- Research recommendation;
- chat statement;
- generated file existing;
- implementation summary;
- Builder saying done;
- Manager saying pass;
- stale approval;
- previous Cycle knowledge.

## 12. Authority Supersession

When authority is revised:

- previous authority remains historical;
- new authority must have new binding/revision;
- stale tickets/approvals must not act on newer authority;
- issue lifecycle must identify supersession.

## 13. Authority Matrix

| Concern | Owner |
|---|---|
| User intent | User |
| External Research | Outside runtime |
| Semantic Scope finalization | Planning |
| Scope approval | User |
| Accepted Scope binding | Deterministic Workplan |
| Technical architecture | Planning |
| Execution approval | User |
| Task/Phase routing | Deterministic Workplan |
| Task-local diagnosis | Manager |
| Repository mutation | Builder |
| Task PASS | Task Gate |
| Phase PASS | Phase Gate |
| Escalated diagnosis | External Diagnosis |
| Recovery design | External Recovery |
| Material authority expansion approval | User |
| Final acceptance reasoning | Independent Evaluation |
| CLOSED_VALIDATED | Deterministic finalization |
