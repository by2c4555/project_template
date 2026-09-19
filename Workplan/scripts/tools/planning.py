#!/usr/bin/env python3
import argparse, json
from _bootstrap import *
from _core.state import load_state, save_state, now
from _core.paths import WORKPLAN
from _core.integrity import build_package_manifest
from _core.contracts import load_contract_package
from _core.approval import create_pending, grant_matches, consume_grant
from _core.command import continuation
p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True); sp.add_parser('status'); fs=sp.add_parser('finalize-scope'); fs.add_argument('--summary',required=True); sp.add_parser('mark-ready'); sp.add_parser('request-execution-approval'); sp.add_parser('accept-execution'); a=p.parse_args(); st=load_state(); cid=st.get('active_cycle'); cycle=(st.get('cycles') or {}).get(cid,{})
if a.cmd=='status': print('PLANNING_STATE'); print('cycle:',cid); print('stage:',st.get('lifecycle_stage')); print('planning:',(cycle.get('planning') or {}).get('status')); raise SystemExit
if a.cmd=='finalize-scope':
    if st.get('lifecycle_stage')!='PLANNING_A': raise SystemExit('PLANNING_A: BLOCKED\nwrong stage')
    lw=st.get('last_completed_work'); meta=json.loads((WORKPLAN/'work'/lw/'WORK.json').read_text()) if lw else {}
    if meta.get('role')!='PLANNING' or meta.get('status')!='COMPLETED': raise SystemExit('PLANNING_A: BLOCKED\ncompleted Planning A Work required')
    rid=st.get('active_research_revision'); rev=(st.get('research_revisions') or {}).get(rid)
    if not rev: raise SystemExit('PLANNING_A: BLOCKED\nResearch revision missing')
    # Scope finalization binds exact archived evidence; a Planning A agent may
    # propose wording but cannot add authority beyond the archived handoff.
    scope={'revision_label':'SCOPE_001','digest':rev['ingest']['scope_digest'],'research_revision_id':rid,'summary':a.summary,'files':rev['ingest']['logical_files'],'finalized_at':now()}
    rev['scope_candidate']=scope; rev['status']='SCOPE_APPROVAL'; st['research_revisions'][rid]=rev; st['planning_a']={'research_revision_id':rid,'status':'FINALIZED','scope_digest':scope['digest']}; st['project_state']='SCOPE_APPROVAL'; st['lifecycle_stage']='SCOPE_APPROVAL'; st['next_action']='REQUEST_SCOPE_APPROVAL'; save_state(st,event='SCOPE_FINALIZED',actor='tool:planning',details={'research_revision':rid,'scope_digest':scope['digest']}); print('PLANNING_A: SCOPE_FINALIZED'); raise SystemExit
if a.cmd=='request-execution-approval':
    if st.get('lifecycle_stage')!='EXECUTION_APPROVAL': raise SystemExit('EXECUTION_APPROVAL: BLOCKED\nvalidated planning package required')
    subject=f"EXECUTION:{cid}:{(cycle.get('planning') or {}).get('candidate_package_digest','')}"
    rec=create_pending('EXECUTION_APPROVAL','ACCEPT_EXECUTION',subject); print('EXECUTION_APPROVAL: REQUIRED'); print('id:',rec['approval_id']); print('challenge:',rec['challenge']); raise SystemExit(2)
if a.cmd=='accept-execution':
    subject=f"EXECUTION:{cid}:{(cycle.get('planning') or {}).get('candidate_package_digest','')}"
    if st.get('lifecycle_stage')!='EXECUTION_APPROVAL' or not grant_matches(st,'ACCEPT_EXECUTION',subject): raise SystemExit('EXECUTION_APPROVAL: BLOCKED\ncurrent bound approval required')
    cycle['planning']['status']='PLAN_READY'; cycle.setdefault('approval',{})['execution_approval_subject']=subject; st['cycles'][cid]=cycle; st['project_state']='PLAN_READY'; st['lifecycle_stage']='PLAN_READY'; st['next_action']='EXECUTE_IMPLEMENTATION'; consume_grant(st,'ACCEPT_EXECUTION',subject); save_state(st,event='EXECUTION_APPROVAL_CONSUMED',actor='tool:planning',details={'cycle_id':cid,'package_digest':cycle['planning']['candidate_package_digest']}); print('PLAN_READY: PASS'); raise SystemExit
if st.get('lifecycle_stage') not in {'PLANNING_B'}: raise SystemExit('PLANNING_B: BLOCKED\nnot in Planning B stage')
lw=st.get('last_completed_work')
if not lw: raise SystemExit('PLANNING: BLOCKED\nno completed Planning Work')
meta=json.loads((WORKPLAN/'work'/lw/'WORK.json').read_text())
if meta.get('role')!='PLANNING' or meta.get('status')!='COMPLETED': raise SystemExit('PLANNING: BLOCKED\nlast completed work is not PLANNING')
try: package=load_contract_package(validate=True)
except Exception as e: raise SystemExit(f'PLANNING: BLOCKED\ncontract validation failed: {e}')
manifest=build_package_manifest(); scope=cycle['scope']
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
cycle['planning']={'status':'EXECUTION_APPROVAL_REQUIRED','version':f'Planning_V{revision_no}','revision_label':f'Revision_{revision_no}','based_on_scope_revision':scope['revision_label'],'based_on_scope_digest':scope['digest'],'based_on_ingest_digest':cycle['ingest']['package_digest'],'candidate_package_digest':manifest['package_digest'],'task_count':manifest['task_count'],'phase_count':len(package['phases']),'task_digests':manifest['task_digests'],'phase_digests':manifest['phase_digests'],'manifest':manifest}
st['cycles'][cid]=cycle; st['project_state']='EXECUTION_APPROVAL'; st['lifecycle_stage']='EXECUTION_APPROVAL'; st['next_action']='REQUEST_EXECUTION_APPROVAL'; save_state(st,event='PLANNING_PACKAGE_VALIDATED',actor='tool:planning',details={'package_digest':manifest['package_digest'],'task_count':manifest['task_count'],'phase_count':len(package['phases'])}); print('PLANNING: EXECUTION_APPROVAL_REQUIRED')
