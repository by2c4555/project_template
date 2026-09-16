#!/usr/bin/env python3
from pathlib import Path
import configparser
import json
import py_compile

R = Path(__file__).resolve().parents[1]
errors = []
warns = []


def req(rel):
    p = R / rel
    if not p.exists():
        errors.append(f'missing: {rel}')
    return p


def text(rel):
    p = req(rel)
    return p.read_text(encoding='utf-8', errors='replace') if p.exists() and p.is_file() else ''


required = [
    'VERSION', 'README.md', 'CHANGELOG.md', 'EXECUTE_PROJECT_PROMPT.md',
    'EXECUTE/PROJECT_STATUS.md', 'EXECUTE/PROJECT_CONFIG.md', 'EXECUTE/project_details.md',
    'EXECUTE/MODEL_CONFIG.ini', 'EXECUTE/MODEL_BINDINGS.json',
    'EXECUTE/chatgpt/PROJECT_INSTRUCTIONS.txt', 'EXECUTE/chatgpt/MASTER_RESEARCH_PROMPT.md',
    'EXECUTE/chatgpt/START_RESEARCH_PROMPT.md', 'EXECUTE/chatgpt/START_NEXT_VERSION_PROMPT.md',
    'EXECUTE/chatgpt/PROCESS_SCOPE_CLARIFICATION_PROMPT.md',
    'EXECUTE/codex/IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md',
    'EXECUTE/codex/PLANNING_AND_COMPILATION_PROMPT.md',
    'EXECUTE/codex/ISSUE_DIAGNOSIS_AND_RECOVERY_PROMPT.md',
    'EXECUTE/codex/EVALUATION_PROMPT.md',
    'EXECUTE/compiled/PROJECT_BRIEF.md', 'EXECUTE/compiled/ARCHITECTURE.md',
    'EXECUTE/compiled/DECISIONS.md', 'EXECUTE/compiled/GLOBAL_CONSTRAINTS.md',
    'EXECUTE/compiled/INTERFACES.md', 'EXECUTE/compiled/DATA_MODEL.md', 'EXECUTE/compiled/KNOWN_RISKS.md',
    'EXECUTE/plan/IMPLEMENTATION_PLAN.md', 'EXECUTE/plan/PLANNING_STATUS.md',
    'EXECUTE/plan/PLANNING_REVISION_TEMPLATE.md',
    'EXECUTE/tasks/TASK_INDEX.md', 'EXECUTE/tasks/TASK_TEMPLATE.md',
    'EXECUTE/execution/EXECUTION_STATE.md', 'EXECUTE/execution/EXECUTION_SUMMARY.md',
    'EXECUTE/issues/ISSUE_INDEX.md', 'EXECUTE/issues/ISSUE_TEMPLATE.md',
    'EXECUTE/diagnostics/DIAGNOSIS_STATUS.md', 'EXECUTE/diagnostics/DIAGNOSIS_TEMPLATE.md',
    'EXECUTE/knowledge/KNOWLEDGE_INDEX.md', 'EXECUTE/knowledge/resolutions/RESOLUTION_TEMPLATE.md',
    'EXECUTE/reference/KNOWLEDGE_INDEX.md',
    'EXECUTE/evaluation/EVALUATION_STATUS.md', 'EXECUTE/evaluation/EVALUATION_REPORT_TEMPLATE.md',
    'EXECUTE/evaluation/EVALUATION_REVIEW_TEMPLATE.md', 'EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_TEMPLATE.md',
    'EXECUTE/scope/SCOPE_CLARIFICATION_REQUIRED_TEMPLATE.md',
    '.github/agents/project-manager.agent.md', '.github/agents/builder100k.agent.md',
    '.github/skills/builder-task-execution/SKILL.md',
    'scripts/approve_plan.py', 'scripts/configure_models.py', 'scripts/context_guard.py',
    'scripts/recovery_gate.py', 'scripts/validate_v4.py',
    'EXECUTE/docs/raw', 'EXECUTE/execution/evidence',
    'EXECUTE/history/planning', 'EXECUTE/history/evaluation', 'EXECUTE/history/diagnostics',
    'EXECUTE/history/recovery', 'EXECUTE/history/completion',
    'EXECUTE/knowledge/patterns', 'EXECUTE/knowledge/decisions',
]
for rel in required:
    req(rel)

version = text('VERSION').strip()
if version != '4.2.0':
    errors.append('VERSION must be 4.2.0')

status = text('EXECUTE/PROJECT_STATUS.md')
for marker in [
    'workflow_version: "4.2.0"', 'active_issue:', 'last_resolved_issue:',
    'recovery_status:', 'resume_authorized:', 'completion_report:', 'scope_clarification_status:'
]:
    if marker not in status:
        errors.append(f'PROJECT_STATUS missing v4.2.0 marker: {marker}')

execution = text('EXECUTE/execution/EXECUTION_STATE.md')
for marker in [
    'PAUSED_FOR_EXTERNAL_REPAIR', 'RECOVERY_VERIFICATION', 'READY_TO_RESUME',
    'recovered_tasks:', 'active_issue:', 'resume_authorized:', 'recovery_baseline:'
]:
    if marker not in execution:
        errors.append(f'EXECUTION_STATE missing recovery marker: {marker}')

issue_template = text('EXECUTE/issues/ISSUE_TEMPLATE.md')
for marker in ['resume_authorized: false', 'Evidence Pointers', 'Attempts Ruled Out', 'Recovery Control']:
    if marker not in issue_template:
        errors.append(f'ISSUE_TEMPLATE missing forensic marker: {marker}')

recovery_prompt = text('EXECUTE/codex/ISSUE_DIAGNOSIS_AND_RECOVERY_PROMPT.md')
for marker in [
    'IMPLEMENTATION_DEFECT', 'TASK_DEFECT', 'PLAN_DEFECT', 'EVALUATION_DEFECT',
    'SCOPE_AMBIGUITY', 'EXTERNAL_BLOCKER', 'PASS_RECOVERED', 'RESOLUTION_NNNN',
    'READY_TO_RESUME', 'Never send an undiagnosed technical failure directly to ChatGPT'
]:
    if marker not in recovery_prompt:
        errors.append(f'Recovery prompt missing marker: {marker}')

eval_prompt = text('EXECUTE/codex/EVALUATION_PROMPT.md')
for marker in ['DIAGNOSIS_REQUIRED', 'PROJECT_COMPLETION_REPORT_Vx.md', 'False Evaluation Protection', 'PASS_RECOVERED']:
    if marker not in eval_prompt:
        errors.append(f'EVALUATION_PROMPT missing marker: {marker}')

completion_template = text('EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_TEMPLATE.md')
for marker in ['Delivered Capability Inventory', 'Final Architecture', 'Execution and Recovery History', 'Critical Invariants', 'Context for Future Version Research']:
    if marker not in completion_template:
        errors.append(f'Completion report template missing section: {marker}')

planning_prompt = text('EXECUTE/codex/IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md')
for marker in [
    'Prior Resolution Knowledge Check', 'EXECUTE/knowledge/KNOWLEDGE_INDEX.md',
    'material_unknowns: 0', 'implementation_approval_requested: true',
    'A complete plan is **not** permission to implement', 'PLAN_DEFECT'
]:
    if marker not in planning_prompt:
        errors.append(f'Planning prompt missing marker: {marker}')

manager = text('.github/agents/project-manager.agent.md')
for marker in ['Mandatory Incident Transition', 'PAUSED_FOR_EXTERNAL_REPAIR', 'recovery_gate.py', 'PASS_RECOVERED', 'Do not ask ChatGPT to diagnose the failure']:
    if marker not in manager:
        errors.append(f'Manager agent missing marker: {marker}')

builder = text('.github/agents/builder100k.agent.md')
for marker in ['external_recovery_required: true', 'Local Repair Limit', 'Do not become an open-ended recovery agent']:
    if marker not in builder:
        errors.append(f'Builder agent missing marker: {marker}')

chatgpt = text('EXECUTE/chatgpt/PROJECT_INSTRUCTIONS.txt')
for marker in ['NEXT_VERSION_RESEARCH', 'SCOPE_CLARIFICATION', 'PROJECT_COMPLETION_REPORT_Vx.md', 'ChatGPT = WHAT / WHY / SCOPE / PRODUCT EVOLUTION']:
    if marker not in chatgpt:
        errors.append(f'ChatGPT instructions missing marker: {marker}')

# Obsolete v4.1.3 technical-routing entry prompts must not exist in v4.2.0.
for obsolete in [
    'EXECUTE/chatgpt/PROCESS_EVALUATION_PROMPT.md',
    'EXECUTE/chatgpt/PROCESS_ISSUE_PROMPT.md',
    'EXECUTE/research/CHATGPT_RESEARCH_HANDOFF.md',
]:
    if (R / obsolete).exists():
        errors.append(f'obsolete v4.1 technical routing artifact still present: {obsolete}')

# Core v4.2 active files must not expose obsolete Evaluation terminal states.
for rel in [
    'EXECUTE/PROJECT_CONFIG.md', 'EXECUTE/codex/EVALUATION_PROMPT.md',
    'EXECUTE/evaluation/EVALUATION_REPORT_TEMPLATE.md', '.github/agents/project-manager.agent.md', 'README.md'
]:
    t = text(rel)
    for obsolete_state in ['RESEARCH_REQUIRED', 'CORRECTION_REQUIRED']:
        if obsolete_state in t:
            errors.append(f'{rel} contains obsolete evaluation route {obsolete_state}')

planning_status = text('EXECUTE/plan/PLANNING_STATUS.md')
for marker in ['planning_revision', 'material_unknowns', 'implementation_approval_requested', 'AWAITING_USER_FEEDBACK', 'AWAITING_USER_APPROVAL']:
    if marker not in planning_status:
        errors.append(f'PLANNING_STATUS missing approval-loop marker: {marker}')

# Verify human-editable local model configuration.
config_path = R / 'EXECUTE/MODEL_CONFIG.ini'
if config_path.exists():
    cp = configparser.ConfigParser(interpolation=None)
    try:
        cp.read(config_path, encoding='utf-8')
        for section, floor in {'manager': 512000, 'builder': 102400}.items():
            if not cp.has_section(section):
                errors.append(f'MODEL_CONFIG missing [{section}]')
                continue
            for key in ('model_id', 'vscode_model_name', 'vendor', 'context'):
                if not cp.has_option(section, key):
                    errors.append(f'MODEL_CONFIG [{section}] missing {key}')
            try:
                cap = cp.getint(section, 'context')
                if cap < floor:
                    errors.append(f'MODEL_CONFIG [{section}] context {cap} < minimum {floor}')
            except (ValueError, configparser.Error):
                errors.append(f'MODEL_CONFIG [{section}] context must be an integer')
    except configparser.Error as e:
        errors.append(f'MODEL_CONFIG parse error: {e}')

try:
    bindings = json.loads(text('EXECUTE/MODEL_BINDINGS.json') or '{}')
except json.JSONDecodeError as e:
    errors.append(f'MODEL_BINDINGS invalid JSON: {e}')
    bindings = {}

if bindings.get('schema_version') != '4.2.0':
    errors.append('MODEL_BINDINGS schema_version must be 4.2.0')

tech = bindings.get('external_intelligence', {}).get('technical_authority', {})
for responsibility in ['planning', 'diagnosis', 'recovery', 'evaluation', 'project_completion_handoff']:
    if responsibility not in tech.get('responsibilities', []):
        errors.append(f'MODEL_BINDINGS technical_authority missing responsibility: {responsibility}')

for role, floor in {'ProjectManager500K': 512000, 'Builder100K': 102400}.items():
    r = bindings.get('roles', {}).get(role, {})
    if r.get('minimum_context_tokens') != floor:
        errors.append(f'{role} minimum mismatch')
    model = r.get('model')
    model_id = r.get('model_id')
    vscode_model_name = r.get('vscode_model_name')
    vendor = r.get('vendor')
    cap = r.get('documented_context_tokens', 0)
    if model and cap < floor:
        errors.append(f'{role} bound below floor')
    if model and vscode_model_name and vendor:
        expected = f'{vscode_model_name} ({vendor})'
        if model != expected:
            errors.append(f'{role} qualified model mismatch: expected {expected!r}')
    if model and not model_id:
        errors.append(f'{role} bound model missing model_id provenance')
    if not model:
        warns.append(f'{role} unbound')

# Python syntax sanity.
for rel in ['scripts/approve_plan.py', 'scripts/configure_models.py', 'scripts/context_guard.py', 'scripts/recovery_gate.py']:
    try:
        py_compile.compile(str(R / rel), doraise=True)
    except Exception as e:
        errors.append(f'python syntax error in {rel}: {e}')

if errors:
    print('TEMPLATE_VALID: FAIL')
    for e in errors:
        print('FAIL:', e)
    raise SystemExit(1)

print('TEMPLATE_VALID: PASS (v4.2.0)')
for w in warns:
    print('WARN:', w)
print('RUNTIME_READY:', 'YES' if not warns else 'NO - edit EXECUTE/MODEL_CONFIG.ini, then run python scripts/configure_models.py')
