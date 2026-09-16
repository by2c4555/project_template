#!/usr/bin/env python3
"""Structural/invariant validator for Project Template v4.3.0."""
from __future__ import annotations
import json, py_compile, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]; warnings=[]

def req(rel):
    p=ROOT/rel
    if not p.is_file(): errors.append(f'missing required file: {rel}')
    return p

def read(rel):
    p=req(rel); return p.read_text(encoding='utf-8',errors='replace') if p.is_file() else ''

version=read('VERSION').strip()
if version!='4.3.0': errors.append(f'VERSION must be 4.3.0, found {version!r}')

required=[
 'README.md','CHANGELOG.md','EXECUTE/PROJECT_CONFIG.md','EXECUTE/control/STATE.json','EXECUTE/control/TRANSITIONS.jsonl',
 'EXECUTE/plan/PLANNING_CONTROL.md','EXECUTE/plan/PLANNING_STATUS.md','EXECUTE/execution/EXECUTION_STATE.md','EXECUTE/evaluation/EVALUATION_STATUS.md',
 'EXECUTE/codex/IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md','EXECUTE/codex/ISSUE_DIAGNOSIS_PROMPT.md','EXECUTE/codex/RECOVERY_PROMPT.md','EXECUTE/codex/EVALUATION_PROMPT.md',
 '.github/agents/project-manager.agent.md','.github/agents/builder100k.agent.md','.github/skills/builder-task-execution/SKILL.md',
 'scripts/workflow_state.py','scripts/start_cycle.py','scripts/planning_gate.py','scripts/approve_plan.py','scripts/execution_gate.py','scripts/reset_manager_batch.py',
 'scripts/diagnosis_gate.py','scripts/approve_recovery.py','scripts/recovery_gate.py','scripts/resume_execution.py','scripts/start_replan.py','scripts/start_evaluation.py','scripts/finalize_evaluation.py','scripts/safe_exec.py','scripts/context_guard.py'
]
for r in required: req(r)

# Machine state schema / clean-template state.
try:
    st=json.loads(read('EXECUTE/control/STATE.json'))
    if st.get('workflow_version')!='4.3.0': errors.append('STATE workflow_version must be 4.3.0')
    if st.get('schema_version')!=1: errors.append('STATE schema_version must be 1')
    for key in ['project_state','active_cycle','counters','runtime_policy','cycles']:
        if key not in st: errors.append(f'STATE missing {key}')
    pol=st.get('runtime_policy',{})
    if int(pol.get('manager_max_task_dispatches_per_batch',0))<1: errors.append('manager batch limit must be >=1')
    if int(pol.get('default_local_repair_attempts_per_task',-1))<0: errors.append('repair default must be >=0')
except Exception as exc:
    errors.append(f'invalid STATE.json: {exc}')

# Human gates must be interactive and must not expose old static approval arguments.
for rel in ['scripts/approve_plan.py','scripts/approve_recovery.py','scripts/resume_execution.py','scripts/reset_manager_batch.py','scripts/start_evaluation.py']:
    t=read(rel)
    if 'human_tty_challenge' not in t: errors.append(f'{rel} must use human_tty_challenge')
    if '--yes' in t or 'I_APPROVE_IMPLEMENTATION' in t: errors.append(f'{rel} contains forbidden static/noninteractive approval bypass marker')
helper=read('scripts/workflow_state.py')
if 'sys.stdin.isatty()' not in helper or 'sys.stdout.isatty()' not in helper:
    errors.append('workflow_state.human_tty_challenge must require stdin/stdout TTY')

# Planning semantics.
planning=read('EXECUTE/codex/IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md')
for marker in ['PLAN_READY','Any later chat message','approve_plan.py','mark-plan-ready','must never call human approval gates' if False else 'Never execute `approve_plan.py`']:
    if marker not in planning: errors.append(f'planning prompt missing marker: {marker}')
if 'AWAITING_USER_APPROVAL' in planning: errors.append('planning prompt must not restore v4.2.1 AWAITING_USER_APPROVAL conversational gate')
control=read('EXECUTE/plan/PLANNING_CONTROL.md')
if 'Chat is feedback, never implementation authority' not in control: errors.append('PLANNING_CONTROL missing chat!=approval invariant')

# Task contract/runtime separation.
task_template=read('EXECUTE/tasks/TASK_TEMPLATE.md')
if re.search(r'^status:\s*',task_template,re.M): errors.append('TASK_TEMPLATE must not contain mutable runtime status field')
for marker in ['planning_revision: Revision_N','artifact_status: COMPILED','execution_gate.py authorize-repair']:
    if marker not in task_template: errors.append(f'TASK_TEMPLATE missing {marker}')
for p in sorted((ROOT/'EXECUTE/tasks').glob('TASK_*.md')):
    if p.name in {'TASK_INDEX.md','TASK_TEMPLATE.md'}: continue
    txt=p.read_text(encoding='utf-8',errors='replace')
    if re.search(r'^status:\s*',txt,re.M): errors.append(f'{p.relative_to(ROOT)} contains mutable runtime status')

# Recovery split / self-authorization prevention.
legacy=read('EXECUTE/codex/ISSUE_DIAGNOSIS_AND_RECOVERY_PROMPT.md')
if 'DEPRECATED' not in legacy or 'STOP' not in legacy: errors.append('combined Diagnosis+Recovery prompt must be a deprecated hard stop')
diag=read('EXECUTE/codex/ISSUE_DIAGNOSIS_PROMPT.md'); rec=read('EXECUTE/codex/RECOVERY_PROMPT.md')
if 'No production repair' not in diag and 'No production repair in this invocation' not in diag: errors.append('Diagnosis prompt must prohibit production repair')
if 'resume_authorized: false' not in rec and 'does not' not in rec: warnings.append('Recovery prompt should explicitly state it cannot authorize resume')
if 'approve_recovery.py' not in diag: errors.append('Diagnosis prompt must route implementation defects to human recovery approval')
if 'recovery_gate.py' not in rec: errors.append('Recovery prompt must end at recovery_gate verification')

# Evaluation gating / cycle semantics.
evalp=read('EXECUTE/codex/EVALUATION_PROMPT.md')
for marker in ['start_evaluation.py','finalize_evaluation.py','One authorization covers','new change cycle']:
    if marker.lower() not in evalp.lower(): errors.append(f'Evaluation prompt missing marker: {marker}')
readme=read('README.md')
for marker in ['CLOSED_VALIDATED','NEW EXTERNAL SCOPE -> NEW CYCLE','No approval or execution authority carries forward','safe_exec.py']:
    if marker.lower() not in readme.lower(): errors.append(f'README missing v4.3 invariant: {marker}')

# Agent state ownership.
pm=read('.github/agents/project-manager.agent.md'); builder=read('.github/agents/builder100k.agent.md')
for marker in ['execution_gate.py begin-task','execution_gate.py complete-task','execution_gate.py fail-task','MANAGER_CONTEXT_RESET_REQUIRED']:
    if marker not in pm: errors.append(f'Manager agent missing {marker}')
if 'execution_gate.py authorize-repair' not in builder: errors.append('Builder must use machine repair counter')
if 'STATE.json' not in pm or 'STATE.json' not in builder: errors.append('agents must read machine state')

# Package-integrity implementation markers.
ws=read('scripts/workflow_state.py')
for marker in ['build_package_manifest','verify_manifest','snapshot_package','reset_package_workspace','package_digest']:
    if marker not in ws: errors.append(f'workflow_state missing integrity primitive: {marker}')
for rel in ['scripts/execution_gate.py','scripts/recovery_gate.py','scripts/resume_execution.py','scripts/start_evaluation.py','scripts/finalize_evaluation.py']:
    if 'ensure_package_integrity' not in read(rel): errors.append(f'{rel} must verify approved package integrity')

# Compile every Python script.
for p in sorted((ROOT/'scripts').glob('*.py')):
    try: py_compile.compile(str(p),doraise=True)
    except Exception as exc: errors.append(f'Python compile failed {p.relative_to(ROOT)}: {exc}')

# Model-binding readiness is a warning, not template invalidity.
try:
    mb=json.loads(read('EXECUTE/MODEL_BINDINGS.json'))
    if mb.get('schema_version')!='4.3.0': errors.append('MODEL_BINDINGS schema_version must be 4.3.0')
    unready=[]
    for role in ['ProjectManager500K','Builder100K']:
        r=(mb.get('roles') or {}).get(role,{})
        if not r.get('model') or int(r.get('documented_context_tokens') or 0)<int(r.get('minimum_context_tokens') or 0): unready.append(role)
    if unready: warnings.append('RUNTIME_READY: NO (configure local models): '+', '.join(unready))
except Exception as exc: errors.append(f'invalid MODEL_BINDINGS.json: {exc}')

if warnings:
    for w in warnings: print('WARN:',w)
if errors:
    print('TEMPLATE_VALID: FAIL')
    for e in errors: print('FAIL:',e)
    raise SystemExit(1)
print('TEMPLATE_VALID: PASS (v4.3.0)')
print('Machine-governed state, human phase gates, package integrity, recovery split and cycle boundaries validated.')
