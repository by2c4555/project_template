#!/usr/bin/env python3
import argparse
from _bootstrap import *
from _core.state import load_state
from _core import work as W
from _core.ingest import revalidate_bound
ROLE_BY_STAGE={'PLANNING':'PLANNING','DIAGNOSIS':'DIAGNOSIS','RECOVERY':'RECOVERY','EVALUATION':'EVALUATION'}
p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True); a=sp.add_parser('acquire'); a.add_argument('--tool',default='unknown'); a.add_argument('--model',default='unknown'); ns=p.parse_args(); st=load_state(); role=ROLE_BY_STAGE.get(st.get('lifecycle_stage'))
if not role: raise SystemExit('EXTERNAL_ENTRY: BLOCKED\ncurrent stage is not an external reasoning role')
if role=='PLANNING': revalidate_bound(st['cycles'][st['active_cycle']]['ingest'])
mode,meta,ticket=W.acquire(role,ns.tool,ns.model)
print('EXTERNAL_ENTRY:',mode); print('role:',role); print('work_id:',meta['work_id']); print('generation:',meta['generation']); print('ticket:',ticket)
