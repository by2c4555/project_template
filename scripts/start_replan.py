#!/usr/bin/env python3
"""Start a new Planning Vx inside the same open change cycle after TASK/PLAN defect."""
from copy import deepcopy
from workflow_state import active_cycle, append_transition, load_state, next_id, reset_package_workspace, save_state, utc_now
state=load_state(); cid,cycle=active_cycle(state); ex=cycle.get('execution') or {}; rec=ex.get('recovery') or {}
if rec.get('status')!='REPLAN_REQUIRED': raise SystemExit('START_REPLAN: BLOCKED\nactive diagnosis did not route to replan')
if cycle.get('approval'):
    old_approval=deepcopy(cycle['approval']); old_approval['status']='SUPERSEDED'; cycle.setdefault('approval_history',[]).append(old_approval)
if cycle.get('execution'): cycle.setdefault('execution_history',[]).append(deepcopy(cycle['execution']))
cycle.setdefault('planning_history',[]).append(deepcopy(cycle.get('planning')))
active_issue=cycle.get('active_issue')
if active_issue:
    for issue in cycle.get('issues',[]):
        if issue.get('issue_id')==active_issue:
            issue['status']='ROUTED_TO_REPLAN'
            break
pv=next_id(state,'planning','Planning_V',width=1)
cycle['planning']={'version':pv,'revision':1,'revision_label':'Revision_1','status':'IN_PROGRESS','material_unknowns':None,'package_status':'NOT_COMPILED','task_expansion_allowed':False,'interaction_gate':'NONE','invocation_stop_required':False,'candidate_package_digest':None}
cycle['approval']=None; cycle['execution']=None; cycle['active_issue']=None; reset_package_workspace(pv, 'Revision_1'); cycle['status']='PLANNING'; cycle['lifecycle_stage']='PLANNING'; cycle['next_action']='RUN_CODEX_PLANNING'; state['project_state']='PLANNING'
save_state(state); append_transition('REPLAN_STARTED',actor='python:start_replan',cycle_id=cid,details={'new_planning_version':pv})
print('START_REPLAN: PASS'); print(f'planning_version: {pv}'); print('All prior execution authority is superseded. A new approve_plan.py gate will be required.')
