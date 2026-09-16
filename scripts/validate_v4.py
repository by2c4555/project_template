#!/usr/bin/env python3
from pathlib import Path
import configparser
import json
import sys

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
    return p.read_text(encoding='utf-8', errors='replace') if p.exists() else ''


for rel in [
    'VERSION', 'README.md', 'EXECUTE_PROJECT_PROMPT.md', 'EXECUTE/PROJECT_STATUS.md', 'EXECUTE/PROJECT_CONFIG.md', 'EXECUTE/project_details.md',
    'EXECUTE/MODEL_CONFIG.ini', 'EXECUTE/MODEL_BINDINGS.json', 'EXECUTE/codex/PLANNING_AND_COMPILATION_PROMPT.md', 'EXECUTE/codex/EVALUATION_PROMPT.md',
    'EXECUTE/compiled/PROJECT_BRIEF.md', 'EXECUTE/compiled/ARCHITECTURE.md', 'EXECUTE/compiled/DECISIONS.md', 'EXECUTE/compiled/GLOBAL_CONSTRAINTS.md',
    'EXECUTE/plan/IMPLEMENTATION_PLAN.md', 'EXECUTE/plan/PLANNING_STATUS.md', 'EXECUTE/tasks/TASK_INDEX.md', 'EXECUTE/tasks/TASK_TEMPLATE.md',
    'EXECUTE/execution/EXECUTION_STATE.md', 'EXECUTE/evaluation/EVALUATION_STATUS.md', 'EXECUTE/reference/KNOWLEDGE_INDEX.md',
    '.github/agents/project-manager.agent.md', '.github/agents/builder100k.agent.md', '.github/skills/builder-task-execution/SKILL.md',
    'EXECUTE/docs/raw', 'EXECUTE/execution/evidence', 'EXECUTE/history/planning', 'EXECUTE/history/evaluation'
]:
    req(rel)

version = text('VERSION').strip()
if version != '4.1.1':
    errors.append('VERSION must be 4.1.1')

status = text('EXECUTE/PROJECT_STATUS.md')
if 'workflow_version: "4.1.1"' not in status:
    errors.append('PROJECT_STATUS workflow_version must be 4.1.1')
for x in ['research_version', 'planning_version', 'execution_version', 'evaluation_version']:
    if x not in status:
        errors.append(f'PROJECT_STATUS missing {x}')

if 'Only external independent Evaluation' not in text('.github/agents/project-manager.agent.md'):
    errors.append('Manager completion gate/evaluation separation missing')

# Verify human-editable configuration shape.
config_path = R / 'EXECUTE/MODEL_CONFIG.ini'
if config_path.exists():
    cp = configparser.ConfigParser(interpolation=None)
    try:
        cp.read(config_path, encoding='utf-8')
        for section, floor in {'manager': 512000, 'builder': 102400}.items():
            if not cp.has_section(section):
                errors.append(f'MODEL_CONFIG missing [{section}]')
                continue
            for key in ('model', 'provider', 'context'):
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
    b = json.loads(text('EXECUTE/MODEL_BINDINGS.json') or '{}')
except json.JSONDecodeError as e:
    errors.append(f'MODEL_BINDINGS invalid JSON: {e}')
    b = {}

if b.get('schema_version') != '4.1.1':
    errors.append('MODEL_BINDINGS schema_version must be 4.1.1')

for role, floor in {'ProjectManager500K': 512000, 'Builder100K': 102400}.items():
    r = b.get('roles', {}).get(role, {})
    if r.get('minimum_context_tokens') != floor:
        errors.append(f'{role} minimum mismatch')
    model = r.get('model')
    cap = r.get('documented_context_tokens', 0)
    if model and cap < floor:
        errors.append(f'{role} bound below floor')
    if not model:
        warns.append(f'{role} unbound')

if errors:
    print('TEMPLATE_VALID: FAIL')
    [print('FAIL:', e) for e in errors]
    raise SystemExit(1)

print('TEMPLATE_VALID: PASS (v4.1.1)')
for w in warns:
    print('WARN:', w)
print('RUNTIME_READY:', 'YES' if not warns else 'NO - edit EXECUTE/MODEL_CONFIG.ini, then run python scripts/configure_models.py')
