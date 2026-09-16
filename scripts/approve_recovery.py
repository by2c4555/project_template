#!/usr/bin/env python3
"""HUMAN/OPERATOR-ONLY authorization for broad external recovery work."""
from __future__ import annotations
import hashlib
from workflow_state import CONTROL, ROOT, active_cycle, append_transition, human_tty_challenge, load_state, next_id, save_state, utc_now, write_json

state=load_state(); cid,cycle=active_cycle(state); issue_id=cycle.get('active_issue')
if not issue_id: raise SystemExit('RECOVERY_APPROVAL: BLOCKED\nno active issue')
issue=next((x for x in cycle.get('issues',[]) if x.get('issue_id')==issue_id),None)
if not issue: raise SystemExit('RECOVERY_APPROVAL: BLOCKED\nactive issue record missing')
if issue.get('classification')!='IMPLEMENTATION_DEFECT': raise SystemExit(f'RECOVERY_APPROVAL: BLOCKED\nclassification {issue.get("classification")} does not permit direct repair')
if issue.get('recovery_approval'): raise SystemExit('RECOVERY_APPROVAL: BLOCKED\nrecovery already approved')
diag=issue.get('diagnosis'); p=ROOT/diag if diag else None
if not p or not p.is_file(): raise SystemExit('RECOVERY_APPROVAL: BLOCKED\ndiagnosis artifact missing')
digest=hashlib.sha256(p.read_bytes()).hexdigest()
if digest!=issue.get('diagnosis_digest'): raise SystemExit('RECOVERY_APPROVAL: BLOCKED\ndiagnosis changed after registration')
human_tty_challenge('RECOVERY APPROVAL',[f'Cycle: {cid}',f'Issue: {issue_id}',f'Diagnosis: {diag}',f'Diagnosis SHA-256: {digest}',f'Origin: {issue.get("origin_type")}'])
rid=next_id(state,'recovery_approval','RECOVERY_APPROVAL_',4)
record={'recovery_approval_id':rid,'cycle_id':cid,'issue_id':issue_id,'diagnosis':diag,'diagnosis_digest':digest,'authorized_at':utc_now(),'status':'ACTIVE','human_interactive':True}
path=CONTROL/'recovery_approvals'/f'{rid}.json'; write_json(path,record)
issue['recovery_approval']=rid
ex=cycle.get('execution') or {}; rec=ex.get('recovery') or {}; rec['status']='RECOVERY_AUTHORIZED'; rec['resume_authorized']=False; ex['recovery']=rec
cycle['lifecycle_stage']='RECOVERY'; cycle['next_action']='RUN_CODEX_RECOVERY_PROMPT'; save_state(state); append_transition('RECOVERY_APPROVED',actor='user:approve_recovery',cycle_id=cid,details={'issue':issue_id,'recovery_approval':rid,'diagnosis_digest':digest})
print('RECOVERY_APPROVAL: PASS'); print(f'recovery_approval_id: {rid}'); print('Next: run Codex with EXECUTE/codex/RECOVERY_PROMPT.md. Recovery must stop at VERIFIED; it cannot authorize resume.')
