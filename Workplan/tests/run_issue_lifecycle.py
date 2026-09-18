#!/usr/bin/env python3
from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2]


def run(root: Path, *args: str):
    env = dict(os.environ); env['PYTHONDONTWRITEBYTECODE'] = '1'
    return subprocess.run([sys.executable, *args], cwd=root, text=True, capture_output=True, env=env, timeout=10)


def prepare(root: Path, classification: str):
    state_path = root / 'Workplan/control/STATE.json'
    st = json.loads(state_path.read_text(encoding='utf-8'))
    issue = {
        'issue_id':'ISSUE_0001','origin_type':'EXECUTION','task':'TASK_001','phase_id':'PHASE_001',
        'reason':'synthetic failure','status':'AWAITING_DIAGNOSIS','classification':None,'created_at':'2026-09-18T00:00:00Z'
    }
    st.update({
        'active_cycle':'CYCLE_0001','active_work':None,'last_completed_work':'WORK_0001',
        'project_state':'DIAGNOSIS','lifecycle_stage':'DIAGNOSIS','next_action':'EXECUTE_DIAGNOSIS',
    })
    st['cycles']={'CYCLE_0001':{
        'cycle_id':'CYCLE_0001','status':'EXECUTION',
        'scope':{'revision_label':'SCOPE_001','digest':'scope'},
        'planning':{'candidate_package_digest':'old-plan'},
        'execution':{'active_issue':'ISSUE_0001','tasks':{}},
        'issues':[issue], 'evaluation':{'attempts':[]},
    }}
    state_path.write_text(json.dumps(st, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    work = root / 'Workplan/work/WORK_0001'; work.mkdir(parents=True, exist_ok=True)
    (work/'WORK.json').write_text(json.dumps({'work_id':'WORK_0001','role':'DIAGNOSIS','status':'COMPLETED'}, indent=2)+'\n', encoding='utf-8')
    diag = root / f'Workplan/diagnosis/{classification}.md'; diag.parent.mkdir(parents=True, exist_ok=True); diag.write_text('# Diagnosis\n', encoding='utf-8')
    return state_path, diag


def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)/'repo'; shutil.copytree(SOURCE,root)
        state,diag=prepare(root,'PLAN_DEFECT')
        r=run(root,'Workplan/scripts/tools/diagnosis.py','register','--classification','PLAN_DEFECT','--diagnosis',str(diag.relative_to(root)))
        assert r.returncode == 0, r.stdout+r.stderr
        st=json.loads(state.read_text()); issue=st['cycles']['CYCLE_0001']['issues'][0]
        assert st['lifecycle_stage']=='PLANNING' and st['next_action']=='EXECUTE_PLANNING'
        assert issue['status']=='PLAN_REVISION_REQUIRED' and issue['previous_planning_package_digest']=='old-plan'
        assert st['cycles']['CYCLE_0001']['execution']['active_issue'] is None

    with tempfile.TemporaryDirectory() as td:
        root=Path(td)/'repo'; shutil.copytree(SOURCE,root)
        state,diag=prepare(root,'SCOPE_DEFECT')
        r=run(root,'Workplan/scripts/tools/diagnosis.py','register','--classification','SCOPE_DEFECT','--diagnosis',str(diag.relative_to(root)))
        assert r.returncode == 0, r.stdout+r.stderr
        st=json.loads(state.read_text()); issue=st['cycles']['CYCLE_0001']['issues'][0]
        assert issue['status']=='OWNER_ACTION_REQUIRED'
        assert st['next_action']=='OWNER_OR_EXTERNAL_RESOLUTION_REQUIRED'
        r=run(root,'Workplan/scripts/command.py','WORKPLAN_NEXT','--surface','EXTERNAL_AI','--tool','test','--model','test')
        assert r.returncode == 0, r.stdout+r.stderr
        payload=json.loads(r.stdout)
        cont=payload['continuation']
        assert cont['next_surface']=='HUMAN' and cont['next_command'] is None

    print('ISSUE_LIFECYCLE_VALID: PASS')


if __name__ == '__main__':
    main()
