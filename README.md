# Project Template v5.3.1

Project Template is a repository-resident control plane for AI-assisted software development. It separates expensive reasoning from bounded implementation, keeps workflow authority in deterministic files/scripts, and makes repository state resumable across chat sessions, providers, and model changes.

v5.3.1 keeps the v5.3 architecture intact:

```text
Research -> Plan -> Manage -> Build -> Verify/Gate -> Evaluate
```

The release hardens two practical boundaries:

1. **Research quality before Planning** — External Research must produce a canonical ingest package using a dedicated instruction, detailed research protocol, and deterministic ingest validation.
2. **VS Code model/cost separation** — the user-selected Manager model coordinates execution while normal implementation is delegated to a pinned local/low-cost Builder model.

The workflow schema remains **6** and the authoritative execution hierarchy remains:

```text
Cycle -> Phase -> Task -> Attempt
```

---

## 1. Design goals

Project Template is designed around the following rules:

- expensive models are used for high-value reasoning rather than routine coding;
- a low-cost/local Builder performs bounded implementation;
- deterministic Workplan software owns state, routing, tickets, approvals, repair budgets, mutation authority, gates, integrity, and resume;
- repository/filesystem state is durable authority;
- chat/session/model state is disposable;
- a model cannot self-authorize a workflow transition or self-declare a deterministic PASS;
- Task/Repair/Recovery implementation always operates under a bounded ticket;
- full conversation replay is not required to resume work;
- normal users should not manually manage Phase IDs, Task IDs, Attempt IDs, generations, digests, or repair counters.

---

## 2. What changed in v5.3.1

v5.3.1 is a hardening release, not a workflow redesign.

### Research / ingest hardening

New Research handoffs must use:

- `Workplan/external_agent/RESEARCH_INSTRUCTION.md`
- `Workplan/external_agent/RESEARCH_POTOCAL_PROMPT.md`
- `Workplan/templates/PROJECT_DETAILS_TEMPLATE.md`

The Research package must pass:

```bash
python Workplan/scripts/tools/ingest.py check
```

New handoffs require protocol marker `EXTERNAL_RESEARCH_PROTOCOL_V1`, canonical scope sections, valid supporting-file declarations, and `product_scope_unknowns: 0` only after all material scope unknowns are actually resolved.

Already-accepted v5.3.0 ingest remains digest-revalidatable so a patch upgrade does not silently rewrite approved Scope.

### VS Code Manager / Builder hardening

Workspace agents are intentionally asymmetric:

- `.github/agents/manager.agent.md`
  - agent name: `ExecutionManager`
  - no `model:` entry: uses the model selected by the user in VS Code Chat;
  - no production `edit` tool;
  - may invoke only `Builder`.
- `.github/agents/builder.agent.md`
  - hidden from normal user invocation;
  - model pinned to `Project Builder Local`;
  - owns bounded production editing for Task/Repair/Recovery tickets.

This means a paid Manager model does not need to perform routine implementation work.

### Cleanup

The full release removes stale compatibility/placeholder material that no longer contributes authority, including the old Builder100K agent alias, duplicate Research template/protocol files, legacy `Workplan/project_details.md`, and empty root project placeholder directories.

---

## 3. Requirements

Minimum repository/runtime requirements:

- Python 3.11+ recommended; release validation was executed with Python 3.13;
- a filesystem/worktree writable by the selected execution tools;
- VS Code for the built-in Manager/Builder agent workflow;
- a VS Code language model registered with display name `Project Builder Local` for Builder execution;
- an external reasoning surface such as ChatGPT, Copilot, OpenRouter, or another compatible model for Research/Planning/Diagnosis/Recovery/Evaluation.

The Workplan core does not require a specific model vendor.

---

## 4. Quick start

### Step 1 — inspect authoritative continuation

From repository root:

```bash
python Workplan/scripts/command.py WORKPLAN_NEXT \
  --surface EXTERNAL_AI --tool "<tool>" --model "<model>"
```

A new project should route to:

```text
EXECUTE_RESEARCH
```

### Step 2 — run Research externally

Submit:

```bash
python Workplan/scripts/command.py EXECUTE_RESEARCH \
  --surface EXTERNAL_AI --tool "<tool>" --model "<model>"
```

Follow the returned Research role instruction and the detailed protocol in:

```text
Workplan/external_agent/RESEARCH_INSTRUCTION.md
Workplan/external_agent/RESEARCH_POTOCAL_PROMPT.md
```

Create:

```text
Workplan/ingest/project_details.md
Workplan/ingest/docs/raw/*    # only declared supporting files
```

Validate:

```bash
python Workplan/scripts/tools/ingest.py check
```

Only `INGEST_VALID: PASS` proves the ingest package is structurally valid.

### Step 3 — import Scope

After valid Research:

```bash
python Workplan/scripts/tools/scope.py import
```

Then query:

```bash
python Workplan/scripts/command.py WORKPLAN_NEXT \
  --surface EXTERNAL_AI --tool "<tool>" --model "<model>"
```

### Step 4 — Planning

When Workplan selects `EXECUTE_PLANNING`, submit the exact token. New Planning may require explicit human approval. If Workplan returns `APPROVAL_REQUIRED`, the AI must stop and show the exact human approval command. Only the human runs it.

Planning compiles the immutable Planning Package under:

```text
Workplan/plan/
Workplan/tasks/
Workplan/compiled/
```

### Step 5 — implementation in VS Code

Open VS Code Chat and select:

```text
Agent: ExecutionManager
Model: your desired Manager model
```

Then execute the authoritative `EXECUTE_IMPLEMENTATION` path. ExecutionManager delegates normal production work to Builder automatically when Workplan issues a ticket.

### Step 6 — final Evaluation

After all required Phase Gates PASS, Workplan routes to `EXECUTE_EVALUATION`. External Evaluation independently verifies approved acceptance criteria and final behavior before `evaluation.py finalize` may close the Cycle.

---

## 5. VS Code setup

### Manager model

`ExecutionManager` intentionally does not pin a model. Choose the Manager model from the VS Code Chat model picker.

Typical use:

```text
reasoning / coordination / local diagnosis -> paid or strong model
```

### Builder model

Register the intended local/low-cost coding model in VS Code with the display name:

```text
Project Builder Local
```

For example, this alias may point to a local Qwen2.5-Coder deployment. The exact provider is machine-specific and is not part of Workplan authority.

### Why the Builder is separate

Routine implementation often consumes many more tokens than routing and supervision. Keeping Builder local creates an explicit cost boundary:

```text
Manager: user-selected reasoning model
        |
        | exact bounded ticket
        v
Builder: Project Builder Local
        |
        v
production changes
        |
        v
Workplan verification / gates
```

Manager must not explicitly override Builder's model during delegation.

### Least-privilege tools

Manager has:

```text
read, search, execute, agent
```

Builder has:

```text
read, search, edit, execute
```

Manager has no normal production edit capability. Builder has no subagent capability and cannot expand its own workflow authority.

---

## 6. ChatGPT Project setup

For a ChatGPT Project using this repository, use the concise bootstrap in:

```text
Workplan/CHATGPT_PROJECT_INSTRUCTIONS.md
```

It intentionally does not duplicate the entire Research protocol. During Research it routes the model to:

```text
RESEARCH_INSTRUCTION.md
        -> RESEARCH_POTOCAL_PROMPT.md
        -> PROJECT_DETAILS_TEMPLATE.md
        -> ingest.py check
```

This keeps Project Instructions compact while preserving high-quality Research output.

---

## 7. Research contract

Research owns product WHAT/WHY, not implementation decomposition.

Research must establish:

- desired outcome;
- verified current state;
- problem statement;
- functional requirements;
- non-functional requirements;
- mandatory constraints;
- material external/user-visible interfaces;
- acceptance criteria;
- explicit in-scope and out-of-scope boundaries;
- assumptions;
- resolved material unknowns;
- remaining genuinely non-blocking unknowns;
- source/evidence mapping.

Research must not create Tasks/Phases, modify production code, or use `Workplan/Objective_dev.md` as user-product Scope.

### Canonical output

Start from:

```text
Workplan/templates/PROJECT_DETAILS_TEMPLATE.md
```

The final file must live at:

```text
Workplan/ingest/project_details.md
```

Required control fields include:

```text
artifact_kind: PROJECT_DETAILS
artifact_status: READY_FOR_PLANNING
research_protocol: EXTERNAL_RESEARCH_PROTOCOL_V1
product_scope_unknowns: 0
supporting_files: [...]
```

### Supporting files

The metadata uses logical paths:

```text
Workplan/docs/raw/REQ.md
```

but the incoming physical file is stored at:

```text
Workplan/ingest/docs/raw/REQ.md
```

The ingest validator maps and validates this relationship deterministically.

---

## 8. Planning contract

Planning starts only from accepted Scope.

Planning owns technical decomposition and must bind enough durable structure that routine execution requires minimal reasoning. The Planning Package includes/binds:

- project brief;
- architecture;
- global constraints;
- interfaces;
- data model;
- decisions;
- known risks;
- Phase contracts;
- Task contracts;
- acceptance/verification expectations;
- authorized production paths;
- required evidence;
- repair budgets.

After approval/`PLAN_READY`, material bound contracts are immutable unless a controlled revision path is used.

---

## 9. Execution hierarchy

The canonical hierarchy is:

```text
Cycle -> Phase -> Task -> Attempt
```

- every Task belongs to exactly one Phase;
- a simple plan can use implicit `PHASE_001`;
- each Builder dispatch creates a fresh Attempt;
- Attempt kinds include `INITIAL`, `REPAIR`, and `RECOVERY`;
- resume generations fence stale sessions;
- Task and Phase dependency graphs must remain valid and acyclic.

---

## 10. Ticket authority

Every Builder Attempt receives a durable ticket bound to current authority, including applicable:

- Cycle;
- Phase;
- Task;
- Attempt;
- Work;
- generation;
- Scope digest;
- Planning Package digest;
- Phase/Task digests;
- authorized production paths;
- granted read context;
- verification/evidence requirements;
- Repair/Recovery metadata.

A model cannot expand a ticket by asking for more write authority in conversation.

---

## 11. Production mutation authority

Workplan captures the production-worktree baseline and reconciles create/modify/delete changes for the active Builder Work.

Unauthorized production mutation causes Task Gate failure.

Control-plane and runtime-local paths are treated separately. Common caches, bytecode, virtual environments, editor-local content, and defined Workplan runtime state do not become Builder production authority.

---

## 12. Task Gate

Only deterministic Task Gate logic marks a Task PASS.

Task Gate verifies applicable:

- current Task/Phase/Attempt identity;
- current generation;
- ticket digest and ticket identity;
- immutable Scope/Plan/Phase/Task/Recovery binding;
- completed Builder Work;
- structured evidence;
- declared verification results;
- required evidence artifacts/digests;
- mutation manifest identity;
- production mutations against authorized paths.

Manager and Builder may coordinate execution, but neither owns PASS authority.

---

## 13. Phase Gate

A Phase cannot pass until required Tasks pass and declared Phase-level integration/regression evidence is satisfied.

No later dependent Phase becomes eligible before deterministic Phase Gate PASS.

---

## 14. Repair

Task contracts define `max_repairs`, defaulting to 2 with supported range `0..5`.

A repair:

- creates a fresh Repair Attempt;
- uses a fresh Repair Ticket;
- remains bound to the same Task authority;
- does not expand authorized paths automatically;
- must pass the normal Task Gate.

Workplan can escalate immediately when the problem is structural instead of wasting repair budget.

---

## 15. Diagnosis and Recovery

Escalated Diagnosis and Recovery run externally and are reasoning-only.

Required flow:

```text
failure
  -> External Diagnosis
  -> External Recovery reasoning
  -> Recovery Contract
  -> ExecutionManager
  -> fresh Recovery Ticket
  -> Builder
  -> verification/evidence
  -> Task Gate
  -> Phase Gate
```

Recovery cannot directly mark a Task PASS.

---

## 16. Human approval

Human approval is explicit, state-bound, action-bound, subject-bound, time-bound, stale-safe, and single-use.

AI must never execute:

```bash
python Workplan/scripts/approve.py -- <challenge>
```

for the user.

When approval is required, the model reports the exact command and stops.

---

## 17. Resume and provider switching

Repository state is designed to outlive individual sessions/providers.

Resume uses durable:

- Workplan state;
- accepted Scope;
- immutable contracts;
- Work records;
- tickets;
- evidence;
- checkpoints;
- generation fencing.

Do not reconstruct authority from old chat messages. `WORKPLAN_NEXT` is the universal continuation mechanism.

---

## 18. Independent Evaluation and final acceptance

External Evaluation begins only after required Phase Gates PASS.

Evaluation independently maps approved acceptance criteria to implementation and current evidence. It should re-run the smallest sufficient final behavior checks rather than merely restating prior gate results.

Final accepted state is:

```text
lifecycle_stage = CLOSED_VALIDATED
project_state   = CLOSED_VALIDATED
```

A new Cycle then routes back to `EXECUTE_RESEARCH`.

---

## 19. Exact public commands

The supported exact tokens are:

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

Commands are literal authority. Lowercase, surrounding whitespace, prose-wrapped variants, wrong surfaces, and wrong lifecycle stages are rejected.

See `Workplan/ENTRY_PROMPT.md` for the full bootstrap contract.

---

## 20. Directory structure

The release intentionally keeps only repository-level material that participates in control, documentation, testing, migration, or supported workflow structure.

```text
.github/
  agents/
    manager.agent.md
    builder.agent.md
  skills/
    builder-task-execution/

Workplan/
  VERSION
  README.md
  Objective_dev.md
  ENTRY_PROMPT.md
  CHATGPT_PROJECT_INSTRUCTIONS.md
  RELEASE_VALIDATION.md
  CHANGELOG.md
  FILE_SHA256SUMS.txt

  external_agent/
    README.md
    RESEARCH_INSTRUCTION.md
    RESEARCH_POTOCAL_PROMPT.md
    PLANNING_PROMPT.md
    DIAGNOSIS_PROMPT.md
    RECOVERY_PROMPT.md
    EVALUATION_PROMPT.md

  templates/
    PROJECT_DETAILS_TEMPLATE.md

  config/
  control/
  ingest/
  plan/
  tasks/
  compiled/
  work/
  diagnosis/
  recovery/
  evaluation/
  history/
  archive/
  knowledge/
  USE_CASES/
  scripts/
  tests/
```

No empty root `src/`, `test/`, `docs/`, or `package/` placeholders are shipped. User projects may create their own production structure according to approved Planning.

---

## 21. Validation

After release files are stable, regenerate integrity:

```bash
python Workplan/scripts/integrity.py generate
```

Run structural validation:

```bash
python Workplan/scripts/validate.py
```

Run full validation:

```bash
python Workplan/scripts/validate.py --full
```

Full validation covers:

- release/version/schema/document consistency;
- Python syntax;
- release integrity manifest;
- exact command protocol;
- v5.3 deterministic invariants;
- v5.3.1 hardening rules;
- v5.3.1 real final-acceptance scenario;
- normal end-to-end execution;
- Diagnosis/Recovery end-to-end execution.

A skipped, timed-out, or unexecuted suite is not PASS.

See `Workplan/RELEASE_VALIDATION.md` for the release procedure and actual v5.3.1 acceptance record.

---

## 22. Integrity and package cleanliness

`Workplan/FILE_SHA256SUMS.txt` is generated deterministically from release files.

Release packaging excludes defined runtime/local content such as:

```text
.git/
__pycache__/
*.pyc
virtual environments
cache directories
editor-local files
runtime Work/approval/history state
secrets/credentials
temporary files
ZIP artifacts
```

A stale, missing, extra, or digest-mismatched release file causes integrity validation failure.

---

## 23. Upgrade from v5.3.0

Read:

```text
Workplan/MIGRATION_V5_3_0_TO_V5_3_1.md
```

The patch preserves schema 6. State migration is allowed only at a safe boundary and rejects active Work where deterministic equivalence cannot be guaranteed.

Migration tool:

```bash
python Workplan/scripts/migrate_v530_to_v531.py
```

Do not blindly overwrite an active repository without following migration rules.

---

## 24. Common failure handling

### Research does not pass ingest

Do not start Planning. Fix only the Research package until:

```text
INGEST_VALID: PASS
```

### Planning requests approval

Show the exact approval command and stop. The human must execute it.

### Builder needs an unauthorized path

Do not let Builder expand authority. Return to deterministic Workplan/Planning/Recovery as appropriate.

### Verification fails

Use the bounded repair path if allowed. Structural defects may route directly to Diagnosis/Recovery.

### Chat/provider session is lost

Do not restart from zero. Inspect repository state and use `WORKPLAN_NEXT`/resume.

### Full validation fails

Narrow the failing suite. Do not repeatedly rerun a giant workflow without diagnosing the specific deterministic blocker.

---

## 25. Documentation map

| File | Purpose |
|---|---|
| `README.md` | Primary user/operator guide. |
| `Workplan/README.md` | Advanced control-plane/operator reference. |
| `Workplan/Objective_dev.md` | Development constitution and invariants for Project Template itself. |
| `Workplan/ENTRY_PROMPT.md` | Exact public-command/bootstrap protocol. |
| `Workplan/CHATGPT_PROJECT_INSTRUCTIONS.md` | Compact ChatGPT Project bootstrap. |
| `Workplan/external_agent/RESEARCH_INSTRUCTION.md` | Machine-selected Research role instruction. |
| `Workplan/external_agent/RESEARCH_POTOCAL_PROMPT.md` | Detailed Research methodology and ingest handoff protocol. |
| `Workplan/templates/PROJECT_DETAILS_TEMPLATE.md` | Canonical Research output template. |
| `Workplan/RELEASE_VALIDATION.md` | Authoritative candidate validation/release procedure and acceptance record. |
| `Workplan/MIGRATION_V5_3_0_TO_V5_3_1.md` | Patch migration rules. |
| `Workplan/CHANGELOG.md` | Release history. |

---

## 26. Core invariant

```text
verified Research
  -> deterministic ingest
  -> immutable Scope
  -> approved Planning Package
  -> deterministic Phase/Task routing
  -> bounded local Builder Attempts
  -> Task Gates
  -> Phase Gates
  -> independent Evaluation
  -> CLOSED_VALIDATED
```

No model statement replaces a link in this chain.
