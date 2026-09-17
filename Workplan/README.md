# Workplan v5.3.1 — Deterministic Control Plane Reference

`Workplan/` is the durable authority layer for Project Template. It controls workflow state, role routing, tickets, approvals, immutable bindings, mutation authority, repair/recovery, gates, integrity, resume, and final closure.

The normal workflow remains:

```text
Research -> Ingest -> Scope -> Planning -> Manage -> Build -> Gate -> Evaluate
```

The execution hierarchy remains:

```text
Cycle -> Phase -> Task -> Attempt
```

v5.3.1 keeps schema 6 and hardens Research input quality plus VS Code Manager/Builder cost separation.

---

## 1. Public interface

The public command protocol is exact-token authority. Supported tokens:

```text
WORKPLAN_STATUS
WORKPLAN_NEXT
EXECUTE_RESEARCH
EXECUTE_PLANNING
EXECUTE_IMPLEMENTATION
EXECUTE_DIAGNOSIS
EXECUTE_RECOVERY
EXECUTE_EVALUATION
RESET_PLANNING
RESET_DIAGNOSIS
RESET_RECOVERY
RESET_EVALUATION
```

Do not trim, lowercase, paraphrase, infer, or extract these tokens from prose. Wrong token, wrong surface, or wrong lifecycle stage must fail closed.

`WORKPLAN_NEXT` is the universal continuation query.

---

## 2. Surfaces

### External AI

Used for:

- Research;
- Planning/architecture;
- escalated Diagnosis;
- Recovery reasoning;
- Independent Evaluation.

Typical command shape:

```bash
python Workplan/scripts/command.py <COMMAND> \
  --surface EXTERNAL_AI --tool "<tool>" --model "<model>"
```

### VS Code

Used for bounded implementation through `ExecutionManager` and `Builder`.

Typical command shape:

```bash
python Workplan/scripts/command.py EXECUTE_IMPLEMENTATION \
  --surface VS_CODE --tool "vscode" --model "<manager-model>"
```

---

## 3. Research ingress

New Research handoffs use:

```text
external_agent/RESEARCH_INSTRUCTION.md
external_agent/RESEARCH_POTOCAL_PROMPT.md
templates/PROJECT_DETAILS_TEMPLATE.md
```

The canonical physical handoff is:

```text
ingest/project_details.md
ingest/docs/raw/*
```

The metadata declares supporting files as logical `Workplan/docs/raw/...` paths. `_core/ingest.py` validates the mapping, content hashes, package digest, protocol marker, required sections, and path safety.

Required protocol marker:

```text
research_protocol: EXTERNAL_RESEARCH_PROTOCOL_V1
```

Required readiness field:

```text
product_scope_unknowns: 0
```

For new v5.3.1 Research this means no unresolved material product-scope unknown remains. Existing already-accepted v5.3.0 ingest may be revalidated in compatibility mode by immutable digest during patch migration.

Validation command:

```bash
python Workplan/scripts/tools/ingest.py check
```

Only actual `INGEST_VALID: PASS` proves package validity.

---

## 4. Scope

`scope.py import` snapshots validated Research into immutable active Scope authority. Scope is product WHAT/WHY, not implementation decomposition.

`Objective_dev.md` is never user-product Scope.

Scope bindings are persisted and later checked by Planning, Work, resume, gates, Recovery, and Evaluation.

---

## 5. Planning Package

Planning is external reasoning and normally approval-gated because it creates a new cost/rework envelope.

Planning Package authority includes:

```text
plan/IMPLEMENTATION_PLAN.md
plan/PHASES.json               # optional; implicit PHASE_001 if absent
tasks/TASK_INDEX.md
tasks/TASK_*.md
compiled/PROJECT_BRIEF.md
compiled/ARCHITECTURE.md
compiled/GLOBAL_CONSTRAINTS.md
compiled/INTERFACES.md
compiled/DATA_MODEL.md
compiled/DECISIONS.md
compiled/KNOWN_RISKS.md
```

At `PLAN_READY`, Workplan binds Scope digest, package digest, Phase digests, and Task digests. Material post-approval changes invalidate execution authority.

---

## 6. Phase contract

A Phase defines at minimum:

- `phase_id`;
- objective;
- dependencies;
- architecture bindings;
- interface bindings;
- acceptance criteria;
- verification;
- required evidence.

Dependencies must be valid and acyclic.

A flat/small project may omit `PHASES.json`; Workplan then deterministically supplies implicit `PHASE_001`.

---

## 7. Task contract

A Task defines at minimum:

- `task_id`;
- `phase_id`;
- objective;
- dependencies;
- `authorized_paths`;
- required read context;
- architecture/interface bindings;
- acceptance criteria;
- verification;
- required evidence;
- `max_repairs`.

Default repair budget is 2; supported range is `0..5`.

Task authority is immutable after Planning approval except through controlled revision/recovery paths.

---

## 8. VS Code agents

### ExecutionManager

File:

```text
.github/agents/manager.agent.md
```

Properties:

- user-invocable;
- no `model:` declaration — uses the user's current VS Code Chat model;
- no production `edit` tool;
- may invoke only `Builder`;
- follows deterministic `execution.py next` routing.

### Builder

File:

```text
.github/agents/builder.agent.md
```

Properties:

- hidden from normal user invocation;
- model pinned to `Project Builder Local`;
- can read/search/edit/execute within ticket authority;
- cannot invoke subagents;
- cannot select workflow authority or decide PASS.

The model alias is local configuration, not Workplan authority. A local Qwen deployment is one valid mapping.

---

## 9. Attempt identity

Each Builder dispatch creates a fresh Attempt of kind:

```text
INITIAL
REPAIR
RECOVERY
```

Attempt/Work metadata binds applicable:

- Cycle;
- Phase;
- Task;
- Attempt;
- Work;
- generation;
- Scope digest;
- Planning Package digest;
- Phase digest;
- Task digest;
- Recovery Contract digest;
- ticket digest.

Resume never silently recalculates and overwrites original bindings.

---

## 10. Generation fencing

Resumed Work receives a newer generation. Stale sessions/agents using an older generation cannot checkpoint or complete newer Work authority.

Generation is execution fencing, not a conversational hint.

---

## 11. Context grants

Extra context is read authority only.

A durable grant records:

- reason;
- path/resource;
- Work/Attempt identity;
- generation;
- time;
- `authority_unchanged=true`.

A context grant never expands `authorized_paths`.

---

## 12. Mutation authority

Builder Work records a production snapshot before mutation and a mutation manifest at completion.

Workplan reconciles the complete relevant production mutation set:

```text
create
modify
delete
```

against ticket-authorized paths.

Unauthorized mutation fails the Task Gate.

Workplan control-plane state and defined runtime-local/generated files are separated from production authority.

---

## 13. Verification and evidence

Verification declared by the approved Task/Phase contract must actually execute. Structured evidence is bound to current Attempt/ticket/generation and required artifacts.

File existence or model prose is not sufficient proof.

Final External Evaluation independently rechecks the smallest sufficient acceptance-critical behavior instead of trusting prior model claims.

---

## 14. Task Gate

Task Gate owns deterministic Task PASS.

It validates applicable:

- identity and current generation;
- Work completion;
- current ticket and digest;
- immutable Scope/Plan/Phase/Task/Recovery binding;
- Planning Package integrity;
- evidence identity;
- verification exit codes;
- required artifacts/digests;
- mutation manifest;
- production path authority.

Manager/Builder cannot bypass or replace this decision.

---

## 15. Phase Gate

Phase Gate requires:

- all required Phase Tasks PASS;
- Phase dependencies satisfied;
- Phase-level verification/evidence when declared;
- no unresolved blocking issue for the Phase.

Only Phase Gate PASS makes dependent phases eligible.

---

## 16. Local repair

Ordinary Task-local implementation failures may use a bounded repair path.

Every repair:

- has a fresh Attempt;
- has a fresh ticket;
- records parent failure evidence;
- preserves Task authority;
- consumes deterministic repair budget;
- passes the normal Task Gate.

A repeated or structural failure can escalate before budget exhaustion.

---

## 17. Diagnosis

External Diagnosis is reasoning-only. It should identify:

- observed failure;
- evidence;
- affected component;
- root cause;
- violated contract/invariant;
- blast radius;
- classification;
- recovery boundary.

It does not edit production files.

---

## 18. Recovery

External Recovery is reasoning-only and creates a durable Recovery Contract.

Recovery cannot silently broaden immutable Task write authority. Implementation is performed later through a fresh Recovery Builder Attempt.

Canonical flow:

```text
Diagnosis
  -> Recovery reasoning
  -> Recovery Contract
  -> Manager
  -> Recovery Ticket
  -> Builder
  -> Task Gate
  -> Phase Gate
```

There is no direct recovered-PASS shortcut.

---

## 19. Approval

Approval grants are:

- human actions;
- exact action-bound;
- subject-bound;
- state-bound;
- time-bound;
- stale-safe;
- single-use.

AI cannot approve itself.

---

## 20. Evaluation

External Independent Evaluation runs after all required Phase Gates PASS unless a risk policy requires otherwise.

Evaluation is reasoning/review, not production mutation.

Evaluation should independently map approved criteria to current repository behavior/evidence and execute the smallest sufficient final checks.

Only `evaluation.py finalize` can close the Cycle.

Accepted closure:

```text
lifecycle_stage = CLOSED_VALIDATED
project_state   = CLOSED_VALIDATED
```

---

## 21. Resume and reconciliation

`WORKPLAN_NEXT` and `scripts/resume.py` recover continuation from durable repository state.

After an interruption:

1. inspect current Workplan state;
2. inspect active Work/tickets/checkpoints;
3. reconcile repository mutation state;
4. resume only from the last deterministic checkpoint;
5. never assume a timed-out chat implies all filesystem work was lost.

---

## 22. Model/cost policy

The core principle is:

```text
expensive reasoning = exception/high-value path
local Builder       = normal implementation path
deterministic code  = authority/control path
```

Workplan model bindings describe capability classes only. Provider/model identity never grants state/gate authority.

Current v5.3.1 bindings:

```text
ExecutionManager -> USER_SELECTED
Builder          -> Project Builder Local
```

---

## 23. File ownership

| Path | Ownership |
|---|---|
| `VERSION` | Release version. |
| `Objective_dev.md` | Project Template development constitution. |
| `ENTRY_PROMPT.md` | Public exact-command bootstrap. |
| `CHATGPT_PROJECT_INSTRUCTIONS.md` | Compact ChatGPT Project bootstrap. |
| `external_agent/` | External reasoning role instructions/protocols. |
| `templates/` | Canonical handoff templates. |
| `control/STATE.json` | Authoritative durable workflow state. |
| `plan/`, `tasks/`, `compiled/` | Approved Planning authority. |
| `work/` | Work/tickets/checkpoints/evidence. |
| `scripts/_core/` | Deterministic authority mechanisms. |
| `scripts/tools/` | Operational tool surfaces. |
| `tests/` | Behavioral validation. |
| `FILE_SHA256SUMS.txt` | Deterministic release integrity manifest. |
| `RELEASE_VALIDATION.md` | Release validation specification + actual v5.3.1 record. |

---

## 24. Release validation

Generate manifest only after release files are stable:

```bash
python Workplan/scripts/integrity.py generate
```

Structural validation:

```bash
python Workplan/scripts/validate.py
```

Full validation:

```bash
python Workplan/scripts/validate.py --full
```

Full mode runs bounded suites with independent timeout/failure reporting. Required suites currently include command protocol, v5.3 invariants, v5.3.1 hardening, real final acceptance, normal E2E, and Recovery E2E.

A suite that was not executed successfully is not PASS.

---

## 25. Release cleanliness

Release integrity excludes defined runtime/local artifacts including `.git`, caches, bytecode, virtual environments, editor-local content, runtime Work/history/approval/ingest payloads, temporary files, and ZIPs.

The full release does not ship unrelated empty root project placeholders. User production directories are created by actual project Planning/implementation as needed.

---

## 26. Migration

For v5.3.0 -> v5.3.1:

```text
MIGRATION_V5_3_0_TO_V5_3_1.md
scripts/migrate_v530_to_v531.py
```

Schema remains 6. Migration rejects unsafe active-Work boundaries rather than silently reinterpret in-flight authority.

Older migration documents remain only where they are needed to explain supported historical state/schema transitions.

---

## 27. Authority summary

```text
conversation -> may propose
model        -> may reason/implement within role
ticket       -> bounds one execution attempt
Workplan     -> decides authority/routing/gates
repository   -> durable state
```

If prose conflicts with deterministic Workplan state, Workplan state wins.
