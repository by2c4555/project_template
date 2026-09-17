from __future__ import annotations
import json
from datetime import datetime, timezone
from .paths import STATE_PATH, TRANSITIONS_PATH
from .io import atomic_write_json
WORKFLOW_VERSION='5.1.0'; SCHEMA_VERSION=4

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def load_state():
    try: st=json.loads(STATE_PATH.read_text(encoding='utf-8'))
    except Exception as e: raise SystemExit(f'WORKPLAN_STATE: FAIL\n{e}')
    if st.get('workflow_version')!=WORKFLOW_VERSION: raise SystemExit(f'WORKPLAN_STATE: FAIL\nworkflow_version must be {WORKFLOW_VERSION}')
    if st.get('schema_version')!=SCHEMA_VERSION: raise SystemExit(f'WORKPLAN_STATE: FAIL\nschema_version must be {SCHEMA_VERSION}')
    return st

def next_id(st, kind, prefix, width=4):
    st['counters'][kind]=int(st['counters'].get(kind,0))+1
    return f"{prefix}{st['counters'][kind]:0{width}d}"

def save_state(st, event=None, actor='machine', details=None, expected_seq=None):
    current=load_state()
    if expected_seq is not None and int(current.get('state_seq',0))!=int(expected_seq):
        raise SystemExit(f'STATE_TRANSITION: BLOCKED\nexpected_seq={expected_seq} current_seq={current.get("state_seq")}')
    if int(st.get('state_seq',0))!=int(current.get('state_seq',0)):
        raise SystemExit(f'STATE_TRANSITION: BLOCKED\nstale state object {st.get("state_seq")} != {current.get("state_seq")}')
    st['state_seq']=int(current.get('state_seq',0))+1
    st['last_transition_at']=now()
    atomic_write_json(STATE_PATH,st)
    if event:
        rec={'timestamp':now(),'state_seq':st['state_seq'],'event':event,'actor':actor,'cycle_id':st.get('active_cycle'),'details':details or {}}
        TRANSITIONS_PATH.parent.mkdir(parents=True,exist_ok=True)
        with TRANSITIONS_PATH.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(rec,sort_keys=True)+'\n')
    return st['state_seq']

def compact(st):
    return {'state_seq':st.get('state_seq'),'project_state':st.get('project_state'),'lifecycle_stage':st.get('lifecycle_stage'),'active_cycle':st.get('active_cycle'),'active_work':st.get('active_work'),'active_task':st.get('active_task'),'pending_approval':(st.get('pending_approval') or {}).get('approval_id')}
