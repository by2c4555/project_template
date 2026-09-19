#!/usr/bin/env python3
import argparse, shutil
from _bootstrap import *
from _core.state import load_state,save_state,next_id,now
from _core.paths import ROOT,ARCHIVE_DIR
from _core.ingest import validate,_physical_for,clear_exact_consumed,revalidate_bound
from _core.approval import create_pending,grant_matches,consume_grant
from _core.command import continuation
p=argparse.ArgumentParser(); p.add_argument('cmd',choices=['status','import','request-approval','accept','reject']); a=p.parse_args(); st=load_state()
if a.cmd=='status': print('SCOPE_STATE'); print('active_cycle:',st.get('active_cycle')); print('research_revision:',st.get('active_research_revision')); print('stage:',st.get('lifecycle_stage')); raise SystemExit
if a.cmd=='import':
    if st.get('active_cycle') and st.get('project_state')!='CLOSED_VALIDATED': raise SystemExit('RESEARCH_IMPORT: BLOCKED\nactive non-closed Cycle exists')
    if st.get('lifecycle_stage') not in {'BOOTSTRAP','CLOSED_VALIDATED','AWAITING_RESEARCH','RESEARCH_REVISION_REQUIRED'}: raise SystemExit('RESEARCH_IMPORT: BLOCKED\nwrong stage')
    r=validate(); rid=next_id(st,'research_revision','RESEARCH_'); dst=ARCHIVE_DIR/'research'/rid/r['ingest_id']
    for row in r['logical_files']:
        src=_physical_for(row['path'],ROOT/r['source_root']); out=dst/row['path']; out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,out)
    archived=dict(r); archived['source_root']=str(dst.relative_to(ROOT)).replace('\\','/'); revalidate_bound(archived); cleanup=clear_exact_consumed(r)
    st.setdefault('research_revisions',{})[rid]={'research_revision_id':rid,'predecessor':st.get('active_research_revision'),'status':'PLANNING_A','ingest':archived,'archive_digest':r['package_digest'],'imported_at':now(),'cleanup':cleanup,'findings':[],'scope_candidate':None}
    st['active_research_revision']=rid; st['active_cycle']=None; st['planning_a']={'research_revision_id':rid,'status':'REQUIRED'}; st['project_state']='PLANNING_A'; st['lifecycle_stage']='PLANNING_A'; st['next_action']='EXECUTE_PLANNING'; save_state(st,event='RESEARCH_IMPORTED_ARCHIVED',actor='tool:scope',details={'research_revision':rid,'ingest_id':r['ingest_id'],'cleanup':cleanup})
    print('RESEARCH_IMPORT: PASS'); print('research_revision:',rid); print('continuation:',continuation(load_state())); raise SystemExit
rid=st.get('active_research_revision'); revision=(st.get('research_revisions') or {}).get(rid)
if not revision: raise SystemExit('SCOPE: BLOCKED\nno active Research revision')
candidate=revision.get('scope_candidate') or {}; subject=f"SCOPE:{rid}:{candidate.get('digest','NO_FINAL_SCOPE')}"
if a.cmd=='request-approval':
    if st.get('lifecycle_stage')!='SCOPE_APPROVAL' or not candidate.get('digest'): raise SystemExit('SCOPE_APPROVAL: BLOCKED\nfinalized Scope required')
    rec=create_pending('SCOPE_APPROVAL','ACCEPT_SCOPE',subject); print('SCOPE_APPROVAL: REQUIRED'); print('id:',rec['approval_id']); print('challenge:',rec['challenge']); raise SystemExit(2)
if a.cmd=='accept':
    if st.get('lifecycle_stage')!='SCOPE_APPROVAL' or not grant_matches(st,'ACCEPT_SCOPE',subject): raise SystemExit('SCOPE_APPROVAL: BLOCKED\ncurrent bound approval required')
    cid=next_id(st,'cycle','CYCLE_'); scope=dict(candidate); scope['accepted_at']=now(); st['cycles'][cid]={'cycle_id':cid,'status':'PLANNING_B','research_revision_id':rid,'ingest':revision['ingest'],'scope':scope,'planning':None,'approval':{'scope_approval_subject':subject},'execution':None,'issues':[],'evaluation':{'attempts':[]},'created_at':now()}
    st['active_cycle']=cid; st['planning_a']['status']='ACCEPTED'; revision['status']='ACCEPTED_SCOPE'; st['research_revisions'][rid]=revision; st['project_state']='PLANNING_B'; st['lifecycle_stage']='PLANNING_B'; st['next_action']='EXECUTE_PLANNING'; consume_grant(st,'ACCEPT_SCOPE',subject); save_state(st,event='SCOPE_APPROVAL_CONSUMED',actor='tool:scope',details={'cycle_id':cid,'research_revision':rid,'scope_digest':scope['digest']}); print('SCOPE_ACCEPTED:',cid); print('continuation:',continuation(load_state())); raise SystemExit
if a.cmd=='reject':
    revision['status']='RESEARCH_REVISION_REQUIRED'; st['research_revisions'][rid]=revision; st['project_state']='RESEARCH_REVISION_REQUIRED'; st['lifecycle_stage']='RESEARCH_REVISION_REQUIRED'; st['next_action']='EXECUTE_RESEARCH'; save_state(st,event='SCOPE_REJECTED',actor='human:scope',details={'research_revision':rid}); print('SCOPE_REJECTED: PASS')
