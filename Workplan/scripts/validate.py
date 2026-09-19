#!/usr/bin/env python3
"""Deterministic candidate checks; full mode runs behavioral conformance tests."""
import json, os, runpy, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; W=ROOT/'Workplan'; errors=[]
for rel in ['Workplan/VERSION','Workplan/control/STATE.json','Workplan/scripts/tools/scope.py','Workplan/scripts/tools/planning.py','Workplan/scripts/migrate_v532_to_v540.py','Workplan/tests/run_v54_conformance.py']:
    if not (ROOT/rel).is_file(): errors.append('missing: '+rel)
try:
    st=json.loads((W/'control/STATE.json').read_text()); assert st['workflow_version']=='5.4.0' and st['schema_version']==7
except Exception as e: errors.append('invalid v5.4 state: '+str(e))
try:
    checker=runpy.run_path(str(W/'tests/run_constitution_hardening.py')); errors.extend(checker['check_documents'](ROOT))
except Exception as e: errors.append('constitution document validation: '+str(e))
for p in ROOT.rglob('*.py'):
    if '__pycache__' not in p.parts:
        try: compile(p.read_text(encoding='utf-8'),str(p),'exec')
        except Exception as e: errors.append(f'compile {p.relative_to(ROOT)}: {e}')
if errors:
    print('TEMPLATE_VALID: FAIL'); print('\n'.join(errors)); raise SystemExit(1)
print('STRUCTURAL_VALID: PASS (v5.4.0 schema 7)')
if '--full' in sys.argv:
    env=dict(os.environ); env['PYTHONDONTWRITEBYTECODE']='1'
    r=subprocess.run([sys.executable,str(W/'tests/run_v54_conformance.py')],cwd=ROOT,text=True,capture_output=True,env=env,timeout=60)
    if r.stdout: print(r.stdout,end='')
    if r.stderr: print(r.stderr,file=sys.stderr,end='')
    if r.returncode: raise SystemExit(r.returncode)
print('TEMPLATE_VALID: PASS')
