#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, sys, tempfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2]


def write_state(root, stage='PLANNING'):
    p = root / 'Workplan/control/STATE.json'
    st = json.loads(p.read_text())
    st.update({
        'lifecycle_stage': stage, 'project_state': stage, 'active_cycle': 'CYCLE_0001',
        'cycles': {'CYCLE_0001': {'cycle_id': 'CYCLE_0001', 'scope': {'digest': 'scope123', 'revision_label': 'SCOPE_001'}, 'issues': []}},
        'active_work': None, 'active_task': None, 'active_phase': None, 'active_attempt': None,
        'pending_approval': None, 'last_granted_approval': None,
    })
    p.write_text(json.dumps(st, indent=2, sort_keys=True) + '\n')


def scenario():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / 'repo'; shutil.copytree(SOURCE, root)
        sys.path.insert(0, str(root / 'Workplan/scripts'))
        from _core.command import execute
        from _core.approval import submit
        from _core.state import load_state, save_state

        statep = root / 'Workplan/control/STATE.json'
        before = json.loads(statep.read_text())['state_seq']
        for bad in ['execute_research', ' EXECUTE_RESEARCH', 'EXECUTE_RESEARCH ', 'please EXECUTE_RESEARCH']:
            r = execute(bad, 'EXTERNAL_AI')
            assert r['status'] == 'REJECTED' and r['reason'] == 'UNKNOWN_COMMAND'
            assert json.loads(statep.read_text())['state_seq'] == before
        r = execute('EXECUTE_RESEARCH', 'EXTERNAL_AI'); assert r['status'] == 'ACCEPTED' and r['role'] == 'RESEARCH'
        r = execute('EXECUTE_RESEARCH', 'VS_CODE'); assert r['status'] == 'REJECTED'

        write_state(root, 'PLANNING')
        r = execute('EXECUTE_PLANNING', 'EXTERNAL_AI'); assert r['status'] == 'APPROVAL_REQUIRED'
        status, _, _ = submit(r['challenge']); assert status == 'GRANTED'
        r = execute('EXECUTE_PLANNING', 'EXTERNAL_AI', 'test', 'strong'); assert r['status'] == 'ACCEPTED' and r['mode'] == 'START'
        st = load_state(); assert st['last_granted_approval']['status'] == 'CONSUMED' and st['last_granted_approval']['consumed_at']
        r = execute('EXECUTE_PLANNING', 'EXTERNAL_AI', 'other', 'strong2'); assert r['mode'] == 'RESUME' and r['generation'] == 2
        r = execute('EXECUTE_EVALUATION', 'EXTERNAL_AI'); assert r['reason'] == 'COMMAND_STAGE_MISMATCH'

        r = execute('RESET_PLANNING', 'EXTERNAL_AI'); assert r['status'] == 'APPROVAL_REQUIRED'
        status, _, _ = submit(r['challenge']); assert status == 'GRANTED'
        r = execute('RESET_PLANNING', 'EXTERNAL_AI'); assert r['status'] == 'ACCEPTED' and r['mode'] == 'RESET'
        r = execute('RESET_PLANNING', 'EXTERNAL_AI'); assert r['status'] == 'APPROVAL_REQUIRED'  # single use

        # Expired pending approval fails closed.
        st = load_state(); st['pending_approval']['expires_at'] = '2000-01-01T00:00:00Z'; statep.write_text(json.dumps(st, indent=2, sort_keys=True) + '\n')
        status, _, _ = submit(st['pending_approval']['challenge']); assert status == 'EXPIRED'

        # A granted but not-yet-consumed approval becomes unusable after any state transition.
        write_state(root, 'PLANNING')
        r = execute('EXECUTE_PLANNING', 'EXTERNAL_AI'); status, _, _ = submit(r['challenge']); assert status == 'GRANTED'
        st = load_state(); seq = st['state_seq']; st['next_action'] = 'NOOP_STATE_CHANGE'; save_state(st, event='TEST_STATE_ADVANCE', expected_seq=seq)
        r = execute('EXECUTE_PLANNING', 'EXTERNAL_AI'); assert r['status'] == 'APPROVAL_REQUIRED'

        st = load_state(); st['pending_approval'] = None; st['lifecycle_stage'] = 'PLAN_READY'; st['project_state'] = 'PLAN_READY'; statep.write_text(json.dumps(st, indent=2, sort_keys=True) + '\n')
        r = execute('WORKPLAN_NEXT', 'EXTERNAL_AI'); assert r['continuation']['next_surface'] == 'VS_CODE' and r['continuation']['next_command'] == 'EXECUTE_IMPLEMENTATION'
    print('COMMAND_PROTOCOL_VALID: PASS')


if __name__ == '__main__':
    scenario()
