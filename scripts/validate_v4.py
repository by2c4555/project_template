#!/usr/bin/env python3
"""Deterministic structural/architecture validator for project template v4.0.1."""
from pathlib import Path
import re, subprocess, sys, json

ROOT=Path(__file__).resolve().parents[1]
REQUIRED=[
 'README.md','CHANGELOG.md','VERSION','.gitignore','EXECUTE_PROJECT_PROMPT.md',
 '.github/agents/project-manager.agent.md','.github/agents/planner512k.agent.md',
 '.github/agents/builder128k.agent.md','.github/agents/builder256k.agent.md',
 '.github/skills/project-planning/SKILL.md','.github/skills/builder-task-execution/SKILL.md',
 'EXECUTE/.env.execute','EXECUTE/PROJECT_CONFIG.md','EXECUTE/PROJECT_STATUS.md',
 'EXECUTE/project_details.md','EXECUTE/reference/KNOWLEDGE_INDEX.md',
 'EXECUTE/plan/IMPLEMENTATION_PLAN.md','EXECUTE/tasks/TASK_INDEX.md',
 'EXECUTE/tasks/TASK_TEMPLATE.md','EXECUTE/issues/ISSUE_INDEX.md','EXECUTE/issues/ISSUE_TEMPLATE.md',
 'scripts/context_guard.py','scripts/configure_models.py','EXECUTE/MODEL_BINDINGS.json'
]
SECRET_KEY_RE=re.compile(r'(^|_)(PASSWORD|PASSWD|TOKEN|SECRET|API_KEY|ACCESS_KEY|PRIVATE_KEY|CLIENT_SECRET|SESSION|COOKIE|AUTHORIZATION)($|_)',re.I)
errors=[]
def check(cond,msg):
    if not cond: errors.append(msg)
def text(rel): return (ROOT/rel).read_text(encoding='utf-8')

for rel in REQUIRED: check((ROOT/rel).exists(),f'missing required file: {rel}')
if errors:
    for e in errors: print('FAIL:',e)
    raise SystemExit(1)

check(text('VERSION').strip()=='4.0.1','VERSION must be 4.0.1')
check('.env.user' in text('.gitignore'),'.gitignore must ignore .env.user')
for p in (ROOT/'.github/agents').glob('*.agent.md'):
    check('32k' not in p.name.lower() and '64k' not in p.name.lower(),f'unsupported low-context agent: {p.name}')

cfg=text('EXECUTE/PROJECT_CONFIG.md')
for n in ('524288','131072','262144','49152','65536','98304'):
    check(n in cfg,f'PROJECT_CONFIG missing context value {n}')
for marker in ('task_is_fresh_subagent_invocation: true','planner_transaction_is_fresh_subagent_invocation: true','retry_is_fresh_subagent_invocation: true','inter_agent_handoff: result_capsule_only','local_output_budget:'):
    check(marker in cfg,f'PROJECT_CONFIG missing architecture marker: {marker}')

pm=text('.github/agents/project-manager.agent.md')
for marker in ("tools: ['read', 'edit', 'agent']","agents: ['Planner512K', 'Builder128K', 'Builder256K']",'1 Task = 1 execution contract = 1 isolated subagent invocation = 1 fresh context window'):
    check(marker in pm,f'ProjectManager missing isolation marker: {marker}')
for rel in ('.github/agents/planner512k.agent.md','.github/agents/builder128k.agent.md','.github/agents/builder256k.agent.md'):
    t=text(rel); check('agents: []' in t,f'{rel} must not spawn subagents'); check('user-invocable: false' in t,f'{rel} must be internal subagent')

planner=text('.github/skills/project-planning/SKILL.md')
for txn in ('PT1_INPUT_KNOWLEDGE','PT2_ARCHITECTURE_PLAN','PT3_RISK_PHASES','PT4_TASK_COMPILATION','PT5_TASK_PACK_VALIDATION'):
    check(txn in planner,f'planning skill missing transaction {txn}')
check('context_guard.py' in planner,'planning skill must use context_guard.py')

builder=text('.github/skills/builder-task-execution/SKILL.md')
for marker in ('context_guard.py','Bounded Tool Output','Result Capsule','retry is always a new Builder invocation'):
    check(marker.lower() in builder.lower(),f'builder skill missing marker: {marker}')

bindings=json.loads(text('EXECUTE/MODEL_BINDINGS.json'))
expected={'Planner512K':524288,'Builder128K':131072,'Builder256K':262144}
unbound=[]
agent_files={'Planner512K':'.github/agents/planner512k.agent.md','Builder128K':'.github/agents/builder128k.agent.md','Builder256K':'.github/agents/builder256k.agent.md'}
for role,minimum in expected.items():
    r=bindings.get('roles',{}).get(role,{})
    check(r.get('minimum_context_tokens')==minimum,f'{role} binding minimum mismatch')
    model=r.get('model'); cap=r.get('documented_context_tokens',0)
    if not model:
        unbound.append(role)
    else:
        check(isinstance(cap,int) and cap>=minimum,f'{role} bound capacity {cap!r} below {minimum}')
        agent=text(agent_files[role])
        check(re.search(r'^model:\s*.+$',agent,re.M) is not None,f'{role} is bound but agent frontmatter lacks model:')
        if re.search(r'^model:\s*.+$',agent,re.M):
            check(model in re.search(r'^model:\s*(.+)$',agent,re.M).group(1),f'{role} model binding does not match agent frontmatter')

env=text('EXECUTE/.env.execute')
for i,raw in enumerate(env.splitlines(),1):
    line=raw.strip()
    if not line or line.startswith('#') or '=' not in line: continue
    key=line.split('=',1)[0].strip()
    check(not SECRET_KEY_RE.search(key),f'.env.execute secret-bearing key {key!r} line {i}')

# Smoke-test context guard against template: it may WARN because placeholder paths do not exist, but must execute deterministically.
p=subprocess.run([sys.executable,str(ROOT/'scripts/context_guard.py'),'EXECUTE/tasks/TASK_TEMPLATE.md'],cwd=ROOT,text=True,capture_output=True)
check(p.returncode in (0,10,20),f'context_guard smoke test failed: {p.stderr.strip() or p.stdout.strip()}')

if errors:
    print('STRUCTURE_VALIDATION: FAIL')
    print('ARCHITECTURE_VALIDATION: FAIL')
    print('POLICY_VALIDATION: FAIL')
    for e in errors: print('FAIL:',e)
    raise SystemExit(1)
print('STRUCTURE_VALIDATION: PASS')
print('ARCHITECTURE_VALIDATION: PASS')
print('POLICY_VALIDATION: PASS')
if unbound:
    print('MODEL_BINDING_VALIDATION: WARN (unbound: ' + ', '.join(unbound) + ')')
    print('RUNTIME_READY: NO - run scripts/configure_models.py with trusted model capacities')
else:
    print('MODEL_BINDING_VALIDATION: PASS')
    print('RUNTIME_READY: YES')
print('TEMPLATE_VALID: PASS (v4.0.1)')
