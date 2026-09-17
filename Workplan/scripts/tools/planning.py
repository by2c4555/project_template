#!/usr/bin/env python3
import argparse,json
from _bootstrap import *
from _core.state import load_state,save_state
from _core.paths import WORKPLAN
from _core.integrity import build_package_manifest
from _core import work as W
p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True); sp.add_parser('status'); m=sp.add_parser('mark-ready'); a=p.parse_args(); st=load_state(); cid=st.get('active_cycle'); cycle=(st.get('cycles') or {}).get(cid,{})
if a.cmd=='status':
    print('PLANNING_STATE'); print('cycle:',cid); print('stage:',st.get('lifecycle_stage')); print('planning:',(cycle.get('planning') or {}).get('status')); raise SystemExit
if st.get('lifecycle_stage')!='PLANNING': raise SystemExit('PLANNING: BLOCKED\nnot in PLANNING stage')
# Planning Work must already be completed.
lw=st.get('last_completed_work')
if not lw: raise SystemExit('PLANNING: BLOCKED\nno completed Planning Work')
meta=json.loads((WORKPLAN/'work'/lw/'WORK.json').read_text())
if meta.get('role')!='PLANNING' or meta.get('status')!='COMPLETED': raise SystemExit('PLANNING: BLOCKED\nlast completed work is not PLANNING')
manifest=build_package_manifest(); scope=cycle['scope']
cycle['planning']={'status':'PLAN_READY','version':'Planning_V1','revision_label':'Revision_1','based_on_scope_revision':scope['revision_label'],'based_on_scope_digest':scope['digest'],'candidate_package_digest':manifest['package_digest'],'task_count':manifest['task_count'],'manifest':manifest}
st['cycles'][cid]=cycle; st['project_state']='PLAN_READY'; st['lifecycle_stage']='PLAN_READY'; st['next_action']='START_EXECUTION_WHEN_RISK_POLICY_ALLOWS'
save_state(st,event='PLAN_READY',actor='tool:planning',details={'package_digest':manifest['package_digest'],'task_count':manifest['task_count']})
print('PLANNING: PLAN_READY'); print('package_digest:',manifest['package_digest']); print('task_count:',manifest['task_count'])
