from __future__ import annotations
import json
from .state import load_state, save_state, now
from .paths import WORKPLAN, WORK_DIR
from .io import atomic_write_json
from .approval import create_pending
from . import work as W

PUBLIC_COMMANDS=(
    'WORKPLAN_STATUS','WORKPLAN_NEXT','EXECUTE_RESEARCH','EXECUTE_PLANNING',
    'EXECUTE_IMPLEMENTATION','EXECUTE_DIAGNOSIS','EXECUTE_RECOVERY','EXECUTE_EVALUATION',
    'RESET_PLANNING','RESET_DIAGNOSIS','RESET_RECOVERY','RESET_EVALUATION'
)
ROLE_COMMAND={'PLANNING':'EXECUTE_PLANNING','DIAGNOSIS':'EXECUTE_DIAGNOSIS','RECOVERY':'EXECUTE_RECOVERY','EVALUATION':'EXECUTE_EVALUATION'}
COMMAND_ROLE={v:k for k,v in ROLE_COMMAND.items()}
ROLE_CONSTITUTION={r:f'Workplan/external_agent/{r}_PROMPT.md' for r in ROLE_COMMAND}
RESET_ROLE={f'RESET_{r}':r for r in ROLE_COMMAND}
SURFACE_BY_ROLE={'PLANNING':'EXTERNAL_AI','DIAGNOSIS':'EXTERNAL_AI','RECOVERY':'EXTERNAL_AI','EVALUATION':'EXTERNAL_AI'}


def continuation(st=None):
    st=st or load_state(); stage=st.get('lifecycle_stage')
    if st.get('pending_approval'):
        p=st['pending_approval']; return {'current_result':'Human approval is required before the requested command may proceed.','current_stage':stage,'next_surface':'HUMAN','next_command':None,'why':'A deterministic token/cost/rework gate is pending.','approval_id':p['approval_id'],'challenge':p['challenge'],'expires_at':p.get('expires_at'),'human_command':f"python Workplan/scripts/approve.py -- {p['challenge']}"}
    if stage in ROLE_COMMAND:
        cmd=ROLE_COMMAND[stage]; return {'current_result':f'{stage.title()} work is ready or resumable.','current_stage':stage,'next_surface':'EXTERNAL_AI','next_command':cmd,'why':'Material reasoning is assigned to an external reasoning model.'}
    if stage in {'PLAN_READY','EXECUTION'}:
        return {'current_result':'Bounded implementation is ready or resumable.','current_stage':stage,'next_surface':'VS_CODE','next_command':'EXECUTE_IMPLEMENTATION','why':'Implementation is delegated through deterministic execution routing.'}
    if stage=='CLOSED_VALIDATED':
        return {'current_result':'The cycle is validated and closed.','current_stage':stage,'next_surface':'EXTERNAL_AI','next_command':'EXECUTE_RESEARCH','why':'A new feature/version starts from a new Research handoff.'}
    if stage in {'BOOTSTRAP',None}:
        return {'current_result':'No active validated Scope exists.','current_stage':stage or 'BOOTSTRAP','next_surface':'EXTERNAL_AI','next_command':'EXECUTE_RESEARCH','why':'Research must establish product WHAT/WHY before Planning.'}
    return {'current_result':'Workplan requires deterministic status inspection.','current_stage':stage,'next_surface':'UNKNOWN','next_command':'WORKPLAN_STATUS','why':'No public execution command is valid for the current stage.'}


def allowed_commands(st=None):
    st=st or load_state(); c=continuation(st); out=['WORKPLAN_STATUS','WORKPLAN_NEXT']
    if c.get('next_command'): out.append(c['next_command'])
    stage=st.get('lifecycle_stage')
    if stage in ROLE_COMMAND: out.append(f'RESET_{stage}')
    return list(dict.fromkeys(out))


def _subject(st, role):
    cid=st.get('active_cycle') or 'NO_CYCLE'; cycle=(st.get('cycles') or {}).get(cid,{})
    scope=(cycle.get('scope') or {}).get('digest','NO_SCOPE')
    return f'{role}:{cid}:{scope}'


def _granted(st, action, subject):
    g=st.get('last_granted_approval') or {}
    return g.get('requested_action')==action and g.get('subject')==subject


def _reject(command,st,reason):
    return {'status':'REJECTED','command':command,'reason':reason,'current_stage':st.get('lifecycle_stage'),'allowed_commands':allowed_commands(st),'state_changed':False}


def _approval(command,st,risk,subject):
    p=st.get('pending_approval')
    if p:
        return {'status':'APPROVAL_REQUIRED','command':command,'current_stage':st.get('lifecycle_stage'),'approval_id':p['approval_id'],'challenge':p['challenge'],'expires_at':p.get('expires_at'),'human_command':f"python Workplan/scripts/approve.py -- {p['challenge']}",'state_changed':False}
    rec=create_pending(risk,command,subject)
    return {'status':'APPROVAL_REQUIRED','command':command,'current_stage':st.get('lifecycle_stage'),'approval_id':rec['approval_id'],'challenge':rec['challenge'],'expires_at':rec.get('expires_at'),'human_command':f"python Workplan/scripts/approve.py -- {rec['challenge']}",'state_changed':True}


def _invalidate_active_work(st, role):
    wid=st.get('active_work')
    if not wid: return None
    p=WORK_DIR/wid/'WORK.json'
    if not p.is_file(): return None
    meta=json.loads(p.read_text(encoding='utf-8'))
    if meta.get('role')!=role or meta.get('status')=='COMPLETED': return None
    meta['status']='INVALIDATED'; meta['invalidated_at']=now(); meta['invalidation_reason']=f'RESET_{role}'
    atomic_write_json(p,meta); st['active_work']=None
    return wid


def execute(command, surface, tool='unknown', model='unknown'):
    command=command.strip().upper(); surface=surface.strip().upper()
    st=load_state()
    if command not in PUBLIC_COMMANDS: return _reject(command,st,'UNKNOWN_COMMAND')
    if command=='WORKPLAN_STATUS': return {'status':'OK','command':command,'state_changed':False,'state':{'stage':st.get('lifecycle_stage'),'project_state':st.get('project_state'),'cycle':st.get('active_cycle'),'active_work':st.get('active_work'),'active_task':st.get('active_task')},'continuation':continuation(st),'allowed_commands':allowed_commands(st)}
    if command=='WORKPLAN_NEXT': return {'status':'OK','command':command,'state_changed':False,'continuation':continuation(st),'allowed_commands':allowed_commands(st)}
    if command=='EXECUTE_RESEARCH':
        if surface!='EXTERNAL_AI': return _reject(command,st,'RESEARCH_REQUIRES_EXTERNAL_AI')
        if st.get('lifecycle_stage') not in {'BOOTSTRAP','CLOSED_VALIDATED'}: return _reject(command,st,'ACTIVE_CYCLE_MUST_FINISH_BEFORE_NEW_RESEARCH')
        return {'status':'ACCEPTED','command':command,'mode':'INIT' if st.get('lifecycle_stage')=='BOOTSTRAP' else 'NEW_CYCLE','surface':'EXTERNAL_AI','role':'RESEARCH','role_constitution':'Workplan/external_agent/RESEARCH_PROMPT.md','expected_output':['Workplan/ingest/project_details.md','Workplan/ingest/docs/raw/*'],'state_changed':False}
    if command=='EXECUTE_IMPLEMENTATION':
        if surface!='VS_CODE': return _reject(command,st,'IMPLEMENTATION_REQUIRES_VS_CODE')
        if st.get('lifecycle_stage') not in {'PLAN_READY','EXECUTION'}: return _reject(command,st,'IMPLEMENTATION_NOT_ALLOWED_IN_CURRENT_STAGE')
        return {'status':'ACCEPTED','command':command,'surface':'VS_CODE','machine_entry':'python Workplan/scripts/tools/execution.py next','protocol':'Run the machine entry, execute only its returned deterministic action, then re-run EXECUTE_IMPLEMENTATION until Workplan hands off to another surface.','state_changed':False}
    if command in COMMAND_ROLE:
        role=COMMAND_ROLE[command]
        if surface!='EXTERNAL_AI': return _reject(command,st,f'{role}_REQUIRES_EXTERNAL_AI')
        if st.get('lifecycle_stage')!=role: return _reject(command,st,'COMMAND_STAGE_MISMATCH')
        aw=st.get('active_work'); resumable=False
        if aw:
            p=WORK_DIR/aw/'WORK.json'
            if p.is_file():
                meta=json.loads(p.read_text(encoding='utf-8')); resumable=meta.get('role')==role and meta.get('status')!='COMPLETED'
        subject=_subject(st,role)
        if role=='PLANNING' and not resumable and not _granted(st,command,subject): return _approval(command,st,'NEW_COST_ENVELOPE',subject)
        mode,meta,ticket=W.acquire(role,tool,model)
        if role=='PLANNING' and not resumable:
            current=load_state()
            if _granted(current,command,subject):
                current['last_granted_approval']=None
                save_state(current,event='COMMAND_APPROVAL_CONSUMED',actor='machine:command',details={'command':command,'subject':subject})
        return {'status':'ACCEPTED','command':command,'mode':mode,'surface':'EXTERNAL_AI','role':role,'role_constitution':ROLE_CONSTITUTION[role],'work_id':meta['work_id'],'generation':meta['generation'],'ticket':ticket,'state_changed':True}
    if command in RESET_ROLE:
        role=RESET_ROLE[command]
        if surface!='EXTERNAL_AI': return _reject(command,st,f'{role}_RESET_REQUIRES_EXTERNAL_AI')
        if st.get('lifecycle_stage')!=role: return _reject(command,st,'RESET_STAGE_MISMATCH')
        subject=_subject(st,role)
        if not _granted(st,command,subject): return _approval(command,st,'SUBSTANTIAL_INVALIDATION',subject)
        invalidated=_invalidate_active_work(st,role); st['next_action']=ROLE_COMMAND[role]; st['last_granted_approval']=None
        save_state(st,event='ROLE_WORK_RESET',actor='machine:command',details={'role':role,'invalidated_work':invalidated,'command':command})
        return {'status':'ACCEPTED','command':command,'mode':'RESET','surface':'EXTERNAL_AI','role':role,'invalidated_work':invalidated,'next_command':ROLE_COMMAND[role],'state_changed':True}
    return _reject(command,st,'UNHANDLED_COMMAND')
