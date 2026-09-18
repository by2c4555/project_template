#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'Workplan/scripts'))
from _core.io import atomic_write_json
from _core.state import now

STATE = ROOT / 'Workplan/control/STATE.json'
TRANSITIONS = ROOT / 'Workplan/control/TRANSITIONS.jsonl'
OLD = '5.3.1'
NEW = '5.3.2'
SCHEMA = 6


def main():
    st = json.loads(STATE.read_text(encoding='utf-8'))
    found = st.get('workflow_version')
    schema = st.get('schema_version')

    if found == NEW and schema == SCHEMA:
        print('MIGRATION_V531_TO_V532: ALREADY_CURRENT')
        return
    if found != OLD or schema != SCHEMA:
        raise SystemExit(
            'MIGRATION_V531_TO_V532: BLOCKED\n'
            f'expected workflow={OLD} schema={SCHEMA}; found workflow={found} schema={schema}'
        )
    if st.get('active_work') is not None:
        raise SystemExit('MIGRATION_V531_TO_V532: BLOCKED\nactive_work must be null; finish/reset the active Work first')
    if st.get('pending_approval') is not None:
        raise SystemExit('MIGRATION_V531_TO_V532: BLOCKED\npending_approval must be null; resolve/expire it before migration')

    st['workflow_version'] = NEW
    st['state_seq'] = int(st.get('state_seq', 0)) + 1
    st['last_transition_at'] = now()
    atomic_write_json(STATE, st)

    TRANSITIONS.parent.mkdir(parents=True, exist_ok=True)
    rec = {
        'timestamp': now(),
        'state_seq': st['state_seq'],
        'event': 'MIGRATE_V531_TO_V532',
        'actor': 'machine',
        'cycle_id': st.get('active_cycle'),
        'details': {'from': OLD, 'to': NEW, 'schema_version': SCHEMA},
    }
    with TRANSITIONS.open('a', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(rec, sort_keys=True) + '\n')

    from _core.state import load_state
    load_state()
    print('MIGRATION_V531_TO_V532: PASS')
    print('workflow_version:', NEW)
    print('schema_version:', SCHEMA)
    print('state_seq:', st['state_seq'])


if __name__ == '__main__':
    main()
