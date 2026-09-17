from __future__ import annotations
import json, hashlib
from pathlib import Path
from .paths import WORK_DIR
from .state import load_state, save_state, next_id, now
from .io import atomic_write_json, atomic_write_text
ROLES={'PLANNING','BUILDER','DIAGNOSIS','RECOVERY','EVALUATION'}

def work_path(wid): return WORK_DIR/wid

def begin(role, tool='unknown', model='unknown', task_id=None):
    role=role.upper()
    if role not in ROLES: raise SystemExit('WORK: BLOCKED\nunsupported role')
    st=load_state(); aw=st.get('active_work')
    if aw:
        meta=json.loads((work_path(aw)/'WORK.json').read_text())
        if meta['status']!='COMPLETED' and meta['role']==role and (not task_id or meta.get('task_id')==task_id):
            meta['last_agent']={'tool':tool,'model':model,'at':now()}; atomic_write_json(work_path(aw)/'WORK.json',meta)
            return 'RESUME',meta
        raise SystemExit(f'WORK: BLOCKED\nactive work exists: {aw}')
    wid=next_id(st,'work','WORK_')
    p=work_path(wid); (p/'checkpoints').mkdir(parents=True,exist_ok=True); (p/'evidence').mkdir(exist_ok=True)
    meta={'work_id':wid,'role':role,'task_id':task_id,'status':'IN_PROGRESS','checkpoint_seq':0,'current_unit':'INIT','next_unit':'INIT_MAP' if role!='BUILDER' else 'TASK_PREFLIGHT','last_agent':{'tool':tool,'model':model,'at':now()},'created_at':now()}
    atomic_write_json(p/'WORK.json',meta)
    atomic_write_text(p/'MAP.md',f'# {wid} {role} Work Map\n\nstatus: INIT\n\nCreate a concise role-specific Stage/Topic map bound to current authoritative inputs before deep work.\n' if role!='BUILDER' else f'# {wid} Builder Task Map\n\nTask contract is the execution map. Record bounded implementation/verification units only.\n')
    atomic_write_text(p/'RESUME.md',f'# Resume {wid}\n\nrole: {role}\ncheckpoint_seq: 0\nnext_unit: {meta["next_unit"]}\n')
    st['active_work']=wid
    if role=='BUILDER' and task_id: st['active_task']=task_id
    save_state(st,event='WORK_BEGIN',actor='agent:work',details={'work_id':wid,'role':role,'task_id':task_id})
    return 'START',meta

def status():
    st=load_state(); wid=st.get('active_work')
    if not wid: return None
    return json.loads((work_path(wid)/'WORK.json').read_text())

def checkpoint(unit,next_unit,note):
    st=load_state(); wid=st.get('active_work')
    if not wid: raise SystemExit('WORK: BLOCKED\nno active work')
    p=work_path(wid); meta=json.loads((p/'WORK.json').read_text()); seq=int(meta.get('checkpoint_seq',0))+1
    cp={'work_id':wid,'checkpoint_seq':seq,'unit':unit,'next_unit':next_unit,'note':note,'created_at':now()}
    atomic_write_json(p/'checkpoints'/f'CP_{seq:04d}.json',cp)
    meta.update({'checkpoint_seq':seq,'current_unit':unit,'next_unit':next_unit,'status':'CHECKPOINTED'}); atomic_write_json(p/'WORK.json',meta)
    atomic_write_text(p/'RESUME.md',f'# Resume {wid}\n\nrole: {meta["role"]}\ncheckpoint_seq: {seq}\nlast_completed_unit: {unit}\nnext_unit: {next_unit}\n\n## Verified durable note\n\n{note}\n')
    save_state(st,event='WORK_CHECKPOINT',actor='agent:work',details={'work_id':wid,'checkpoint_seq':seq,'unit':unit,'next_unit':next_unit})
    return cp

def complete(note=''):
    st=load_state(); wid=st.get('active_work')
    if not wid: raise SystemExit('WORK: BLOCKED\nno active work')
    p=work_path(wid); meta=json.loads((p/'WORK.json').read_text()); meta['status']='COMPLETED'; meta['completed_at']=now(); meta['completion_note']=note; atomic_write_json(p/'WORK.json',meta)
    st['last_completed_work']=wid; st['active_work']=None
    save_state(st,event='WORK_COMPLETE',actor='agent:work',details={'work_id':wid,'role':meta['role']})
    return meta
