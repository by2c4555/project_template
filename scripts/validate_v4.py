#!/usr/bin/env python3
"""Structural/invariant validator for Project Template v4.4.0."""
from __future__ import annotations
import json, py_compile, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]; warnings=[]

def req(rel):
    p=ROOT/rel
    if not p.is_file(): errors.append(f'missing required file: {rel}')
    return p

def read(rel):
    p=req(rel)
    return p.read_text(encoding='utf-8',errors='replace') if p.is_file() else ''

# Root/meta invariants.
if read('VERSION').strip()!='4.4.0': errors.append('VERSION must be 4.4.0')
obj=read('Objective_dev.md')
for marker in ['User-Mandated Invariants','Mandatory Repository Structure','VERSION / CHANGE CYCLE','Manager / Builder','not user-project scope','Owner Feedback / Change Policy']:
    if marker.lower() not in obj.lower(): errors.append(f'Objective_dev.md missing marker: {marker}')
readme=read('README.md')
for marker in ['Objective_dev.md','# VERSION / CHANGE CYCLE','External Agent','Manager','Fresh Builder','PROJECT_COMPLETION_REPORT','CLOSED_VALIDATED','Research_Vx.md','agent_work.py']:
    if marker.lower() not in readme.lower(): errors.append(f'README missing v4.4.0 marker: {marker}')
if '```mermaid' not in readme: errors.append('README canonical VERSION / CHANGE CYCLE must include a Mermaid flow diagram')

# Required external-agent surfaces.
for rel in [
    'EXECUTE/external_agent/README.md','EXECUTE/external_agent/PLANNING_PROMPT.md','EXECUTE/external_agent/DIAGNOSIS_PROMPT.md',
    'EXECUTE/external_agent/RECOVERY_PROMPT.md','EXECUTE/external_agent/EVALUATION_PROMPT.md','scripts/agent_work.py',
    'EXECUTE/control/AGENT_WORK.json','EXECUTE/work/.gitkeep'
]: req(rel)
for rel, role in [
    ('EXECUTE/external_agent/PLANNING_PROMPT.md','PLANNING'),('EXECUTE/external_agent/DIAGNOSIS_PROMPT.md','DIAGNOSIS'),
    ('EXECUTE/external_agent/RECOVERY_PROMPT.md','RECOVERY'),('EXECUTE/external_agent/EVALUATION_PROMPT.md','EVALUATION')
]:
    t=read(rel)
    for marker in ['agent_work.py','checkpoint','resume']:
        if marker.lower() not in t.lower(): errors.append(f'{rel} missing resumability marker: {marker}')
    if f'--role {role}' not in t: errors.append(f'{rel} must begin provider-neutral work with role {role}')

# Deprecated Codex compatibility paths must hard-stop and redirect.
for rel in ['EXECUTE/codex/IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md','EXECUTE/codex/ISSUE_DIAGNOSIS_PROMPT.md','EXECUTE/codex/RECOVERY_PROMPT.md','EXECUTE/codex/EVALUATION_PROMPT.md','EXECUTE/codex/PLANNING_AND_COMPILATION_PROMPT.md','EXECUTE/codex/ISSUE_DIAGNOSIS_AND_RECOVERY_PROMPT.md']:
    t=read(rel)
    if 'DEPRECATED' not in t or 'STOP' not in t or 'EXECUTE/external_agent/' not in t: errors.append(f'{rel} must be deprecated STOP/redirect compatibility path')

# External research remains vendor neutral and no Research_Vx handoff.
guide=read('EXECUTE/external_research/RESEARCH_GUIDE.md')
for marker in ['READY_FOR_PLANNING','External Agent Context Map','project_details.md','docs/raw']:
    if marker.lower() not in guide.lower(): errors.append(f'RESEARCH_GUIDE missing marker: {marker}')
if 'Research_Vx.md' in guide and 'no `Research_Vx.md`' not in guide and 'no Research_Vx.md' not in guide:
    warnings.append('RESEARCH_GUIDE mentions Research_Vx.md; verify it is explanatory only')
pd=read('EXECUTE/project_details.md')
for marker in ['artifact_kind: PROJECT_DETAILS','artifact_status: INCOMPLETE','product_scope_unknowns: unknown','supporting_files: []','External Agent Context Map']:
    if marker not in pd: errors.append(f'project_details template missing: {marker}')

# Machine state schema / clean template.
try:
    st=json.loads(read('EXECUTE/control/STATE.json'))
    if st.get('workflow_version')!='4.4.0': errors.append('STATE workflow_version must be 4.4.0')
    if st.get('schema_version')!=2: errors.append('STATE schema_version must be 2')
    for key in ['project_state','active_cycle','active_external_work','counters','runtime_policy','cycles']:
        if key not in st: errors.append(f'STATE missing {key}')
    if 'agent_work' not in st.get('counters',{}): errors.append('STATE counters missing agent_work')
except Exception as exc: errors.append(f'invalid STATE.json: {exc}')

ws=read('scripts/workflow_state.py')
for marker in ['WORKFLOW_VERSION = "4.4.0"','SCHEMA_VERSION = 2','require_external_work_complete','validate_project_details_handoff','ensure_package_integrity']:
    if marker not in ws: errors.append(f'workflow_state missing v4.4 primitive: {marker}')
if 'READY_FOR_PLANNING' not in ws: errors.append('workflow_state handoff validation must be provider-neutral READY_FOR_PLANNING')

aw=read('scripts/agent_work.py')
for marker in ['PLANNING','DIAGNOSIS','RECOVERY','EVALUATION','checkpoint_seq','binding_digest','git_dirty_digest','EXTERNAL_AGENT_CHECKPOINT','expected-seq']:
    if marker not in aw: errors.append(f'agent_work.py missing marker: {marker}')

# Stage finalizers must require completed role work.
for rel,role in [('scripts/planning_gate.py','PLANNING'),('scripts/diagnosis_gate.py','DIAGNOSIS'),('scripts/recovery_gate.py','RECOVERY'),('scripts/finalize_evaluation.py','EVALUATION')]:
    t=read(rel)
    if 'require_external_work_complete' not in t or role not in t: errors.append(f'{rel} must require completed {role} External Agent work')

# Human gates remain interactive.
for rel in ['scripts/approve_plan.py','scripts/approve_recovery.py','scripts/resume_execution.py','scripts/reset_manager_batch.py','scripts/start_evaluation.py']:
    t=read(rel)
    if 'human_tty_challenge' not in t: errors.append(f'{rel} must use human_tty_challenge')
    if '--yes' in t or 'I_APPROVE_IMPLEMENTATION' in t: errors.append(f'{rel} contains forbidden noninteractive approval bypass')
if 'sys.stdin.isatty()' not in ws or 'sys.stdout.isatty()' not in ws: errors.append('human_tty_challenge must require stdin/stdout TTY')

# Planning/package/scope invariants remain.
pg=read('scripts/planning_gate.py')
for marker in ['based_on_scope_revision','based_on_scope_digest','candidate_scope_digest','ensure_scope_integrity','mark-plan-ready']:
    if marker not in pg: errors.append(f'planning_gate missing marker: {marker}')
ap=read('scripts/approve_plan.py')
for marker in ['scope_revision','scope_digest','candidate_scope_digest','approved_scope_digest']:
    if marker not in ap: errors.append(f'approve_plan missing exact scope binding marker: {marker}')

# Manager/Builder remain bounded and independent of External Agent scratch context.
pm=read('.github/agents/project-manager.agent.md'); builder=read('.github/agents/builder100k.agent.md')
for marker in ['execution_gate.py begin-task','execution_gate.py complete-task','execution_gate.py fail-task','MANAGER_CONTEXT_RESET_REQUIRED']:
    if marker not in pm: errors.append(f'Manager agent missing {marker}')
if 'execution_gate.py authorize-repair' not in builder: errors.append('Builder must use machine repair counter')
if 'STATE.json' not in pm or 'STATE.json' not in builder: errors.append('Manager/Builder must read authoritative STATE.json')
if 'AGENT_WORK.json' in builder: errors.append('Builder must not consume External Agent scratch/checkpoint state')

# Package integrity stays enforced downstream.
for rel in ['scripts/execution_gate.py','scripts/recovery_gate.py','scripts/resume_execution.py','scripts/start_evaluation.py','scripts/finalize_evaluation.py']:
    if 'ensure_package_integrity' not in read(rel): errors.append(f'{rel} must verify approved package + scope integrity')

# Completion report retains exact Scope binding.
completion=read('EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_TEMPLATE.md')
for marker in ['based_on_scope_revision','based_on_scope_digest']:
    if marker not in completion: errors.append(f'Completion Report template missing {marker}')

# Runtime model bindings are local Manager/Builder only; versioned schema.
try:
    mb=json.loads(read('EXECUTE/MODEL_BINDINGS.json'))
    if mb.get('schema_version')!='4.4.0': errors.append('MODEL_BINDINGS schema_version must be 4.4.0')
    unready=[]
    for role in ['ProjectManager500K','Builder100K']:
        r=(mb.get('roles') or {}).get(role,{})
        if not r.get('model') or int(r.get('documented_context_tokens') or 0)<int(r.get('minimum_context_tokens') or 0): unready.append(role)
    if unready: warnings.append('RUNTIME_READY: NO (configure local models): '+', '.join(unready))
except Exception as exc: errors.append(f'invalid MODEL_BINDINGS.json: {exc}')

# Compile all Python scripts.
for p in sorted((ROOT/'scripts').glob('*.py')):
    try: py_compile.compile(str(p),doraise=True)
    except Exception as exc: errors.append(f'Python compile failed {p.relative_to(ROOT)}: {exc}')

if warnings:
    for w in warnings: print('WARN:',w)
if errors:
    print('TEMPLATE_VALID: FAIL')
    for e in errors: print('FAIL:',e)
    raise SystemExit(1)
print('TEMPLATE_VALID: PASS (v4.4.0)')
print('Objective intent, canonical cycle diagram, provider-neutral resumability, deterministic gates, Manager/Builder boundaries, and cycle handoff invariants validated.')
