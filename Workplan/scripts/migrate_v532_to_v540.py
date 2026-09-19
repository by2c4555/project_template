#!/usr/bin/env python3
"""Conservative migration: only an idle v5.3.2 control plane can upgrade."""
import json
from pathlib import Path
from _core.io import atomic_write_json

root = Path(__file__).resolve().parents[2]; path = root / 'control' / 'STATE.json'
st = json.loads(path.read_text(encoding='utf-8'))
if st.get('workflow_version') != '5.3.2' or st.get('schema_version') != 6:
    raise SystemExit('MIGRATION: BLOCKED\nrequires v5.3.2 schema 6 state')
if st.get('active_cycle') or st.get('active_work') or st.get('pending_approval'):
    raise SystemExit('MIGRATION: BLOCKED\nactive runtime authority must finish, cancel, or be reconciled before migration')
st.update({'workflow_version':'5.4.0','schema_version':7,'project_state':'AWAITING_RESEARCH','lifecycle_stage':'BOOTSTRAP','research_revisions':{},'active_research_revision':None,'planning_a':None,'next_action':None})
atomic_write_json(path, st)
print('MIGRATION: PASS v5.3.2 -> v5.4.0 schema 7')
