from __future__ import annotations
import hashlib, json, secrets
from .paths import APPROVAL_DIR
from .state import load_state, save_state, next_id, now
from .io import atomic_write_json
ALLOWED_RISKS={'NEW_COST_ENVELOPE','MATERIAL_WORK_EXPANSION','LARGE_REWORK','EXCESS_REPAIR_EXPANSION','BROAD_RECOVERY','EXPENSIVE_REEVALUATION','SUBSTANTIAL_INVALIDATION'}

def _digest_binding(st,risk,action,subject):
    payload={'state_seq':st['state_seq'],'cycle':st.get('active_cycle'),'stage':st.get('lifecycle_stage'),'work':st.get('active_work'),'task':st.get('active_task'),'risk':risk,'action':action,'subject':subject}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def _challenge(): return f'{secrets.randbelow(900000)+100000:06d}'

def create_pending(risk, action, subject=''):
    if risk not in ALLOWED_RISKS: raise SystemExit('APPROVAL_CREATE: BLOCKED\nunsupported risk kind')
    st=load_state()
    if st.get('pending_approval'): raise SystemExit('APPROVAL_CREATE: BLOCKED\na pending approval already exists')
    aid=next_id(st,'approval','APPROVAL_'); challenge=_challenge(); target_seq=int(st['state_seq'])+1
    projected=dict(st); projected['state_seq']=target_seq
    rec={'approval_id':aid,'status':'PENDING','risk_kind':risk,'requested_action':action,'subject':subject,'challenge':challenge,'challenge_generation':1,'attempts':0,'bound_state_seq':target_seq,'binding_digest':_digest_binding(projected,risk,action,subject),'created_at':now()}
    st['pending_approval']=rec; save_state(st,event='APPROVAL_CHALLENGE_ISSUED',actor='machine:risk_gate',details={'approval_id':aid,'risk_kind':risk,'requested_action':action,'generation':1})
    return load_state()['pending_approval']

def get_pending(aid=None):
    st=load_state(); rec=st.get('pending_approval')
    if not rec: raise SystemExit('APPROVAL: NONE')
    if aid and rec.get('approval_id')!=aid: raise SystemExit('APPROVAL: BLOCKED\nunknown/non-current approval id')
    return st,rec

def submit(challenge):
    st,rec=get_pending(); expected=_digest_binding(st,rec['risk_kind'],rec['requested_action'],rec.get('subject',''))
    if rec.get('binding_digest')!=expected or int(rec.get('bound_state_seq',-1))!=int(st['state_seq']):
        rec['status']='STALE'; rec['stale_at']=now(); atomic_write_json(APPROVAL_DIR/f"{rec['approval_id']}.json",rec); st['pending_approval']=None; save_state(st,event='APPROVAL_STALE',actor='human:approve',details={'approval_id':rec['approval_id']}); return 'STALE',rec,None
    if str(challenge)!=str(rec.get('challenge')):
        rec['attempts']=int(rec.get('attempts',0))+1; rec['challenge_generation']=int(rec.get('challenge_generation',1))+1; rec['challenge']=_challenge(); target_seq=int(st['state_seq'])+1; projected=dict(st); projected['state_seq']=target_seq; rec['bound_state_seq']=target_seq; rec['binding_digest']=_digest_binding(projected,rec['risk_kind'],rec['requested_action'],rec.get('subject','')); st['pending_approval']=rec; save_state(st,event='APPROVAL_CHALLENGE_ROTATED',actor='human:approve',details={'approval_id':rec['approval_id'],'generation':rec['challenge_generation'],'reason':'CHALLENGE_MISMATCH'}); return 'REJECTED',rec,rec['challenge']
    rec['status']='GRANTED'; rec['granted_at']=now(); rec['accepted_challenge_generation']=rec['challenge_generation']; atomic_write_json(APPROVAL_DIR/f"{rec['approval_id']}.json",rec); aid=rec['approval_id']; action=rec['requested_action']; st['pending_approval']=None; st['last_granted_approval']={'approval_id':aid,'requested_action':action,'subject':rec.get('subject',''),'granted_at':rec['granted_at']}; save_state(st,event='APPROVAL_GRANTED',actor='human:approve',details={'approval_id':aid,'requested_action':action}); return 'GRANTED',rec,None
