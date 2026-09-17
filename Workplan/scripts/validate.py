#!/usr/bin/env python3
from pathlib import Path
import json, py_compile, sys, tempfile, subprocess, shutil
ROOT=Path(__file__).resolve().parents[2]; W=ROOT/'Workplan'; errors=[]
def req(p):
    q=ROOT/p
    if not q.exists(): errors.append(f'missing: {p}')
    return q
for p in ['Workplan/VERSION','Workplan/Objective_dev.md','Workplan/README.md','Workplan/control/STATE.json','Workplan/scripts/resume.py','Workplan/scripts/approve.py','Workplan/scripts/tools/approve_req.py','Workplan/scripts/tools/approve_res.py','Workplan/USE_CASES/README.md']:
    req(p)
if (W/'VERSION').read_text().strip()!='5.0.0': errors.append('VERSION must be 5.0.0')
obj=(W/'Objective_dev.md').read_text()
for m in ['Universal resumability','Cross-machine portability','Single human approval interface','Minimal state exposure','Script interface separation','Operational use cases']:
    if m.lower() not in obj.lower(): errors.append(f'Objective_dev missing {m}')
try:
    st=json.loads((W/'control/STATE.json').read_text())
    if st.get('workflow_version')!='5.0.0' or st.get('schema_version')!=3: errors.append('invalid state version/schema')
except Exception as e: errors.append(f'invalid state json: {e}')
# Prompts must forbid human approval command.
for p in (W/'external_agent').glob('*_PROMPT.md'):
    t=p.read_text()
    if 'NEVER execute `python Workplan/scripts/approve.py`' not in t: errors.append(f'{p.name} missing approve.py prohibition')
    if 'Work Map' not in t: errors.append(f'{p.name} missing Work Map contract')
# Agent adapters must not instruct raw state edit.
for p in (ROOT/'.github/agents').glob('*.md'):
    if 'edit Workplan/control/STATE.json' in p.read_text(): errors.append(f'{p.name} permits raw state edit')
# Compile python.
for p in W.rglob('*.py'):
    try: py_compile.compile(str(p),doraise=True)
    except Exception as e: errors.append(f'compile {p.relative_to(ROOT)}: {e}')
if errors:
    print('TEMPLATE_VALID: FAIL'); [print('FAIL:',e) for e in errors]; raise SystemExit(1)
print('TEMPLATE_VALID: PASS (v5.0.0)')
