#!/usr/bin/env python3
"""Authoritative task dispatch/completion/failure transitions for v4.3.0."""
from __future__ import annotations
import argparse
from pathlib import Path
from workflow_state import ROOT, active_cycle, append_transition, ensure_package_integrity, load_state, next_id, save_state, utc_now


def ctx():
    state=load_state(); cid,cycle=active_cycle(state); ex=cycle.get('execution')
    if not ex: raise SystemExit('EXECUTION_GATE: BLOCKED\nno authorized execution exists')
    return state,cid,cycle,ex


def get_task(ex,task_id):
    task=(ex.get('tasks') or {}).get(task_id)
    if not task: raise SystemExit(f'EXECUTION_GATE: BLOCKED\nunknown/unapproved task: {task_id}')
    return task


def require_integrity(cycle):
    ensure_package_integrity(cycle)


def cmd_status(_):
    state,cid,cycle,ex=ctx(); print(f'cycle_id: {cid}'); print(f'execution_status: {ex.get("status")}'); print(f'active_task: {ex.get("active_task")}'); print(f'active_issue: {ex.get("active_issue")}')
    b=ex.get('manager_batch') or {}; print(f'manager_batch: {b.get("number")}'); print(f'dispatches: {b.get("dispatches")}/{b.get("max_dispatches")}'); print(f'context_reset_required: {str(bool(b.get("reset_required"))).lower()}')
    for tid,t in sorted((ex.get('tasks') or {}).items()): print(f'{tid}: {t.get("status")} dispatches={t.get("dispatch_count")} repairs={t.get("repair_attempts")}/{t.get("max_repairs")}')
    return 0


def cmd_begin(a):
    state,cid,cycle,ex=ctx(); require_integrity(cycle)
    if cycle.get('status')!='EXECUTION': raise SystemExit(f'EXECUTION_GATE: BLOCKED\ncycle status is {cycle.get("status")}')
    if ex.get('status') not in {'READY','IN_PROGRESS','READY_TO_RESUME'}: raise SystemExit(f'EXECUTION_GATE: BLOCKED\nexecution status {ex.get("status")} does not permit dispatch')
    if ex.get('active_issue') or cycle.get('active_issue'): raise SystemExit('EXECUTION_GATE: BLOCKED\nan unresolved Issue is active')
    if ex.get('active_task'): raise SystemExit(f'EXECUTION_GATE: BLOCKED\nactive task already exists: {ex.get("active_task")}')
    batch=ex['manager_batch']
    if batch.get('reset_required') or int(batch.get('dispatches',0)) >= int(batch.get('max_dispatches',10)):
        batch['reset_required']=True; cycle['next_action']='START_FRESH_MANAGER_AND_RESET_BATCH'; save_state(state)
        raise SystemExit('EXECUTION_GATE: MANAGER_CONTEXT_RESET_REQUIRED\nStart a fresh Manager chat, then manually run scripts/reset_manager_batch.py before continuing.')
    task=get_task(ex,a.task)
    if task.get('status')!='PENDING': raise SystemExit(f'EXECUTION_GATE: BLOCKED\n{a.task} status must be PENDING, found {task.get("status")}')
    if int(task.get('dispatch_count',0)) != 0: raise SystemExit(f'EXECUTION_GATE: BLOCKED\n{a.task} has already been dispatched as ordinary Builder work')
    unmet=[d for d in task.get('dependencies',[]) if (ex['tasks'].get(d) or {}).get('status') not in {'PASS','PASS_RECOVERED'}]
    if unmet: raise SystemExit('EXECUTION_GATE: BLOCKED\nunmet dependencies: '+', '.join(unmet))
    task['status']='IN_PROGRESS'; task['dispatch_count']=1; task['started_at']=utc_now(); ex['active_task']=a.task; ex['status']='IN_PROGRESS'; batch['dispatches']=int(batch.get('dispatches',0))+1
    cycle['next_action']=f'RUN_BUILDER_FOR_{a.task}'
    save_state(state); append_transition('TASK_DISPATCH_AUTHORIZED',actor='manager:execution_gate',cycle_id=cid,details={'task':a.task,'manager_batch':batch['number']})
    print('EXECUTION_GATE: PASS'); print(f'task: {a.task}'); print('Builder dispatch authorized exactly once. Run context_guard.py, then one fresh Builder100K invocation.')
    return 0


def cmd_repair(a):
    state,cid,cycle,ex=ctx(); require_integrity(cycle); task=get_task(ex,a.task)
    if ex.get('active_task')!=a.task or task.get('status')!='IN_PROGRESS': raise SystemExit('EXECUTION_GATE: BLOCKED\nrepair authorization requires the active IN_PROGRESS task')
    n=int(task.get('repair_attempts',0)); maxn=int(task.get('max_repairs',0))
    if n>=maxn: raise SystemExit(f'EXECUTION_GATE: REPAIR_BUDGET_EXHAUSTED\n{a.task}: {n}/{maxn}; persist evidence and fail-task')
    task['repair_attempts']=n+1; save_state(state); append_transition('TASK_LOCAL_REPAIR_AUTHORIZED',actor='builder:execution_gate',cycle_id=cid,details={'task':a.task,'attempt':n+1,'max':maxn})
    print('EXECUTION_GATE: PASS'); print(f'local_repair_attempt: {n+1}/{maxn}'); print('Authorization covers one evidence-driven local repair attempt only.')
    return 0


def cmd_complete(a):
    state,cid,cycle,ex=ctx(); require_integrity(cycle); task=get_task(ex,a.task)
    if ex.get('active_task')!=a.task or task.get('status')!='IN_PROGRESS': raise SystemExit('EXECUTION_GATE: BLOCKED\ncomplete-task requires active IN_PROGRESS task')
    ep=ROOT/a.evidence
    if not ep.is_file(): raise SystemExit(f'EXECUTION_GATE: BLOCKED\nevidence missing: {a.evidence}')
    task['status']='PASS'; task['evidence']=a.evidence; task['completed_at']=utc_now(); ex['active_task']=None; ex['status']='IN_PROGRESS'; cycle['next_action']='DISPATCH_NEXT_READY_TASK_OR_FINALIZE'
    save_state(state); append_transition('TASK_COMPLETED',actor='manager:execution_gate',cycle_id=cid,details={'task':a.task,'evidence':a.evidence})
    print('EXECUTION_GATE: PASS'); print(f'{a.task}: PASS')
    return 0


def issue_path(issue_id): return ROOT/'EXECUTE/issues'/f'{issue_id}.md'


def cmd_fail(a):
    state,cid,cycle,ex=ctx(); require_integrity(cycle); task=get_task(ex,a.task)
    if ex.get('active_task')!=a.task or task.get('status')!='IN_PROGRESS': raise SystemExit('EXECUTION_GATE: BLOCKED\nfail-task requires active IN_PROGRESS task')
    ep=ROOT/a.evidence
    if not ep.is_file(): raise SystemExit(f'EXECUTION_GATE: BLOCKED\nevidence missing: {a.evidence}')
    issue_id=next_id(state,'issue','ISSUE_',4)
    task['status']='BLOCKED'; task['evidence']=a.evidence; ex['active_task']=None; ex['active_issue']=issue_id; ex['status']='PAUSED_FOR_DIAGNOSIS'; ex['recovery']={'status':'DIAGNOSIS_REQUIRED','diagnosis':None,'resolution':None,'verification':None,'resume_authorized':False,'next_task':None,'recovery_baseline':None}
    issue={'issue_id':issue_id,'origin_type':'EXECUTION','origin_task':a.task,'origin_execution':ex['version'],'status':'OPEN','evidence':a.evidence,'reason':a.reason,'opened_at':utc_now(),'diagnosis':None,'classification':None,'recovery_approval':None,'resolution':None}
    cycle['issues'].append(issue); cycle['active_issue']=issue_id; cycle['status']='RECOVERY'; cycle['lifecycle_stage']='DIAGNOSIS'; cycle['next_action']='RUN_CODEX_ISSUE_DIAGNOSIS'; state['project_state']='RECOVERY'
    txt=f'''---\nissue_id: {issue_id}\nstatus: OPEN\norigin_type: EXECUTION\norigin_execution: {ex['version']}\norigin_task: {a.task}\nopened_at: {issue['opened_at']}\nresume_authorized: false\n---\n\n# {issue_id} — Execution incident\n\n## Failure Summary\n\n{a.reason}\n\n## Evidence Pointers\n\n- `{a.evidence}`\n\n## Recovery Control\n\n```yaml\nlocal_execution_paused: true\nresume_authorized: false\ndiagnosis_artifact: none\nresolution_artifact: none\n```\n\n## Next Action\n\nRun `EXECUTE/codex/ISSUE_DIAGNOSIS_PROMPT.md`. Diagnosis is read/analyze/propose only.\n'''
    issue_path(issue_id).write_text(txt,encoding='utf-8')
    save_state(state); append_transition('ISSUE_OPENED',actor='manager:execution_gate',cycle_id=cid,details={'issue':issue_id,'task':a.task,'evidence':a.evidence})
    print('EXECUTION_GATE: HARD_STOP'); print(f'issue: {issue_id}'); print('execution_status: PAUSED_FOR_DIAGNOSIS'); print('Next: run Codex ISSUE_DIAGNOSIS_PROMPT.md. Do not dispatch another Builder.')
    return 0


def cmd_finalize(_a):
    state,cid,cycle,ex=ctx(); require_integrity(cycle)
    if ex.get('active_task') or ex.get('active_issue') or cycle.get('active_issue'): raise SystemExit('EXECUTION_GATE: BLOCKED\nactive task/issue exists')
    incomplete=[tid for tid,t in ex['tasks'].items() if t.get('status') not in {'PASS','PASS_RECOVERED'}]
    if incomplete: raise SystemExit('EXECUTION_GATE: BLOCKED\nincomplete tasks: '+', '.join(incomplete))
    summary=ROOT/'EXECUTE/execution/EXECUTION_SUMMARY.md'
    if not summary.is_file(): raise SystemExit('EXECUTION_GATE: BLOCKED\nEXECUTION_SUMMARY.md missing')
    summary_text=summary.read_text(encoding='utf-8',errors='replace')
    if 'artifact_status: COMPLETE' not in summary_text or f'execution_version: {ex.get("version")}' not in summary_text:
        raise SystemExit('EXECUTION_GATE: BLOCKED\nEXECUTION_SUMMARY.md must be COMPLETE and bound to the active execution_version')
    ex['status']='AWAITING_EVALUATION'; cycle['status']='EXECUTION_COMPLETE'; cycle['lifecycle_stage']='AWAITING_EVALUATION_AUTHORIZATION'; cycle['next_action']='USER_RUN_START_EVALUATION'; state['project_state']='AWAITING_EVALUATION_AUTHORIZATION'
    save_state(state); append_transition('EXECUTION_COMPLETE',actor='manager:execution_gate',cycle_id=cid,details={'execution':ex['version'],'tasks':len(ex['tasks'])})
    print('EXECUTION_GATE: PASS'); print('execution_status: AWAITING_EVALUATION'); print('HARD_STOP_REQUIRED: true'); print('Next: user manually runs python scripts/start_evaluation.py')
    return 0


def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    s=sub.add_parser('status'); s.set_defaults(func=cmd_status)
    b=sub.add_parser('begin-task'); b.add_argument('task'); b.set_defaults(func=cmd_begin)
    r=sub.add_parser('authorize-repair'); r.add_argument('task'); r.set_defaults(func=cmd_repair)
    c=sub.add_parser('complete-task'); c.add_argument('task'); c.add_argument('--evidence',required=True); c.set_defaults(func=cmd_complete)
    f=sub.add_parser('fail-task'); f.add_argument('task'); f.add_argument('--evidence',required=True); f.add_argument('--reason',required=True); f.set_defaults(func=cmd_fail)
    z=sub.add_parser('finalize-execution'); z.set_defaults(func=cmd_finalize)
    a=ap.parse_args(); return a.func(a)
if __name__=='__main__': raise SystemExit(main())
