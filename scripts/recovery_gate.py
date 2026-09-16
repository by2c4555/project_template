#!/usr/bin/env python3
"""Verify recovery evidence and transition to a human-gated resume or re-evaluation boundary."""
from __future__ import annotations
import argparse, hashlib
from workflow_state import ROOT, active_cycle, append_transition, ensure_package_integrity, load_state, save_state, utc_now

def issue_of(cycle,i):
    return next((x for x in cycle.get('issues',[]) if x.get('issue_id')==i),None)

ap=argparse.ArgumentParser()
ap.add_argument('--issue',required=True); ap.add_argument('--resolution',required=True); ap.add_argument('--baseline',required=True); ap.add_argument('--verification',required=True,choices=['RECOVERY_PASS','VERIFIED','PASS'])
a=ap.parse_args()
state=load_state(); cid,cycle=active_cycle(state); ex=cycle.get('execution') or {}
if cycle.get('active_issue')!=a.issue: raise SystemExit('RECOVERY_GATE: BLOCKED\nissue is not active')
issue=issue_of(cycle,a.issue)
if not issue or not issue.get('recovery_approval'): raise SystemExit('RECOVERY_GATE: BLOCKED\nactive recovery lacks human recovery approval')
if issue.get('classification')!='IMPLEMENTATION_DEFECT': raise SystemExit('RECOVERY_GATE: BLOCKED\nonly IMPLEMENTATION_DEFECT direct repair may use this verification gate')
ensure_package_integrity(cycle)
res=ROOT/a.resolution
if not res.is_file(): raise SystemExit(f'RECOVERY_GATE: BLOCKED\nresolution artifact missing: {a.resolution}')
issue.update({'resolution':a.resolution,'resolution_digest':hashlib.sha256(res.read_bytes()).hexdigest(),'status':'RESOLVED_PENDING_NEXT_GATE','recovery_verified_at':utc_now()})
rec=ex.get('recovery') or {}; rec.update({'status':'VERIFIED','resolution':a.resolution,'verification':a.verification,'recovery_baseline':a.baseline,'resume_authorized':False})
origin=issue.get('origin_type')
if origin=='EXECUTION':
    task_id=issue.get('origin_task'); task=(ex.get('tasks') or {}).get(task_id)
    if not task: raise SystemExit('RECOVERY_GATE: BLOCKED\norigin task missing from execution state')
    task['status']='PASS_RECOVERED'; task['recovery']={'issue':a.issue,'diagnosis':issue.get('diagnosis'),'resolution':a.resolution}
    ex['active_issue']=a.issue; ex['status']='RECOVERY_VERIFIED'; cycle['status']='RECOVERY'; cycle['lifecycle_stage']='AWAITING_RESUME_APPROVAL'; cycle['next_action']='USER_RUN_RESUME_EXECUTION'
elif origin=='EVALUATION':
    ex['active_issue']=None; ex['status']='AWAITING_EVALUATION'; issue['status']='RESOLVED'; cycle['active_issue']=None; cycle['status']='EXECUTION_COMPLETE'; cycle['lifecycle_stage']='AWAITING_EVALUATION_AUTHORIZATION'; cycle['next_action']='USER_RUN_START_EVALUATION'
else:
    raise SystemExit(f'RECOVERY_GATE: BLOCKED\nunsupported origin_type: {origin}')
ex['recovery']=rec; save_state(state); append_transition('RECOVERY_VERIFIED',actor='python:recovery_gate',cycle_id=cid,details={'issue':a.issue,'origin_type':origin,'resolution':a.resolution,'baseline':a.baseline})
print('RECOVERY_GATE: PASS'); print(f'origin_type: {origin}'); print('resume_authorized: false')
print(f'next_action: {cycle["next_action"]}')
