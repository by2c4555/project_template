#!/usr/bin/env python3
import argparse,json
from _bootstrap import *
from _core.state import load_state,save_state
from _core.paths import ROOT,WORKPLAN
from _core.integrity import sha256_file
p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True); sp.add_parser('status'); r=sp.add_parser('register'); r.add_argument('--classification',required=True,choices=['IMPLEMENTATION_DEFECT','TASK_DEFECT','PLAN_DEFECT','EVALUATION_DEFECT','SCOPE_AMBIGUITY','EXTERNAL_BLOCKER','UNKNOWN']); r.add_argument('--diagnosis',required=True); a=p.parse_args(); st=load_state(); cid=st.get('active_cycle'); cycle=st['cycles'][cid]
if a.cmd=='status': print('DIAGNOSIS_STATE'); print('stage:',st.get('lifecycle_stage')); print('issues:',len(cycle.get('issues',[]))); raise SystemExit
if st.get('lifecycle_stage')!='DIAGNOSIS': raise SystemExit('DIAGNOSIS: BLOCKED\nwrong stage')
lw=st.get('last_completed_work'); meta=json.loads((WORKPLAN/'work'/lw/'WORK.json').read_text()) if lw else {}
if meta.get('role')!='DIAGNOSIS' or meta.get('status')!='COMPLETED': raise SystemExit('DIAGNOSIS: BLOCKED\ncompleted DIAGNOSIS Work required')
issue=next((x for x in reversed(cycle.get('issues',[])) if x.get('status')=='AWAITING_DIAGNOSIS'),None)
if not issue: raise SystemExit('DIAGNOSIS: BLOCKED\nno active issue')
dp=ROOT/a.diagnosis
if not dp.is_file(): raise SystemExit('DIAGNOSIS: BLOCKED\ndiagnosis artifact missing')
issue.update({'classification':a.classification,'diagnosis':a.diagnosis,'diagnosis_digest':sha256_file(dp),'status':'DIAGNOSED'})
if a.classification=='IMPLEMENTATION_DEFECT': st['lifecycle_stage']='RECOVERY'; st['project_state']='RECOVERY'; st['next_action']='RUN_EXTERNAL_AGENT_RECOVERY'
elif a.classification in {'TASK_DEFECT','PLAN_DEFECT'}: st['lifecycle_stage']='PLANNING'; st['project_state']='PLANNING'; st['next_action']='REPLAN_WITH_BOUND_INGEST'
else: st['next_action']='OWNER_OR_EXTERNAL_RESOLUTION_REQUIRED'
st['cycles'][cid]=cycle; save_state(st,event='DIAGNOSIS_REGISTERED',actor='tool:diagnosis',details={'issue':issue['issue_id'],'classification':a.classification}); print('DIAGNOSIS: REGISTERED'); print('classification:',a.classification)
