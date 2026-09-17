#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
SOURCE=Path(__file__).resolve().parents[2]

def run(root,*args,ok=(0,)):
    p=subprocess.run([sys.executable,*args],cwd=root,text=True,capture_output=True)
    if p.returncode not in ok: raise AssertionError(f"command failed {args}\nrc={p.returncode}\nstdout={p.stdout}\nstderr={p.stderr}")
    return p

def obj(p): return json.loads(p.stdout)
def write_state(root,stage='PLANNING'):
    p=root/'Workplan/control/STATE.json'; st=json.loads(p.read_text()); st.update({'lifecycle_stage':stage,'project_state':stage,'active_cycle':'CYCLE_0001','cycles':{'CYCLE_0001':{'scope':{'digest':'scope123','revision_label':'SCOPE_001'}}},'active_work':None,'pending_approval':None,'last_granted_approval':None}); p.write_text(json.dumps(st,indent=2,sort_keys=True)+'\n')

def scenario():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)/'repo'; shutil.copytree(SOURCE,root)
        # Discussion-like/unknown token cannot start work.
        r=obj(run(root,'Workplan/scripts/command.py','please_continue_planning','--surface','EXTERNAL_AI',ok=(2,))); assert r['status']=='REJECTED' and r['state_changed'] is False
        # Research is the only execution entry from bootstrap.
        r=obj(run(root,'Workplan/scripts/command.py','EXECUTE_RESEARCH','--surface','EXTERNAL_AI')); assert r['status']=='ACCEPTED' and r['role']=='RESEARCH'
        r=obj(run(root,'Workplan/scripts/command.py','EXECUTE_IMPLEMENTATION','--surface','VS_CODE',ok=(2,))); assert r['status']=='REJECTED'
        # Planning INIT is explicitly cost-gated.
        write_state(root,'PLANNING')
        r=obj(run(root,'Workplan/scripts/command.py','EXECUTE_PLANNING','--surface','EXTERNAL_AI')); assert r['status']=='APPROVAL_REQUIRED'; challenge=r['challenge']
        st=json.loads((root/'Workplan/control/STATE.json').read_text()); assert st['active_work'] is None
        run(root,'Workplan/scripts/approve.py','--',challenge)
        r=obj(run(root,'Workplan/scripts/command.py','EXECUTE_PLANNING','--surface','EXTERNAL_AI','--tool','test','--model','strong')); assert r['status']=='ACCEPTED' and r['mode']=='START'
        # Re-entry is RESUME and does not create another approval.
        r=obj(run(root,'Workplan/scripts/command.py','EXECUTE_PLANNING','--surface','EXTERNAL_AI','--tool','other','--model','strong2')); assert r['status']=='ACCEPTED' and r['mode']=='RESUME' and r['generation']==2
        # Wrong-stage command is rejected without interpretation.
        r=obj(run(root,'Workplan/scripts/command.py','EXECUTE_EVALUATION','--surface','EXTERNAL_AI',ok=(2,))); assert r['status']=='REJECTED' and r['reason']=='COMMAND_STAGE_MISMATCH'
        # Reset is explicit and approval-gated.
        r=obj(run(root,'Workplan/scripts/command.py','RESET_PLANNING','--surface','EXTERNAL_AI')); assert r['status']=='APPROVAL_REQUIRED'; reset_challenge=r['challenge']
        run(root,'Workplan/scripts/approve.py','--',reset_challenge)
        r=obj(run(root,'Workplan/scripts/command.py','RESET_PLANNING','--surface','EXTERNAL_AI')); assert r['status']=='ACCEPTED' and r['mode']=='RESET'
        st=json.loads((root/'Workplan/control/STATE.json').read_text()); assert st['active_work'] is None and st['lifecycle_stage']=='PLANNING'
        # Approval lease expiry preserves lifecycle stage and denies authorization.
        r=obj(run(root,'Workplan/scripts/command.py','RESET_PLANNING','--surface','EXTERNAL_AI')); assert r['status']=='APPROVAL_REQUIRED'; exp_challenge=r['challenge']
        stp=root/'Workplan/control/STATE.json'; st=json.loads(stp.read_text()); st['pending_approval']['expires_at']='2000-01-01T00:00:00Z'; stp.write_text(json.dumps(st,indent=2,sort_keys=True)+'\n')
        p=run(root,'Workplan/scripts/approve.py','--',exp_challenge,ok=(2,)); assert 'APPROVAL: EXPIRED' in p.stdout
        st=json.loads(stp.read_text()); assert st['lifecycle_stage']=='PLANNING' and st['pending_approval'] is None
        # Universal continuation is exact and surface-aware.
        st['lifecycle_stage']='PLAN_READY'; st['project_state']='PLAN_READY'; stp.write_text(json.dumps(st,indent=2,sort_keys=True)+'\n')
        r=obj(run(root,'Workplan/scripts/command.py','WORKPLAN_NEXT','--surface','EXTERNAL_AI')); assert r['continuation']['next_surface']=='VS_CODE' and r['continuation']['next_command']=='EXECUTE_IMPLEMENTATION'
        r=obj(run(root,'Workplan/scripts/command.py','EXECUTE_PLANNING','--surface','VS_CODE',ok=(2,))); assert r['status']=='REJECTED'
    print('COMMAND_PROTOCOL_VALID: PASS')
if __name__=='__main__': scenario()
