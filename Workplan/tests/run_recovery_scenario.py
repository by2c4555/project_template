#!/usr/bin/env python3
from __future__ import annotations
import contextlib, io, json, os, runpy, shutil, sys, tempfile, types
from pathlib import Path

SOURCE=Path(__file__).resolve().parents[2]

def write(p,text): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')

def run(root,*args,ok=(0,)):
    script=root/args[0]; stdout,stderr=io.StringIO(),io.StringIO(); oldargv,oldcwd,oldpath=sys.argv[:],os.getcwd(),sys.path[:]
    sys.argv=list(args); os.chdir(root); sys.path.insert(0,str(script.parent)); rc=0
    try:
        with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
            try: runpy.run_path(str(script),run_name='__main__')
            except SystemExit as e:
                if isinstance(e.code,int): rc=e.code
                elif e.code in (None,''): rc=0
                else: rc=1; print(e.code,file=sys.stderr)
    except BaseException as e: rc=1; print(f'{type(e).__name__}: {e}',file=stderr)
    finally: sys.argv=oldargv; os.chdir(oldcwd); sys.path[:]=oldpath
    r=types.SimpleNamespace(returncode=rc,stdout=stdout.getvalue(),stderr=stderr.getvalue())
    if rc not in ok: raise AssertionError(f'command failed {args}\nrc={rc}\nstdout={r.stdout}\nstderr={r.stderr}')
    return r

def evidence(root,rel):
    st=json.loads((root/'Workplan/control/STATE.json').read_text()); wid=st['last_completed_work']; meta=json.loads((root/'Workplan/work'/wid/'WORK.json').read_text())
    obj={'schema_version':1,'attempt_id':meta['attempt_id'],'task_id':meta['task_id'],'phase_id':meta['phase_id'],'generation':meta['generation'],'ticket_digest':meta['ticket_digest'],'verification':[],'artifacts':[],'mutation_manifest_path':meta['mutation_manifest_path'],'status':'PASS'}
    write(root/rel,json.dumps(obj,indent=2,sort_keys=True)+'\n')

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)/'repo'; shutil.copytree(SOURCE,root)
        # One explicit task/phase package.
        write(root/'Workplan/plan/PHASES.json',json.dumps({'phases':[{'phase_id':'PHASE_001','objective':'demo','depends_on':[],'architecture_bindings':[],'interface_bindings':[],'acceptance_criteria':[],'verification':[],'required_evidence':[]}]},indent=2)+'\n')
        write(root/'Workplan/tasks/TASK_001.md','# TASK_001\nphase_id: PHASE_001\nobjective: Fix A\ndepends_on: []\nauthorized_paths: [src/a.txt]\nrequired_context: []\narchitecture_bindings: []\ninterface_bindings: []\nacceptance_criteria: [A]\nverification: []\nrequired_evidence: []\nmax_repairs: 2\n')
        write(root/'Workplan/tasks/TASK_INDEX.md','# Task Index\n- TASK_001\n')
        sys.path.insert(0,str(root/'Workplan/scripts'))
        from _core.integrity import build_package_manifest
        man=build_package_manifest(); sp=root/'Workplan/control/STATE.json'; st=json.loads(sp.read_text())
        st.update({'active_cycle':'CYCLE_0001','lifecycle_stage':'PLAN_READY','project_state':'PLAN_READY','cycles':{'CYCLE_0001':{'cycle_id':'CYCLE_0001','scope':{'digest':'scope','revision_label':'SCOPE_001'},'ingest':{'package_digest':'ingest'},'planning':{'status':'PLAN_READY','candidate_package_digest':man['package_digest'],'task_count':1},'issues':[]}}})
        sp.write_text(json.dumps(st,indent=2,sort_keys=True)+'\n')
        run(root,'Workplan/scripts/tools/execution.py','start'); run(root,'Workplan/scripts/tools/execution.py','dispatch')
        # Initial Builder completes but has no evidence; gate fails, then deterministic escalation is requested.
        st=json.loads(sp.read_text()); meta=json.loads((root/'Workplan/work'/st['active_work']/'WORK.json').read_text()); write(root/'src/a.txt','initial bad\n')
        run(root,'Workplan/scripts/tools/work.py','complete','--generation',str(meta['generation']),'--note','failed implementation')
        run(root,'Workplan/scripts/tools/execution.py','complete','--evidence','Workplan/work/MISSING.json',ok=(2,))
        run(root,'Workplan/scripts/tools/execution.py','fail','--reason','deep implementation defect')
        st=json.loads(sp.read_text()); issue=st['cycles']['CYCLE_0001']['issues'][-1]; assert st['lifecycle_stage']=='DIAGNOSIS'

        # Diagnosis is reasoning-only and routes implementation defects to Recovery reasoning.
        d=json.loads(run(root,'Workplan/scripts/command.py','EXECUTE_DIAGNOSIS','--surface','EXTERNAL_AI').stdout); dgen=d['generation']
        write(root/'Workplan/diagnosis/DIAG.md','# Diagnosis\nRoot cause isolated.\n')
        run(root,'Workplan/scripts/tools/work.py','complete','--generation',str(dgen),'--note','diagnosis complete')
        run(root,'Workplan/scripts/tools/diagnosis.py','register','--classification','IMPLEMENTATION_DEFECT','--diagnosis','Workplan/diagnosis/DIAG.md')
        assert json.loads(sp.read_text())['lifecycle_stage']=='RECOVERY'

        # Recovery produces a contract only; it cannot directly pass the Task.
        r=json.loads(run(root,'Workplan/scripts/command.py','EXECUTE_RECOVERY','--surface','EXTERNAL_AI').stdout); rgen=r['generation']
        contract_rel='Workplan/recovery/RECOVERY_CONTRACT.json'; contract={
            'issue_id':issue['issue_id'],'task_id':'TASK_001','repair_objective':'correct A','affected_contracts':['TASK_001'],
            'authorized_paths':['src/a.txt'],'required_changes':['replace bad A'],'verification':[],'regression_verification':[],'completion_criteria':['Task Gate PASS']}
        write(root/contract_rel,json.dumps(contract,indent=2,sort_keys=True)+'\n')
        run(root,'Workplan/scripts/tools/work.py','complete','--generation',str(rgen),'--note','recovery contract ready')
        run(root,'Workplan/scripts/tools/recovery.py','register','--contract',contract_rel)
        st=json.loads(sp.read_text()); assert st['cycles']['CYCLE_0001']['execution']['tasks']['TASK_001']['status']=='PENDING'
        n=json.loads(run(root,'Workplan/scripts/tools/execution.py','next').stdout.splitlines()[-1]); assert n['action']=='DISPATCH_RECOVERY_TASK'
        run(root,'Workplan/scripts/tools/execution.py','dispatch')
        st=json.loads(sp.read_text()); recovery_attempt=st['active_attempt']; wid=st['active_work']; meta=json.loads((root/'Workplan/work'/wid/'WORK.json').read_text()); ticket=json.loads((root/meta['current_ticket_path']).read_text())
        assert meta['attempt_kind']=='RECOVERY' and ticket['ticket_kind']=='RECOVERY' and ticket['authorized_paths']==['src/a.txt']

        # Recovery Contract is immutable after ticket issue; resume compares the actual file digest.
        original=(root/contract_rel).read_text(); write(root/contract_rel,original+'\n')
        bad=run(root,'Workplan/scripts/tools/execution.py','resume',ok=(1,)); assert 'WORK_BINDING_MISMATCH' in bad.stdout+bad.stderr
        write(root/contract_rel,original)

        # Fresh Recovery Builder completes and still must pass normal Task/Phase gates.
        write(root/'src/a.txt','recovered\n'); run(root,'Workplan/scripts/tools/work.py','complete','--generation',str(meta['generation']),'--note','recovery implementation complete')
        evidence(root,'Workplan/work/RECOVERY_EVIDENCE.json'); run(root,'Workplan/scripts/tools/execution.py','complete','--evidence','Workplan/work/RECOVERY_EVIDENCE.json')
        st=json.loads(sp.read_text()); ex=st['cycles']['CYCLE_0001']['execution']; assert ex['attempts'][recovery_attempt]['status']=='PASS'
        resolved=next(x for x in st['cycles']['CYCLE_0001']['issues'] if x['issue_id']==issue['issue_id']); assert resolved['status']=='RESOLVED'
        n=json.loads(run(root,'Workplan/scripts/tools/execution.py','next').stdout.splitlines()[-1]); assert n['action']=='RUN_PHASE_GATE'
        run(root,'Workplan/scripts/tools/execution.py','phase-gate'); n=json.loads(run(root,'Workplan/scripts/tools/execution.py','next').stdout.splitlines()[-1]); assert n['action']=='START_EVALUATION'
    print('RECOVERY_SCENARIO_VALID: PASS')

if __name__=='__main__': main()
