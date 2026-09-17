#!/usr/bin/env python3
"""HUMAN/OPERATOR-ONLY resume after verified execution-origin recovery."""
from workflow_state import active_cycle, append_transition, ensure_package_integrity, human_tty_challenge, load_state, save_state
state=load_state(); cid,cycle=active_cycle(state); ex=cycle.get('execution') or {}; rec=ex.get('recovery') or {}; issue_id=cycle.get('active_issue')
if ex.get('status')!='RECOVERY_VERIFIED' or rec.get('status')!='VERIFIED': raise SystemExit('RESUME_EXECUTION: BLOCKED\nrecovery is not VERIFIED')
if rec.get('resume_authorized'): raise SystemExit('RESUME_EXECUTION: BLOCKED\nalready authorized')
if not issue_id: raise SystemExit('RESUME_EXECUTION: BLOCKED\nactive recovered issue missing')
ensure_package_integrity(cycle)
human_tty_challenge('RESUME EXECUTION',[f'Cycle: {cid}',f'Resolved issue: {issue_id}',f'Recovery baseline: {rec.get("recovery_baseline")}'])
issue=next((x for x in cycle.get('issues',[]) if x.get('issue_id')==issue_id),None)
if issue: issue['status']='RESOLVED'
ex['last_resolved_issue']=issue_id; ex['active_issue']=None; rec['resume_authorized']=True; rec['status']='RESUMED'; ex['recovery']=rec; ex['status']='READY_TO_RESUME'; cycle['active_issue']=None; cycle['status']='EXECUTION'; cycle['lifecycle_stage']='EXECUTION'; cycle['next_action']='START_FRESH_VSCODE_PROJECT_MANAGER'; state['project_state']='EXECUTION'
save_state(state); append_transition('EXECUTION_RESUME_AUTHORIZED',actor='user:resume_execution',cycle_id=cid,details={'issue':issue_id})
print('RESUME_EXECUTION: PASS'); print('execution_status: READY_TO_RESUME'); print('Start a fresh ProjectManager500K invocation and continue from machine state.')
