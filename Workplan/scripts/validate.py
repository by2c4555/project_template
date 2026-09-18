#!/usr/bin/env python3
from __future__ import annotations
import configparser, json, os, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
W=ROOT/'Workplan'
EXPECTED_VERSION='5.3.2'
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
    'README.md','Workplan/VERSION','Workplan/ENTRY_PROMPT.md','Workplan/README.md',
    'Workplan/development_constitution/README.md','Workplan/development_constitution/OBJECTIVE.md',
    'Workplan/development_constitution/REFERENCE_ARCHITECTURE.md','Workplan/development_constitution/DEVELOPMENT_PROMPT.md',
    'Workplan/MIGRATION_V5_2_TO_V5_3.md','Workplan/MIGRATION_V5_3_0_TO_V5_3_1.md','Workplan/MIGRATION_V5_3_1_TO_V5_3_2.md',
    'Workplan/RELEASE_VALIDATION.md','Workplan/FILE_SHA256SUMS.txt',
    'Workplan/CHATGPT_PROJECT_INSTRUCTIONS.md','Workplan/templates/PROJECT_DETAILS_TEMPLATE.md',
    'Workplan/external_agent/RESEARCH_INSTRUCTION.md','Workplan/external_agent/RESEARCH_POTOCAL_PROMPT.md',
    'Workplan/control/STATE.json','Workplan/config/MODEL_CONFIG.ini','Workplan/config/MODEL_BINDINGS.json',
    'Workplan/scripts/command.py','Workplan/scripts/resume.py','Workplan/scripts/approve.py','Workplan/scripts/integrity.py',
    'Workplan/scripts/migrate_v530_to_v531.py','Workplan/scripts/migrate_v531_to_v532.py',
    'Workplan/scripts/_core/contracts.py','Workplan/scripts/_core/mutation.py','Workplan/scripts/_core/gates.py','Workplan/scripts/_core/tickets.py','Workplan/scripts/_core/ingest.py',
    'Workplan/scripts/tools/execution.py','Workplan/scripts/tools/diagnosis.py','Workplan/scripts/tools/recovery.py','Workplan/scripts/tools/ingest.py',
    'Workplan/tests/run_command_protocol.py','Workplan/tests/run_v53_invariants.py','Workplan/tests/run_research_builder_hardening.py',
    'Workplan/tests/run_constitution_hardening.py','Workplan/tests/run_issue_lifecycle.py','Workplan/tests/run_migration_regressions.py','Workplan/tests/run_final_acceptance.py',
    'Workplan/tests/run_scenarios.py','Workplan/tests/run_recovery_scenario.py',
    '.github/agents/manager.agent.md','.github/agents/builder.agent.md',
]
for rel in required: req(rel)

if (W/'VERSION').is_file() and (W/'VERSION').read_text().strip()!=EXPECTED_VERSION:
    errors.append(f'VERSION must be {EXPECTED_VERSION}')

contains('README.md',['Project Template v5.3.2','Cycle -> Phase -> Task -> Attempt','WORKPLAN_NEXT','Project Builder Local','development_constitution','MIGRATION_V5_3_1_TO_V5_3_2.md'])
contains('Workplan/development_constitution/OBJECTIVE.md',['AI-assisted software-development control plane','Cycle -> Phase -> Task -> Attempt','External Diagnosis is reasoning-only','hard maximum is **5 local Repair Attempts'])
contains('Workplan/development_constitution/REFERENCE_ARCHITECTURE.md',['VS CODE COPILOT AGENT ONLY','Manager Diagnosis #5','Builder REPAIR #5','External Diagnosis','CLOSED_VALIDATED'])
contains('Workplan/development_constitution/DEVELOPMENT_PROMPT.md',['CONSTITUTION_CHANGE_REQUIRED','Do not make the constitution follow the latest patch'])
contains('Workplan/ENTRY_PROMPT.md',['v5.3.2','exact literal token','EXECUTE_IMPLEMENTATION','EXECUTE_RECOVERY','WORKPLAN_NEXT'])
contains('Workplan/MIGRATION_V5_2_TO_V5_3.md',['schema 6','in-flight v5.2','implicit `PHASE_001`','Do not silently upgrade'])
contains('Workplan/MIGRATION_V5_3_0_TO_V5_3_1.md',['schema 6','Project Builder Local','EXTERNAL_RESEARCH_PROTOCOL_V1','migrate_v530_to_v531.py'])
contains('Workplan/MIGRATION_V5_3_1_TO_V5_3_2.md',['schema 6','development_constitution','migrate_v531_to_v532.py','Objective_dev.md` must not remain'])
contains('Workplan/CHATGPT_PROJECT_INSTRUCTIONS.md',['RESEARCH_INSTRUCTION.md','RESEARCH_POTOCAL_PROMPT.md','PROJECT_DETAILS_TEMPLATE.md','product_scope_unknowns: 0'])
contains('Workplan/external_agent/RESEARCH_INSTRUCTION.md',['EXECUTE_RESEARCH','RESEARCH_POTOCAL_PROMPT.md','PROJECT_DETAILS_TEMPLATE.md','INGEST_VALID: PASS'])
contains('Workplan/external_agent/RESEARCH_POTOCAL_PROMPT.md',['EXTERNAL_RESEARCH_PROTOCOL_V1','product_scope_unknowns: 0','Source / Evidence Map','INGEST_VALID: PASS'])
contains('Workplan/templates/PROJECT_DETAILS_TEMPLATE.md',['research_protocol: EXTERNAL_RESEARCH_PROTOCOL_V1','## Acceptance Criteria','## Source / Evidence Map'])
contains('.github/agents/manager.agent.md',['v5.3.2',"agents: ['Builder']",'no production `edit`','software debugging/diagnosis','Repair strategy','Task Gate','Phase Gate'])
contains('.github/agents/builder.agent.md',['Builder — Project Template v5.3.2',"model: 'Project Builder Local'",'Task', 'Repair', 'Recovery Ticket','open-ended diagnose/edit/retry loop'])

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
    roles=mb.get('roles') or {}
    if roles.get('Builder',{}).get('model')!='Project Builder Local': errors.append('MODEL_BINDINGS Builder must pin Project Builder Local')
    if roles.get('ExecutionManager',{}).get('model')!='USER_SELECTED': errors.append('MODEL_BINDINGS ExecutionManager must be USER_SELECTED')
except Exception as e: errors.append(f'invalid MODEL_BINDINGS.json: {e}')

# Current operational docs/prompts must not advertise older releases or direct recovered PASS.
operational=[ROOT/'README.md',W/'README.md',W/'ENTRY_PROMPT.md',W/'CHATGPT_PROJECT_INSTRUCTIONS.md',*(W/'external_agent').glob('*.md'),ROOT/'.github/agents/manager.agent.md',ROOT/'.github/agents/builder.agent.md']

# Canonical v5.3.2 release files replace obsolete duplicate/compatibility paths.
for rel in [
    '.github/agents/builder100k.agent.md',
    'Workplan/external_agent/RESEARCH_PROMPT.md',
    'Workplan/external_agent/EXTERNAL_RESEARCH_PROTOCOL.md',
    'Workplan/docs/INGEST_PROJECT_DETAILS_TEMPLATE.md',
    'Workplan/project_details.md',
    'Workplan/Objective_dev.md',
    'Workplan/tests/run_v531_hardening.py',
    'Workplan/tests/run_v531_acceptance.py',
]:
    if (ROOT/rel).exists(): errors.append(f'obsolete release file remains: {rel}')
for p in operational:
    if not p.is_file(): continue
    text=p.read_text(encoding='utf-8')
    first_heading = next((line for line in text.splitlines() if line.startswith('#')), '')
    if 'v5.3.0' in first_heading or 'v5.2.0' in first_heading or 'v5.1.0' in first_heading:
        errors.append(f'stale release heading in operational file: {p.relative_to(ROOT)}')
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

print('STRUCTURAL_VALID: PASS (v5.3.2 schema 6)')

if '--full' in sys.argv:
    suites=[
        ('command_protocol','Workplan/tests/run_command_protocol.py'),
        ('v53_invariants','Workplan/tests/run_v53_invariants.py'),
        ('research_builder_hardening','Workplan/tests/run_research_builder_hardening.py'),
        ('constitution_hardening','Workplan/tests/run_constitution_hardening.py'),
        ('issue_lifecycle','Workplan/tests/run_issue_lifecycle.py'),
        ('migration_regressions','Workplan/tests/run_migration_regressions.py'),
        ('final_acceptance','Workplan/tests/run_final_acceptance.py'),
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
    print('TEMPLATE_VALID: PASS (v5.3.2 --full)')
else:
    print('TEMPLATE_VALID: PASS (v5.3.2 structural)')
