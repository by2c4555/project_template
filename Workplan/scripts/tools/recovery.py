#!/usr/bin/env python3
import argparse,json
from _bootstrap import *
from _core.state import load_state,save_state
from _core.paths import ROOT,WORKPLAN
from _core.integrity import sha256_file
from _core.command import continuation
p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True); sp.add_parser('status'); v=sp.add_parser('verify'); v.add_argument('--resolution',required=True); v.add_argument('--baseline',required=True); a=p.parse_args(); st=load_state(); cid=st.get('active_cycle'); cycle=st['cycles'][cid]
if a.cmd=='status': print('RECOVERY_STATE'); print('stage:',st.get('lifecycle_stage')); raise SystemExit
if st.get('lifecycle_stage')!='RECOVERY': raise SystemExit('RECOVERY: BLOCKED\nwrong stage')
lw=st.get('last_completed_work'); meta=json.loads((WORKPLAN/'work'/lw/'WORK.json').read_text()) if lw else {}
if meta.get('role')!='RECOVERY' or meta.get('status')!='COMPLETED': raise SystemExit('RECOVERY: BLOCKED\ncompleted RECOVERY Work required')
issue=next((x for x in reversed(cycle.get('issues',[])) if x.get('classification')=='IMPLEMENTATION_DEFECT' and x.get('status')=='DIAGNOSED'),None)
if not issue: raise SystemExit('RECOVERY: BLOCKED\nno diagnosed implementation defect')
rp=ROOT/a.resolution
if not rp.is_file(): raise SystemExit('RECOVERY: BLOCKED\nresolution missing')
issue.update({'status':'RESOLVED','resolution':a.resolution,'resolution_digest':sha256_file(rp),'recovery_baseline':a.baseline})
ex=cycle.get('execution') or {}; task=issue.get('task')
if task and task in ex.get('tasks',{}): ex['tasks'][task]['status']='PASS_RECOVERED'; ex['active_issue']=None; ex['status']='READY'; cycle['execution']=ex; st['lifecycle_stage']='EXECUTION'; st['project_state']='EXECUTION'; st['next_action']='EXECUTE_IMPLEMENTATION'
else: st['lifecycle_stage']='EVALUATION'; st['project_state']='EVALUATION'; st['next_action']='EXECUTE_EVALUATION'
st['cycles'][cid]=cycle; save_state(st,event='RECOVERY_VERIFIED',actor='tool:recovery',details={'issue':issue['issue_id'],'baseline':a.baseline}); print('RECOVERY: VERIFIED'); print('continuation:',continuation(load_state()))
