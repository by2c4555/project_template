from __future__ import annotations
import hashlib, json
from pathlib import Path
from .paths import ROOT, WORKPLAN
from .contracts import load_contract_package
from .integrity import build_package_manifest, sha256_file
from .mutation import validate_mutations
from .tickets import load_ticket


def _json_digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def _load_json(path: Path, label):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        raise ValueError(f'{label}: invalid JSON: {e}')


def _current_bindings(st, cycle, task, phase, attempt):
    recovery_digest = None
    if (attempt or {}).get('kind') == 'RECOVERY':
        task_state = ((((cycle.get('execution') or {}).get('tasks') or {}).get(task.get('task_id')) or {}))
        rec = task_state.get('recovery') or {}
        rel = rec.get('contract')
        rp = ROOT / rel if rel else None
        recovery_digest = sha256_file(rp) if rp and rp.is_file() else None
    return {
        'cycle_id': st.get('active_cycle'),
        'scope_digest': (cycle.get('scope') or {}).get('digest'),
        'ingest_digest': (cycle.get('ingest') or {}).get('package_digest'),
        'planning_package_digest': (cycle.get('planning') or {}).get('candidate_package_digest'),
        'phase_digest': _json_digest(phase),
        'task_digest': task.get('digest'),
        'recovery_contract_digest': recovery_digest,
    }


def task_gate(st, cycle, task_id, evidence_rel):
    ex = cycle.get('execution') or {}
    tstate = (ex.get('tasks') or {}).get(task_id)
    if not tstate:
        return False, ['task not in execution state'], None
    package = load_contract_package(validate=True)
    task = package['tasks'].get(task_id); phase = package['phases'].get(task['phase_id']) if task else None
    errors = []
    if not task or not phase:
        return False, ['task/phase contract missing'], None
    attempt_id = st.get('active_attempt') or tstate.get('active_attempt')
    attempt = (ex.get('attempts') or {}).get(attempt_id)
    if not attempt:
        errors.append('active attempt missing')
        return False, errors, None
    work_id = attempt.get('work_id'); wp = WORKPLAN / 'work' / str(work_id)
    mp = wp / 'WORK.json'
    if not mp.is_file():
        errors.append('work metadata missing')
        return False, errors, None
    work = _load_json(mp, 'work')
    if work.get('status') != 'COMPLETED': errors.append('Builder Work not completed')
    if work.get('role') != 'BUILDER': errors.append('completed Work is not Builder')
    if work.get('attempt_id') != attempt_id: errors.append('work attempt mismatch')
    if work.get('task_id') != task_id: errors.append('work task mismatch')
    if work.get('phase_id') != task['phase_id']: errors.append('work phase mismatch')
    if int(work.get('generation', -1)) != int(attempt.get('generation', -2)): errors.append('generation mismatch')
    ticket_rel = work.get('current_ticket_path')
    try:
        ticket = load_ticket(ROOT / ticket_rel) if ticket_rel else None
    except Exception as e:
        ticket = None; errors.append(f'ticket invalid: {e}')
    if not ticket:
        errors.append('ticket missing')
    else:
        if ticket.get('ticket_digest') != work.get('ticket_digest') or ticket.get('ticket_digest') != attempt.get('ticket_digest'):
            errors.append('ticket digest mismatch')
        for key, val in [('attempt_id', attempt_id), ('task_id', task_id), ('phase_id', task['phase_id'])]:
            if ticket.get(key) != val: errors.append(f'ticket {key} mismatch')
        if int(ticket.get('generation', -1)) != int(work.get('generation', -2)): errors.append('ticket generation mismatch')
    manifest = build_package_manifest()
    planning = cycle.get('planning') or {}
    if manifest.get('package_digest') != planning.get('candidate_package_digest') or manifest.get('package_digest') != ex.get('package_digest'):
        errors.append('planning package digest changed')
    issued = work.get('input_bindings') or {}
    current = _current_bindings(st, cycle, task, phase, attempt)
    for key, val in current.items():
        if issued.get(key) != val:
            errors.append(f'immutable binding mismatch: {key}')
    ep = ROOT / evidence_rel
    evidence = None
    if not ep.is_file():
        errors.append('evidence manifest missing')
    else:
        try: evidence = _load_json(ep, 'evidence')
        except Exception as e: errors.append(str(e))
    if evidence:
        required = {
            'attempt_id': attempt_id, 'task_id': task_id, 'phase_id': task['phase_id'],
            'generation': work.get('generation'), 'ticket_digest': work.get('ticket_digest'), 'status': 'PASS'
        }
        for key, val in required.items():
            if evidence.get(key) != val: errors.append(f'evidence {key} mismatch')
        actual_verification = evidence.get('verification') or []
        by_command = {row.get('command'): row for row in actual_verification if isinstance(row, dict)}
        required_verification = (ticket or {}).get('verification', task.get('verification', []))
        for command in required_verification:
            row = by_command.get(command)
            if not row: errors.append(f'missing verification: {command}')
            elif int(row.get('exit_code', -1)) != 0: errors.append(f'verification failed: {command}')
        artifacts = {row.get('path'): row for row in (evidence.get('artifacts') or []) if isinstance(row, dict)}
        for req in task.get('required_evidence', []):
            if req not in artifacts: errors.append(f'missing required evidence artifact: {req}')
            elif (ROOT / req).is_file() and artifacts[req].get('sha256') != sha256_file(ROOT / req): errors.append(f'evidence artifact digest mismatch: {req}')
        if evidence.get('mutation_manifest_path') != work.get('mutation_manifest_path'):
            errors.append('mutation manifest binding mismatch')
    mrel = work.get('mutation_manifest_path'); mutation_manifest = None
    if not mrel or not (ROOT / mrel).is_file():
        errors.append('mutation manifest missing')
    else:
        mutation_manifest = _load_json(ROOT / mrel, 'mutation manifest')
        if mutation_manifest.get('attempt_id') != attempt_id or mutation_manifest.get('generation') != work.get('generation'):
            errors.append('mutation manifest identity mismatch')
        auth = validate_mutations(mutation_manifest.get('mutations') or [], (ticket or {}).get('authorized_paths', task.get('authorized_paths', [])))
        if auth['status'] != 'PASS':
            errors.append('unauthorized production mutation: ' + ', '.join(x['path'] for x in auth['unauthorized']))
    if errors:
        return False, errors, {'attempt': attempt, 'work': work, 'evidence': evidence, 'mutation_manifest': mutation_manifest}
    return True, [], {'attempt': attempt, 'work': work, 'evidence': evidence, 'mutation_manifest': mutation_manifest}


def phase_gate(st, cycle, phase_id, evidence_rel=None):
    ex = cycle.get('execution') or {}; package = load_contract_package(validate=True)
    phase = package['phases'].get(phase_id); errors = []
    if not phase:
        return False, ['phase missing'], None
    for dep in phase.get('depends_on', []):
        if (ex.get('phases') or {}).get(dep, {}).get('status') != 'PASS': errors.append(f'phase dependency not PASS: {dep}')
    phase_tasks = [t for t, c in package['tasks'].items() if c['phase_id'] == phase_id]
    for tid in phase_tasks:
        if (ex.get('tasks') or {}).get(tid, {}).get('status') != 'PASS': errors.append(f'task not PASS: {tid}')
    evidence = None
    if phase.get('verification') or phase.get('required_evidence'):
        if not evidence_rel or not (ROOT / evidence_rel).is_file():
            errors.append('phase evidence manifest required')
        else:
            evidence = _load_json(ROOT / evidence_rel, 'phase evidence')
            if evidence.get('phase_id') != phase_id or evidence.get('status') != 'PASS': errors.append('phase evidence identity/status mismatch')
            by_command = {x.get('command'): x for x in (evidence.get('verification') or []) if isinstance(x, dict)}
            for command in phase.get('verification', []):
                row = by_command.get(command)
                if not row or int(row.get('exit_code', -1)) != 0: errors.append(f'phase verification missing/failed: {command}')
            artifacts = {x.get('path'): x for x in (evidence.get('artifacts') or []) if isinstance(x, dict)}
            for req in phase.get('required_evidence', []):
                if req not in artifacts: errors.append(f'phase evidence artifact missing: {req}')
    unresolved = [i.get('issue_id') for i in cycle.get('issues', []) if i.get('status') not in {'RESOLVED', 'SUPERSEDED'} and (i.get('phase_id') in {None, phase_id})]
    if unresolved: errors.append('unresolved issues: ' + ', '.join(unresolved))
    return (not errors), errors, evidence
