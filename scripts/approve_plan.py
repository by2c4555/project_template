#!/usr/bin/env python3
"""HUMAN/OPERATOR-ONLY interactive implementation approval gate for v4.3.1."""
from __future__ import annotations
from workflow_state import (
    CONTROL, active_cycle, append_transition, approval_path_for, build_package_manifest,
    human_tty_challenge, load_state, manifest_path_for, next_id, save_state, snapshot_package, utc_now,
    write_json,
)

state=load_state(); cid, cycle=active_cycle(state); p=cycle.get('planning') or {}
errors=[]
if cycle.get('status')!='PLANNING': errors.append(f'cycle status must be PLANNING, found {cycle.get("status")}')
if p.get('status')!='PLAN_READY': errors.append(f'planning status must be PLAN_READY, found {p.get("status")}')
if p.get('material_unknowns')!=0: errors.append('material_unknowns must be exactly 0')
if cycle.get('approval'): errors.append('current Planning already has an approval; do not approve twice')
try:
    manifest=build_package_manifest(p.get('version'),p.get('revision_label'))
except ValueError as exc:
    errors.extend(str(exc).splitlines()); manifest=None
if manifest and p.get('candidate_package_digest') != manifest.get('package_digest'):
    errors.append('package changed after PLAN_READY; return to planning and mark PLAN_READY again')
if errors:
    raise SystemExit('IMPLEMENTATION_APPROVAL: BLOCKED\n'+'\n'.join('FAIL: '+e for e in errors))

human_tty_challenge('IMPLEMENTATION APPROVAL',[
    f'Cycle: {cid}', f'Planning: {p["version"]} / {p["revision_label"]}',
    f'Tasks: {manifest["task_count"]}', f'Package SHA-256: {manifest["package_digest"]}'
])

approval_id=next_id(state,'approval','APPROVAL_',4)
execution_version=next_id(state,'execution','Execution_V',width=1)
manifest_path=manifest_path_for(approval_id); write_json(manifest_path,manifest)
history_snapshot=snapshot_package(cid, approval_id, manifest)
approval={
    'approval_id':approval_id,'cycle_id':cid,'status':'ACTIVE','approved_at':utc_now(),
    'planning_version':p['version'],'planning_revision':p['revision_label'],
    'package_digest':manifest['package_digest'],'task_count':manifest['task_count'],
    'manifest_path':str(manifest_path.relative_to(CONTROL.parents[1])).replace('\\','/'),
    'human_interactive':True,'history_snapshot':history_snapshot,
}
# relative_to(ROOT), CONTROL.parents[1] is repository root
write_json(approval_path_for(approval_id),approval)
policy=state['runtime_policy']
tasks={}
for c in manifest['task_contracts']:
    max_repairs=c.get('max_repairs')
    if max_repairs is None: max_repairs=policy['default_local_repair_attempts_per_task']
    tasks[c['task_id']]={
        'status':'PENDING','contract_path':c['path'],'dependencies':c['depends_on'],
        'dispatch_count':0,'repair_attempts':0,'max_repairs':max_repairs,'evidence':None,'recovery':None,
    }
cycle['approval']=approval
p.update({'status':'APPROVED','package_status':'APPROVED','interaction_gate':'NONE','invocation_stop_required':False,'task_expansion_allowed':False})
cycle['execution']={
    'version':execution_version,'status':'READY','bound_planning_version':p['version'],'bound_planning_revision':p['revision_label'],
    'approval_id':approval_id,'approved_package_digest':manifest['package_digest'],'tasks':tasks,
    'active_task':None,'active_issue':None,'last_resolved_issue':None,
    'manager_batch':{'number':1,'dispatches':0,'max_dispatches':policy['manager_max_task_dispatches_per_batch'],'reset_required':False},
    'recovery':{'status':'NOT_ACTIVE','diagnosis':None,'resolution':None,'verification':None,'resume_authorized':False,'next_task':None,'recovery_baseline':None},
}
cycle['status']='EXECUTION'; cycle['lifecycle_stage']='EXECUTION'; cycle['next_action']='START_VSCODE_PROJECT_MANAGER'
state['project_state']='EXECUTION'
save_state(state); append_transition('PLAN_APPROVED',actor='user:approve_plan',cycle_id=cid,details={'approval_id':approval_id,'execution_version':execution_version,'package_digest':manifest['package_digest'],'task_count':manifest['task_count']})
print('IMPLEMENTATION_APPROVAL: PASS')
print(f'approval_id: {approval_id}')
print(f'execution_version: {execution_version}')
print('Next: start a fresh VS Code ProjectManager500K invocation.')
