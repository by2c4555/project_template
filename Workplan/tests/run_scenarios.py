#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
SOURCE=Path(__file__).resolve().parents[2]

def run(root,*args,ok=(0,)):
    p=subprocess.run([sys.executable,*args],cwd=root,text=True,capture_output=True)
    if p.returncode not in ok:
        raise AssertionError(f"command failed {args}\nrc={p.returncode}\nstdout={p.stdout}\nstderr={p.stderr}")
    return p

def write(p,text): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')
def cmd(root,command,surface='EXTERNAL_AI',tool='test',model='strong',ok=(0,)):
    p=run(root,'Workplan/scripts/command.py',command,'--surface',surface,'--tool',tool,'--model',model,ok=ok)
    return json.loads(p.stdout)

def scenario():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)/'repo'; shutil.copytree(SOURCE,root)
        # Valid Research ingest with canonical supporting path.
        write(root/'Workplan/ingest/project_details.md','''artifact_kind: PROJECT_DETAILS\nartifact_status: READY_FOR_PLANNING\nscope_title: Demo\nbaseline_ref: main\nproduct_scope_unknowns: 0\nsupporting_files: [Workplan/docs/raw/REQ.md]\n''')
        write(root/'Workplan/ingest/docs/raw/REQ.md','# Requirement\nBuild demo.\n')
        r=run(root,'Workplan/scripts/tools/ingest.py','check'); assert 'INGEST_VALID: PASS' in r.stdout
        run(root,'Workplan/scripts/tools/scope.py','import')
        st=json.loads((root/'Workplan/control/STATE.json').read_text()); cid=st['active_cycle']; assert st['lifecycle_stage']=='PLANNING'; assert st['cycles'][cid]['ingest']['package_digest']!=st['cycles'][cid]['scope']['digest']
        # Planning INIT is command-gated; human authorizes the new cost envelope.
        c=cmd(root,'EXECUTE_PLANNING'); assert c['status']=='APPROVAL_REQUIRED'
        run(root,'Workplan/scripts/approve.py','--',c['challenge'])
        c=cmd(root,'EXECUTE_PLANNING'); assert c['status']=='ACCEPTED' and c['role']=='PLANNING' and c['generation']==1
        run(root,'Workplan/scripts/tools/work.py','checkpoint','--generation','1','--unit','ARCH','--next-unit','TASKS','--note','architecture fixed')
        # Provider handoff is an approval-free RESUME and fences the old generation.
        c=cmd(root,'EXECUTE_PLANNING',tool='other',model='strong2'); assert c['mode']=='RESUME' and c['generation']==2
        bad=run(root,'Workplan/scripts/tools/work.py','checkpoint','--generation','1','--unit','OLD','--next-unit','OLD','--note','stale',ok=(1,)); assert 'STALE_GENERATION' in bad.stderr+bad.stdout
        # Compile one bounded Task, then finish Planning.
        write(root/'Workplan/tasks/TASK_001.md','''# TASK_001\n\nstatus: IMMUTABLE_AFTER_APPROVAL\nobjective: Create demo file\ndepends_on: []\nauthorized_paths: [src/demo.txt]\ncontext_manifest: []\nacceptance_criteria: [demo exists]\nverification_commands: []\nmax_repairs: 2\n''')
        write(root/'Workplan/tasks/TASK_INDEX.md','# Task Index\n\n- TASK_001\n')
        write(root/'Workplan/plan/IMPLEMENTATION_PLAN.md','# Implementation Plan\n\nstatus: READY\n')
        run(root,'Workplan/scripts/tools/work.py','checkpoint','--generation','2','--unit','TASKS','--next-unit','DONE','--note','task compiled')
        run(root,'Workplan/scripts/tools/work.py','complete','--generation','2','--note','planning complete')
        r=run(root,'Workplan/scripts/tools/planning.py','mark-ready'); assert 'EXECUTE_IMPLEMENTATION' in r.stdout
        st=json.loads((root/'Workplan/control/STATE.json').read_text()); assert st['lifecycle_stage']=='PLAN_READY'; assert 'archive/' in st['cycles'][cid]['ingest']['source_root']; assert not (root/'Workplan/ingest/project_details.md').exists()
        # Deterministic implementation intent remains VS Code-only and execution.py owns Task routing.
        c=cmd(root,'EXECUTE_IMPLEMENTATION',surface='VS_CODE'); assert c['status']=='ACCEPTED'
        run(root,'Workplan/scripts/tools/execution.py','start')
        r=run(root,'Workplan/scripts/tools/execution.py','next'); assert 'DISPATCH_TASK' in r.stdout and 'TASK_001' in r.stdout
        r=run(root,'Workplan/scripts/tools/execution.py','dispatch'); assert 'TASK_001' in r.stdout and 'generation' in r.stdout
        # Interrupted Builder acquisition increments generation; stale builder is fenced.
        r=run(root,'Workplan/scripts/tools/execution.py','resume'); assert '"generation": 2' in r.stdout
        bad=run(root,'Workplan/scripts/tools/work.py','checkpoint','--generation','1','--unit','WRITE','--next-unit','VERIFY','--note','old session',ok=(1,)); assert 'STALE_GENERATION' in bad.stderr+bad.stdout
        # Worktree reconciliation is machine-computed.
        write(root/'src/demo.txt','hello\n')
        r=run(root,'Workplan/scripts/resume.py'); assert 'RECONCILE_ACTIVE_UNIT' in r.stdout
        run(root,'Workplan/scripts/tools/work.py','checkpoint','--generation','2','--unit','WRITE','--next-unit','VERIFY','--note','demo created')
        r=run(root,'Workplan/scripts/resume.py'); assert '"status": "CLEAN"' in r.stdout
        write(root/'Workplan/work/evidence.txt','verified\n')
        run(root,'Workplan/scripts/tools/work.py','complete','--generation','2','--note','task verified')
        run(root,'Workplan/scripts/tools/execution.py','complete','--evidence','Workplan/work/evidence.txt')
        r=run(root,'Workplan/scripts/tools/execution.py','next'); assert 'START_EVALUATION' in r.stdout
        run(root,'Workplan/scripts/tools/execution.py','finalize')
        # Evaluation is selected through the public command protocol and exact Completion binding remains required.
        c=cmd(root,'EXECUTE_EVALUATION'); assert c['status']=='ACCEPTED' and c['role']=='EVALUATION'
        run(root,'Workplan/scripts/tools/work.py','checkpoint','--generation','1','--unit','VERIFY','--next-unit','DONE','--note','actual behavior verified')
        run(root,'Workplan/scripts/tools/work.py','complete','--generation','1','--note','evaluation complete')
        scope=st['cycles'][cid]['scope']; write(root/'Workplan/evaluation/Evaluation_V1.md','# Evaluation\nPASS\n'); write(root/'Workplan/evaluation/PROJECT_COMPLETION_REPORT.md',f"# Completion\n{scope['revision_label']}\n{scope['digest']}\n")
        run(root,'Workplan/scripts/tools/evaluation.py','finalize','--result','PASS','--report','Workplan/evaluation/Evaluation_V1.md','--completion-report','Workplan/evaluation/PROJECT_COMPLETION_REPORT.md')
        st=json.loads((root/'Workplan/control/STATE.json').read_text()); assert st['project_state']=='CLOSED_VALIDATED'
    print('SCENARIO_VALID: PASS')

if __name__=='__main__': scenario()
