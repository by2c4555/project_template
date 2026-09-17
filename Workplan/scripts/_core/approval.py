from __future__ import annotations
import hashlib, json, secrets
from datetime import datetime, timedelta, timezone
from .paths import APPROVAL_DIR
from .state import load_state, save_state, next_id, now
from .io import atomic_write_json

ALLOWED_RISKS = {'NEW_COST_ENVELOPE','MATERIAL_WORK_EXPANSION','LARGE_REWORK','EXCESS_REPAIR_EXPANSION','BROAD_RECOVERY','EXPENSIVE_REEVALUATION','SUBSTANTIAL_INVALIDATION'}
DEFAULT_TTL_SECONDS = 900


def _digest_binding(st, risk, action, subject):
    payload = {'state_seq': st['state_seq'], 'cycle': st.get('active_cycle'), 'stage': st.get('lifecycle_stage'), 'work': st.get('active_work'), 'task': st.get('active_task'), 'attempt': st.get('active_attempt'), 'risk': risk, 'action': action, 'subject': subject}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def _challenge(): return f'{secrets.randbelow(900000)+100000:06d}'
def _expiry(ttl_seconds): return (datetime.now(timezone.utc)+timedelta(seconds=int(ttl_seconds))).replace(microsecond=0).isoformat().replace('+00:00','Z')
def _expired(rec):
    raw = rec.get('expires_at')
    return bool(raw) and datetime.now(timezone.utc) >= datetime.fromisoformat(raw.replace('Z','+00:00'))


def create_pending(risk, action, subject='', ttl_seconds=DEFAULT_TTL_SECONDS):
    if risk not in ALLOWED_RISKS: raise SystemExit('APPROVAL_CREATE: BLOCKED\nunsupported risk kind')
    st = load_state()
    if st.get('pending_approval'): raise SystemExit('APPROVAL_CREATE: BLOCKED\na pending approval already exists')
    aid = next_id(st, 'approval', 'APPROVAL_'); challenge = _challenge(); target_seq = int(st['state_seq']) + 1
    projected = dict(st); projected['state_seq'] = target_seq
    rec = {'approval_id': aid, 'status': 'PENDING', 'risk_kind': risk, 'requested_action': action, 'subject': subject, 'challenge': challenge, 'challenge_generation': 1, 'attempts': 0, 'bound_state_seq': target_seq, 'binding_digest': _digest_binding(projected, risk, action, subject), 'created_at': now(), 'expires_at': _expiry(ttl_seconds), 'granted_at': None, 'consumed_at': None}
    st['pending_approval'] = rec
    save_state(st, event='APPROVAL_CHALLENGE_ISSUED', actor='machine:risk_gate', details={'approval_id': aid, 'risk_kind': risk, 'requested_action': action, 'generation': 1, 'expires_at': rec['expires_at']})
    return load_state()['pending_approval']


def get_pending(aid=None):
    st = load_state(); rec = st.get('pending_approval')
    if not rec: raise SystemExit('APPROVAL: NONE')
    if aid and rec.get('approval_id') != aid: raise SystemExit('APPROVAL: BLOCKED\nunknown/non-current approval id')
    return st, rec


def submit(challenge):
    st, rec = get_pending()
    if _expired(rec):
        rec['status'] = 'EXPIRED'; rec['expired_at'] = now(); atomic_write_json(APPROVAL_DIR/f"{rec['approval_id']}.json", rec); st['pending_approval'] = None
        save_state(st, event='APPROVAL_EXPIRED', actor='human:approve', details={'approval_id': rec['approval_id']}); return 'EXPIRED', rec, None
    expected = _digest_binding(st, rec['risk_kind'], rec['requested_action'], rec.get('subject',''))
    if rec.get('binding_digest') != expected or int(rec.get('bound_state_seq',-1)) != int(st['state_seq']):
        rec['status'] = 'STALE'; rec['stale_at'] = now(); atomic_write_json(APPROVAL_DIR/f"{rec['approval_id']}.json", rec); st['pending_approval'] = None
        save_state(st, event='APPROVAL_STALE', actor='human:approve', details={'approval_id': rec['approval_id']}); return 'STALE', rec, None
    if str(challenge) != str(rec.get('challenge')):
        rec['attempts'] = int(rec.get('attempts',0)) + 1; rec['challenge_generation'] = int(rec.get('challenge_generation',1)) + 1; rec['challenge'] = _challenge(); rec['expires_at'] = _expiry(DEFAULT_TTL_SECONDS)
        target_seq = int(st['state_seq']) + 1; projected = dict(st); projected['state_seq'] = target_seq; rec['bound_state_seq'] = target_seq; rec['binding_digest'] = _digest_binding(projected, rec['risk_kind'], rec['requested_action'], rec.get('subject','')); st['pending_approval'] = rec
        save_state(st, event='APPROVAL_CHALLENGE_ROTATED', actor='human:approve', details={'approval_id': rec['approval_id'], 'generation': rec['challenge_generation'], 'reason': 'CHALLENGE_MISMATCH', 'expires_at': rec['expires_at']}); return 'REJECTED', rec, rec['challenge']
    rec['status'] = 'GRANTED'; rec['granted_at'] = now(); rec['accepted_challenge_generation'] = rec['challenge_generation']; rec['consumed_at'] = None
    # The usable grant is bound to the exact post-grant state. Any intervening
    # state transition makes it stale before it can authorize an action.
    granted_state_seq = int(st['state_seq']) + 1
    projected = dict(st); projected['state_seq'] = granted_state_seq; projected['pending_approval'] = None
    rec['granted_state_seq'] = granted_state_seq
    rec['grant_binding_digest'] = _digest_binding(projected, rec['risk_kind'], rec['requested_action'], rec.get('subject',''))
    atomic_write_json(APPROVAL_DIR/f"{rec['approval_id']}.json", rec)
    st['pending_approval'] = None; st['last_granted_approval'] = {k: rec.get(k) for k in ('approval_id','status','risk_kind','requested_action','subject','created_at','expires_at','granted_at','consumed_at','granted_state_seq','grant_binding_digest')}
    save_state(st, event='APPROVAL_GRANTED', actor='human:approve', details={'approval_id': rec['approval_id'], 'requested_action': rec['requested_action']}); return 'GRANTED', rec, None


def grant_matches(st, action, subject):
    g = st.get('last_granted_approval') or {}
    if g.get('requested_action') != action or g.get('subject') != subject or g.get('consumed_at') or g.get('status') != 'GRANTED':
        return False
    if _expired(g) or int(g.get('granted_state_seq', -1)) != int(st.get('state_seq', -2)):
        return False
    expected = _digest_binding(st, g.get('risk_kind'), action, subject)
    return g.get('grant_binding_digest') == expected


def consume_grant(st, action, subject):
    if not grant_matches(st, action, subject):
        return False
    g = dict(st['last_granted_approval']); g['consumed_at'] = now(); g['status'] = 'CONSUMED'; st['last_granted_approval'] = g
    return True
