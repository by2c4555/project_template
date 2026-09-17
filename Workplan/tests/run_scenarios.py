#!/usr/bin/env python3
from __future__ import annotations
import contextlib, io, json, os, runpy, shutil, sys, tempfile, types
from pathlib import Path
SOURCE=Path(__file__).resolve().parents[2]

def run(root,*args,ok=(0,)):
    script = root / args[0]
    stdout, stderr = io.StringIO(), io.StringIO()
    old_argv, old_cwd, old_path = sys.argv[:], os.getcwd(), sys.path[:]
    sys.argv = list(args); os.chdir(root); sys.path.insert(0, str(script.parent))
    rc = 0
    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                runpy.run_path(str(script), run_name='__main__')
            except SystemExit as e:
                if isinstance(e.code, int): rc = e.code
                elif e.code in (None, ''): rc = 0
                else:
                    rc = 1; print(e.code, file=sys.stderr)
    except BaseException as e:
        rc = 1; print(f'{type(e).__name__}: {e}', file=stderr)
    finally:
        sys.argv = old_argv; os.chdir(old_cwd); sys.path[:] = old_path
    result = types.SimpleNamespace(returncode=rc, stdout=stdout.getvalue(), stderr=stderr.getvalue())
    if rc not in ok: raise AssertionError(f"command failed {args}\nrc={rc}\nstdout={result.stdout}\nstderr={result.stderr}")
    return result

def write(p,text): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')
def cmd(root,command,surface='EXTERNAL_AI',tool='test',model='strong',ok=(0,)):
    return json.loads(run(root,'Workplan/scripts/command.py',command,'--surface',surface,'--tool',tool,'--model',model,ok=ok).stdout)

def evidence(root, rel):
    st=json.loads((root/'Workplan/control/STATE.json').read_text()); wid=st['last_completed_work']; meta=json.loads((root/'Workplan/work'/wid/'WORK.json').read_text())
    obj={'schema_version':1,'attempt_id':meta['attempt_id'],'task_id':meta['task_id'],'phase_id':meta['phase_id'],'generation':meta['generation'],'ticket_digest':meta['ticket_digest'],'verification':[],'artifacts':[],'mutation_manifest_path':meta['mutation_manifest_path'],'status':'PASS'}
    write(root/rel,json.dumps(obj,indent=2,sort_keys=True)+'\n'); return obj

def scenario():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)/'repo'; shutil.copytree(SOURCE,root)
        write(root/'Workplan/ingest/project_details.md', '''artifact_kind: PROJECT_DETAILS
artifact_status: READY_FOR_PLANNING
research_protocol: EXTERNAL_RESEARCH_PROTOCOL_V1
product_scope_unknowns: 0
supporting_files: [Workplan/docs/raw/REQ.md]

# Project Details

## Objective
Build the demo behavior requested by the user.

## Current State
The isolated test repository has no demo production artifact yet.

## Problem Statement
Create the bounded demo artifact and verify deterministic workflow execution.

## Functional Requirements
- FR-001: Build the demo artifact.

## Non-Functional Requirements
- NFR-001: Preserve Workplan authority boundaries.

## Constraints
- Use only the authorized Task paths.

## Interfaces
- Repository file output only.

## Acceptance Criteria
- AC-001: Required demo artifacts are created through passing Task/Phase gates.

## In Scope
- Demo artifacts A and B.

## Out of Scope
- Unrelated repository changes.

## Assumptions
- None.

## Resolved Unknowns
- Demo scope is fixed by this scenario.

## Remaining Non-Blocking Unknowns
- None.

## Source / Evidence Map
- USER_REQUIREMENT — Build demo — Workplan/docs/raw/REQ.md
''')
        write(root/'Workplan/ingest/docs/raw/REQ.md','# Requirement\nBuild demo.\n')
        run(root,'Workplan/scripts/tools/ingest.py','check'); run(root,'Workplan/scripts/tools/scope.py','import')
        c=cmd(root,'EXECUTE_PLANNING'); run(root,'Workplan/scripts/approve.py','--',c['challenge']); c=cmd(root,'EXECUTE_PLANNING'); assert c['generation']==1
        run(root,'Workplan/scripts/tools/work.py','checkpoint','--generation','1','--unit','ARCH','--next-unit','TASKS','--note','architecture fixed')
        c=cmd(root,'EXECUTE_PLANNING',tool='other',model='strong2'); assert c['mode']=='RESUME' and c['generation']==2
        bad=run(root,'Workplan/scripts/tools/work.py','checkpoint','--generation','1','--unit','OLD','--next-unit','OLD','--note','stale',ok=(1,)); assert 'STALE_GENERATION' in bad.stderr+bad.stdout
        write(root/'Workplan/plan/PHASES.json',json.dumps({'schema_version':1,'phases':[
          {'phase_id':'PHASE_001','objective':'foundation','depends_on':[],'architecture_bindings':[],'interface_bindings':[],'acceptance_criteria':[],'verification':[],'required_evidence':[]},
          {'phase_id':'PHASE_002','objective':'integration','depends_on':['PHASE_001'],'architecture_bindings':[],'interface_bindings':[],'acceptance_criteria':[],'verification':[],'required_evidence':[]}
        ]},indent=2)+'\n')
        write(root/'Workplan/tasks/TASK_001.md','# TASK_001\nstatus: IMMUTABLE_AFTER_APPROVAL\nphase_id: PHASE_001\nobjective: Create A\ndepends_on: []\nauthorized_paths: [src/a.txt]\nrequired_context: []\narchitecture_bindings: []\ninterface_bindings: []\nacceptance_criteria: [A exists]\nverification: []\nrequired_evidence: []\nmax_repairs: 2\n')
        write(root/'Workplan/tasks/TASK_002.md','# TASK_002\nstatus: IMMUTABLE_AFTER_APPROVAL\nphase_id: PHASE_002\nobjective: Create B\ndepends_on: [TASK_001]\nauthorized_paths: [src/b.txt]\nrequired_context: []\narchitecture_bindings: []\ninterface_bindings: []\nacceptance_criteria: [B exists]\nverification: []\nrequired_evidence: []\nmax_repairs: 2\n')
        write(root/'Workplan/tasks/TASK_INDEX.md','# Task Index\n\n- TASK_001\n- TASK_002\n'); write(root/'Workplan/plan/IMPLEMENTATION_PLAN.md','# Implementation Plan\n\nstatus: READY\n')
        run(root,'Workplan/scripts/tools/work.py','checkpoint','--generation','2','--unit','TASKS','--next-unit','DONE','--note','contracts compiled'); run(root,'Workplan/scripts/tools/work.py','complete','--generation','2','--note','planning complete')
        run(root,'Workplan/scripts/tools/planning.py','mark-ready'); cmd(root,'EXECUTE_IMPLEMENTATION',surface='VS_CODE'); run(root,'Workplan/scripts/tools/execution.py','start')
        n=json.loads(run(root,'Workplan/scripts/tools/execution.py','next').stdout.splitlines()[-1]); assert n['action']=='DISPATCH_TASK' and n['task']=='TASK_001'
        run(root,'Workplan/scripts/tools/execution.py','dispatch')
        st=json.loads((root/'Workplan/control/STATE.json').read_text()); wid=st['active_work']; mpath=root/'Workplan/work'/wid/'WORK.json'; meta=json.loads(mpath.read_text()); original_binding=dict(meta['input_bindings']); attempt1=meta['attempt_id']
        # Context grants persist and never expand production write authority.
        run(root,'Workplan/scripts/tools/work.py','request-context','--reason','ARCHITECTURE'); meta=json.loads(mpath.read_text()); ticket=json.loads((root/meta['current_ticket_path']).read_text()); assert 'Workplan/compiled/ARCHITECTURE.md' in ticket['granted_context'] and ticket['authorized_paths']==['src/a.txt']
        # Approved contract mutation blocks resume and does not overwrite original binding.
        taskp=root/'Workplan/tasks/TASK_001.md'; original=taskp.read_text(); taskp.write_text(original.replace('Create A','Create changed A'))
        bad=run(root,'Workplan/scripts/tools/work.py','acquire','--role','BUILDER','--tool','x','--model','x','--task','TASK_001',ok=(1,)); assert 'WORK_BINDING_MISMATCH' in bad.stderr+bad.stdout
        assert json.loads(mpath.read_text())['input_bindings']==original_binding; taskp.write_text(original)
        # Normal resume increments generation; stale session is fenced.
        run(root,'Workplan/scripts/tools/execution.py','resume'); meta=json.loads(mpath.read_text()); assert meta['generation']==2
        bad=run(root,'Workplan/scripts/tools/work.py','checkpoint','--generation','1','--unit','OLD','--next-unit','OLD','--note','stale',ok=(1,)); assert 'STALE_GENERATION' in bad.stderr+bad.stdout
        # Unauthorized create is detected by the deterministic Task Gate.
        write(root/'src/a.txt','a1\n'); write(root/'rogue.txt','unauthorized\n'); run(root,'Workplan/scripts/tools/work.py','complete','--generation','2','--note','attempt complete')
        evidence(root,'Workplan/work/EVIDENCE_1.json'); bad=run(root,'Workplan/scripts/tools/execution.py','complete','--evidence','Workplan/work/EVIDENCE_1.json',ok=(2,)); assert 'unauthorized production mutation' in bad.stdout
        # Local repair gets a fresh Attempt bound to its parent; cumulative Task baseline prevents laundering.
        r=run(root,'Workplan/scripts/tools/execution.py','repair'); st=json.loads((root/'Workplan/control/STATE.json').read_text()); wid2=st['active_work']; meta2=json.loads((root/'Workplan/work'/wid2/'WORK.json').read_text()); assert meta2['attempt_id']!=attempt1 and meta2['parent_attempt_id']==attempt1 and meta2['attempt_kind']=='REPAIR'
        (root/'rogue.txt').unlink(); write(root/'src/a.txt','a2\n'); run(root,'Workplan/scripts/tools/work.py','complete','--generation','1','--note','repaired'); evidence(root,'Workplan/work/EVIDENCE_1R.json'); run(root,'Workplan/scripts/tools/execution.py','complete','--evidence','Workplan/work/EVIDENCE_1R.json')
        n=json.loads(run(root,'Workplan/scripts/tools/execution.py','next').stdout.splitlines()[-1]); assert n['action']=='RUN_PHASE_GATE' and n['phase']=='PHASE_001'
        run(root,'Workplan/scripts/tools/execution.py','phase-gate')
        n=json.loads(run(root,'Workplan/scripts/tools/execution.py','next').stdout.splitlines()[-1]); assert n['action']=='DISPATCH_TASK' and n['task']=='TASK_002'
        run(root,'Workplan/scripts/tools/execution.py','dispatch'); st=json.loads((root/'Workplan/control/STATE.json').read_text()); meta=json.loads((root/'Workplan/work'/st['active_work']/'WORK.json').read_text()); write(root/'src/b.txt','b\n'); run(root,'Workplan/scripts/tools/work.py','complete','--generation','1','--note','B complete'); evidence(root,'Workplan/work/EVIDENCE_2.json'); run(root,'Workplan/scripts/tools/execution.py','complete','--evidence','Workplan/work/EVIDENCE_2.json'); run(root,'Workplan/scripts/tools/execution.py','phase-gate')
        n=json.loads(run(root,'Workplan/scripts/tools/execution.py','next').stdout.splitlines()[-1]); assert n['action']=='START_EVALUATION'; run(root,'Workplan/scripts/tools/execution.py','finalize')
        c=cmd(root,'EXECUTE_EVALUATION'); run(root,'Workplan/scripts/tools/work.py','complete','--generation','1','--note','evaluation complete')
        st=json.loads((root/'Workplan/control/STATE.json').read_text()); scope=st['cycles'][st['active_cycle']]['scope']; write(root/'Workplan/evaluation/Evaluation_V1.md','# Evaluation\nPASS\n'); write(root/'Workplan/evaluation/PROJECT_COMPLETION_REPORT.md',f"# Completion\n{scope['revision_label']}\n{scope['digest']}\n")
        run(root,'Workplan/scripts/tools/evaluation.py','finalize','--result','PASS','--report','Workplan/evaluation/Evaluation_V1.md','--completion-report','Workplan/evaluation/PROJECT_COMPLETION_REPORT.md')
        st=json.loads((root/'Workplan/control/STATE.json').read_text()); assert st['project_state']=='CLOSED_VALIDATED'
    print('SCENARIO_VALID: PASS')
if __name__=='__main__': scenario()
