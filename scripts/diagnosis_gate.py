#!/usr/bin/env python3
"""Register an immutable Codex diagnosis and route the active issue without granting repair authority."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from workflow_state import ROOT, active_cycle, append_transition, load_state, save_state, utc_now

CLASSES={'IMPLEMENTATION_DEFECT','TASK_DEFECT','PLAN_DEFECT','EVALUATION_DEFECT','SCOPE_AMBIGUITY','EXTERNAL_BLOCKER','UNKNOWN'}

def find_issue(cycle,issue_id):
    for x in cycle.get('issues',[]):
        if x.get('issue_id')==issue_id: return x
    raise SystemExit(f'DIAGNOSIS_GATE: BLOCKED\nunknown issue: {issue_id}')

ap=argparse.ArgumentParser()
ap.add_argument('--issue',required=True)
ap.add_argument('--diagnosis',required=True,help='path to immutable Diagnosis markdown')
ap.add_argument('--classification',required=True,choices=sorted(CLASSES))
a=ap.parse_args()
state=load_state(); cid,cycle=active_cycle(state)
if cycle.get('active_issue')!=a.issue: raise SystemExit('DIAGNOSIS_GATE: BLOCKED\n--issue is not the active issue')
issue=find_issue(cycle,a.issue)
if issue.get('diagnosis'): raise SystemExit('DIAGNOSIS_GATE: BLOCKED\nactive issue already has a registered diagnosis; create a new diagnosis version only through an explicit supersession workflow')
p=ROOT/a.diagnosis
if not p.is_file(): raise SystemExit(f'DIAGNOSIS_GATE: BLOCKED\ndiagnosis artifact missing: {a.diagnosis}')
digest=hashlib.sha256(p.read_bytes()).hexdigest()
issue.update({'diagnosis':a.diagnosis,'diagnosis_digest':digest,'classification':a.classification,'diagnosed_at':utc_now()})
ex=cycle.get('execution') or {}; rec=ex.get('recovery') or {}
rec['diagnosis']=a.diagnosis
if a.classification=='IMPLEMENTATION_DEFECT':
    rec['status']='RECOVERY_PROPOSED'; cycle['lifecycle_stage']='AWAITING_RECOVERY_APPROVAL'; cycle['next_action']='USER_RUN_APPROVE_RECOVERY'
elif a.classification in {'TASK_DEFECT','PLAN_DEFECT'}:
    rec['status']='REPLAN_REQUIRED'; cycle['lifecycle_stage']='REPLAN_REQUIRED'; cycle['next_action']='RUN_START_REPLAN'; cycle['status']='REPLAN_REQUIRED'
elif a.classification=='EVALUATION_DEFECT':
    issue['status']='RESOLVED_AS_EVALUATION_DEFECT'
    cycle['active_issue']=None
    if ex:
        ex['active_issue']=None
        ex['status']='AWAITING_EVALUATION'
    rec['status']='RE_EVALUATION_REQUIRED'; cycle['lifecycle_stage']='AWAITING_EVALUATION_AUTHORIZATION'; cycle['next_action']='USER_RUN_START_EVALUATION'; cycle['status']='EXECUTION_COMPLETE'
elif a.classification=='SCOPE_AMBIGUITY':
    rec['status']='SCOPE_CLARIFICATION_REQUIRED'; cycle['lifecycle_stage']='SCOPE_CLARIFICATION_REQUIRED'; cycle['next_action']='EXTERNAL_SCOPE_CLARIFICATION'
elif a.classification=='EXTERNAL_BLOCKER':
    rec['status']='EXTERNAL_ACTION_REQUIRED'; cycle['lifecycle_stage']='EXTERNAL_BLOCKER'; cycle['next_action']='USER_EXTERNAL_ACTION'
else:
    rec['status']='CONTINUE_DIAGNOSIS'; cycle['lifecycle_stage']='DIAGNOSIS'; cycle['next_action']='CONTINUE_CODEX_DIAGNOSIS'
if ex: ex['recovery']=rec
save_state(state); append_transition('DIAGNOSIS_REGISTERED',actor='python:diagnosis_gate',cycle_id=cid,details={'issue':a.issue,'diagnosis':a.diagnosis,'classification':a.classification,'digest':digest})
print('DIAGNOSIS_GATE: PASS')
print(f'classification: {a.classification}')
print(f'next_action: {cycle["next_action"]}')
if a.classification=='IMPLEMENTATION_DEFECT': print('No repair authority granted. User must manually run scripts/approve_recovery.py.')
