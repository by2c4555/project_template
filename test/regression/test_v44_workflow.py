import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[2]


def run(root, *args):
    return subprocess.run(
        ['python', *args], cwd=root, text=True,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )


def import_ws(root):
    path = root / 'scripts/workflow_state.py'
    spec = importlib.util.spec_from_file_location(f'workflow_state_{id(root)}', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class V44WorkflowRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name) / 'repo'
        shutil.copytree(
            SOURCE_ROOT, cls.root,
            ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'project_template-v4.4.0.zip')
        )

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def setUp(self):
        ws = import_ws(self.root)
        ws.save_state(ws.initial_state())
        ws.LEDGER_PATH.write_text('', encoding='utf-8')
        ws.reset_package_workspace('none', 'none')
        for d in [
            self.root/'EXECUTE/control/approvals',
            self.root/'EXECUTE/control/recovery_approvals',
            self.root/'EXECUTE/control/manifests',
        ]:
            for item in d.glob('*.json'):
                item.unlink()
        h = self.root/'EXECUTE/history/cycles'
        if h.exists():
            shutil.rmtree(h)
        for item in (self.root/'EXECUTE/issues').glob('ISSUE_[0-9]*.md'):
            item.unlink()
        for item in (self.root/'EXECUTE/docs/raw').glob('source-*.md'):
            item.unlink()

    def write_handoff(self, title='Test Scope', suffix='v1', supporting=False):
        files=[]
        if supporting:
            raw=self.root/f'EXECUTE/docs/raw/source-{suffix}.md'
            raw.parent.mkdir(parents=True,exist_ok=True)
            raw.write_text(f'# Source {suffix}\nverified evidence\n',encoding='utf-8')
            files=[str(raw.relative_to(self.root)).replace('\\','/')]
        inline='['+', '.join(files)+']'
        text=(
            '---\n'
            'artifact_kind: PROJECT_DETAILS\n'
            'artifact_status: READY_FOR_PLANNING\n'
            f'scope_title: {title}\n'
            'baseline_ref: none\n'
            'product_scope_unknowns: 0\n'
            f'supporting_files: {inline}\n'
            '---\n\n'
            '# Project Details\n\n'
            f'## 1. Executive Handoff\n{title} {suffix}\n\n'
            f'## 3. Change Summary / Delta\n- change {suffix}\n\n'
            '## 4. Requirements\n- REQ-001 — required\n\n'
            '## 5. Scope\n### In Scope\n- feature\n### Out of Scope / Non-Goals\n- none\n### Explicitly Unchanged\n- none\n\n'
            '## 6. Constraints and Invariants\n- preserve baseline\n\n'
            '## 7. Confirmed Decisions\n- confirmed\n\n'
            '## 8. Implementation-Relevant Facts\n- FACT-001\n\n'
            '## 9. External / Reference Findings\n- none\n\n'
            '## 10. Known Risks\n- none\n\n'
            '## 11. Remaining Unknowns\n### Product / Scope Unknowns\nNONE\n### Technical Unknowns for External Agent Planning\n- TECH-001\n\n'
            '## 12. Repository Investigation Targets\n- INV-001\n\n'
            '## 13. Success Criteria\n- SC-001 -> REQ-001\n\n'
            '## 14. External Agent Context Map\n### P0 — Read During Planning\n- none\n\n'
            '## 15. Supporting Research Index\n- none\n'
        )
        (self.root/'EXECUTE/project_details.md').write_text(text,encoding='utf-8')

    def start_cycle(self, title='Test cycle', suffix='v1', supporting=False):
        self.write_handoff(title='Test Scope', suffix=suffix, supporting=supporting)
        p = run(self.root, 'scripts/start_cycle.py', '--title', title)
        self.assertEqual(p.returncode, 0, p.stdout)
        return p

    def complete_external_work(self, role):
        b=run(self.root,'scripts/agent_work.py','begin','--role',role,'--tool','test-agent','--model','test-model')
        self.assertEqual(b.returncode,0,b.stdout)
        st=json.loads((self.root/'EXECUTE/control/STATE.json').read_text())
        seq=st['active_external_work']['checkpoint_seq']
        c=run(self.root,'scripts/agent_work.py','complete','--expected-seq',str(seq),'--unit','FINAL','--note',f'{role} test work complete','--tool','test-agent','--model','test-model')
        self.assertEqual(c.returncode,0,c.stdout)

    def compile_package(self, task_count=1, max_repairs=2):
        ws = import_ws(self.root)
        state = ws.load_state(); cid, cycle = ws.active_cycle(state); p = cycle['planning']
        pv, rev = p['version'], p['revision_label']
        for cp in sorted((self.root/'EXECUTE/compiled').glob('*.md')):
            cp.write_text(
                f'---\nartifact_kind: {cp.stem}\nartifact_status: COMPILED\nplanning_version: {pv}\nplanning_revision: {rev}\n---\n\n# {cp.stem}\ncompiled\n',
                encoding='utf-8'
            )
        (self.root/'EXECUTE/plan/IMPLEMENTATION_PLAN.md').write_text(
            f'---\nartifact_kind: IMPLEMENTATION_PLAN\nartifact_status: COMPILED\nplanning_version: {pv}\nplanning_revision: {rev}\n---\n\n# Plan\nready\n', encoding='utf-8'
        )
        task_lines=[]
        for i in range(1, task_count+1):
            tid=f'TASK_{i:03d}'
            task_lines.append(f'- {tid}')
            (self.root/f'EXECUTE/tasks/{tid}.md').write_text(
                f'''---
task_id: {tid}
artifact_status: COMPILED
planning_version: {pv}
planning_revision: {rev}
phase: PHASE_01
builder: Builder100K
depends_on: []
---

# {tid}

## Context Manifest
### mandatory
- `EXECUTE/compiled/GLOBAL_CONSTRAINTS.md`

## Allowed Scope
### WRITE
- `src/file_{i}.txt`

## Acceptance Criteria
- AC-01

## Verification
`true`

## Local Repair Budget
```yaml
max_evidence_driven_repair_attempts: {max_repairs}
```
''', encoding='utf-8'
            )
        (self.root/'EXECUTE/tasks/TASK_INDEX.md').write_text(
            f'---\nartifact_kind: TASK_INDEX\nartifact_status: COMPILED\nplanning_version: {pv}\nplanning_revision: {rev}\n---\n\n# Tasks\n'+'\n'.join(task_lines)+'\n', encoding='utf-8'
        )
        for cmd in [
            ['scripts/planning_gate.py','set-material-zero'],
            ['scripts/planning_gate.py','authorize-expansion'],
        ]:
            q=run(self.root,*cmd); self.assertEqual(q.returncode,0,q.stdout)
        self.complete_external_work('PLANNING')
        q=run(self.root,'scripts/planning_gate.py','mark-plan-ready'); self.assertEqual(q.returncode,0,q.stdout)
        return pv, rev

    def force_test_approval(self):
        ws=import_ws(self.root); state=ws.load_state(); cid,cycle=ws.active_cycle(state); p=cycle['planning']; scope=cycle['scope']
        manifest=ws.build_package_manifest(p['version'],p['revision_label'])
        approval_id='APPROVAL_TEST'
        mp=ws.manifest_path_for(approval_id); ws.write_json(mp,manifest)
        approval={
            'approval_id':approval_id,'cycle_id':cid,'status':'ACTIVE',
            'scope_revision':scope['revision_label'],'scope_digest':scope['digest'],'scope_snapshot':scope['snapshot_path'],
            'planning_version':p['version'],'planning_revision':p['revision_label'],'package_digest':manifest['package_digest'],
            'task_count':manifest['task_count'],'manifest_path':str(mp.relative_to(self.root)).replace('\\','/'),
            'human_interactive':True,
        }
        tasks={}
        for c in manifest['task_contracts']:
            tasks[c['task_id']]={
                'status':'PENDING','contract_path':c['path'],'dependencies':c['depends_on'],'dispatch_count':0,
                'repair_attempts':0,'max_repairs':c.get('max_repairs') if c.get('max_repairs') is not None else 2,
                'evidence':None,'recovery':None,
            }
        cycle['approval']=approval; p['status']='APPROVED'; p['package_status']='APPROVED'
        cycle['execution']={
            'version':'Execution_Test','status':'READY','bound_scope_revision':scope['revision_label'],'approved_scope_digest':scope['digest'],
            'bound_planning_version':p['version'],'bound_planning_revision':p['revision_label'],'approval_id':approval_id,
            'approved_package_digest':manifest['package_digest'],'tasks':tasks,'active_task':None,'active_issue':None,'last_resolved_issue':None,
            'manager_batch':{'number':1,'dispatches':0,'max_dispatches':state['runtime_policy']['manager_max_task_dispatches_per_batch'],'reset_required':False},
            'recovery':{'status':'NOT_ACTIVE','diagnosis':None,'resolution':None,'verification':None,'resume_authorized':False,'next_task':None,'recovery_baseline':None},
        }
        cycle['status']='EXECUTION'; cycle['lifecycle_stage']='EXECUTION'; state['project_state']='EXECUTION'; ws.save_state(state)
        return manifest

    def evidence(self, tid):
        p=self.root/f'EXECUTE/execution/evidence/{tid}.md'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text('# evidence\nPASS\n',encoding='utf-8')
        return str(p.relative_to(self.root)).replace('\\','/')

    def test_incomplete_project_details_blocks_cycle(self):
        (self.root/'EXECUTE/project_details.md').write_text('---\nartifact_kind: PROJECT_DETAILS\nartifact_status: INCOMPLETE\nscope_title: test\nproduct_scope_unknowns: 1\nsupporting_files: []\n---\n',encoding='utf-8')
        p=run(self.root,'scripts/start_cycle.py','--title','Blocked')
        self.assertNotEqual(p.returncode,0); self.assertIn('READY_FOR_PLANNING',p.stdout)

    def test_missing_supporting_file_blocks_cycle(self):
        self.write_handoff()
        t=(self.root/'EXECUTE/project_details.md').read_text(encoding='utf-8').replace('supporting_files: []','supporting_files: [EXECUTE/docs/raw/missing.md]')
        (self.root/'EXECUTE/project_details.md').write_text(t,encoding='utf-8')
        p=run(self.root,'scripts/start_cycle.py')
        self.assertNotEqual(p.returncode,0); self.assertIn('supporting file missing',p.stdout)

    def test_scope_snapshot_is_immutable_when_root_handoff_changes(self):
        self.start_cycle(suffix='v1',supporting=True)
        ws=import_ws(self.root); st=ws.load_state(); cid,cy=ws.active_cycle(st); scope=cy['scope']; snap=self.root/scope['snapshot_path']/'EXECUTE/project_details.md'
        before=snap.read_text(encoding='utf-8')
        self.write_handoff(title='Changed Root',suffix='v2',supporting=False)
        self.assertEqual(snap.read_text(encoding='utf-8'),before)
        self.assertEqual(ws.verify_active_scope(cy),[])

    def test_import_scope_revisions_planning_and_invalidates_plan_ready(self):
        self.start_cycle(); self.compile_package()
        ws=import_ws(self.root); st=ws.load_state(); cid,cy=ws.active_cycle(st); old_scope=cy['scope']['digest']; old_rev=cy['planning']['revision_label']
        self.write_handoff(title='Updated Scope',suffix='v2')
        p=run(self.root,'scripts/import_scope.py','--reason','new confirmed feature')
        self.assertEqual(p.returncode,0,p.stdout)
        st=json.loads((self.root/'EXECUTE/control/STATE.json').read_text()); cy=st['cycles'][cid]
        self.assertEqual(cy['scope']['revision_label'],'SCOPE_002'); self.assertNotEqual(cy['scope']['digest'],old_scope)
        self.assertEqual(cy['planning']['status'],'IN_PROGRESS'); self.assertNotEqual(cy['planning']['revision_label'],old_rev)
        self.assertIsNone(cy['planning']['candidate_package_digest'])

    def test_scope_change_after_approval_routes_to_replan(self):
        self.start_cycle(); self.compile_package(); self.force_test_approval()
        self.write_handoff(title='Changed Approved Scope',suffix='v2')
        p=run(self.root,'scripts/import_scope.py','--reason','material scope change')
        self.assertEqual(p.returncode,0,p.stdout); self.assertIn('REPLAN_REQUIRED',p.stdout)
        st=json.loads((self.root/'EXECUTE/control/STATE.json').read_text()); cy=st['cycles'][st['active_cycle']]
        self.assertEqual(cy['status'],'REPLAN_REQUIRED'); self.assertIsNone(cy['approval'])
        self.assertTrue(cy['approval_history']); self.assertEqual(cy['approval_history'][-1]['status'],'SUPERSEDED_BY_SCOPE_CHANGE')
        q=run(self.root,'scripts/start_replan.py')
        self.assertEqual(q.returncode,0,q.stdout)
        st=json.loads((self.root/'EXECUTE/control/STATE.json').read_text()); cy=st['cycles'][st['active_cycle']]
        self.assertEqual(cy['status'],'PLANNING'); self.assertEqual(cy['planning']['based_on_scope_revision'],'SCOPE_002')

    def test_material_unknown_hard_stop_blocks_expansion(self):
        self.start_cycle()
        p=run(self.root,'scripts/planning_gate.py','hold-material-feedback','--unknowns','2')
        self.assertEqual(p.returncode,0,p.stdout); self.assertIn('HARD_STOP_REQUIRED: true',p.stdout)
        q=run(self.root,'scripts/planning_gate.py','authorize-expansion')
        self.assertNotEqual(q.returncode,0); self.assertIn('material_unknowns',q.stdout)

    def test_plan_ready_chat_cannot_noninteractively_approve(self):
        self.start_cycle(); self.compile_package()
        before=json.loads((self.root/'EXECUTE/control/STATE.json').read_text())
        p=run(self.root,'scripts/approve_plan.py')
        self.assertNotEqual(p.returncode,0); self.assertIn('interactive TTY',p.stdout)
        after=json.loads((self.root/'EXECUTE/control/STATE.json').read_text())
        cid=after['active_cycle']; self.assertEqual(after['cycles'][cid]['planning']['status'],'PLAN_READY')
        self.assertIsNone(after['cycles'][cid]['approval'])
        self.assertEqual(before['cycles'][cid]['planning']['candidate_package_digest'], after['cycles'][cid]['planning']['candidate_package_digest'])

    def test_package_mutation_blocks_dispatch(self):
        self.start_cycle(); self.compile_package(); self.force_test_approval()
        task=self.root/'EXECUTE/tasks/TASK_001.md'; task.write_text(task.read_text()+'\nmutated\n',encoding='utf-8')
        p=run(self.root,'scripts/execution_gate.py','begin-task','TASK_001')
        self.assertNotEqual(p.returncode,0); self.assertIn('PACKAGE_INTEGRITY: FAIL',p.stdout)

    def test_scope_snapshot_mutation_blocks_dispatch(self):
        self.start_cycle(); self.compile_package(); self.force_test_approval()
        ws=import_ws(self.root); st=ws.load_state(); _,cy=ws.active_cycle(st); snap=self.root/cy['scope']['snapshot_path']/'EXECUTE/project_details.md'
        snap.write_text(snap.read_text()+'\nmutated\n',encoding='utf-8')
        p=run(self.root,'scripts/execution_gate.py','begin-task','TASK_001')
        self.assertNotEqual(p.returncode,0); self.assertIn('SCOPE_INTEGRITY: FAIL',p.stdout)

    def test_repair_budget_is_machine_counted(self):
        self.start_cycle(); self.compile_package(max_repairs=2); self.force_test_approval()
        b=run(self.root,'scripts/execution_gate.py','begin-task','TASK_001'); self.assertEqual(b.returncode,0,b.stdout)
        for _ in range(2):
            p=run(self.root,'scripts/execution_gate.py','authorize-repair','TASK_001'); self.assertEqual(p.returncode,0,p.stdout)
        p=run(self.root,'scripts/execution_gate.py','authorize-repair','TASK_001')
        self.assertNotEqual(p.returncode,0); self.assertIn('REPAIR_BUDGET_EXHAUSTED',p.stdout)

    def test_manager_batch_forces_context_reset(self):
        self.start_cycle(); self.compile_package(task_count=3); self.force_test_approval()
        ws=import_ws(self.root); st=ws.load_state(); _,cy=ws.active_cycle(st); cy['execution']['manager_batch']['max_dispatches']=2; ws.save_state(st)
        for tid in ['TASK_001','TASK_002']:
            p=run(self.root,'scripts/execution_gate.py','begin-task',tid); self.assertEqual(p.returncode,0,p.stdout)
            ev=self.evidence(tid)
            p=run(self.root,'scripts/execution_gate.py','complete-task',tid,'--evidence',ev); self.assertEqual(p.returncode,0,p.stdout)
        p=run(self.root,'scripts/execution_gate.py','begin-task','TASK_003')
        self.assertNotEqual(p.returncode,0); self.assertIn('MANAGER_CONTEXT_RESET_REQUIRED',p.stdout)
        q=run(self.root,'scripts/reset_manager_batch.py'); self.assertNotEqual(q.returncode,0); self.assertIn('interactive TTY',q.stdout)

    def test_new_cycle_does_not_inherit_approval(self):
        self.start_cycle(); self.compile_package(); self.force_test_approval()
        ws=import_ws(self.root); st=ws.load_state(); cid,cy=ws.active_cycle(st); cy['status']='CLOSED_VALIDATED'; cy['lifecycle_stage']='AWAITING_NEW_SCOPE'; st['project_state']='AWAITING_NEW_SCOPE'; ws.save_state(st)
        self.write_handoff(title='Next Scope',suffix='v2')
        p=run(self.root,'scripts/start_cycle.py','--title','Next')
        self.assertEqual(p.returncode,0,p.stdout)
        st=json.loads((self.root/'EXECUTE/control/STATE.json').read_text()); new=st['cycles'][st['active_cycle']]
        self.assertEqual(new['status'],'PLANNING'); self.assertIsNone(new['approval']); self.assertIsNone(new['execution']); self.assertNotEqual(st['active_cycle'],cid)
        self.assertEqual(new['scope']['revision_label'],'SCOPE_001')

    def test_open_cycle_blocks_new_cycle(self):
        self.start_cycle()
        self.write_handoff(title='Second',suffix='v2')
        p=run(self.root,'scripts/start_cycle.py')
        self.assertNotEqual(p.returncode,0); self.assertIn('only CLOSED_VALIDATED',p.stdout)

    def test_evaluation_requires_human_tty(self):
        self.start_cycle(); self.compile_package(); self.force_test_approval()
        ws=import_ws(self.root); st=ws.load_state(); _,cy=ws.active_cycle(st); ex=cy['execution']
        for t in ex['tasks'].values(): t['status']='PASS'
        ex['status']='AWAITING_EVALUATION'; cy['status']='EXECUTION_COMPLETE'; cy['lifecycle_stage']='AWAITING_EVALUATION_AUTHORIZATION'; ws.save_state(st)
        p=run(self.root,'scripts/start_evaluation.py')
        self.assertNotEqual(p.returncode,0); self.assertIn('interactive TTY',p.stdout)

    def test_execution_finalize_requires_bound_complete_summary(self):
        self.start_cycle(); self.compile_package(); self.force_test_approval()
        ws=import_ws(self.root); st=ws.load_state(); cid,cy=ws.active_cycle(st); ex=cy['execution']
        for t in ex['tasks'].values(): t['status']='PASS'
        ws.save_state(st)
        p=run(self.root,'scripts/execution_gate.py','finalize-execution')
        self.assertNotEqual(p.returncode,0); self.assertIn('EXECUTION_SUMMARY.md must be COMPLETE',p.stdout)
        (self.root/'EXECUTE/execution/EXECUTION_SUMMARY.md').write_text(
            f'---\nartifact_kind: EXECUTION_SUMMARY\nartifact_status: COMPLETE\nexecution_version: {ex["version"]}\ncycle_id: {cid}\n---\n\n# Summary\nAll tasks complete.\n',encoding='utf-8')
        p=run(self.root,'scripts/execution_gate.py','finalize-execution')
        self.assertEqual(p.returncode,0,p.stdout); self.assertIn('AWAITING_EVALUATION',p.stdout)

    def test_finalize_pass_closes_cycle(self):
        self.start_cycle(); self.compile_package(); self.force_test_approval()
        ws=import_ws(self.root); st=ws.load_state(); _,cy=ws.active_cycle(st); ex=cy['execution']
        for t in ex['tasks'].values(): t['status']='PASS'
        ex['status']='AWAITING_EVALUATION'; cy['status']='EVALUATION'; cy['lifecycle_stage']='EVALUATION'
        cy['evaluation']={'status':'AUTHORIZED','active':{'version':'Evaluation_V1','status':'AUTHORIZED','execution_version':ex['version'],'report':'EXECUTE/evaluation/Evaluation_V1.md','result':None,'blocking_findings':0},'attempts':[],'latest_result':None,'next_route':'RUN_EXTERNAL_AGENT_EVALUATION'}
        ws.save_state(st)
        (self.root/'EXECUTE/evaluation/Evaluation_V1.md').write_text('# Evaluation\n\n```yaml\nresult: PASS\nblocking_findings: 0\n```\n',encoding='utf-8')
        scope=cy['scope']
        (self.root/'EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_V1.md').write_text(
            f'# Completion\n\nbased_on_scope_revision: {scope["revision_label"]}\nbased_on_scope_digest: {scope["digest"]}\nverified\n',encoding='utf-8')
        self.complete_external_work('EVALUATION')
        p=run(self.root,'scripts/finalize_evaluation.py','--evaluation','Evaluation_V1','--completion-report','EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_V1.md')
        self.assertEqual(p.returncode,0,p.stdout); self.assertIn('CLOSED_VALIDATED',p.stdout)
        st=json.loads((self.root/'EXECUTE/control/STATE.json').read_text()); cy=st['cycles'][st['active_cycle']]
        self.assertEqual(cy['status'],'CLOSED_VALIDATED'); self.assertEqual(st['project_state'],'AWAITING_NEW_SCOPE'); self.assertEqual(cy['approval']['status'],'CONSUMED')

    def test_diagnosis_does_not_grant_recovery_authority(self):
        self.start_cycle(); self.compile_package(); self.force_test_approval()
        b=run(self.root,'scripts/execution_gate.py','begin-task','TASK_001'); self.assertEqual(b.returncode,0,b.stdout)
        ev=self.evidence('TASK_001')
        f=run(self.root,'scripts/execution_gate.py','fail-task','TASK_001','--evidence',ev,'--reason','test failure'); self.assertEqual(f.returncode,0,f.stdout)
        st=json.loads((self.root/'EXECUTE/control/STATE.json').read_text()); cy=st['cycles'][st['active_cycle']]; issue=cy['active_issue']
        diag=self.root/'EXECUTE/diagnostics/Diagnosis_V99.md'; diag.write_text('# Diagnosis\nimplementation defect\n',encoding='utf-8')
        self.complete_external_work('DIAGNOSIS')
        d=run(self.root,'scripts/diagnosis_gate.py','--issue',issue,'--diagnosis','EXECUTE/diagnostics/Diagnosis_V99.md','--classification','IMPLEMENTATION_DEFECT')
        self.assertEqual(d.returncode,0,d.stdout); self.assertIn('No repair authority granted',d.stdout)
        a=run(self.root,'scripts/approve_recovery.py')
        self.assertNotEqual(a.returncode,0); self.assertIn('interactive TTY',a.stdout)

    def test_external_agent_checkpoint_resumes_across_provider(self):
        self.start_cycle()
        b=run(self.root,'scripts/agent_work.py','begin','--role','PLANNING','--tool','claude-code','--model','opus')
        self.assertEqual(b.returncode,0,b.stdout)
        c=run(self.root,'scripts/agent_work.py','checkpoint','--expected-seq','0','--phase','REPOSITORY_RESEARCH','--unit','RU-001','--next-unit','RU-002','--note','Verified repository structure; next inspect state transitions.','--tool','claude-code','--model','opus')
        self.assertEqual(c.returncode,0,c.stdout)
        r=run(self.root,'scripts/agent_work.py','resume','--tool','opencode','--model','other-large-model')
        self.assertEqual(r.returncode,0,r.stdout); self.assertIn('RU-002',r.stdout)
        stale=run(self.root,'scripts/agent_work.py','checkpoint','--expected-seq','0','--phase','REPOSITORY_RESEARCH','--unit','RU-002','--note','stale writer')
        self.assertNotEqual(stale.returncode,0); self.assertIn('STALE',stale.stdout)

    def test_plan_ready_requires_completed_external_work(self):
        self.start_cycle()
        ws=import_ws(self.root); state=ws.load_state(); _,cycle=ws.active_cycle(state); p=cycle['planning']; pv,rev=p['version'],p['revision_label']
        for cp in sorted((self.root/'EXECUTE/compiled').glob('*.md')):
            cp.write_text(f'---\nartifact_kind: {cp.stem}\nartifact_status: COMPILED\nplanning_version: {pv}\nplanning_revision: {rev}\n---\n',encoding='utf-8')
        (self.root/'EXECUTE/plan/IMPLEMENTATION_PLAN.md').write_text(f'---\nartifact_kind: IMPLEMENTATION_PLAN\nartifact_status: COMPILED\nplanning_version: {pv}\nplanning_revision: {rev}\n---\n',encoding='utf-8')
        (self.root/'EXECUTE/tasks/TASK_001.md').write_text(f'---\ntask_id: TASK_001\nartifact_status: COMPILED\nplanning_version: {pv}\nplanning_revision: {rev}\ndepends_on: []\n---\n\nmax_evidence_driven_repair_attempts: 1\n',encoding='utf-8')
        (self.root/'EXECUTE/tasks/TASK_INDEX.md').write_text(f'---\nartifact_kind: TASK_INDEX\nartifact_status: COMPILED\nplanning_version: {pv}\nplanning_revision: {rev}\n---\n',encoding='utf-8')
        self.assertEqual(run(self.root,'scripts/planning_gate.py','set-material-zero').returncode,0)
        self.assertEqual(run(self.root,'scripts/planning_gate.py','authorize-expansion').returncode,0)
        q=run(self.root,'scripts/planning_gate.py','mark-plan-ready')
        self.assertNotEqual(q.returncode,0); self.assertIn('EXTERNAL_WORK: BLOCKED',q.stdout)


if __name__ == '__main__':
    unittest.main()
