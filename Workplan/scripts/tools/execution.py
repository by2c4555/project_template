#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from _bootstrap import *
from _core.state import load_state,save_state,next_id,now
from _core.paths import WORKPLAN,ROOT
from _core.integrity import build_package_manifest,sha256_file
from _core.approval import create_pending
p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
sp.add_parser('status'); sp.add_parser('start')
b=sp.add_parser('begin'); b.add_argument('task')
c=sp.add_parser('complete'); c.add_argument('task'); c.add_argument('--evidence',required=True)
f=sp.add_parser('fail'); f.add_argument('task'); f.add_argument('--reason',required=True)
sp.add_parser('finalize')
a=p.parse_args(); st=load_state(); cid=st.get('active_cycle'); cycle=(st.get('cycles') or {}).get(cid,{})
def package_ok():
    pl=cycle.get('planning') or {}; cur=build_package_manifest(); return pl.get('candidate_package_digest')==cur['package_digest'],cur
if a.cmd=='status':
    ex=cycle.get('execution') or {}; print('EXECUTION_STATE'); print('status:',ex.get('status')); print('active_task:',st.get('active_task')); raise SystemExit
if a.cmd=='start':
    if st.get('lifecycle_stage')!='PLAN_READY': raise SystemExit('EXECUTION: BLOCKED\nPLAN_READY required')
    ok,man=package_ok()
    if not ok: raise SystemExit('EXECUTION: BLOCKED\npackage changed after PLAN_READY')
    # >3 tasks is a material new cost envelope unless matching latest human grant exists.
    subject=man['package_digest']; grant=st.get('last_granted_approval') or {}
    if man['task_count']>3 and not (grant.get('requested_action')=='START_EXECUTION' and grant.get('subject')==subject):
        if not st.get('pending_approval'):
            rec=create_pending('NEW_COST_ENVELOPE','START_EXECUTION',subject); print('EXECUTION: HUMAN_APPROVAL_REQUIRED'); print('id:',rec['approval_id']); print('challenge:',rec['challenge']); raise SystemExit(2)
        raise SystemExit('EXECUTION: BLOCKED\npending approval exists')
    tasks={}
    for fp in sorted((WORKPLAN/'tasks').glob('TASK_*.md')):
        if fp.name in {'TASK_INDEX.md','TASK_TEMPLATE.md'}: continue
        tasks[fp.stem]={'status':'PENDING','contract':str(fp.relative_to(ROOT)).replace('\\','/'),'evidence':None,'repair_attempts':0}
    ex={'version':next_id(st,'execution','Execution_V',1),'status':'READY','package_digest':man['package_digest'],'tasks':tasks,'active_issue':None}
    cycle['execution']=ex; cycle['status']='EXECUTION'; st['cycles'][cid]=cycle; st['project_state']='EXECUTION'; st['lifecycle_stage']='EXECUTION'; st['next_action']='RUN_EXECUTION_MANAGER'
    save_state(st,event='EXECUTION_STARTED',actor='tool:execution',details={'task_count':len(tasks),'package_digest':man['package_digest']}); print('EXECUTION: READY'); raise SystemExit
ex=cycle.get('execution') or {}
if st.get('lifecycle_stage')!='EXECUTION': raise SystemExit('EXECUTION: BLOCKED\nnot in EXECUTION stage')
ok,man=package_ok()
if not ok or man['package_digest']!=ex.get('package_digest'): raise SystemExit('EXECUTION: BLOCKED\npackage integrity failed')
if a.cmd=='begin':
    if st.get('active_task'): raise SystemExit('EXECUTION: BLOCKED\nanother task is active')
    t=ex.get('tasks',{}).get(a.task)
    if not t or t['status']!='PENDING': raise SystemExit('EXECUTION: BLOCKED\ntask is not PENDING')
    t['status']='IN_PROGRESS'; ex['tasks'][a.task]=t; st['active_task']=a.task; cycle['execution']=ex; st['cycles'][cid]=cycle; save_state(st,event='TASK_BEGIN',actor='tool:execution',details={'task':a.task}); print('TASK_BEGIN: PASS'); raise SystemExit
if a.cmd=='complete':
    if st.get('active_task')!=a.task: raise SystemExit('EXECUTION: BLOCKED\nnot active task')
    ep=ROOT/a.evidence
    if not ep.is_file(): raise SystemExit('EXECUTION: BLOCKED\nevidence missing')
    t=ex['tasks'][a.task]; t['status']='PASS'; t['evidence']=a.evidence; t['evidence_sha256']=sha256_file(ep); ex['tasks'][a.task]=t; st['active_task']=None; cycle['execution']=ex; st['cycles'][cid]=cycle; save_state(st,event='TASK_PASS',actor='tool:execution',details={'task':a.task}); print('TASK_COMPLETE: PASS'); raise SystemExit
if a.cmd=='fail':
    if st.get('active_task')!=a.task: raise SystemExit('EXECUTION: BLOCKED\nnot active task')
    issue=next_id(st,'issue','ISSUE_'); iid=issue; rec={'issue_id':iid,'origin_type':'EXECUTION','task':a.task,'reason':a.reason,'status':'AWAITING_DIAGNOSIS','classification':None,'created_at':now()}; cycle.setdefault('issues',[]).append(rec); ex['active_issue']=iid; ex['status']='PAUSED_FOR_DIAGNOSIS'; cycle['execution']=ex; st['cycles'][cid]=cycle; st['active_task']=None; st['project_state']='DIAGNOSIS'; st['lifecycle_stage']='DIAGNOSIS'; st['next_action']='RUN_EXTERNAL_AGENT_DIAGNOSIS'; save_state(st,event='TASK_FAILED',actor='tool:execution',details={'task':a.task,'issue':iid}); print('TASK_FAIL: REGISTERED'); print('issue:',iid); raise SystemExit
if a.cmd=='finalize':
    incomplete=[k for k,v in ex.get('tasks',{}).items() if v.get('status') not in {'PASS','PASS_RECOVERED'}]
    if incomplete: raise SystemExit('EXECUTION: BLOCKED\nincomplete: '+', '.join(incomplete))
    ex['status']='COMPLETE'; cycle['execution']=ex; cycle['status']='EVALUATION'; st['cycles'][cid]=cycle; st['project_state']='EVALUATION'; st['lifecycle_stage']='EVALUATION'; st['next_action']='RUN_EXTERNAL_AGENT_EVALUATION'; save_state(st,event='EXECUTION_COMPLETE',actor='tool:execution'); print('EXECUTION_COMPLETE: PASS')
