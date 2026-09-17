#!/usr/bin/env python3
import argparse,json
from _bootstrap import *
from _core.state import load_state,save_state
from _core.paths import ROOT,WORKPLAN
from _core.integrity import sha256_file
from _core.contracts import load_contract_package, normalize_relpath
from _core.mutation import path_authorized
from _core.command import continuation
p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True); sp.add_parser('status'); r=sp.add_parser('register'); r.add_argument('--contract',required=True); a=p.parse_args(); st=load_state(); cid=st.get('active_cycle'); cycle=st['cycles'][cid]
if a.cmd=='status': print('RECOVERY_STATE'); print('stage:',st.get('lifecycle_stage')); raise SystemExit
if st.get('lifecycle_stage')!='RECOVERY': raise SystemExit('RECOVERY: BLOCKED\nwrong stage')
lw=st.get('last_completed_work'); meta=json.loads((WORKPLAN/'work'/lw/'WORK.json').read_text()) if lw else {}
if meta.get('role')!='RECOVERY' or meta.get('status')!='COMPLETED': raise SystemExit('RECOVERY: BLOCKED\ncompleted reasoning-only RECOVERY Work required')
issue=next((x for x in reversed(cycle.get('issues',[])) if x.get('status')=='DIAGNOSED'),None)
if not issue: raise SystemExit('RECOVERY: BLOCKED\nno diagnosed issue')
cp=ROOT/a.contract
if not cp.is_file(): raise SystemExit('RECOVERY: BLOCKED\nRecovery Contract missing')
try: contract=json.loads(cp.read_text(encoding='utf-8'))
except Exception as e: raise SystemExit(f'RECOVERY: BLOCKED\ninvalid Recovery Contract JSON: {e}')
required={'issue_id','task_id','repair_objective','affected_contracts','authorized_paths','required_changes','verification','regression_verification','completion_criteria'}
missing=sorted(required-set(contract))
if missing: raise SystemExit('RECOVERY: BLOCKED\nmissing fields: '+', '.join(missing))
if contract['issue_id']!=issue['issue_id'] or contract['task_id']!=issue.get('task'): raise SystemExit('RECOVERY: BLOCKED\ncontract issue/task mismatch')
ex=cycle.get('execution') or {}; task=issue.get('task')
if not task or task not in ex.get('tasks',{}): raise SystemExit('RECOVERY: BLOCKED\nissue is not bound to an execution task')
package=load_contract_package(validate=True); task_contract=package['tasks'].get(task)
try: recovery_paths=[normalize_relpath(x) for x in contract.get('authorized_paths',[])]
except Exception as e: raise SystemExit(f'RECOVERY: BLOCKED\ninvalid authorized_paths: {e}')
for rel in recovery_paths:
    probe=rel.rstrip('/') + ('/__probe__' if rel.endswith('/') else '')
    if not path_authorized(probe, task_contract.get('authorized_paths',[])):
        raise SystemExit(f'RECOVERY: BLOCKED\nauthorized path expands immutable Task authority: {rel}')
digest=sha256_file(cp); issue.update({'recovery_contract':a.contract,'recovery_contract_digest':digest,'status':'RECOVERY_CONTRACT_READY'})
t=ex['tasks'][task]; t['status']='PENDING'; t['pending_attempt_kind']='RECOVERY'; t['recovery']={
    'issue_id':issue['issue_id'],'contract':a.contract,'contract_digest':digest,'repair_objective':contract['repair_objective'],
    'affected_contracts':contract['affected_contracts'],'authorized_paths':recovery_paths,'required_changes':contract['required_changes'],
    'verification':contract['verification'],'regression_verification':contract['regression_verification'],'completion_criteria':contract['completion_criteria']}
ex['tasks'][task]=t; ex['active_issue']=None; ex['status']='READY'; cycle['execution']=ex
st['active_task']=None; st['active_attempt']=None; st['lifecycle_stage']='EXECUTION'; st['project_state']='EXECUTION'; st['next_action']='EXECUTE_IMPLEMENTATION'; st['cycles'][cid]=cycle
save_state(st,event='RECOVERY_CONTRACT_REGISTERED',actor='tool:recovery',details={'issue':issue['issue_id'],'task':task,'contract_digest':digest}); print('RECOVERY: CONTRACT_READY'); print('continuation:',continuation(load_state()))
