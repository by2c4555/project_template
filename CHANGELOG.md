# Changelog

## v4.2.0 — Recovery, Diagnosis, Evaluation Integrity & Project Learning

### Lifecycle architecture
- Expanded the canonical lifecycle to **Research -> Plan -> Execute -> Recover -> Evaluate -> Learn -> Evolve**.
- Formalized responsibility ownership: ChatGPT owns WHAT/WHY/SCOPE/product evolution; Codex owns HOW/Planning/Tasks/Diagnosis/Recovery/Evaluation; Manager owns execution control; Builder owns bounded implementation; User owns approval/product decisions.
- Removed direct normal routing of runtime issues and blocking Evaluation findings to ChatGPT Research. Technical failures now route to Codex Diagnosis first.

### Local execution incident recovery
- Added mandatory execution pause semantics for Builder failures that exceed bounded local repair.
- Added durable Issue forensic handoff contract with evidence pointers, reproduction, failure signature, safe baseline, attempts ruled out, and resume lock.
- Added execution states: `ISSUE_DETECTED`, `PAUSED_FOR_DIAGNOSIS`, `PAUSED_FOR_EXTERNAL_REPAIR`, `RECOVERY_VERIFICATION`, and `READY_TO_RESUME`.
- Added `ISSUE_DIAGNOSIS_AND_RECOVERY_PROMPT.md` for Codex or compatible external recovery agents.
- Added `PASS_RECOVERED` Task status so recovered incidents remain visible to final Evaluation.
- Added `scripts/recovery_gate.py` so local Manager resume is based on verified disk artifacts, not chat claims.

### Diagnosis and routing
- Added `EXECUTE/diagnostics/**` with durable Diagnosis artifacts.
- Standardized root-cause classifications: `IMPLEMENTATION_DEFECT`, `TASK_DEFECT`, `PLAN_DEFECT`, `EVALUATION_DEFECT`, `SCOPE_AMBIGUITY`, `EXTERNAL_BLOCKER`, `UNKNOWN`.
- Added explicit false-evaluation handling: preserve prior Evaluation, create Evaluation Review, and re-evaluate without unnecessary code changes.
- Added `SCOPE_CLARIFICATION_REQUIRED_Vx.md` as the rare technical-to-product escalation artifact.

### Resolution knowledge base
- Added `EXECUTE/knowledge/KNOWLEDGE_INDEX.md` and `knowledge/resolutions/RESOLUTION_NNNN.md`.
- Every material successful execution recovery now records symptoms, root cause, trigger conditions, failed approaches, correct fix, verification, prevention rules, regression protection, and future detection signals.
- Codex Planning, Manager context selection, and Codex Evaluation are required to consume relevant verified resolution knowledge.
- Clarified the distinction between `reference/KNOWLEDGE_INDEX.md` (prepared project knowledge) and `knowledge/KNOWLEDGE_INDEX.md` (verified incident/recovery learning).

### Evaluation redesign
- Simplified terminal Evaluation results to `PASS`, `PASS_WITH_FINDINGS`, or `DIAGNOSIS_REQUIRED`.
- Blocking findings no longer self-classify the correction route; Codex Diagnosis determines whether code, Task, Plan, Evaluation, scope, or an external dependency is defective.
- Recovered Tasks are mandatory high-attention regression areas during Evaluation.

### Full post-implementation handoff
- Added `PROJECT_COMPLETION_REPORT_Vx.md` contract/template.
- `PASS` and `PASS_WITH_FINDINGS` now require a detailed full-system report describing delivered behavior, final architecture, repository map, interfaces/data, decisions, plan deviations, recovery history, verification, limitations, technical debt, risks, critical invariants, extension points, and the verified baseline.
- The Completion Report becomes the preferred baseline input for ChatGPT next-version/feature Research.

### ChatGPT prompt pack
- Refocused ChatGPT on initial Research, next-version Research, and true scope clarification.
- Added `START_NEXT_VERSION_PROMPT.md` and `PROCESS_SCOPE_CLARIFICATION_PROMPT.md`.
- Removed obsolete direct `PROCESS_ISSUE_PROMPT.md` and `PROCESS_EVALUATION_PROMPT.md` technical routing entry points.

### Validation and documentation
- Updated model-binding metadata to v4.2.0 and expanded Codex technical-authority responsibilities.
- Reworked README around the complete happy path, incident path, false-evaluation path, safe resume, knowledge reuse, and future-version loop.
- Expanded template validation to enforce the new recovery/diagnosis/completion contracts and reject obsolete v4.1 routing states.


## v4.1.3 — Codex Preparation & Approval Loop Patch

### Role architecture
- Canonicalized the responsibility split: **ChatGPT Research = define scope; Codex GPT-6 = prepare the work; Manager = manage the work; Builder = perform the work**.
- Reframed Codex from one-shot “Planning & Knowledge Compilation” into repository-level **Implementation Research, Context Compilation & Planning**.
- Kept the previous `PLANNING_AND_COMPILATION_PROMPT.md` as a compatibility entry point while making `IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md` canonical.

### Planning refinement loop
- Added an explicit Codex material-unknown/user-feedback loop before implementation approval.
- Added `AWAITING_USER_FEEDBACK` as distinct from `AWAITING_USER_APPROVAL`.
- Added `planning_revision`, `material_unknowns`, and `implementation_approval_requested` state fields.
- Pre-approval comments normally create revisions inside the same Planning Vx; Planning Vx increments only for a materially new planning cycle/replan.

### Hard implementation approval gate
- A complete plan no longer implies permission to implement. Codex must explicitly request implementation authorization only after `material_unknowns: 0`.
- `approve_plan.py` now refuses approval unless the exact plan is `AWAITING_USER_APPROVAL`, has zero material unknowns, and records `implementation_approval_requested: true`.
- Local Manager/Builder are explicitly forbidden from guessing missing material requirements; preparation defects escalate to Codex/user resolution or replan.

### Version / validation
- Updated workflow/model-binding metadata and validators to v4.1.3.
- README now documents the feedback loop, explicit implementation approval, revised tool ownership, and new canonical Codex prompt.

## v4.1.2 — Tool Map & Model Identity Patch

### Onboarding / workflow clarity
- Reworked the README so the lifecycle starts with **Research V1 in ChatGPT Project**, not with an artificial VS Code “Step 0”.
- Added a required-tools section covering ChatGPT Project, Codex/GPT-6 Astra, VS Code, VS Code Chat/custom agents, Other Models/BYOK providers (OpenRouter/Ollama), Python, and recommended Git.
- Added an explicit tool owner to every workflow step plus a state-to-tool routing table.
- Separated one-time workstation/project setup from the versioned Research → Planning → Approval → Execution → Evaluation lifecycle.

### Model identity correctness
- Split runtime model configuration into `model_id`, `vscode_model_name`, `vendor`, and `context`.
- `model_id` is preserved for provider/API provenance; `.agent.md` is pinned with the VS Code qualified model name `Model Name (vendor)`.
- README now explains how to use **Chat: Manage Language Models** and why provider JSON alone might not identify an individual model.
- Updated `MODEL_BINDINGS.json` to binding schema v4 and extended validation for model identity/provenance.
- Kept legacy CLI `--*-model` / `--*-provider` aliases for advanced migration/automation, while requiring explicit model-ID provenance in v4.1.2 configuration.

## v4.1.1 — Configuration & Onboarding Patch

### Usability
- Rewrote the root README around a usage-first Quick Start with explicit Research → Planning → Approval → Execution → Evaluation routing.
- Added a “Where am I now?” state-to-next-action table and a prompt-selection table.
- Documented `docs/raw/**` as durable evidence that must not be cleared after Planning.

### Model configuration
- Added human-editable `EXECUTE/MODEL_CONFIG.ini`.
- `scripts/configure_models.py` now reads the INI by default; normal setup is `python scripts/configure_models.py` with no six-argument command.
- Existing CLI model/provider/context flags remain available as optional overrides for automation and backward compatibility.
- Added friendly incomplete-config and context-floor errors.

### Knowledge and workspace consistency
- Planning now explicitly updates `EXECUTE/reference/KNOWLEDGE_INDEX.md` while preserving raw evidence/provenance.
- Added distributed placeholder directories for `docs/raw`, execution evidence, Planning/Evaluation history, and Research inbox categories.
- Updated template/schema/workflow validation to v4.1.1.

## v4.1.0 — External Intelligence / Closed Evaluation Loop

### Architecture
- Replaced the VS Code Planner512K role with external Codex / GPT-6 Astra Planning & Knowledge Compilation.
- Added explicit `Research Vx -> Planning Vx -> Approval -> Execution Vx -> Evaluation Vx` lifecycle.
- Added independent read-only Codex/Astra Evaluation after local execution.
- Evaluation can route to correction, replanning, or Research Vx+1.

### Local execution
- Added `ProjectManager500K` local orchestration role (minimum 512000 tokens).
- Added `Builder100K` bounded local implementation role (minimum 102400 tokens).
- Local roles are explicitly no-RAG compatible and consume compiled context manifests.
- `Execution COMPLETE` now transitions to `Evaluation REQUIRED`, never directly to project validation.

### Knowledge preservation
- Added compiled intelligence layer: project brief, architecture, decisions, global constraints, interfaces, data model, known risks.
- Task template now requires self-contained context manifests, decision/requirement provenance, invariants, out-of-scope boundaries, and evidence output.
- Added immutable Planning/Evaluation history structure.

### Evaluation feedback
- Added `Evaluation_Vx.md` and `RESEARCH_HANDOFF_Vx.md` contracts.
- Added findings classification/routing for implementation bugs, plan defects, research gaps, architecture violations, test gaps, security/performance risks, and technical debt.

### Breaking changes from v4.0.1
- `Planner512K`, `Builder128K`, and `Builder256K` are no longer the v4.1 runtime roles.
- Planning is not performed by ProjectManager or local VS Code agents.
- User approval is required for each Planning Vx before execution.
- The project cannot be declared validated solely from local Task completion.
