#!/usr/bin/env python3
import argparse, shutil
from _bootstrap import *
from _core.state import load_state,save_state,next_id,now
from _core.paths import ROOT,WORKPLAN
from _core.ingest import validate,_physical_for
from _core.command import continuation
p=argparse.ArgumentParser(); p.add_argument('cmd',choices=['status','import']); a=p.parse_args(); st=load_state()
if a.cmd=='status': print('SCOPE_STATE'); print('active_cycle:',st.get('active_cycle')); print('stage:',st.get('lifecycle_stage')); raise SystemExit
if st.get('active_cycle') and st.get('project_state')!='CLOSED_VALIDATED': raise SystemExit('SCOPE_IMPORT: BLOCKED\nactive non-closed cycle exists')
r=validate(); cid=next_id(st,'cycle','CYCLE_'); rev='SCOPE_001'; dst=WORKPLAN/'history'/'cycles'/cid/'scope'/rev
for row in r['logical_files']:
    src=_physical_for(row['path'],ROOT/r['source_root']); out=dst/row['path']; out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,out)
cycle={'cycle_id':cid,'status':'PLANNING','ingest':{'ingest_id':r['ingest_id'],'source_root':r['source_root'],'package_digest':r['package_digest'],'scope_digest':r['scope_digest']},'scope':{'revision_label':rev,'digest':r['scope_digest'],'snapshot_path':str(dst.relative_to(ROOT)).replace('\\','/'),'files':r['logical_files']},'planning':None,'approval':None,'execution':None,'issues':[],'evaluation':{'attempts':[]},'created_at':now()}
st['cycles'][cid]=cycle; st['active_cycle']=cid; st['project_state']='PLANNING'; st['lifecycle_stage']='PLANNING'; st['next_action']='EXECUTE_PLANNING'; save_state(st,event='SCOPE_IMPORTED',actor='tool:scope',details={'cycle_id':cid,'ingest_id':r['ingest_id'],'scope_digest':r['scope_digest']})
print('SCOPE_IMPORT: PASS'); print('cycle:',cid); print('scope_revision:',rev); print('scope_digest:',r['scope_digest']); print('continuation:',continuation(load_state()))
