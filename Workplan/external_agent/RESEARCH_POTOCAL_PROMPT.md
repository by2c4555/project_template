# External Research Protocol Prompt — Project Template v5.3.1

Protocol ID: `EXTERNAL_RESEARCH_PROTOCOL_V1`

> Filename note: `RESEARCH_POTOCAL_PROMPT.md` is the canonical repository filename for v5.3.1. The protocol identifier remains correctly named `EXTERNAL_RESEARCH_PROTOCOL_V1` for compatibility with deterministic ingest validation.

Use this protocol only after Workplan accepts `EXECUTE_RESEARCH` and selects `Workplan/external_agent/RESEARCH_INSTRUCTION.md`.

## 1. Purpose

Research converts user intent, current repository behavior, supplied files, and required external evidence into a planning-ready **product WHAT/WHY contract**. The result must be detailed enough that Planning can design architecture and bounded Tasks without rediscovering basic scope.

Research is not Planning. It must not create implementation Tasks, pick arbitrary implementation files, write production code, or grant workflow authority.

## 2. Source priority and ground truth

Use the smallest sufficient evidence set and distinguish source classes explicitly.

Preferred order when applicable:

1. current user instruction for the active scope;
2. current repository/filesystem state;
3. current attached/project source documents;
4. authoritative external documentation required by the task;
5. accepted assumptions explicitly recorded in the handoff.

Do not use old chat summaries or memory when they conflict with current repository/source evidence. Do not treat `Workplan/Objective_dev.md` as user-product Scope; it governs development of Project Template itself.

When external research is necessary, prefer primary/official sources for technical facts, versions, specifications, APIs, laws, standards, or vendor behavior. Record concise source references and the exact claim each source supports. Do not copy large passages into the ingest package.

## 3. Required research questions

Research must determine, where applicable:

- What outcome does the user actually need?
- What is the current verified state/behavior?
- What concrete problem or gap must change?
- What functional behavior is required?
- What non-functional behavior is required?
- What compatibility/platform/runtime constraints are mandatory?
- What user-visible, external, protocol, file-format, API, CLI, UI, data, or hardware interfaces are in scope?
- What is explicitly in scope?
- What is explicitly out of scope?
- What assumptions are accepted?
- What unknowns could materially change architecture, interfaces, acceptance, security, compatibility, or scope?
- What observable acceptance criteria prove the requested outcome?
- What evidence supports each material requirement/constraint?

## 4. Fact / requirement / assumption discipline

Classify material statements using one of these authority labels in the Source / Evidence Map:

- `USER_REQUIREMENT`
- `REPOSITORY_CURRENT_STATE`
- `DOCUMENTED_CONSTRAINT`
- `EXTERNAL_SOURCE`
- `ACCEPTED_ASSUMPTION`

Do not silently convert implementation preferences into product requirements. Do not invent constraints to make Planning easier. When sources conflict, record the conflict and resolve it from the highest applicable authority or leave Research not-ready.

## 5. Material unknown rule

A **material product-scope unknown** is an unresolved question that could change any of:

- approved product scope;
- architecture-driving constraints;
- required external/user-visible interfaces;
- acceptance criteria;
- compatibility expectations;
- security/privacy expectations;
- mandatory data behavior;
- required platform/toolchain/runtime behavior.

Before declaring `READY_FOR_PLANNING`, every material unknown must be resolved by evidence/user direction or converted into an explicit accepted assumption supported by authority.

`product_scope_unknowns: 0` means:

> No unresolved question remains that could materially change product scope, architecture-driving constraints, acceptance criteria, required interfaces, compatibility, security expectations, or another planning-critical boundary.

If that statement is not defensible, do **not** emit `READY_FOR_PLANNING`.

Non-blocking unknowns may remain only if they cannot alter approved scope or acceptance authority. Record them in `Remaining Non-Blocking Unknowns`.

## 6. Acceptance criteria quality

Acceptance criteria must be observable and product/interface facing. Prefer criteria that can later map to executable commands or independent inspection.

Good examples:

- `CLI add 2 3 prints 5 and exits 0.`
- `Existing v1 configuration files remain readable.`
- `The API rejects an invalid token with the approved error contract.`

Avoid Planning details such as:

- `Create TASK_003.`
- `Refactor module X first.`
- `Use class Y unless that technology is itself an approved product constraint.`

Each material functional requirement should map to at least one acceptance criterion or be explicitly covered by a broader criterion.

## 7. Scope boundary discipline

`In Scope` must state what this Cycle is expected to deliver.

`Out of Scope` must explicitly reject adjacent work that could otherwise cause Planning or Builder scope creep.

Research may record architecture-relevant constraints but must not decide the implementation decomposition. Planning owns architecture, Phases, Tasks, authorized production paths, repair budgets, and verification contracts after Workplan accepts Scope.

## 8. Existing repository research

For an existing codebase, inspect only relevant implementation/tests/docs/config required to establish current behavior. Capture:

- current public behavior/interfaces;
- relevant implementation limitations;
- existing compatibility commitments;
- current tests/evidence related to the requested change;
- constraints that Planning must preserve.

Do not perform broad repository summarization merely to fill context. Selective evidence is preferred over whole-repository context.

## 9. New project research

For a new project, do not invent implementation architecture prematurely. Capture the product goal, target environment, required interfaces, non-functional constraints, acceptance behavior, and source-backed assumptions sufficient for Planning to make technical decisions later.

## 10. Canonical ingest package

Start from:

`Workplan/templates/PROJECT_DETAILS_TEMPLATE.md`

Write the authoritative handoff to:

`Workplan/ingest/project_details.md`

Required control fields:

```text
artifact_kind: PROJECT_DETAILS
artifact_status: READY_FOR_PLANNING
research_protocol: EXTERNAL_RESEARCH_PROTOCOL_V1
product_scope_unknowns: 0
supporting_files: [...]
```

Required sections:

1. `Objective`
2. `Current State`
3. `Problem Statement`
4. `Functional Requirements`
5. `Non-Functional Requirements`
6. `Constraints`
7. `Interfaces`
8. `Acceptance Criteria`
9. `In Scope`
10. `Out of Scope`
11. `Assumptions`
12. `Resolved Unknowns`
13. `Remaining Non-Blocking Unknowns`
14. `Source / Evidence Map`

Each section must contain meaningful content. Use `None.` only when the category is genuinely not applicable.

## 11. Supporting files

Supporting files are optional. Include only evidence needed by Planning or later Evaluation.

In `supporting_files`, declare logical paths such as:

```text
Workplan/docs/raw/REQ.md
Workplan/docs/raw/API_SPEC.md
```

Place the physical ingest files at:

```text
Workplan/ingest/docs/raw/REQ.md
Workplan/ingest/docs/raw/API_SPEC.md
```

Do not declare undeclared extras. Do not place secrets, credentials, caches, generated binaries, or unrelated reference dumps in the ingest package.

## 12. Research output quality gate

Before running ingest validation, verify:

```text
[ ] Objective states the desired outcome.
[ ] Current State is grounded in evidence.
[ ] Problem Statement describes the actual gap.
[ ] Functional requirements are complete and non-duplicative.
[ ] Non-functional requirements are explicit or genuinely N/A.
[ ] Constraints distinguish mandatory requirements from preferences.
[ ] Interfaces cover all material external/user-visible boundaries.
[ ] Acceptance criteria are observable and cover material requirements.
[ ] In Scope and Out of Scope prevent obvious scope creep.
[ ] Assumptions are explicit and source-supported.
[ ] All material unknowns are resolved.
[ ] Remaining unknowns are truly non-blocking.
[ ] Evidence map traces every material requirement/constraint.
[ ] No Tasks/Phases/implementation plan were created during Research.
[ ] No production files were modified.
```

## 13. Deterministic ingest validation

Run from repository root:

```bash
python Workplan/scripts/tools/ingest.py check
```

Only actual `INGEST_VALID: PASS` proves format/package validity. A model statement cannot replace this result.

If validation fails, correct only the Research handoff/package. Do not bypass the validator and do not start Planning.

## 14. Handoff invariant

```text
verified user/source/repository evidence
  -> research reasoning
  -> resolved product-scope unknowns
  -> canonical project_details.md
  -> declared supporting files
  -> deterministic INGEST_VALID: PASS
  -> immutable Scope snapshot
  -> Planning
```

Research ends at this boundary.
