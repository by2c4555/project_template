#!/usr/bin/env python3
import argparse,json,shutil
from _bootstrap import *
from _core.state import load_state,save_state,next_id,now
from _core.paths import WORKPLAN,ROOT
from _core.integrity import field,digest_files
p=argparse.ArgumentParser(); p.add_argument('cmd',choices=['status','import']); a=p.parse_args(); st=load_state()
if a.cmd=='status':
    print('SCOPE_STATE'); print('active_cycle:',st.get('active_cycle')); print('stage:',st.get('lifecycle_stage')); raise SystemExit
src=WORKPLAN/'project_details.md'; text=src.read_text()
if field(text,'artifact_kind')!='PROJECT_DETAILS' or field(text,'artifact_status')!='READY_FOR_PLANNING' or field(text,'product_scope_unknowns')!='0':
    raise SystemExit('SCOPE_IMPORT: BLOCKED\nproject_details must be PROJECT_DETAILS / READY_FOR_PLANNING / product_scope_unknowns: 0')
if st.get('active_cycle') and st.get('project_state')!='CLOSED_VALIDATED': raise SystemExit('SCOPE_IMPORT: BLOCKED\nactive non-closed cycle exists')
cid=next_id(st,'cycle','CYCLE_')
# support simple inline [path, path]
raw=field(text,'supporting_files') or '[]'; inner=raw[1:-1].strip() if raw.startswith('[') and raw.endswith(']') else ''
rels=['Workplan/project_details.md']+[x.strip().strip('"\'') for x in inner.split(',') if x.strip()]
files=[]
for rel in rels:
    fp=ROOT/rel
    if not fp.is_file(): raise SystemExit(f'SCOPE_IMPORT: BLOCKED\nmissing {rel}')
    if rel!='Workplan/project_details.md' and not rel.startswith('Workplan/docs/raw/'): raise SystemExit(f'SCOPE_IMPORT: BLOCKED\ninvalid supporting path {rel}')
    files.append(fp)
digest,rows=digest_files(files); rev='SCOPE_001'; dst=WORKPLAN/'history'/'cycles'/cid/'scope'/rev
for fp in files:
    rel=fp.relative_to(ROOT); out=dst/rel; out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(fp,out)
cycle={'cycle_id':cid,'status':'PLANNING','scope':{'revision_label':rev,'digest':digest,'snapshot_path':str(dst.relative_to(ROOT)).replace('\\','/'),'files':rows},'planning':None,'approval':None,'execution':None,'issues':[],'evaluation':{'attempts':[]},'created_at':now()}
st['cycles'][cid]=cycle; st['active_cycle']=cid; st['project_state']='PLANNING'; st['lifecycle_stage']='PLANNING'; st['next_action']='RUN_EXTERNAL_AGENT_PLANNING'
save_state(st,event='SCOPE_IMPORTED',actor='tool:scope',details={'cycle_id':cid,'scope_revision':rev,'scope_digest':digest})
print('SCOPE_IMPORT: PASS'); print('cycle:',cid); print('scope_revision:',rev); print('scope_digest:',digest); print('next: Workplan/external_agent/PLANNING_PROMPT.md')
