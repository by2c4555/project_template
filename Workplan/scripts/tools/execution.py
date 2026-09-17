#!/usr/bin/env python3
import argparse,json,re
from _bootstrap import *
from _core.state import load_state,save_state,next_id,now
from _core.paths import WORKPLAN,ROOT
from _core.integrity import build_package_manifest,sha256_file,field,inline_list
from _core.approval import create_pending
from _core import work as W

def task_meta(fp):
    text=fp.read_text(encoding='utf-8')
    return {'status':'PENDING','contract':str(fp.relative_to(ROOT)).replace('\\','/'),'evidence':None,'repair_attempts':0,'max_repairs':int(field(text,'max_repairs') or 2),'depends_on':inline_list(text,'depends_on')}

def load():
    st=load_state(); cid=st.get('active_cycle'); return st,cid,(st.get('cycles') or {}).get(cid,{})

def package_ok(cycle):
    pl=cycle.get('planning') or {}; cur=build_package_manifest(); return pl.get('candidate_package_digest')==cur['package_digest'],cur

def eligible_task(ex):
    for tid,t in ex.get('tasks',{}).items():
        if t.get('status')!='PENDING': continue
        deps=t.get('depends_on') or []
        if all(ex['tasks'].get(d,{}).get('status') in {'PASS','PASS_RECOVERED'} for d in deps): return tid
    return None

def route(st,cycle):
    if st.get('pending_approval'): return {'action':'HUMAN_APPROVAL_REQUIRED','approval_id':st['pending_approval']['approval_id']}
    stage=st.get('lifecycle_stage')
    if stage=='PLAN_READY': return {'action':'START_EXECUTION'}
    if stage=='DIAGNOSIS': return {'action':'START_DIAGNOSIS'}
    if stage=='RECOVERY': return {'action':'START_RECOVERY'}
    if stage=='EVALUATION': return {'action':'START_EVALUATION'}
    if stage=='CLOSED_VALIDATED': return {'action':'DONE'}
    if stage!='EXECUTION': return {'action':'BLOCKED','reason':stage}
    ex=cycle.get('execution') or {}
    if ex.get('active_issue'): return {'action':'START_DIAGNOSIS','issue':ex['active_issue']}
    if st.get('active_task'):
        meta=W.status(); rec=W.reconcile(meta) if meta else {'status':'RESTART_ACTIVE_UNIT','changed':[]}
        return {'action':'RECONCILE_TASK' if rec['status']!='CLEAN' else 'RESUME_TASK','task':st['active_task'],'reconciliation':rec}
    tid=eligible_task(ex)
    if tid: return {'action':'DISPATCH_TASK','task':tid,'contract':ex['tasks'][tid]['contract']}
    incomplete=[k for k,v in ex.get('tasks',{}).items() if v.get('status') not in {'PASS','PASS_RECOVERED'}]
    if incomplete: return {'action':'BLOCKED','reason':'NO_ELIGIBLE_TASK','incomplete':incomplete}
    return {'action':'START_EVALUATION'}

p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
sp.add_parser('status'); sp.add_parser('next'); sp.add_parser('start'); sp.add_parser('dispatch'); sp.add_parser('resume')
c=sp.add_parser('complete'); c.add_argument('--evidence',required=True)
f=sp.add_parser('fail'); f.add_argument('--reason',required=True)
sp.add_parser('repair'); sp.add_parser('finalize')
a=p.parse_args(); st,cid,cycle=load()
if a.cmd=='status': print('EXECUTION_STATE'); print('route:',route(st,cycle)); raise SystemExit
if a.cmd=='next': print('EXECUTION_NEXT'); print(json.dumps(route(st,cycle),sort_keys=True)); raise SystemExit
if a.cmd=='start':
    if st.get('lifecycle_stage')!='PLAN_READY': raise SystemExit('EXECUTION: BLOCKED\nPLAN_READY required')
    ok,man=package_ok(cycle)
    if not ok: raise SystemExit('EXECUTION: BLOCKED\npackage changed after PLAN_READY')
    subject=man['package_digest']; grant=st.get('last_granted_approval') or {}
    if man['task_count']>3 and not (grant.get('requested_action')=='START_EXECUTION' and grant.get('subject')==subject):
        if not st.get('pending_approval'):
            rec=create_pending('NEW_COST_ENVELOPE','START_EXECUTION',subject); print('EXECUTION: HUMAN_APPROVAL_REQUIRED'); print('id:',rec['approval_id']); print('challenge:',rec['challenge']); raise SystemExit(2)
        raise SystemExit('EXECUTION: BLOCKED\npending approval exists')
    tasks={}
    for fp in sorted((WORKPLAN/'tasks').glob('TASK_*.md')):
        if fp.name in {'TASK_INDEX.md','TASK_TEMPLATE.md'}: continue
        tasks[fp.stem]=task_meta(fp)
    cycle['execution']={'version':next_id(st,'execution','Execution_V',1),'status':'READY','package_digest':man['package_digest'],'tasks':tasks,'active_issue':None}; cycle['status']='EXECUTION'; st['cycles'][cid]=cycle; st['project_state']='EXECUTION'; st['lifecycle_stage']='EXECUTION'; st['next_action']='RUN_EXECUTION_MANAGER'; save_state(st,event='EXECUTION_STARTED',actor='tool:execution',details={'task_count':len(tasks),'package_digest':man['package_digest']}); print('EXECUTION: READY'); raise SystemExit
ex=cycle.get('execution') or {}
if st.get('lifecycle_stage')!='EXECUTION': raise SystemExit('EXECUTION: BLOCKED\nnot in EXECUTION stage')
ok,man=package_ok(cycle)
if not ok or man['package_digest']!=ex.get('package_digest'): raise SystemExit('EXECUTION: BLOCKED\npackage integrity failed')
if a.cmd=='dispatch':
    if st.get('active_task'): raise SystemExit('EXECUTION: BLOCKED\nactive task exists')
    tid=eligible_task(ex)
    if not tid: raise SystemExit('EXECUTION: BLOCKED\nno eligible task')
    ex['tasks'][tid]['status']='IN_PROGRESS'; st['active_task']=tid; cycle['execution']=ex; st['cycles'][cid]=cycle; save_state(st,event='TASK_DISPATCHED',actor='tool:execution',details={'task':tid})
    mode,meta,ticket=W.acquire('BUILDER','vscode','Builder100K',tid); print('TASK_DISPATCH: PASS'); print('task:',tid); print('ticket:',json.dumps(ticket,sort_keys=True)); raise SystemExit
if a.cmd=='resume':
    tid=st.get('active_task')
    if not tid: raise SystemExit('EXECUTION: BLOCKED\nno active task')
    mode,meta,ticket=W.acquire('BUILDER','vscode','Builder100K',tid); print('TASK_RESUME:',mode); print('task:',tid); print('ticket:',json.dumps(ticket,sort_keys=True)); raise SystemExit
if a.cmd=='repair':
    tid=st.get('active_task'); t=ex.get('tasks',{}).get(tid)
    if not tid or not t: raise SystemExit('EXECUTION: BLOCKED\nno active task')
    if int(t.get('repair_attempts',0))>=int(t.get('max_repairs',2)):
        iid=next_id(st,'issue','ISSUE_'); cycle.setdefault('issues',[]).append({'issue_id':iid,'origin_type':'EXECUTION','task':tid,'reason':'bounded local repair limit exceeded','status':'AWAITING_DIAGNOSIS','classification':None,'created_at':now()}); ex['active_issue']=iid; ex['status']='PAUSED_FOR_DIAGNOSIS'; st['active_task']=None; st['active_work']=None; st['lifecycle_stage']='DIAGNOSIS'; st['project_state']='DIAGNOSIS'; st['next_action']='RUN_EXTERNAL_AGENT_DIAGNOSIS'; cycle['execution']=ex; st['cycles'][cid]=cycle; save_state(st,event='REPAIR_LIMIT_EXCEEDED',actor='tool:execution',details={'task':tid,'issue':iid}); print('REPAIR: DIAGNOSIS_REQUIRED'); raise SystemExit(2)
    t['repair_attempts']=int(t.get('repair_attempts',0))+1; ex['tasks'][tid]=t; cycle['execution']=ex; st['cycles'][cid]=cycle; save_state(st,event='LOCAL_REPAIR_GRANTED',actor='tool:execution',details={'task':tid,'attempt':t['repair_attempts']}); print('REPAIR: ALLOWED'); print('attempt:',t['repair_attempts']); raise SystemExit
if a.cmd=='complete':
    tid=st.get('active_task')
    if not tid: raise SystemExit('EXECUTION: BLOCKED\nno active task')
    lw=st.get('last_completed_work'); meta=json.loads((WORKPLAN/'work'/lw/'WORK.json').read_text()) if lw else {}
    if meta.get('role')!='BUILDER' or meta.get('task_id')!=tid or meta.get('status')!='COMPLETED': raise SystemExit('EXECUTION: BLOCKED\ncompleted Builder Work required')
    ep=ROOT/a.evidence
    if not ep.is_file(): raise SystemExit('EXECUTION: BLOCKED\nevidence missing')
    t=ex['tasks'][tid]; t['status']='PASS'; t['evidence']=a.evidence; t['evidence_sha256']=sha256_file(ep); ex['tasks'][tid]=t; st['active_task']=None; cycle['execution']=ex; st['cycles'][cid]=cycle; save_state(st,event='TASK_PASS',actor='tool:execution',details={'task':tid}); print('TASK_COMPLETE: PASS'); raise SystemExit
if a.cmd=='fail':
    tid=st.get('active_task')
    if not tid: raise SystemExit('EXECUTION: BLOCKED\nno active task')
    iid=next_id(st,'issue','ISSUE_'); cycle.setdefault('issues',[]).append({'issue_id':iid,'origin_type':'EXECUTION','task':tid,'reason':a.reason,'status':'AWAITING_DIAGNOSIS','classification':None,'created_at':now()}); ex['active_issue']=iid; ex['status']='PAUSED_FOR_DIAGNOSIS'; cycle['execution']=ex; st['active_task']=None; st['active_work']=None; st['cycles'][cid]=cycle; st['project_state']='DIAGNOSIS'; st['lifecycle_stage']='DIAGNOSIS'; st['next_action']='RUN_EXTERNAL_AGENT_DIAGNOSIS'; save_state(st,event='TASK_FAILED',actor='tool:execution',details={'task':tid,'issue':iid}); print('TASK_FAIL: REGISTERED'); print('issue:',iid); raise SystemExit
if a.cmd=='finalize':
    incomplete=[k for k,v in ex.get('tasks',{}).items() if v.get('status') not in {'PASS','PASS_RECOVERED'}]
    if incomplete: raise SystemExit('EXECUTION: BLOCKED\nincomplete: '+', '.join(incomplete))
    ex['status']='COMPLETE'; cycle['execution']=ex; cycle['status']='EVALUATION'; st['cycles'][cid]=cycle; st['project_state']='EVALUATION'; st['lifecycle_stage']='EVALUATION'; st['next_action']='RUN_EXTERNAL_AGENT_EVALUATION'; save_state(st,event='EXECUTION_COMPLETE',actor='tool:execution'); print('EXECUTION_COMPLETE: PASS')
