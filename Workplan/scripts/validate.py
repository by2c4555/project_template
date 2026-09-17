#!/usr/bin/env python3
from pathlib import Path
import json, py_compile, subprocess, sys
ROOT=Path(__file__).resolve().parents[2]; W=ROOT/'Workplan'; errors=[]
def req(p):
    q=ROOT/p
    if not q.exists(): errors.append(f'missing: {p}')
    return q
for p in ['Workplan/VERSION','Workplan/Objective_dev.md','Workplan/README.md','Workplan/control/STATE.json','Workplan/scripts/resume.py','Workplan/scripts/approve.py','Workplan/scripts/_core/ingest.py','Workplan/scripts/tools/ingest.py','Workplan/scripts/tools/external.py','Workplan/scripts/tools/execution.py','Workplan/tests/run_scenarios.py','.github/agents/project-manager.agent.md','.github/agents/builder100k.agent.md']:
    req(p)
if (W/'VERSION').read_text().strip()!='5.1.0': errors.append('VERSION must be 5.1.0')
obj=(W/'Objective_dev.md').read_text().lower()
for m in ['generation-fenced','explicit untrusted boundary','context is granted progressively','manager routing is deterministic','single human approval interface']:
    if m not in obj: errors.append(f'Objective_dev missing {m}')
try:
    st=json.loads((W/'control/STATE.json').read_text())
    if st.get('workflow_version')!='5.1.0' or st.get('schema_version')!=4: errors.append('invalid state version/schema')
except Exception as e: errors.append(f'invalid state json: {e}')
for p in (W/'external_agent').glob('*_PROMPT.md'):
    t=p.read_text()
    if p.name!='RESEARCH_PROMPT.md' and 'approve.py' not in t: errors.append(f'{p.name} missing approval prohibition')
for p in ROOT.rglob('*.py'):
    try: py_compile.compile(str(p),doraise=True)
    except Exception as e: errors.append(f'compile {p.relative_to(ROOT)}: {e}')
if errors:
    print('TEMPLATE_VALID: FAIL'); [print('FAIL:',e) for e in errors]; raise SystemExit(1)
print('TEMPLATE_VALID: PASS (v5.1.0)')
if '--full' in sys.argv:
    r=subprocess.run([sys.executable,str(W/'tests/run_scenarios.py')],cwd=ROOT,text=True)
    raise SystemExit(r.returncode)
