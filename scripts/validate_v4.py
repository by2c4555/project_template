#!/usr/bin/env python3
"""Structural/invariant validator for Project Template v4.3.2."""
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
    p=req(rel); return p.read_text(encoding='utf-8',errors='replace') if p.is_file() else ''

version=read('VERSION').strip()
if version!='4.3.2': errors.append(f'VERSION must be 4.3.2, found {version!r}')

required=[
 'README.md','CHANGELOG.md','EXECUTE/PROJECT_CONFIG.md','EXECUTE/project_details.md','EXECUTE/control/STATE.json','EXECUTE/control/TRANSITIONS.jsonl',
 'EXECUTE/plan/PLANNING_CONTROL.md','EXECUTE/plan/PLANNING_STATUS.md','EXECUTE/execution/EXECUTION_STATE.md','EXECUTE/evaluation/EVALUATION_STATUS.md',
 'EXECUTE/codex/IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md','EXECUTE/codex/ISSUE_DIAGNOSIS_PROMPT.md','EXECUTE/codex/RECOVERY_PROMPT.md','EXECUTE/codex/EVALUATION_PROMPT.md',
 'EXECUTE/external_research/README.md','EXECUTE/external_research/RESEARCH_GUIDE.md',
 'EXECUTE/external_research/setup/CHATGPT_INSTRUCTIONS.txt','EXECUTE/external_research/setup/EXTERNAL_INSTRUCTIONS_1000.txt',
 '.github/agents/project-manager.agent.md','.github/agents/builder100k.agent.md','.github/skills/builder-task-execution/SKILL.md',
 'scripts/workflow_state.py','scripts/start_cycle.py','scripts/import_scope.py','scripts/planning_gate.py','scripts/approve_plan.py','scripts/execution_gate.py','scripts/reset_manager_batch.py',
 'scripts/diagnosis_gate.py','scripts/approve_recovery.py','scripts/recovery_gate.py','scripts/resume_execution.py','scripts/start_replan.py','scripts/start_evaluation.py','scripts/finalize_evaluation.py','scripts/safe_exec.py','scripts/context_guard.py'
]
for r in required: req(r)

# v4.3.2 external research contract.
guide=read('EXECUTE/external_research/RESEARCH_GUIDE.md')
external_instruction=read('EXECUTE/external_research/setup/EXTERNAL_INSTRUCTIONS_1000.txt').strip()
chatgpt_instruction=read('EXECUTE/external_research/setup/CHATGPT_INSTRUCTIONS.txt').strip()
if len(external_instruction)>1000: errors.append(f'external instruction must be <=1000 characters, found {len(external_instruction)}')
for marker in ['Incomplete scope produces questions, not final artifacts','Rolling topic readiness','Checkpointing for long web-chat contexts','External/reference resource collection','Codex Context Map','project_details.md','docs/raw']:
    if marker.lower() not in guide.lower(): errors.append(f'RESEARCH_GUIDE missing marker: {marker}')
if 'RESEARCH_GUIDE.md' not in external_instruction or 'RESEARCH_GUIDE.md' not in chatgpt_instruction:
    errors.append('platform instructions must delegate detailed behavior to RESEARCH_GUIDE.md')
for obsolete in ['EXECUTE/external_research/RESEARCH_PROTOCOL.md','EXECUTE/external_research/RUN_RESEARCH.md','EXECUTE/research/RESEARCH_VERSION_TEMPLATE.md']:
    if (ROOT/obsolete).exists(): errors.append(f'obsolete v4.3.1 research artifact must not exist: {obsolete}')

# project_details template is machine-readable but intentionally incomplete in a fresh template.
pd=read('EXECUTE/project_details.md')
for marker in ['artifact_kind: PROJECT_DETAILS','artifact_status: INCOMPLETE','product_scope_unknowns: unknown','supporting_files: []','Change Summary / Delta','Explicitly Unchanged','Repository Investigation Targets','Codex Context Map']:
    if marker not in pd: errors.append(f'project_details template missing: {marker}')

# Machine state schema / clean-template state.
try:
    st=json.loads(read('EXECUTE/control/STATE.json'))
    if st.get('workflow_version')!='4.3.2': errors.append('STATE workflow_version must be 4.3.2')
    if st.get('schema_version')!=1: errors.append('STATE schema_version must be 1')
    for key in ['project_state','active_cycle','counters','runtime_policy','cycles']:
        if key not in st: errors.append(f'STATE missing {key}')
    pol=st.get('runtime_policy',{})
    if int(pol.get('manager_max_task_dispatches_per_batch',0))<1: errors.append('manager batch limit must be >=1')
    if int(pol.get('default_local_repair_attempts_per_task',-1))<0: errors.append('repair default must be >=0')
except Exception as exc:
    errors.append(f'invalid STATE.json: {exc}')

# Scope Snapshot / binding primitives.
ws=read('scripts/workflow_state.py')
for marker in ['validate_project_details_handoff','build_scope_manifest','snapshot_scope','verify_active_scope','ensure_scope_integrity','scope_digest']:
    if marker not in ws: errors.append(f'workflow_state missing scope primitive: {marker}')
start_cycle=read('scripts/start_cycle.py')
if '--scope' in start_cycle: errors.append('start_cycle.py must not require legacy --scope/Research_Vx input')
for marker in ['build_scope_manifest','snapshot_scope','SCOPE_001','based_on_scope_digest']:
    if marker not in start_cycle: errors.append(f'start_cycle missing v4.3.2 marker: {marker}')
import_scope=read('scripts/import_scope.py')
for marker in ['SCOPE_REVISION_IMPORTED','SUPERSEDED_BY_SCOPE_CHANGE','REPLAN_REQUIRED','build_scope_manifest']:
    if marker not in import_scope: errors.append(f'import_scope missing marker: {marker}')

# Human gates must be interactive and must not expose old static approval arguments.
for rel in ['scripts/approve_plan.py','scripts/approve_recovery.py','scripts/resume_execution.py','scripts/reset_manager_batch.py','scripts/start_evaluation.py']:
    t=read(rel)
    if 'human_tty_challenge' not in t: errors.append(f'{rel} must use human_tty_challenge')
    if '--yes' in t or 'I_APPROVE_IMPLEMENTATION' in t: errors.append(f'{rel} contains forbidden static/noninteractive approval bypass marker')
if 'sys.stdin.isatty()' not in ws or 'sys.stdout.isatty()' not in ws:
    errors.append('workflow_state.human_tty_challenge must require stdin/stdout TTY')

# Planning semantics + exact Scope binding.
planning=read('EXECUTE/codex/IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md')
for marker in ['Scope Snapshot','Codex Context Map','import_scope.py','PLAN_READY','Any later chat message','approve_plan.py','mark-plan-ready','Never execute `approve_plan.py`']:
    if marker not in planning: errors.append(f'planning prompt missing marker: {marker}')
if 'AWAITING_USER_APPROVAL' in planning: errors.append('planning prompt must not restore v4.2.1 conversational approval gate')
pg=read('scripts/planning_gate.py')
for marker in ['based_on_scope_revision','based_on_scope_digest','candidate_scope_digest','ensure_scope_integrity']:
    if marker not in pg: errors.append(f'planning_gate missing scope binding marker: {marker}')
ap=read('scripts/approve_plan.py')
for marker in ['scope_revision','scope_digest','candidate_scope_digest','approved_scope_digest']:
    if marker not in ap: errors.append(f'approve_plan missing exact scope binding marker: {marker}')
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
if 'approve_recovery.py' not in diag: errors.append('Diagnosis prompt must route implementation defects to human recovery approval')
if 'recovery_gate.py' not in rec: errors.append('Recovery prompt must end at recovery_gate verification')

# Evaluation gating / cycle semantics.
evalp=read('EXECUTE/codex/EVALUATION_PROMPT.md')
for marker in ['start_evaluation.py','finalize_evaluation.py','One authorization covers','new change cycle']:
    if marker.lower() not in evalp.lower(): errors.append(f'Evaluation prompt missing marker: {marker}')
completion=read('EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_TEMPLATE.md')
for marker in ['based_on_scope_revision','based_on_scope_digest']:
    if marker not in completion: errors.append(f'Completion Report template missing {marker}')
readme=read('README.md')
for marker in ['CLOSED_VALIDATED','NEW EXTERNAL SCOPE -> NEW CYCLE','No approval or execution authority carries forward','safe_exec.py','Scope Snapshot','import_scope.py']:
    if marker.lower() not in readme.lower(): errors.append(f'README missing v4.3.2 invariant: {marker}')

# Agent state ownership.
pm=read('.github/agents/project-manager.agent.md'); builder=read('.github/agents/builder100k.agent.md')
for marker in ['execution_gate.py begin-task','execution_gate.py complete-task','execution_gate.py fail-task','MANAGER_CONTEXT_RESET_REQUIRED']:
    if marker not in pm: errors.append(f'Manager agent missing {marker}')
if 'execution_gate.py authorize-repair' not in builder: errors.append('Builder must use machine repair counter')
if 'STATE.json' not in pm or 'STATE.json' not in builder: errors.append('agents must read machine state')

# Package-integrity implementation markers.
for marker in ['build_package_manifest','verify_manifest','snapshot_package','reset_package_workspace','package_digest']:
    if marker not in ws: errors.append(f'workflow_state missing package integrity primitive: {marker}')
for rel in ['scripts/execution_gate.py','scripts/recovery_gate.py','scripts/resume_execution.py','scripts/start_evaluation.py','scripts/finalize_evaluation.py']:
    if 'ensure_package_integrity' not in read(rel): errors.append(f'{rel} must verify approved package + scope integrity')

# No active legacy Research_Vx dependency outside explanatory migration text.
legacy_refs=[]
for base in [ROOT/'scripts',ROOT/'EXECUTE/codex',ROOT/'EXECUTE/plan',ROOT/'EXECUTE/evaluation']:
    for p in base.rglob('*'):
        if p.is_file() and p.suffix in {'.py','.md','.txt'}:
            t=p.read_text(encoding='utf-8',errors='replace')
            if 'Research_Vx' in t and p.name not in {'PLANNING_AND_COMPILATION_PROMPT.md','validate_v4.py'}:
                legacy_refs.append(str(p.relative_to(ROOT)))
if legacy_refs: errors.append('active legacy Research_Vx references remain: '+', '.join(sorted(set(legacy_refs))))

# Compile every Python script.
for p in sorted((ROOT/'scripts').glob('*.py')):
    try: py_compile.compile(str(p),doraise=True)
    except Exception as exc: errors.append(f'Python compile failed {p.relative_to(ROOT)}: {exc}')

# Model-binding readiness is a warning, not template invalidity.
try:
    mb=json.loads(read('EXECUTE/MODEL_BINDINGS.json'))
    if mb.get('schema_version')!='4.3.2': errors.append('MODEL_BINDINGS schema_version must be 4.3.2')
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
print('TEMPLATE_VALID: PASS (v4.3.2)')
print('Checkpointed external research, immutable Scope Snapshots, exact scope+package approval binding, token-safety and cycle boundaries validated.')
