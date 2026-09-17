#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from _bootstrap import *
from _core.state import load_state, save_state, next_id, now
from _core.paths import WORKPLAN, ROOT
from _core.integrity import build_package_manifest
from _core.contracts import load_contract_package
from _core.approval import create_pending, grant_matches, consume_grant
from _core.gates import task_gate, phase_gate
from _core import work as W


def _digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def load():
    st = load_state(); cid = st.get('active_cycle'); return st, cid, (st.get('cycles') or {}).get(cid, {})


def package_ok(cycle):
    pl = cycle.get('planning') or {}; cur = build_package_manifest()
    return pl.get('candidate_package_digest') == cur['package_digest'], cur


def _eligible_phase(ex, package):
    for pid, phase in package['phases'].items():
        ps = (ex.get('phases') or {}).get(pid, {})
        if ps.get('status') == 'PASS':
            continue
        if all((ex.get('phases') or {}).get(d, {}).get('status') == 'PASS' for d in phase.get('depends_on', [])):
            return pid
    return None


def _eligible_task(ex, package, phase_id):
    for tid, task in package['tasks'].items():
        if task['phase_id'] != phase_id:
            continue
        state = (ex.get('tasks') or {}).get(tid, {})
        if state.get('status') != 'PENDING':
            continue
        if all((ex.get('tasks') or {}).get(d, {}).get('status') == 'PASS' for d in task.get('depends_on', [])):
            return tid
    return None


def _all_phase_tasks_pass(ex, package, phase_id):
    tids = [tid for tid, t in package['tasks'].items() if t['phase_id'] == phase_id]
    return all((ex.get('tasks') or {}).get(tid, {}).get('status') == 'PASS' for tid in tids)


def _gate_failure_structural(errors):
    markers = ('binding mismatch', 'digest changed', 'task/phase contract missing', 'ticket ', 'generation mismatch', 'identity mismatch')
    return any(any(m in e for m in markers) for e in errors)


def _escalate(st, cid, cycle, ex, reason, *, task=None, phase=None, classification=None):
    iid = next_id(st, 'issue', 'ISSUE_')
    issue = {
        'issue_id': iid, 'origin_type': 'EXECUTION', 'task': task, 'phase_id': phase,
        'reason': reason, 'status': 'AWAITING_DIAGNOSIS', 'classification': classification, 'created_at': now()
    }
    cycle.setdefault('issues', []).append(issue); ex['active_issue'] = iid; ex['status'] = 'PAUSED_FOR_DIAGNOSIS'
    cycle['execution'] = ex; st['cycles'][cid] = cycle; st['active_work'] = None
    st['lifecycle_stage'] = 'DIAGNOSIS'; st['project_state'] = 'DIAGNOSIS'; st['next_action'] = 'EXECUTE_DIAGNOSIS'
    save_state(st, event='EXECUTION_ESCALATED', actor='tool:execution', details={'task': task, 'phase': phase, 'issue': iid, 'reason': reason})
    return iid


def route(st, cycle):
    if st.get('pending_approval'):
        return {'action': 'HUMAN_APPROVAL_REQUIRED', 'approval_id': st['pending_approval']['approval_id']}
    stage = st.get('lifecycle_stage')
    if stage == 'PLAN_READY': return {'action': 'START_EXECUTION'}
    if stage == 'DIAGNOSIS': return {'action': 'START_DIAGNOSIS'}
    if stage == 'RECOVERY': return {'action': 'START_RECOVERY'}
    if stage == 'EVALUATION': return {'action': 'START_EVALUATION'}
    if stage == 'CLOSED_VALIDATED': return {'action': 'DONE'}
    if stage != 'EXECUTION': return {'action': 'BLOCKED', 'reason': stage}
    ex = cycle.get('execution') or {}
    if ex.get('active_issue'): return {'action': 'START_DIAGNOSIS', 'issue': ex['active_issue']}
    try:
        package = load_contract_package(validate=True)
    except Exception as e:
        return {'action': 'BLOCKED', 'reason': 'CONTRACT_INVALID', 'detail': str(e)}
    if st.get('active_task'):
        tid = st['active_task']; t = (ex.get('tasks') or {}).get(tid, {})
        if st.get('active_work'):
            meta = W.status(); rec = W.reconcile(meta) if meta else {'status': 'RESTART_ACTIVE_UNIT', 'changed': []}
            return {'action': 'RECONCILE_TASK' if rec['status'] != 'CLEAN' else 'RESUME_TASK', 'task': tid, 'attempt': st.get('active_attempt'), 'reconciliation': rec}
        if t.get('status') == 'IN_PROGRESS': return {'action': 'RUN_TASK_GATE', 'task': tid, 'attempt': st.get('active_attempt')}
        if t.get('status') == 'GATE_FAILED':
            if t.get('structural_failure'): return {'action': 'START_DIAGNOSIS', 'task': tid, 'reason': 'STRUCTURAL_GATE_FAILURE'}
            if int(t.get('repair_attempts', 0)) < int(t.get('max_repairs', 2)): return {'action': 'REQUEST_REPAIR', 'task': tid, 'next_repair': int(t.get('repair_attempts', 0)) + 1}
            return {'action': 'START_DIAGNOSIS', 'task': tid, 'reason': 'REPAIR_BUDGET_EXHAUSTED'}
        return {'action': 'BLOCKED', 'reason': 'ACTIVE_TASK_STATE', 'task': tid, 'status': t.get('status')}
    pid = _eligible_phase(ex, package)
    if not pid:
        if all(v.get('status') == 'PASS' for v in (ex.get('phases') or {}).values()): return {'action': 'START_EVALUATION'}
        return {'action': 'BLOCKED', 'reason': 'NO_ELIGIBLE_PHASE'}
    if _all_phase_tasks_pass(ex, package, pid):
        return {'action': 'RUN_PHASE_GATE', 'phase': pid}
    tid = _eligible_task(ex, package, pid)
    if tid:
        t = (ex.get('tasks') or {}).get(tid, {})
        return {'action': 'DISPATCH_RECOVERY_TASK' if t.get('pending_attempt_kind') == 'RECOVERY' else 'DISPATCH_TASK', 'phase': pid, 'task': tid, 'contract': t.get('contract')}
    incomplete = [tid for tid, t in (ex.get('tasks') or {}).items() if t.get('phase_id') == pid and t.get('status') != 'PASS']
    return {'action': 'BLOCKED', 'reason': 'NO_ELIGIBLE_TASK', 'phase': pid, 'incomplete': incomplete}


p = argparse.ArgumentParser(); sp = p.add_subparsers(dest='cmd', required=True)
sp.add_parser('status'); sp.add_parser('next'); sp.add_parser('start'); sp.add_parser('dispatch'); sp.add_parser('resume')
c = sp.add_parser('complete'); c.add_argument('--evidence', required=True)
f = sp.add_parser('fail'); f.add_argument('--reason', required=True)
r = sp.add_parser('repair'); r.add_argument('--reason', default='Task Gate failure')
g = sp.add_parser('phase-gate'); g.add_argument('--evidence')
sp.add_parser('finalize')
a = p.parse_args(); st, cid, cycle = load()
if a.cmd == 'status': print('EXECUTION_STATE'); print('route:', route(st, cycle)); raise SystemExit
if a.cmd == 'next': print('EXECUTION_NEXT'); print(json.dumps(route(st, cycle), sort_keys=True)); raise SystemExit
if a.cmd == 'start':
    if st.get('lifecycle_stage') != 'PLAN_READY': raise SystemExit('EXECUTION: BLOCKED\nPLAN_READY required')
    ok, man = package_ok(cycle)
    if not ok: raise SystemExit('EXECUTION: BLOCKED\npackage changed after PLAN_READY')
    try: package = load_contract_package(validate=True)
    except Exception as e: raise SystemExit(f'EXECUTION: BLOCKED\ncontract validation failed: {e}')
    subject = man['package_digest']; grant = st.get('last_granted_approval') or {}
    if man['task_count'] > 3 and not grant_matches(st, 'START_EXECUTION', subject):
        if not st.get('pending_approval'):
            rec = create_pending('NEW_COST_ENVELOPE', 'START_EXECUTION', subject); print('EXECUTION: HUMAN_APPROVAL_REQUIRED'); print('id:', rec['approval_id']); print('challenge:', rec['challenge']); raise SystemExit(2)
        raise SystemExit('EXECUTION: BLOCKED\npending approval exists')
    phases = {pid: {'status': 'PENDING', 'digest': _digest(pc), 'evidence': None} for pid, pc in package['phases'].items()}
    tasks = {}
    for tid, task in package['tasks'].items():
        tasks[tid] = {
            'status': 'PENDING', 'phase_id': task['phase_id'], 'contract': task['contract'], 'contract_digest': task['digest'],
            'repair_attempts': 0, 'max_repairs': task['max_repairs'], 'depends_on': task['depends_on'], 'evidence': None,
            'last_attempt': None, 'active_attempt': None, 'last_gate_errors': [], 'structural_failure': False,
        }
    cycle['execution'] = {'version': next_id(st, 'execution', 'Execution_V', 1), 'status': 'READY', 'package_digest': man['package_digest'], 'phases': phases, 'tasks': tasks, 'attempts': {}, 'active_issue': None}
    cycle['status'] = 'EXECUTION'; st['cycles'][cid] = cycle; st['project_state'] = 'EXECUTION'; st['lifecycle_stage'] = 'EXECUTION'; st['next_action'] = 'RUN_EXECUTION_MANAGER'
    if grant_matches(st, 'START_EXECUTION', subject):
        consume_grant(st, 'START_EXECUTION', subject)
    save_state(st, event='EXECUTION_STARTED', actor='tool:execution', details={'task_count': len(tasks), 'phase_count': len(phases), 'package_digest': man['package_digest']}); print('EXECUTION: READY'); raise SystemExit
ex = cycle.get('execution') or {}
if st.get('lifecycle_stage') != 'EXECUTION': raise SystemExit('EXECUTION: BLOCKED\nnot in EXECUTION stage')
ok, man = package_ok(cycle)
if not ok or man['package_digest'] != ex.get('package_digest'): raise SystemExit('EXECUTION: BLOCKED\npackage integrity failed')
package = load_contract_package(validate=True)
if a.cmd == 'dispatch':
    if st.get('active_task') or st.get('active_work'): raise SystemExit('EXECUTION: BLOCKED\nactive task/work exists')
    pid = _eligible_phase(ex, package)
    if not pid: raise SystemExit('EXECUTION: BLOCKED\nno eligible phase')
    tid = _eligible_task(ex, package, pid)
    if not tid: raise SystemExit('EXECUTION: BLOCKED\nno eligible task')
    t = ex['tasks'][tid]; kind = t.pop('pending_attempt_kind', None) or 'INITIAL'
    kwargs = {}
    if kind == 'RECOVERY':
        rec = t.get('recovery') or {}; kwargs = {'issue_id': rec.get('issue_id'), 'recovery_contract_digest': rec.get('contract_digest'), 'required_changes': rec.get('required_changes'), 'regression_verification': rec.get('regression_verification'), 'recovery_authorized_paths': rec.get('authorized_paths'), 'recovery_verification': rec.get('verification'), 'recovery_completion_criteria': rec.get('completion_criteria'), 'production_baseline': t.get('task_baseline')}
    t['status'] = 'IN_PROGRESS'; ex['tasks'][tid] = t; cycle['execution'] = ex; st['cycles'][cid] = cycle
    save_state(st, event='TASK_SELECTED', actor='tool:execution', details={'phase': pid, 'task': tid, 'attempt_kind': kind})
    mode, meta, ticket = W.acquire('BUILDER', 'vscode', 'Builder', tid, attempt_kind=kind, **kwargs)
    st = load_state(); cycle = st['cycles'][cid]; ex = cycle['execution']; ex['tasks'][tid]['active_attempt'] = meta['attempt_id']; ex['tasks'][tid]['last_attempt'] = meta['attempt_id']; ex['tasks'][tid].setdefault('task_baseline', meta.get('production_baseline')); cycle['execution'] = ex; st['cycles'][cid] = cycle
    save_state(st, event='TASK_DISPATCHED', actor='tool:execution', details={'phase': pid, 'task': tid, 'attempt': meta['attempt_id'], 'kind': kind})
    print('TASK_DISPATCH: PASS'); print('phase:', pid); print('task:', tid); print('ticket:', json.dumps(ticket, sort_keys=True)); raise SystemExit
if a.cmd == 'resume':
    tid = st.get('active_task')
    if not tid or not st.get('active_work'): raise SystemExit('EXECUTION: BLOCKED\nno active Builder Work')
    meta0 = W.status(); mode, meta, ticket = W.acquire('BUILDER', 'vscode', 'Builder', tid, attempt_kind=meta0.get('attempt_kind', 'INITIAL'))
    print('TASK_RESUME:', mode); print('task:', tid); print('attempt:', meta.get('attempt_id')); print('ticket:', json.dumps(ticket, sort_keys=True)); raise SystemExit
if a.cmd == 'complete':
    tid = st.get('active_task')
    if not tid: raise SystemExit('EXECUTION: BLOCKED\nno active task')
    passed, errors, detail = task_gate(st, cycle, tid, a.evidence)
    t = ex['tasks'][tid]; attempt_id = st.get('active_attempt') or t.get('active_attempt'); attempt = ex.get('attempts', {}).get(attempt_id, {})
    if not passed:
        t['status'] = 'GATE_FAILED'; t['last_gate_errors'] = errors; t['structural_failure'] = _gate_failure_structural(errors); t['evidence'] = a.evidence
        attempt['status'] = 'GATE_FAILED'; attempt['verification_status'] = 'FAIL'; attempt['evidence_manifest'] = a.evidence
        ex['tasks'][tid] = t; ex['attempts'][attempt_id] = attempt; cycle['execution'] = ex; st['cycles'][cid] = cycle
        save_state(st, event='TASK_GATE_FAIL', actor='machine:task_gate', details={'task': tid, 'attempt': attempt_id, 'errors': errors, 'structural': t['structural_failure']})
        print('TASK_GATE: FAIL'); print(json.dumps({'errors': errors, 'structural': t['structural_failure']}, sort_keys=True)); raise SystemExit(2)
    t['status'] = 'PASS'; t['evidence'] = a.evidence; t['last_gate_errors'] = []; t['structural_failure'] = False
    attempt['status'] = 'PASS'; attempt['verification_status'] = 'PASS'; attempt['evidence_manifest'] = a.evidence
    if attempt.get('kind') == 'RECOVERY':
        issue_id = attempt.get('issue_id') or (t.get('recovery') or {}).get('issue_id')
        for issue in cycle.get('issues', []):
            if issue.get('issue_id') == issue_id:
                issue['status'] = 'RESOLVED'; issue['resolved_at'] = now(); issue['resolution_attempt'] = attempt_id
                break
    ex['tasks'][tid] = t; ex['attempts'][attempt_id] = attempt; cycle['execution'] = ex; st['cycles'][cid] = cycle
    st['active_task'] = None; st['active_attempt'] = None
    save_state(st, event='TASK_GATE_PASS', actor='machine:task_gate', details={'task': tid, 'attempt': attempt_id}); print('TASK_GATE: PASS'); raise SystemExit
if a.cmd == 'repair':
    tid = st.get('active_task'); t = ex.get('tasks', {}).get(tid)
    if not tid or not t or t.get('status') != 'GATE_FAILED': raise SystemExit('REPAIR: BLOCKED\nTask Gate failure required')
    if t.get('structural_failure'):
        iid = _escalate(st, cid, cycle, ex, 'structural Task Gate failure: ' + '; '.join(t.get('last_gate_errors') or []), task=tid, phase=t.get('phase_id')); print('REPAIR: DIAGNOSIS_REQUIRED'); print('issue:', iid); raise SystemExit(2)
    used = int(t.get('repair_attempts', 0)); limit = int(t.get('max_repairs', 2))
    if used >= limit:
        iid = _escalate(st, cid, cycle, ex, 'bounded local repair limit exceeded', task=tid, phase=t.get('phase_id')); print('REPAIR: DIAGNOSIS_REQUIRED'); print('issue:', iid); raise SystemExit(2)
    parent = t.get('active_attempt') or t.get('last_attempt'); ordinal = used + 1
    t['repair_attempts'] = ordinal; t['status'] = 'IN_PROGRESS'; ex['tasks'][tid] = t; cycle['execution'] = ex; st['cycles'][cid] = cycle
    save_state(st, event='LOCAL_REPAIR_GRANTED', actor='tool:execution', details={'task': tid, 'repair_ordinal': ordinal, 'parent_attempt': parent})
    mode, meta, ticket = W.acquire('BUILDER', 'vscode', 'Builder', tid, attempt_kind='REPAIR', parent_attempt_id=parent, repair_ordinal=ordinal, failure_evidence=t.get('evidence'), production_baseline=t.get('task_baseline'))
    st = load_state(); cycle = st['cycles'][cid]; ex = cycle['execution']; ex['tasks'][tid]['active_attempt'] = meta['attempt_id']; ex['tasks'][tid]['last_attempt'] = meta['attempt_id']; cycle['execution'] = ex; st['cycles'][cid] = cycle
    save_state(st, event='REPAIR_DISPATCHED', actor='tool:execution', details={'task': tid, 'attempt': meta['attempt_id'], 'repair_ordinal': ordinal, 'parent_attempt': parent})
    print('REPAIR: ALLOWED'); print('attempt:', meta['attempt_id']); print('repair_ordinal:', ordinal); print('ticket:', json.dumps(ticket, sort_keys=True)); raise SystemExit
if a.cmd == 'fail':
    tid = st.get('active_task')
    if not tid: raise SystemExit('EXECUTION: BLOCKED\nno active task')
    iid = _escalate(st, cid, cycle, ex, a.reason, task=tid, phase=(ex.get('tasks') or {}).get(tid, {}).get('phase_id'))
    print('TASK_FAIL: DIAGNOSIS_REQUIRED'); print('issue:', iid); raise SystemExit
if a.cmd == 'phase-gate':
    pid = _eligible_phase(ex, package)
    if not pid or not _all_phase_tasks_pass(ex, package, pid): raise SystemExit('PHASE_GATE: BLOCKED\nphase tasks are not complete')
    passed, errors, evidence = phase_gate(st, cycle, pid, a.evidence)
    if not passed:
        iid = _escalate(st, cid, cycle, ex, 'Phase Gate failure: ' + '; '.join(errors), phase=pid)
        print('PHASE_GATE: FAIL'); print('issue:', iid); print(json.dumps(errors)); raise SystemExit(2)
    ex['phases'][pid]['status'] = 'PASS'; ex['phases'][pid]['evidence'] = a.evidence; cycle['execution'] = ex; st['cycles'][cid] = cycle; st['active_phase'] = None
    save_state(st, event='PHASE_GATE_PASS', actor='machine:phase_gate', details={'phase': pid}); print('PHASE_GATE: PASS'); print('phase:', pid); raise SystemExit
if a.cmd == 'finalize':
    incomplete = [pid for pid, v in ex.get('phases', {}).items() if v.get('status') != 'PASS']
    if incomplete: raise SystemExit('EXECUTION: BLOCKED\nincomplete phases: ' + ', '.join(incomplete))
    ex['status'] = 'COMPLETE'; cycle['execution'] = ex; cycle['status'] = 'EVALUATION'; st['cycles'][cid] = cycle; st['project_state'] = 'EVALUATION'; st['lifecycle_stage'] = 'EVALUATION'; st['next_action'] = 'EXECUTE_EVALUATION'
    save_state(st, event='EXECUTION_COMPLETE', actor='tool:execution'); print('EXECUTION_COMPLETE: PASS')
