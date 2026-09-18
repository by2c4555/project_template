#!/usr/bin/env python3
import argparse, json
from _bootstrap import *
from _core.state import load_state, save_state, now
from _core.paths import WORKPLAN
from _core.integrity import build_package_manifest
from _core.contracts import load_contract_package
from _core.ingest import revalidate_bound, archive_for_cycle, mark_accepted, normalize_active_ingest
from _core.command import continuation
p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True); sp.add_parser('status'); sp.add_parser('mark-ready'); a=p.parse_args(); st=load_state(); cid=st.get('active_cycle'); cycle=(st.get('cycles') or {}).get(cid,{})
if st.get('lifecycle_stage')=='PLANNING' and cycle.get('ingest'): revalidate_bound(cycle['ingest'])
if a.cmd=='status': print('PLANNING_STATE'); print('cycle:',cid); print('stage:',st.get('lifecycle_stage')); print('planning:',(cycle.get('planning') or {}).get('status')); raise SystemExit
if st.get('lifecycle_stage')!='PLANNING': raise SystemExit('PLANNING: BLOCKED\nnot in PLANNING stage')
lw=st.get('last_completed_work')
if not lw: raise SystemExit('PLANNING: BLOCKED\nno completed Planning Work')
meta=json.loads((WORKPLAN/'work'/lw/'WORK.json').read_text())
if meta.get('role')!='PLANNING' or meta.get('status')!='COMPLETED': raise SystemExit('PLANNING: BLOCKED\nlast completed work is not PLANNING')
try: package=load_contract_package(validate=True)
except Exception as e: raise SystemExit(f'PLANNING: BLOCKED\ncontract validation failed: {e}')
revalidate_bound(cycle['ingest']); manifest=build_package_manifest(); scope=cycle['scope']; archived=archive_for_cycle(cid,cycle['ingest'])
revision_issues=[i for i in cycle.get('issues',[]) if i.get('status')=='PLAN_REVISION_REQUIRED']
for issue in revision_issues:
    previous=issue.get('previous_planning_package_digest')
    if previous and previous == manifest['package_digest']:
        raise SystemExit(f"PLANNING: BLOCKED\n{issue.get('issue_id')} requires a changed Planning Package")
for issue in revision_issues:
    issue['status']='SUPERSEDED'; issue['superseded_at']=now(); issue['superseded_by_planning_digest']=manifest['package_digest']
previous_planning=cycle.get('planning') or {}
previous_revision=previous_planning.get('revision_label') or ''
try: revision_no=int(previous_revision.split('_',1)[1])+1 if previous_revision.startswith('Revision_') else 1
except (ValueError,IndexError): revision_no=1
cycle['ingest']=archived; cycle['planning']={'status':'PLAN_READY','version':f'Planning_V{revision_no}','revision_label':f'Revision_{revision_no}','based_on_scope_revision':scope['revision_label'],'based_on_scope_digest':scope['digest'],'based_on_ingest_digest':archived['package_digest'],'candidate_package_digest':manifest['package_digest'],'task_count':manifest['task_count'],'phase_count':len(package['phases']),'task_digests':manifest['task_digests'],'phase_digests':manifest['phase_digests'],'manifest':manifest}
st['cycles'][cid]=cycle; st['project_state']='PLAN_READY'; st['lifecycle_stage']='PLAN_READY'; st['next_action']='EXECUTE_IMPLEMENTATION'; save_state(st,event='PLAN_READY',actor='tool:planning',details={'package_digest':manifest['package_digest'],'task_count':manifest['task_count'],'phase_count':len(package['phases']),'archive_source':archived['source_root']}); mark_accepted(archived); normalize_active_ingest(); print('PLANNING: PLAN_READY'); print('package_digest:',manifest['package_digest']); print('task_count:',manifest['task_count']); print('phase_count:',len(package['phases'])); print('continuation:',continuation(load_state()))
