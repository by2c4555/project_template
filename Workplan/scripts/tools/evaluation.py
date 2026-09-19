#!/usr/bin/env python3
import argparse,json
from _bootstrap import *
from _core.state import load_state,save_state,next_id,now
from _core.paths import ROOT,WORKPLAN
from _core.integrity import sha256_file
from _core.command import continuation
p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True); sp.add_parser('status'); f=sp.add_parser('finalize'); f.add_argument('--result',required=True,choices=['PASS','PASS_WITH_FINDINGS','DIAGNOSIS_REQUIRED']); f.add_argument('--report',required=True); f.add_argument('--completion-report'); a=p.parse_args(); st=load_state(); cid=st.get('active_cycle'); cycle=st['cycles'][cid]
if a.cmd=='status': print('EVALUATION_STATE'); print('stage:',st.get('lifecycle_stage')); print('cycle:',cid); raise SystemExit
if st.get('lifecycle_stage')!='EVALUATION': raise SystemExit('EVALUATION: BLOCKED\nwrong stage')
lw=st.get('last_completed_work'); meta=json.loads((WORKPLAN/'work'/lw/'WORK.json').read_text()) if lw else {}
if meta.get('role')!='EVALUATION' or meta.get('status')!='COMPLETED': raise SystemExit('EVALUATION: BLOCKED\ncompleted EVALUATION Work required')
rp=ROOT/a.report
if not rp.is_file(): raise SystemExit('EVALUATION: BLOCKED\nreport missing')
rec={'version':next_id(st,'evaluation','Evaluation_V',1),'result':a.result,'report':a.report,'report_digest':sha256_file(rp),'created_at':now()}; cycle.setdefault('evaluation',{}).setdefault('attempts',[]).append(rec)
if a.result=='DIAGNOSIS_REQUIRED':
    iid=next_id(st,'issue','ISSUE_'); cycle.setdefault('issues',[]).append({'issue_id':iid,'origin_type':'EVALUATION','reason':'blocking evaluation finding','status':'AWAITING_DIAGNOSIS','classification':None,'created_at':now()}); st['lifecycle_stage']='DIAGNOSIS'; st['project_state']='DIAGNOSIS'; st['next_action']='EXECUTE_DIAGNOSIS'; rec['issue_id']=iid
else:
    if not a.completion_report: raise SystemExit('EVALUATION: BLOCKED\ncompletion report required for PASS')
    cp=ROOT/a.completion_report
    if not cp.is_file(): raise SystemExit('EVALUATION: BLOCKED\ncompletion report missing')
    txt=cp.read_text(); scope=cycle['scope']
    if scope['revision_label'] not in txt or scope['digest'] not in txt: raise SystemExit('EVALUATION: BLOCKED\ncompletion report must contain exact scope revision and digest')
    rec['completion_report']=a.completion_report; rec['completion_digest']=sha256_file(cp); cycle['status']='CLOSED_VALIDATED'; st['project_state']='CLOSED_VALIDATED'; st['lifecycle_stage']='CLOSED_VALIDATED'; st['next_action']=None
st['cycles'][cid]=cycle; save_state(st,event='EVALUATION_FINALIZED',actor='tool:evaluation',details={'result':a.result,'evaluation':rec['version']}); print('EVALUATION:',a.result); print('continuation:',continuation(load_state()))
