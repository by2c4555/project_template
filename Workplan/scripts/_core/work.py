from __future__ import annotations
import json
from pathlib import Path
from .paths import ROOT, WORK_DIR, WORKPLAN
from .state import load_state, save_state, next_id, now
from .io import atomic_write_json, atomic_write_text
from .integrity import inline_list, sha256_file
ROLES={'PLANNING','BUILDER','DIAGNOSIS','RECOVERY','EVALUATION'}
CONTEXT_REASONS={'REQUIREMENT','ARCHITECTURE','INTERFACE','DATA_MODEL','PRIOR_DECISION','ACTIVE_UNIT','FAILURE_EVIDENCE','WORKTREE'}

def work_path(wid): return WORK_DIR/wid

def _task_text(task_id):
    p=WORKPLAN/'tasks'/f'{task_id}.md'; return p.read_text(encoding='utf-8') if p.is_file() else ''

def _input_bindings(st,role,task_id=None):
    cid=st.get('active_cycle'); cycle=(st.get('cycles') or {}).get(cid,{})
    b={'cycle_id':cid,'role':role}
    if cycle.get('scope'): b['scope_digest']=cycle['scope'].get('digest')
    if cycle.get('ingest'): b['ingest_digest']=cycle['ingest'].get('package_digest')
    if cycle.get('planning'): b['package_digest']=cycle['planning'].get('candidate_package_digest')
    if task_id:
        tp=WORKPLAN/'tasks'/f'{task_id}.md'
        if tp.is_file(): b['task_digest']=sha256_file(tp)
    return b

def _tracked_paths(role,task_id=None):
    if role=='BUILDER' and task_id:
        return inline_list(_task_text(task_id),'authorized_paths')
    if role=='RECOVERY':
        paths=[]
        for p in ROOT.rglob('*'):
            if p.is_file() and WORKPLAN not in p.parents and '.git' not in p.parts:
                paths.append(str(p.relative_to(ROOT)).replace('\\','/'))
        return sorted(paths)
    return []

def _snapshot(paths):
    out={}
    for rel in paths:
        p=ROOT/rel
        out[rel]={'exists':p.is_file(),'sha256':sha256_file(p) if p.is_file() else None}
    return out

def reconcile(meta):
    paths=meta.get('tracked_paths') or []
    if not paths: return {'status':'CLEAN','changed':[]}
    before=meta.get('workspace_baseline') or {}; nowshot=_snapshot(paths); changed=[]
    for rel in sorted(set(before)|set(nowshot)):
        if before.get(rel)!=nowshot.get(rel): changed.append({'path':rel,'before':before.get(rel),'now':nowshot.get(rel)})
    return {'status':'RECONCILE_ACTIVE_UNIT' if changed else 'CLEAN','changed':changed}

def _ticket(meta,action='CONTINUE'):
    return {'ticket_schema':1,'kind':'RESUME' if meta.get('checkpoint_seq',0) else 'ACTION','action':action,'role':meta['role'],'work_id':meta['work_id'],'generation':meta['generation'],'checkpoint_seq':meta.get('checkpoint_seq',0),'unit':meta.get('next_unit'),'task_id':meta.get('task_id'),'objective':'Perform only the bounded semantic unit authorized by current Workplan state.','input_bindings':meta.get('input_bindings',{}),'read':meta.get('context_paths',[]),'write':meta.get('tracked_paths',[]),'allowed_actions':['CHECKPOINT','COMPLETE','NEED_CONTEXT']}

def acquire(role, tool='unknown', model='unknown', task_id=None):
    role=role.upper()
    if role not in ROLES: raise SystemExit('WORK: BLOCKED\nunsupported role')
    st=load_state(); aw=st.get('active_work')
    if aw:
        p=work_path(aw); meta=json.loads((p/'WORK.json').read_text())
        compatible=meta['status']!='COMPLETED' and meta['role']==role and (task_id is None or meta.get('task_id')==task_id)
        if not compatible: raise SystemExit(f'WORK: BLOCKED\nactive work exists: {aw}')
        meta['generation']=int(meta.get('generation',0))+1; meta['last_agent']={'tool':tool,'model':model,'at':now()}; meta['input_bindings']=_input_bindings(st,role,meta.get('task_id'))
        atomic_write_json(p/'WORK.json',meta); save_state(st,event='WORK_ACQUIRED',actor='agent:work',details={'work_id':aw,'role':role,'generation':meta['generation']})
        return 'RESUME',meta,_ticket(meta,'RECONCILE' if reconcile(meta)['status']!='CLEAN' else 'CONTINUE')
    wid=next_id(st,'work','WORK_'); p=work_path(wid); (p/'checkpoints').mkdir(parents=True,exist_ok=True); (p/'evidence').mkdir(exist_ok=True)
    tracked=_tracked_paths(role,task_id)
    meta={'work_id':wid,'role':role,'task_id':task_id,'status':'IN_PROGRESS','generation':1,'checkpoint_seq':0,'current_unit':'INIT','next_unit':'INIT_MAP' if role!='BUILDER' else 'TASK_PREFLIGHT','last_agent':{'tool':tool,'model':model,'at':now()},'created_at':now(),'input_bindings':_input_bindings(st,role,task_id),'tracked_paths':tracked,'workspace_baseline':_snapshot(tracked),'context_paths':[]}
    atomic_write_json(p/'WORK.json',meta); atomic_write_text(p/'MAP.md',f'# {wid} {role} Work Map\n\nstatus: INIT\n\nPersist verified decisions/evidence and exact next bounded unit.\n'); atomic_write_text(p/'RESUME.md',f'# Resume {wid}\n\nrole: {role}\ngeneration: 1\ncheckpoint_seq: 0\nnext_unit: {meta["next_unit"]}\n')
    st['active_work']=wid
    if role=='BUILDER' and task_id: st['active_task']=task_id
    save_state(st,event='WORK_BEGIN',actor='agent:work',details={'work_id':wid,'role':role,'task_id':task_id,'generation':1})
    return 'START',meta,_ticket(meta)

def begin(role,tool='unknown',model='unknown',task_id=None): return acquire(role,tool,model,task_id)[:2]

def status():
    st=load_state(); wid=st.get('active_work')
    if not wid: return None
    return json.loads((work_path(wid)/'WORK.json').read_text())

def _require_generation(meta,expected_generation):
    if expected_generation is None or int(expected_generation)!=int(meta.get('generation',0)):
        raise SystemExit(f'STALE_GENERATION\nexpected={expected_generation} current={meta.get("generation")}')

def checkpoint(unit,next_unit,note,expected_generation):
    st=load_state(); wid=st.get('active_work')
    if not wid: raise SystemExit('WORK: BLOCKED\nno active work')
    p=work_path(wid); meta=json.loads((p/'WORK.json').read_text()); _require_generation(meta,expected_generation)
    seq=int(meta.get('checkpoint_seq',0))+1; cp={'work_id':wid,'generation':meta['generation'],'checkpoint_seq':seq,'unit':unit,'next_unit':next_unit,'note':note,'created_at':now()}
    atomic_write_json(p/'checkpoints'/f'CP_{seq:04d}.json',cp); meta.update({'checkpoint_seq':seq,'current_unit':unit,'next_unit':next_unit,'status':'CHECKPOINTED','workspace_baseline':_snapshot(meta.get('tracked_paths',[]))}); atomic_write_json(p/'WORK.json',meta); atomic_write_text(p/'RESUME.md',f'# Resume {wid}\n\nrole: {meta["role"]}\ngeneration: {meta["generation"]}\ncheckpoint_seq: {seq}\nlast_completed_unit: {unit}\nnext_unit: {next_unit}\n\n## Verified durable note\n\n{note}\n')
    save_state(st,event='WORK_CHECKPOINT',actor='agent:work',details={'work_id':wid,'generation':meta['generation'],'checkpoint_seq':seq,'unit':unit,'next_unit':next_unit}); return cp

def complete(note,expected_generation):
    st=load_state(); wid=st.get('active_work')
    if not wid: raise SystemExit('WORK: BLOCKED\nno active work')
    p=work_path(wid); meta=json.loads((p/'WORK.json').read_text()); _require_generation(meta,expected_generation)
    rec=reconcile(meta)
    if meta['role'] in {'BUILDER','RECOVERY'} and rec['status']!='CLEAN': raise SystemExit('WORK_COMPLETE: BLOCKED\nworkspace changed after last checkpoint; checkpoint or reconcile active unit first')
    meta['status']='COMPLETED'; meta['completed_at']=now(); meta['completion_note']=note; atomic_write_json(p/'WORK.json',meta); st['last_completed_work']=wid; st['active_work']=None; save_state(st,event='WORK_COMPLETE',actor='agent:work',details={'work_id':wid,'role':meta['role'],'generation':meta['generation']}); return meta

def request_context(reason):
    reason=reason.upper()
    if reason not in CONTEXT_REASONS: raise SystemExit('CONTEXT: BLOCKED\nunsupported reason')
    st=load_state(); wid=st.get('active_work')
    if not wid: raise SystemExit('CONTEXT: BLOCKED\nno active work')
    meta=json.loads((work_path(wid)/'WORK.json').read_text()); task=meta.get('task_id'); paths=[]
    mapping={'REQUIREMENT':['Workplan/compiled/PROJECT_BRIEF.md','Workplan/compiled/GLOBAL_CONSTRAINTS.md'],'ARCHITECTURE':['Workplan/compiled/ARCHITECTURE.md'],'INTERFACE':['Workplan/compiled/INTERFACES.md'],'DATA_MODEL':['Workplan/compiled/DATA_MODEL.md'],'PRIOR_DECISION':['Workplan/compiled/DECISIONS.md'],'ACTIVE_UNIT':[f'Workplan/work/{wid}/RESUME.md'],'FAILURE_EVIDENCE':[f'Workplan/work/{wid}/evidence'],'WORKTREE':[]}
    paths=mapping[reason][:]
    if task and reason in {'REQUIREMENT','ACTIVE_UNIT'}: paths.insert(0,f'Workplan/tasks/{task}.md')
    return {'reason':reason,'level':'L1','paths':paths,'authority_unchanged':True}
