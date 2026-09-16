# Changelog

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
