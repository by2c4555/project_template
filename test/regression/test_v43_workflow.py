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


class V43WorkflowRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name) / 'repo'
        shutil.copytree(
            SOURCE_ROOT, cls.root,
            ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'project_template-v4.3.1.zip')
        )

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def setUp(self):
        # Reset mutable machine/package workspaces without re-copying the whole template.
        ws = import_ws(self.root)
        ws.save_state(ws.initial_state())
        ws.LEDGER_PATH.write_text('', encoding='utf-8')
        ws.reset_package_workspace('none', 'none')
        for d in [self.root/'EXECUTE/control/approvals', self.root/'EXECUTE/control/recovery_approvals', self.root/'EXECUTE/control/manifests']:
            for item in d.glob('*.json'):
                item.unlink()
        h = self.root/'EXECUTE/history/cycles'
        if h.exists():
            shutil.rmtree(h)
        for item in (self.root/'EXECUTE/issues').glob('ISSUE_[0-9]*.md'):
            item.unlink()

    def start_cycle(self, scope='Research_Test'):
        p = run(self.root, 'scripts/start_cycle.py', '--scope', scope, '--title', 'Test cycle')
        self.assertEqual(p.returncode, 0, p.stdout)
        return p

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
            deps='[]'
            task_lines.append(f'- {tid}')
            (self.root/f'EXECUTE/tasks/{tid}.md').write_text(
                f'''---\ntask_id: {tid}\nartifact_status: COMPILED\nplanning_version: {pv}\nplanning_revision: {rev}\nphase: PHASE_01\nbuilder: Builder100K\ndepends_on: {deps}\n---\n\n# {tid}\n\n## Context Manifest\n### mandatory\n- `EXECUTE/compiled/GLOBAL_CONSTRAINTS.md`\n\n## Allowed Scope\n### WRITE\n- `src/file_{i}.txt`\n\n## Acceptance Criteria\n- AC-01\n\n## Verification\n`true`\n\n## Local Repair Budget\n```yaml\nmax_evidence_driven_repair_attempts: {max_repairs}\n```\n''', encoding='utf-8'
            )
        (self.root/'EXECUTE/tasks/TASK_INDEX.md').write_text(
            f'---\nartifact_kind: TASK_INDEX\nartifact_status: COMPILED\nplanning_version: {pv}\nplanning_revision: {rev}\n---\n\n# Tasks\n'+'\n'.join(task_lines)+'\n', encoding='utf-8'
        )
        for cmd in [
            ['scripts/planning_gate.py','set-material-zero'],
            ['scripts/planning_gate.py','authorize-expansion'],
            ['scripts/planning_gate.py','mark-plan-ready'],
        ]:
            q=run(self.root,*cmd); self.assertEqual(q.returncode,0,q.stdout)
        return pv, rev

    def force_test_approval(self):
        ws=import_ws(self.root); state=ws.load_state(); cid,cycle=ws.active_cycle(state); p=cycle['planning']
        manifest=ws.build_package_manifest(p['version'],p['revision_label'])
        approval_id='APPROVAL_TEST'
        mp=ws.manifest_path_for(approval_id); ws.write_json(mp,manifest)
        approval={
            'approval_id':approval_id,'cycle_id':cid,'status':'ACTIVE','planning_version':p['version'],
            'planning_revision':p['revision_label'],'package_digest':manifest['package_digest'],
            'task_count':manifest['task_count'],'manifest_path':str(mp.relative_to(self.root)).replace('\\','/'),
            'human_interactive':True,
        }
        tasks={}
        for c in manifest['task_contracts']:
            tasks[c['task_id']]={'status':'PENDING','contract_path':c['path'],'dependencies':c['depends_on'],'dispatch_count':0,'repair_attempts':0,'max_repairs':c.get('max_repairs') if c.get('max_repairs') is not None else 2,'evidence':None,'recovery':None}
        cycle['approval']=approval; p['status']='APPROVED'; p['package_status']='APPROVED'
        cycle['execution']={'version':'Execution_Test','status':'READY','bound_planning_version':p['version'],'bound_planning_revision':p['revision_label'],'approval_id':approval_id,'approved_package_digest':manifest['package_digest'],'tasks':tasks,'active_task':None,'active_issue':None,'last_resolved_issue':None,'manager_batch':{'number':1,'dispatches':0,'max_dispatches':state['runtime_policy']['manager_max_task_dispatches_per_batch'],'reset_required':False},'recovery':{'status':'NOT_ACTIVE','diagnosis':None,'resolution':None,'verification':None,'resume_authorized':False,'next_task':None,'recovery_baseline':None}}
        cycle['status']='EXECUTION'; cycle['lifecycle_stage']='EXECUTION'; state['project_state']='EXECUTION'; ws.save_state(state)
        return manifest

    def evidence(self, tid):
        p=self.root/f'EXECUTE/execution/evidence/{tid}.md'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text('# evidence\nPASS\n',encoding='utf-8')
        return str(p.relative_to(self.root)).replace('\\','/')

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

    def test_repair_budget_is_machine_counted(self):
        self.start_cycle(); self.compile_package(max_repairs=2); self.force_test_approval()
        b=run(self.root,'scripts/execution_gate.py','begin-task','TASK_001'); self.assertEqual(b.returncode,0,b.stdout)
        for _ in range(2):
            p=run(self.root,'scripts/execution_gate.py','authorize-repair','TASK_001'); self.assertEqual(p.returncode,0,p.stdout)
        p=run(self.root,'scripts/execution_gate.py','authorize-repair','TASK_001')
        self.assertNotEqual(p.returncode,0); self.assertIn('REPAIR_BUDGET_EXHAUSTED',p.stdout)

    def test_manager_batch_forces_context_reset(self):
        self.start_cycle(); self.compile_package(task_count=3); self.force_test_approval()
        ws=import_ws(self.root); st=ws.load_state(); cid,cy=ws.active_cycle(st); cy['execution']['manager_batch']['max_dispatches']=2; ws.save_state(st)
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
        p=run(self.root,'scripts/start_cycle.py','--scope','Research_V2','--title','Next')
        self.assertEqual(p.returncode,0,p.stdout)
        st=json.loads((self.root/'EXECUTE/control/STATE.json').read_text()); new=st['cycles'][st['active_cycle']]
        self.assertEqual(new['status'],'PLANNING'); self.assertIsNone(new['approval']); self.assertIsNone(new['execution']); self.assertNotEqual(st['active_cycle'],cid)

    def test_open_cycle_blocks_new_cycle(self):
        self.start_cycle()
        p=run(self.root,'scripts/start_cycle.py','--scope','Research_V2')
        self.assertNotEqual(p.returncode,0); self.assertIn('only CLOSED_VALIDATED',p.stdout)

    def test_evaluation_requires_human_tty(self):
        self.start_cycle(); self.compile_package(); self.force_test_approval()
        ws=import_ws(self.root); st=ws.load_state(); cid,cy=ws.active_cycle(st); ex=cy['execution']
        for t in ex['tasks'].values(): t['status']='PASS'
        ex['status']='AWAITING_EVALUATION'; cy['status']='EXECUTION_COMPLETE'; cy['lifecycle_stage']='AWAITING_EVALUATION_AUTHORIZATION'; ws.save_state(st)
        p=run(self.root,'scripts/start_evaluation.py')
        self.assertNotEqual(p.returncode,0); self.assertIn('interactive TTY',p.stdout)

    def test_approved_package_snapshot_helper_preserves_files(self):
        self.start_cycle(); self.compile_package(); ws=import_ws(self.root); st=ws.load_state(); cid,cy=ws.active_cycle(st); p=cy['planning']; m=ws.build_package_manifest(p['version'],p['revision_label'])
        rel=ws.snapshot_package(cid,'APPROVAL_TEST',m)
        snap=self.root/rel
        self.assertTrue((snap/'PACKAGE_MANIFEST.json').is_file())
        self.assertTrue((snap/'package/EXECUTE/tasks/TASK_001.md').is_file())

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
        ws=import_ws(self.root); st=ws.load_state(); cid,cy=ws.active_cycle(st); ex=cy['execution']
        for t in ex['tasks'].values(): t['status']='PASS'
        ex['status']='AWAITING_EVALUATION'; cy['status']='EVALUATION'; cy['lifecycle_stage']='EVALUATION'
        cy['evaluation']={'status':'AUTHORIZED','active':{'version':'Evaluation_V1','status':'AUTHORIZED','execution_version':ex['version'],'report':'EXECUTE/evaluation/Evaluation_V1.md','result':None,'blocking_findings':0},'attempts':[],'latest_result':None,'next_route':'RUN_CODEX_EVALUATION'}
        ws.save_state(st)
        (self.root/'EXECUTE/evaluation/Evaluation_V1.md').write_text('# Evaluation\n\n```yaml\nresult: PASS\nblocking_findings: 0\n```\n',encoding='utf-8')
        (self.root/'EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_V1.md').write_text('# Completion\nverified\n',encoding='utf-8')
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
        d=run(self.root,'scripts/diagnosis_gate.py','--issue',issue,'--diagnosis','EXECUTE/diagnostics/Diagnosis_V99.md','--classification','IMPLEMENTATION_DEFECT')
        self.assertEqual(d.returncode,0,d.stdout); self.assertIn('No repair authority granted',d.stdout)
        a=run(self.root,'scripts/approve_recovery.py')
        self.assertNotEqual(a.returncode,0); self.assertIn('interactive TTY',a.stdout)


if __name__ == '__main__':
    unittest.main()
