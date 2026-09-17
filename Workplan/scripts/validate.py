#!/usr/bin/env python3
from __future__ import annotations
import configparser, json, os, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
W=ROOT/'Workplan'
EXPECTED_VERSION='5.3.0'
EXPECTED_SCHEMA=6
errors=[]

def req(rel):
    p=ROOT/rel
    if not p.exists(): errors.append(f'missing: {rel}')
    return p

def contains(rel, needles):
    p=req(rel)
    if not p.is_file(): return
    text=p.read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text: errors.append(f'{rel} missing {needle!r}')

required=[
    'README.md','Workplan/VERSION','Workplan/ENTRY_PROMPT.md','Workplan/Objective_dev.md','Workplan/README.md',
    'Workplan/MIGRATION_V5_2_TO_V5_3.md','Workplan/RELEASE_VALIDATION.md','Workplan/FILE_SHA256SUMS.txt',
    'Workplan/control/STATE.json','Workplan/config/MODEL_CONFIG.ini','Workplan/config/MODEL_BINDINGS.json',
    'Workplan/scripts/command.py','Workplan/scripts/resume.py','Workplan/scripts/approve.py','Workplan/scripts/integrity.py',
    'Workplan/scripts/_core/contracts.py','Workplan/scripts/_core/mutation.py','Workplan/scripts/_core/gates.py','Workplan/scripts/_core/tickets.py',
    'Workplan/scripts/tools/execution.py','Workplan/scripts/tools/diagnosis.py','Workplan/scripts/tools/recovery.py',
    'Workplan/tests/run_command_protocol.py','Workplan/tests/run_v53_invariants.py','Workplan/tests/run_scenarios.py','Workplan/tests/run_recovery_scenario.py',
    '.github/agents/project-manager.agent.md','.github/agents/builder.agent.md','.github/agents/builder100k.agent.md',
]
for rel in required: req(rel)

if (W/'VERSION').is_file() and (W/'VERSION').read_text().strip()!=EXPECTED_VERSION:
    errors.append(f'VERSION must be {EXPECTED_VERSION}')

contains('README.md',['Project Template v5.3.0','Cycle -> Phase -> Task -> Attempt','WORKPLAN_NEXT','MIGRATION_V5_2_TO_V5_3.md'])
contains('Workplan/Objective_dev.md',['v5.3.0','Cycle -> Phase -> Task -> Attempt','External Recovery is reasoning-only','Public command authority is exact-token authority','Integrity manifest must be deterministically generated'])
contains('Workplan/ENTRY_PROMPT.md',['v5.3.0','exact literal token','EXECUTE_IMPLEMENTATION','EXECUTE_RECOVERY','WORKPLAN_NEXT'])
contains('Workplan/MIGRATION_V5_2_TO_V5_3.md',['schema 6','in-flight v5.2','implicit `PHASE_001`','Do not silently upgrade'])
contains('.github/agents/project-manager.agent.md',['v5.3.0',"agents: ['Builder']",'Task Gate','Phase Gate'])
contains('.github/agents/builder.agent.md',['Builder — v5.3.0','Task', 'Repair', 'Recovery Ticket'])

# State/version/config consistency.
try:
    st=json.loads((W/'control/STATE.json').read_text())
    if st.get('workflow_version')!=EXPECTED_VERSION or st.get('schema_version')!=EXPECTED_SCHEMA:
        errors.append(f'invalid state version/schema: {st.get("workflow_version")}/{st.get("schema_version")}')
except Exception as e: errors.append(f'invalid state json: {e}')
try:
    cfg=configparser.ConfigParser(); cfg.read(W/'config/MODEL_CONFIG.ini')
    if cfg.get('workflow','version',fallback='')!=EXPECTED_VERSION: errors.append('MODEL_CONFIG.ini workflow version mismatch')
except Exception as e: errors.append(f'invalid MODEL_CONFIG.ini: {e}')
try:
    mb=json.loads((W/'config/MODEL_BINDINGS.json').read_text())
    if mb.get('workflow_version')!=EXPECTED_VERSION: errors.append('MODEL_BINDINGS workflow_version mismatch')
    if 'Builder' not in (mb.get('roles') or {}): errors.append('MODEL_BINDINGS missing generic Builder role')
except Exception as e: errors.append(f'invalid MODEL_BINDINGS.json: {e}')

# Current operational docs/prompts must not advertise older releases or direct recovered PASS.
operational=[ROOT/'README.md',W/'README.md',W/'ENTRY_PROMPT.md',*(W/'external_agent').glob('*.md'),ROOT/'.github/agents/project-manager.agent.md',ROOT/'.github/agents/builder.agent.md']
for p in operational:
    if not p.is_file(): continue
    text=p.read_text(encoding='utf-8')
    if 'v5.2.0' in text or 'v5.1.0' in text: errors.append(f'stale release label in operational file: {p.relative_to(ROOT)}')
    if 'PASS_RECOVERED' in text: errors.append(f'direct recovered PASS remains in operational file: {p.relative_to(ROOT)}')

# Syntax check without writing bytecode/cache files.
for p in ROOT.rglob('*.py'):
    if any(part=='__pycache__' for part in p.parts): continue
    try: compile(p.read_text(encoding='utf-8'), str(p), 'exec')
    except Exception as e: errors.append(f'compile {p.relative_to(ROOT)}: {e}')

# Deterministic release manifest must already be current; validation never regenerates it.
try:
    sys.path.insert(0,str(W/'scripts'))
    from _core.integrity import validate_release_manifest
    ok, problems=validate_release_manifest()
    if not ok: errors.extend(f'release manifest: {x}' for x in problems)
except Exception as e: errors.append(f'release manifest validation error: {e}')

if errors:
    print('TEMPLATE_VALID: FAIL')
    for e in errors: print('FAIL:',e)
    raise SystemExit(1)

print('STRUCTURAL_VALID: PASS (v5.3.0 schema 6)')

if '--full' in sys.argv:
    suites=[
        ('command_protocol','Workplan/tests/run_command_protocol.py'),
        ('v53_invariants','Workplan/tests/run_v53_invariants.py'),
        ('normal_e2e','Workplan/tests/run_scenarios.py'),
        ('recovery_e2e','Workplan/tests/run_recovery_scenario.py'),
    ]
    env=dict(os.environ); env['PYTHONDONTWRITEBYTECODE']='1'
    failed=[]
    for name, rel in suites:
        try:
            r=subprocess.run([sys.executable,str(ROOT/rel)],cwd=ROOT,text=True,capture_output=True,timeout=30,env=env)
        except subprocess.TimeoutExpired:
            print(f'SUITE {name}: TIMEOUT'); failed.append(name); continue
        if r.stdout.strip(): print(r.stdout.strip())
        if r.stderr.strip(): print(r.stderr.strip(),file=sys.stderr)
        if r.returncode!=0:
            print(f'SUITE {name}: FAIL (exit {r.returncode})'); failed.append(name)
        else: print(f'SUITE {name}: PASS')
    if failed:
        print('TEMPLATE_VALID: FAIL')
        print('failed_suites:', ', '.join(failed))
        raise SystemExit(1)
    print('TEMPLATE_VALID: PASS (v5.3.0 --full)')
else:
    print('TEMPLATE_VALID: PASS (v5.3.0 structural)')
