# Changelog

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
