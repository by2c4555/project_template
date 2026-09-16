#!/usr/bin/env python3
"""HUMAN/OPERATOR-ONLY authorization to start one bounded independent Codex Evaluation attempt."""
from __future__ import annotations
from workflow_state import active_cycle, append_transition, ensure_package_integrity, human_tty_challenge, load_state, next_id, save_state, utc_now

state=load_state(); cid,cycle=active_cycle(state); ex=cycle.get('execution') or {}; ev=cycle.get('evaluation') or {}
if cycle.get('status')!='EXECUTION_COMPLETE': raise SystemExit(f'START_EVALUATION: BLOCKED\ncycle status must be EXECUTION_COMPLETE, found {cycle.get("status")}')
if ex.get('status')!='AWAITING_EVALUATION': raise SystemExit(f'START_EVALUATION: BLOCKED\nexecution status must be AWAITING_EVALUATION, found {ex.get("status")}')
if cycle.get('active_issue') or ex.get('active_issue'): raise SystemExit('START_EVALUATION: BLOCKED\nunresolved issue is active')
incomplete=[tid for tid,t in (ex.get('tasks') or {}).items() if t.get('status') not in {'PASS','PASS_RECOVERED'}]
if incomplete: raise SystemExit('START_EVALUATION: BLOCKED\nincomplete tasks: '+', '.join(incomplete))
ensure_package_integrity(cycle)
human_tty_challenge('EVALUATION AUTHORIZATION',[f'Cycle: {cid}',f'Execution: {ex.get("version")}',f'Completed tasks: {len(ex.get("tasks") or {})}',f'Previous evaluation attempts: {len(ev.get("attempts") or [])}'])
version=next_id(state,'evaluation','Evaluation_V',width=1)
record={'version':version,'status':'AUTHORIZED','authorized_at':utc_now(),'execution_version':ex.get('version'),'report':f'EXECUTE/evaluation/{version}.md','result':None,'blocking_findings':0}
ev['active']=record; ev['status']='AUTHORIZED'; ev['next_route']='RUN_CODEX_EVALUATION'; cycle['evaluation']=ev; cycle['status']='EVALUATION'; cycle['lifecycle_stage']='EVALUATION'; cycle['next_action']='RUN_CODEX_EVALUATION'; state['project_state']='EVALUATION'
save_state(state); append_transition('EVALUATION_AUTHORIZED',actor='user:start_evaluation',cycle_id=cid,details={'evaluation':version,'execution':ex.get('version')})
print('START_EVALUATION: PASS'); print(f'evaluation_version: {version}'); print(f'expected_report: EXECUTE/evaluation/{version}.md'); print('Next: run Codex with EXECUTE/codex/EVALUATION_PROMPT.md. One authorization covers one evaluation attempt only.')
