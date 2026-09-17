#!/usr/bin/env python3
from pathlib import Path
import json, py_compile, subprocess, sys
ROOT=Path(__file__).resolve().parents[2]; W=ROOT/'Workplan'; errors=[]
def req(p):
    q=ROOT/p
    if not q.exists(): errors.append(f'missing: {p}')
    return q
for p in ['Workplan/VERSION','Workplan/ENTRY_PROMPT.md','Workplan/Objective_dev.md','Workplan/README.md','Workplan/control/STATE.json','Workplan/scripts/command.py','Workplan/scripts/resume.py','Workplan/scripts/approve.py','Workplan/scripts/_core/command.py','Workplan/scripts/_core/approval.py','Workplan/scripts/tools/ingest.py','Workplan/scripts/tools/external.py','Workplan/scripts/tools/execution.py','Workplan/tests/run_scenarios.py','Workplan/tests/run_command_protocol.py','.github/agents/project-manager.agent.md','.github/agents/builder100k.agent.md']:
    req(p)
if (W/'VERSION').read_text().strip()!='5.2.0': errors.append('VERSION must be 5.2.0')
obj=(W/'Objective_dev.md').read_text().lower()
for m in ['generation-fenced','single ai bootstrap entrypoint','natural-language conversation never grants','exact recognized public workplan command','reset operations preserve immutable scope/history']:
    if m not in obj: errors.append(f'Objective_dev missing {m}')
entry=(W/'ENTRY_PROMPT.md').read_text()
for m in ['WORKPLAN_STATUS','WORKPLAN_NEXT','EXECUTE_RESEARCH','EXECUTE_PLANNING','EXECUTE_IMPLEMENTATION','EXECUTE_DIAGNOSIS','EXECUTE_RECOVERY','EXECUTE_EVALUATION','RESET_PLANNING']:
    if m not in entry: errors.append(f'ENTRY_PROMPT missing {m}')
agent=(ROOT/'.github/agents/project-manager.agent.md').read_text()
if 'Workplan/ENTRY_PROMPT.md' not in agent or 'EXECUTE_IMPLEMENTATION' not in agent: errors.append('ExecutionManager must point to ENTRY_PROMPT and exact implementation command')
try:
    st=json.loads((W/'control/STATE.json').read_text())
    if st.get('workflow_version')!='5.2.0' or st.get('schema_version')!=5: errors.append('invalid state version/schema')
except Exception as e: errors.append(f'invalid state json: {e}')
for p in (W/'external_agent').glob('*_PROMPT.md'):
    t=p.read_text()
    if 'machine-selected' not in t: errors.append(f'{p.name} must identify machine-selected role constitution')
for p in ROOT.rglob('*.py'):
    try: py_compile.compile(str(p),doraise=True)
    except Exception as e: errors.append(f'compile {p.relative_to(ROOT)}: {e}')
if errors:
    print('TEMPLATE_VALID: FAIL'); [print('FAIL:',e) for e in errors]; raise SystemExit(1)
print('TEMPLATE_VALID: PASS (v5.2.0)')
if '--full' in sys.argv:
    for test in ['run_scenarios.py','run_command_protocol.py']:
        r=subprocess.run([sys.executable,str(W/'tests'/test)],cwd=ROOT,text=True)
        if r.returncode: raise SystemExit(r.returncode)
