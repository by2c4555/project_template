#!/usr/bin/env python3
"""Validate a External Agent Evaluation artifact and perform the authoritative PASS/blocked transition."""
from __future__ import annotations
import argparse, re
from pathlib import Path
from workflow_state import ROOT, active_cycle, append_transition, ensure_package_integrity, load_state, next_id, save_state, utc_now, require_external_work_complete


def value(text,key):
    m=re.search(rf'^\s*{re.escape(key)}:\s*(.*?)\s*$',text,re.M); return m.group(1).strip().strip('"\'') if m else None

ap=argparse.ArgumentParser(); ap.add_argument('--evaluation',required=True); ap.add_argument('--completion-report',default=None); a=ap.parse_args()
state=load_state(); cid,cycle=active_cycle(state); require_external_work_complete(state,cycle,'EVALUATION'); ex=cycle.get('execution') or {}; ev=cycle.get('evaluation') or {}; active=ev.get('active') or {}
if cycle.get('status')!='EVALUATION' or ev.get('status')!='AUTHORIZED': raise SystemExit('FINALIZE_EVALUATION: BLOCKED\nno authorized evaluation attempt is active')
if active.get('version')!=a.evaluation: raise SystemExit(f'FINALIZE_EVALUATION: BLOCKED\nauthorized evaluation is {active.get("version")}, not {a.evaluation}')
ensure_package_integrity(cycle)
report=ROOT/active['report']
if not report.is_file(): raise SystemExit(f'FINALIZE_EVALUATION: BLOCKED\nmissing report: {active["report"]}')
text=report.read_text(encoding='utf-8',errors='replace'); result=value(text,'result')
if result not in {'PASS','PASS_WITH_FINDINGS','DIAGNOSIS_REQUIRED'}: raise SystemExit('FINALIZE_EVALUATION: BLOCKED\nreport must contain result: PASS | PASS_WITH_FINDINGS | DIAGNOSIS_REQUIRED')
try: blocking=int(value(text,'blocking_findings') or 0)
except ValueError: raise SystemExit('FINALIZE_EVALUATION: BLOCKED\nblocking_findings must be an integer')
active.update({'status':'FINALIZED','result':result,'blocking_findings':blocking,'finalized_at':utc_now()}); ev.setdefault('attempts',[]).append(active.copy()); ev['active']=None; ev['latest_result']=result
if result in {'PASS','PASS_WITH_FINDINGS'}:
    if blocking!=0: raise SystemExit('FINALIZE_EVALUATION: BLOCKED\nPASS/PASS_WITH_FINDINGS requires blocking_findings: 0')
    suffix=a.evaluation.replace('Evaluation_','')
    cp=a.completion_report or f'EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_{suffix}.md'; cpp=ROOT/cp
    if not cpp.is_file(): raise SystemExit(f'FINALIZE_EVALUATION: BLOCKED\nCompletion Report required before validation: {cp}')
    cptext=cpp.read_text(encoding='utf-8',errors='replace'); scope=cycle.get('scope') or {}
    if value(cptext,'based_on_scope_revision') != scope.get('revision_label'):
        raise SystemExit('FINALIZE_EVALUATION: BLOCKED\nCompletion Report based_on_scope_revision must match the active Scope Snapshot')
    if value(cptext,'based_on_scope_digest') != scope.get('digest'):
        raise SystemExit('FINALIZE_EVALUATION: BLOCKED\nCompletion Report based_on_scope_digest must match the active Scope Snapshot')
    ev['status']='PASS'; ev['next_route']='AWAIT_NEW_SCOPE'; cycle['completion_report']=cp; cycle['status']='CLOSED_VALIDATED'; cycle['lifecycle_stage']='AWAITING_NEW_SCOPE'; cycle['closed_at']=utc_now(); cycle['next_action']='IMPORT_NEW_EXTERNAL_SCOPE_THEN_START_NEW_CYCLE'; state['project_state']='AWAITING_NEW_SCOPE'
    if cycle.get('approval'): cycle['approval']['status']='CONSUMED'
    ex['status']='COMPLETE_VALIDATED'
    event='CYCLE_VALIDATED'
else:
    if blocking<1: raise SystemExit('FINALIZE_EVALUATION: BLOCKED\nDIAGNOSIS_REQUIRED requires blocking_findings >= 1')
    issue_id=next_id(state,'issue','ISSUE_',4)
    issue={'issue_id':issue_id,'origin_type':'EVALUATION','origin_evaluation':a.evaluation,'origin_task':None,'origin_execution':ex.get('version'),'status':'OPEN','evidence':active['report'],'reason':f'{blocking} blocking evaluation finding(s)','opened_at':utc_now(),'diagnosis':None,'classification':None,'recovery_approval':None,'resolution':None}
    cycle['issues'].append(issue); cycle['active_issue']=issue_id; ex['active_issue']=issue_id; ex['status']='PAUSED_FOR_DIAGNOSIS'; ex['recovery']={'status':'DIAGNOSIS_REQUIRED','diagnosis':None,'resolution':None,'verification':None,'resume_authorized':False,'next_task':None,'recovery_baseline':None}; ev['status']='DIAGNOSIS_REQUIRED'; ev['next_route']='EXTERNAL_AGENT_DIAGNOSIS'; cycle['status']='RECOVERY'; cycle['lifecycle_stage']='DIAGNOSIS'; cycle['next_action']='RUN_EXTERNAL_AGENT_DIAGNOSIS'; state['project_state']='RECOVERY'
    ip=ROOT/'EXECUTE/issues'/f'{issue_id}.md'; ip.write_text(f'''---\nissue_id: {issue_id}\nstatus: OPEN\norigin_type: EVALUATION\norigin_evaluation: {a.evaluation}\norigin_execution: {ex.get('version')}\nopened_at: {issue['opened_at']}\nresume_authorized: false\n---\n\n# {issue_id} — Blocking Evaluation findings\n\n## Source Evaluation\n\n- `{active['report']}`\n- blocking findings: {blocking}\n\n## Next Action\n\nRun `EXECUTE/external_agent/DIAGNOSIS_PROMPT.md`. Do not modify production code during diagnosis.\n''',encoding='utf-8')
    event='EVALUATION_DIAGNOSIS_REQUIRED'
cycle['evaluation']=ev; cycle['execution']=ex; save_state(state); append_transition(event,actor='python:finalize_evaluation',cycle_id=cid,details={'evaluation':a.evaluation,'result':result,'blocking_findings':blocking,'completion_report':cycle.get('completion_report')})
print('FINALIZE_EVALUATION: PASS'); print(f'result: {result}'); print(f'cycle_status: {cycle["status"]}'); print(f'next_action: {cycle["next_action"]}')
