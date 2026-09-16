import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def set_field(text, key, value):
    return re.sub(rf'^(\s*{re.escape(key)}:\s*).*$', rf'\g<1>{value}', text, count=1, flags=re.M)


class PlanningInteractionGateRegression(unittest.TestCase):
    def copy_project(self):
        td = tempfile.TemporaryDirectory()
        dst = Path(td.name) / 'project'
        shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        return td, dst

    def test_material_unknowns_plus_current_task_is_invalid(self):
        td, dst = self.copy_project()
        self.addCleanup(td.cleanup)
        p = dst / 'EXECUTE/plan/PLANNING_STATUS.md'
        s = p.read_text()
        updates = {
            'planning_version':'Planning_V1','planning_revision':'Revision_1',
            'planning_status':'AWAITING_USER_FEEDBACK','material_unknowns':'9',
            'feedback_reason':'MATERIAL_DECISION','plan_review_status':'NOT_STARTED',
            'package_status':'NOT_COMPILED','interaction_gate':'USER_FEEDBACK_REQUIRED',
            'invocation_stop_required':'true','task_expansion_allowed':'false',
            'implementation_approval_requested':'false','execution_locked':'true',
        }
        for k,v in updates.items(): s=set_field(s,k,v)
        p.write_text(s)
        (dst/'EXECUTE/tasks/TASK_001.md').write_text('---\ntask_id: TASK_001\nplanning_version: Planning_V1\nstatus: PENDING\n---\n')
        r=subprocess.run(['python','scripts/validate_v4.py'],cwd=dst,text=True,capture_output=True)
        self.assertNotEqual(r.returncode,0)
        self.assertIn('material unknowns remain',r.stdout)

    def test_expansion_gate_rejects_nonzero_unknowns(self):
        td, dst = self.copy_project(); self.addCleanup(td.cleanup)
        p=dst/'EXECUTE/plan/PLANNING_STATUS.md'; s=p.read_text()
        for k,v in {'planning_version':'Planning_V1','planning_revision':'Revision_1','planning_status':'IN_PROGRESS','material_unknowns':'9','interaction_gate':'NONE','invocation_stop_required':'false'}.items(): s=set_field(s,k,v)
        p.write_text(s)
        r=subprocess.run(['python','scripts/planning_gate.py','authorize-expansion','--planning','Planning_V1','--revision','Revision_1'],cwd=dst,text=True,capture_output=True)
        self.assertNotEqual(r.returncode,0)
        self.assertIn('material_unknowns must be exactly 0',r.stdout)


if __name__ == '__main__':
    unittest.main()
