from __future__ import annotations
import json, os, time
from datetime import datetime, timezone
from .paths import STATE_PATH, TRANSITIONS_PATH
from .io import atomic_write_json

WORKFLOW_VERSION = '5.4.0'
SCHEMA_VERSION = 7


def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def load_state():
    try:
        st = json.loads(STATE_PATH.read_text(encoding='utf-8'))
    except Exception as e:
        raise SystemExit(f'WORKPLAN_STATE: FAIL\n{e}')
    if st.get('workflow_version') != WORKFLOW_VERSION or st.get('schema_version') != SCHEMA_VERSION:
        raise SystemExit(
            'WORKPLAN_STATE: MIGRATION_REQUIRED\n'
            f'expected workflow={WORKFLOW_VERSION} schema={SCHEMA_VERSION}; '
            f'found workflow={st.get("workflow_version")} schema={st.get("schema_version")}\n'
            'see Workplan/MIGRATION_V5_3_2_TO_V5_4_0.md (or earlier migration documents for older versions)'
        )
    return st


def next_id(st, kind, prefix, width=4):
    st.setdefault('counters', {})[kind] = int(st.setdefault('counters', {}).get(kind, 0)) + 1
    return f"{prefix}{st['counters'][kind]:0{width}d}"


def save_state(st, event=None, actor='machine', details=None, expected_seq=None):
    lock = STATE_PATH.with_suffix('.lock')
    for _ in range(50):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.close(fd); break
        except FileExistsError: time.sleep(0.02)
    else: raise SystemExit('STATE_TRANSITION: BLOCKED\nstate writer lock unavailable')
    try:
        current = load_state()
        current_seq = int(current.get('state_seq', 0))
        if expected_seq is not None and current_seq != int(expected_seq): raise SystemExit(f'STATE_TRANSITION: BLOCKED\nexpected_seq={expected_seq} current_seq={current_seq}')
        if int(st.get('state_seq', 0)) != current_seq: raise SystemExit(f'STATE_TRANSITION: BLOCKED\nstale state object {st.get("state_seq")} != {current_seq}')
        st['state_seq'] = current_seq + 1
        st['last_transition_at'] = now()
    # The authoritative successor contains its own transition receipt.  The
    # append-only journal is a derived recovery/reporting surface and may be
    # reconciled from this receipt after an interruption.
        if event:
            st['last_transition'] = {
            'timestamp': st['last_transition_at'], 'state_seq': st['state_seq'],
            'event': event, 'actor': actor, 'cycle_id': st.get('active_cycle'),
            'details': details or {},
            }
        atomic_write_json(STATE_PATH, st)
        if event:
            rec = st['last_transition']; TRANSITIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
            with TRANSITIONS_PATH.open('a', encoding='utf-8', newline='\n') as f: f.write(json.dumps(rec, sort_keys=True) + '\n')
        return st['state_seq']
    finally:
        try: lock.unlink()
        except FileNotFoundError: pass


def compact(st):
    return {
        'state_seq': st.get('state_seq'), 'project_state': st.get('project_state'),
        'lifecycle_stage': st.get('lifecycle_stage'), 'active_cycle': st.get('active_cycle'),
        'active_phase': st.get('active_phase'), 'active_task': st.get('active_task'),
        'active_attempt': st.get('active_attempt'), 'active_work': st.get('active_work'),
        'pending_approval': (st.get('pending_approval') or {}).get('approval_id')
    }
