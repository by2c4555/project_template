from __future__ import annotations
import hashlib, json
from pathlib import Path
from .paths import ROOT, WORK_DIR, WORKPLAN
from .state import load_state, save_state, next_id, now
from .io import atomic_write_json, atomic_write_text
from .integrity import build_package_manifest, sha256_file
from .contracts import load_contract_package
from .mutation import snapshot_production, diff_snapshots
from .tickets import issue_ticket, load_ticket

ROLES = {'PLANNING', 'BUILDER', 'DIAGNOSIS', 'RECOVERY', 'EVALUATION'}
CONTEXT_REASONS = {'REQUIREMENT', 'ARCHITECTURE', 'INTERFACE', 'DATA_MODEL', 'PRIOR_DECISION', 'ACTIVE_UNIT', 'FAILURE_EVIDENCE', 'WORKTREE'}
REASONING_ONLY_ROLES = {'PLANNING', 'DIAGNOSIS', 'RECOVERY', 'EVALUATION'}


def work_path(wid):
    return WORK_DIR / wid


def _json_digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def _cycle(st):
    cid = st.get('active_cycle')
    return cid, (st.get('cycles') or {}).get(cid, {})


def _current_binding(st, role, task_id=None, attempt_kind='INITIAL', recovery_contract_digest=None):
    cid, cycle = _cycle(st)
    binding = {
        'cycle_id': cid,
        'scope_digest': (cycle.get('scope') or {}).get('digest'),
        'ingest_digest': (cycle.get('ingest') or {}).get('package_digest'),
        'planning_package_digest': (cycle.get('planning') or {}).get('candidate_package_digest'),
        'phase_digest': None,
        'task_digest': None,
        'recovery_contract_digest': recovery_contract_digest,
    }
    if role == 'BUILDER' and task_id:
        package = load_contract_package(validate=True)
        task = package['tasks'].get(task_id)
        if not task:
            raise SystemExit(f'WORK_BINDING: BLOCKED\nmissing task contract {task_id}')
        phase = package['phases'][task['phase_id']]
        binding['phase_digest'] = _json_digest(phase)
        binding['task_digest'] = task['digest']
        if attempt_kind == 'RECOVERY':
            rec = ((((cycle.get('execution') or {}).get('tasks') or {}).get(task_id) or {}).get('recovery') or {})
            rel = rec.get('contract')
            rp = ROOT / rel if rel else None
            current_digest = sha256_file(rp) if rp and rp.is_file() else None
            if not current_digest:
                raise SystemExit('WORK_BINDING: BLOCKED\nRecovery Contract missing')
            if recovery_contract_digest is not None and current_digest != recovery_contract_digest:
                raise SystemExit('WORK_BINDING: BLOCKED\nRecovery Contract digest mismatch')
            binding['recovery_contract_digest'] = current_digest
    return binding


def _compare_binding(original, current):
    return {k: {'issued': original.get(k), 'current': current.get(k)} for k in sorted(set(original) | set(current)) if original.get(k) != current.get(k)}


def _task_contract(task_id):
    package = load_contract_package(validate=True)
    task = package['tasks'].get(task_id)
    if not task:
        raise SystemExit(f'WORK: BLOCKED\nunknown task {task_id}')
    return package, task


def _ticket(meta, st, action='CONTINUE'):
    if meta.get('role') != 'BUILDER':
        return {
            'ticket_schema': 2, 'ticket_kind': 'RESUME' if meta.get('checkpoint_seq', 0) else 'ACTION',
            'action': action, 'role': meta['role'], 'work_id': meta['work_id'], 'generation': meta['generation'],
            'checkpoint_seq': meta.get('checkpoint_seq', 0), 'unit': meta.get('next_unit'),
            'input_bindings': meta.get('input_bindings', {}), 'read': meta.get('context_paths', []),
            'write': [], 'allowed_actions': ['CHECKPOINT', 'COMPLETE', 'NEED_CONTEXT']
        }
    _, task = _task_contract(meta['task_id'])
    b = meta['input_bindings']
    kind = meta.get('attempt_kind', 'INITIAL')
    ticket_kind = 'TASK' if kind == 'INITIAL' else kind
    ticket = {
        'ticket_schema': 2,
        'ticket_kind': ticket_kind,
        'cycle_id': b.get('cycle_id'),
        'phase_id': meta.get('phase_id'),
        'task_id': meta.get('task_id'),
        'attempt_id': meta.get('attempt_id'),
        'work_id': meta.get('work_id'),
        'generation': meta.get('generation'),
        'state_seq': int(st.get('state_seq', 0)) + 1,
        'scope_digest': b.get('scope_digest'),
        'planning_package_digest': b.get('planning_package_digest'),
        'phase_digest': b.get('phase_digest'),
        'task_digest': b.get('task_digest'),
        'authorized_paths': meta.get('recovery_authorized_paths', []) if kind == 'RECOVERY' else task.get('authorized_paths', []),
        'granted_context': sorted(set(task.get('required_context', [])) | set(meta.get('context_paths', []))),
        'architecture_bindings': task.get('architecture_bindings', []),
        'interface_bindings': task.get('interface_bindings', []),
        'verification': list(dict.fromkeys(task.get('verification', []) + (meta.get('recovery_verification', []) if kind == 'RECOVERY' else []) + (meta.get('regression_verification', []) if kind == 'RECOVERY' else []))),
        'required_evidence': task.get('required_evidence', []),
        'allowed_actions': ['CHECKPOINT', 'COMPLETE', 'NEED_CONTEXT', 'FAIL'],
    }
    if kind == 'REPAIR':
        ticket.update({
            'parent_attempt_id': meta.get('parent_attempt_id'),
            'repair_ordinal': meta.get('repair_ordinal'),
            'failure_evidence': meta.get('failure_evidence'),
            'repair_objective': meta.get('repair_objective') or 'Resolve the recorded Task Gate failure without expanding authority.',
            'prohibited_repeated_strategies': meta.get('prohibited_repeated_strategies', []),
            'max_repairs': meta.get('max_repairs'),
            'remaining_repairs': meta.get('remaining_repairs'),
        })
    if kind == 'RECOVERY':
        ticket.update({
            'recovery_contract_digest': b.get('recovery_contract_digest'),
            'issue_id': meta.get('issue_id'),
            'required_changes': meta.get('required_changes', []),
            'regression_verification': meta.get('regression_verification', []),
            'completion_criteria': meta.get('recovery_completion_criteria', []),
        })
    return ticket


def _issue_current_ticket(meta, st):
    p = work_path(meta['work_id']) / 'tickets'
    p.mkdir(parents=True, exist_ok=True)
    seq = int(meta.get('ticket_seq', 0)) + 1
    ticket = issue_ticket(p / f'TICKET_{seq:04d}.json', _ticket(meta, st))
    meta['ticket_seq'] = seq
    meta['current_ticket_path'] = str((p / f'TICKET_{seq:04d}.json').relative_to(ROOT)).replace('\\', '/')
    meta['ticket_digest'] = ticket['ticket_digest']
    return ticket


def current_ticket(meta):
    rel = meta.get('current_ticket_path')
    if not rel:
        return None
    return load_ticket(ROOT / rel)


def reconcile(meta):
    before = meta.get('production_baseline') or {}
    after = snapshot_production()
    changed = diff_snapshots(before, after)
    return {'status': 'RECONCILE_ACTIVE_UNIT' if changed else 'CLEAN', 'changed': changed}


def acquire(role, tool='unknown', model='unknown', task_id=None, *, attempt_kind='INITIAL', parent_attempt_id=None,
            repair_ordinal=None, issue_id=None, recovery_contract_digest=None, failure_evidence=None,
            required_changes=None, regression_verification=None, recovery_authorized_paths=None, recovery_verification=None,
            recovery_completion_criteria=None, production_baseline=None):
    role = role.upper()
    if role not in ROLES:
        raise SystemExit('WORK: BLOCKED\nunsupported role')
    st = load_state(); aw = st.get('active_work')
    if aw:
        p = work_path(aw); meta = json.loads((p / 'WORK.json').read_text(encoding='utf-8'))
        compatible = meta.get('status') != 'COMPLETED' and meta.get('role') == role and (task_id is None or meta.get('task_id') == task_id)
        if not compatible:
            raise SystemExit(f'WORK: BLOCKED\nactive work exists: {aw}')
        current = _current_binding(st, role, meta.get('task_id'), meta.get('attempt_kind', 'INITIAL'))
        mismatch = _compare_binding(meta.get('input_bindings') or {}, current)
        if mismatch:
            raise SystemExit('WORK_BINDING_MISMATCH: BLOCKED\n' + json.dumps(mismatch, sort_keys=True))
        meta['generation'] = int(meta.get('generation', 0)) + 1
        meta['last_agent'] = {'tool': tool, 'model': model, 'at': now()}
        ticket = _issue_current_ticket(meta, st) if role == 'BUILDER' else _ticket(meta, st, 'RECONCILE' if reconcile(meta)['status'] != 'CLEAN' else 'CONTINUE')
        atomic_write_json(p / 'WORK.json', meta)
        if role == 'BUILDER':
            cid, cycle = _cycle(st)
            attempt = ((cycle.get('execution') or {}).get('attempts') or {}).get(meta.get('attempt_id'))
            if attempt:
                attempt['generation'] = meta['generation']; attempt['ticket_digest'] = meta.get('ticket_digest')
                st['cycles'][cid] = cycle
        save_state(st, event='WORK_ACQUIRED', actor='agent:work', details={'work_id': aw, 'role': role, 'generation': meta['generation'], 'attempt_id': meta.get('attempt_id')})
        return 'RESUME', meta, ticket

    wid = next_id(st, 'work', 'WORK_')
    p = work_path(wid); (p / 'checkpoints').mkdir(parents=True, exist_ok=True); (p / 'evidence').mkdir(exist_ok=True); (p / 'tickets').mkdir(exist_ok=True)
    phase_id = None; attempt_id = None; task = None
    if role == 'BUILDER':
        if not task_id:
            raise SystemExit('WORK: BLOCKED\nBuilder requires task_id')
        _, task = _task_contract(task_id); phase_id = task['phase_id']; attempt_id = next_id(st, 'attempt', 'ATTEMPT_')
        if attempt_kind not in {'INITIAL', 'REPAIR', 'RECOVERY'}:
            raise SystemExit('WORK: BLOCKED\ninvalid attempt kind')
        if attempt_kind == 'RECOVERY' and not recovery_contract_digest:
            raise SystemExit('WORK: BLOCKED\nRecovery Attempt requires Recovery Contract digest')
    binding = _current_binding(st, role, task_id, attempt_kind, recovery_contract_digest)
    initial_context = task.get('required_context', []) if task else []
    meta = {
        'work_id': wid, 'role': role, 'task_id': task_id, 'phase_id': phase_id, 'attempt_id': attempt_id,
        'attempt_kind': attempt_kind if role == 'BUILDER' else None, 'parent_attempt_id': parent_attempt_id,
        'repair_ordinal': repair_ordinal, 'issue_id': issue_id, 'status': 'IN_PROGRESS', 'generation': 1,
        'checkpoint_seq': 0, 'ticket_seq': 0, 'current_unit': 'INIT',
        'next_unit': 'TASK_PREFLIGHT' if role == 'BUILDER' else 'INIT_MAP',
        'last_agent': {'tool': tool, 'model': model, 'at': now()}, 'created_at': now(),
        'input_bindings': binding, 'context_paths': list(initial_context), 'production_baseline': dict(production_baseline) if production_baseline is not None else snapshot_production(),
        'failure_evidence': failure_evidence, 'required_changes': required_changes or [],
        'regression_verification': regression_verification or [], 'recovery_authorized_paths': recovery_authorized_paths or [],
        'recovery_verification': recovery_verification or [], 'recovery_completion_criteria': recovery_completion_criteria or [],
    }
    if task:
        max_repairs = int(task.get('max_repairs', 2)); used = int(repair_ordinal or 0)
        meta['max_repairs'] = max_repairs; meta['remaining_repairs'] = max(0, max_repairs - used)
    ticket = _issue_current_ticket(meta, st) if role == 'BUILDER' else _ticket(meta, st)
    atomic_write_json(p / 'WORK.json', meta)
    atomic_write_text(p / 'MAP.md', f'# {wid} {role} Work Map\n\nstatus: INIT\n\nPersist verified decisions/evidence and exact next bounded unit.\n')
    atomic_write_text(p / 'RESUME.md', f'# Resume {wid}\n\nrole: {role}\ngeneration: 1\ncheckpoint_seq: 0\nnext_unit: {meta["next_unit"]}\n')
    st['active_work'] = wid
    if role == 'BUILDER':
        st['active_phase'] = phase_id; st['active_task'] = task_id; st['active_attempt'] = attempt_id
        cid, cycle = _cycle(st); ex = cycle.setdefault('execution', {}); attempts = ex.setdefault('attempts', {})
        attempts[attempt_id] = {
            'attempt_id': attempt_id, 'kind': attempt_kind, 'task_id': task_id, 'phase_id': phase_id,
            'parent_attempt_id': parent_attempt_id, 'repair_ordinal': repair_ordinal, 'work_id': wid,
            'generation': 1, 'state_seq_at_issue': int(st.get('state_seq', 0)) + 1,
            'ticket_digest': meta.get('ticket_digest'), 'status': 'IN_PROGRESS', 'started_at': now(),
            'completed_at': None, 'verification_status': None, 'evidence_manifest': None, 'mutation_manifest': None,
        }
        ex['attempts'] = attempts; cycle['execution'] = ex; st['cycles'][cid] = cycle
    save_state(st, event='WORK_BEGIN', actor='agent:work', details={'work_id': wid, 'role': role, 'task_id': task_id, 'phase_id': phase_id, 'attempt_id': attempt_id, 'generation': 1})
    return 'START', meta, ticket


def begin(role, tool='unknown', model='unknown', task_id=None):
    return acquire(role, tool, model, task_id)[:2]


def status():
    st = load_state(); wid = st.get('active_work')
    if not wid:
        return None
    return json.loads((work_path(wid) / 'WORK.json').read_text(encoding='utf-8'))


def _require_generation(meta, expected_generation):
    if expected_generation is None or int(expected_generation) != int(meta.get('generation', 0)):
        raise SystemExit(f'STALE_GENERATION\nexpected={expected_generation} current={meta.get("generation")}')


def _require_binding(st, meta):
    current = _current_binding(st, meta['role'], meta.get('task_id'), meta.get('attempt_kind', 'INITIAL'))
    mismatch = _compare_binding(meta.get('input_bindings') or {}, current)
    if mismatch:
        raise SystemExit('WORK_BINDING_MISMATCH: BLOCKED\n' + json.dumps(mismatch, sort_keys=True))


def checkpoint(unit, next_unit, note, expected_generation):
    st = load_state(); wid = st.get('active_work')
    if not wid:
        raise SystemExit('WORK: BLOCKED\nno active work')
    p = work_path(wid); meta = json.loads((p / 'WORK.json').read_text(encoding='utf-8'))
    _require_generation(meta, expected_generation); _require_binding(st, meta)
    seq = int(meta.get('checkpoint_seq', 0)) + 1
    cp = {'work_id': wid, 'attempt_id': meta.get('attempt_id'), 'generation': meta['generation'], 'checkpoint_seq': seq, 'unit': unit, 'next_unit': next_unit, 'note': note, 'created_at': now()}
    atomic_write_json(p / 'checkpoints' / f'CP_{seq:04d}.json', cp)
    meta.update({'checkpoint_seq': seq, 'current_unit': unit, 'next_unit': next_unit, 'status': 'CHECKPOINTED'})
    atomic_write_json(p / 'WORK.json', meta)
    atomic_write_text(p / 'RESUME.md', f'# Resume {wid}\n\nrole: {meta["role"]}\ngeneration: {meta["generation"]}\ncheckpoint_seq: {seq}\nlast_completed_unit: {unit}\nnext_unit: {next_unit}\n\n## Verified durable note\n\n{note}\n')
    save_state(st, event='WORK_CHECKPOINT', actor='agent:work', details={'work_id': wid, 'attempt_id': meta.get('attempt_id'), 'generation': meta['generation'], 'checkpoint_seq': seq, 'unit': unit, 'next_unit': next_unit})
    return cp


def complete(note, expected_generation):
    st = load_state(); wid = st.get('active_work')
    if not wid:
        raise SystemExit('WORK: BLOCKED\nno active work')
    p = work_path(wid); meta = json.loads((p / 'WORK.json').read_text(encoding='utf-8'))
    _require_generation(meta, expected_generation); _require_binding(st, meta)
    mutations = diff_snapshots(meta.get('production_baseline') or {}, snapshot_production())
    if meta['role'] in REASONING_ONLY_ROLES and mutations:
        raise SystemExit('REASONING_ONLY_MUTATION: BLOCKED\n' + json.dumps(mutations, sort_keys=True))
    if meta['role'] == 'BUILDER':
        mpath = p / 'evidence' / 'MUTATION_MANIFEST.json'
        atomic_write_json(mpath, {'schema_version': 1, 'attempt_id': meta.get('attempt_id'), 'task_id': meta.get('task_id'), 'phase_id': meta.get('phase_id'), 'generation': meta.get('generation'), 'mutations': mutations, 'created_at': now()})
        meta['mutation_manifest_path'] = str(mpath.relative_to(ROOT)).replace('\\', '/')
    meta['status'] = 'COMPLETED'; meta['completed_at'] = now(); meta['completion_note'] = note
    atomic_write_json(p / 'WORK.json', meta)
    st['last_completed_work'] = wid; st['active_work'] = None
    if meta['role'] == 'BUILDER':
        cid, cycle = _cycle(st); attempt = ((cycle.get('execution') or {}).get('attempts') or {}).get(meta.get('attempt_id'))
        if attempt:
            attempt['status'] = 'COMPLETED_UNGATED'; attempt['completed_at'] = now(); attempt['mutation_manifest'] = meta.get('mutation_manifest_path')
            st['cycles'][cid] = cycle
    save_state(st, event='WORK_COMPLETE', actor='agent:work', details={'work_id': wid, 'role': meta['role'], 'attempt_id': meta.get('attempt_id'), 'generation': meta['generation']})
    return meta


def request_context(reason):
    reason = reason.upper()
    if reason not in CONTEXT_REASONS:
        raise SystemExit('CONTEXT: BLOCKED\nunsupported reason')
    st = load_state(); wid = st.get('active_work')
    if not wid:
        raise SystemExit('CONTEXT: BLOCKED\nno active work')
    p = work_path(wid); meta = json.loads((p / 'WORK.json').read_text(encoding='utf-8')); task = meta.get('task_id')
    mapping = {
        'REQUIREMENT': ['Workplan/compiled/PROJECT_BRIEF.md', 'Workplan/compiled/GLOBAL_CONSTRAINTS.md'],
        'ARCHITECTURE': ['Workplan/compiled/ARCHITECTURE.md'], 'INTERFACE': ['Workplan/compiled/INTERFACES.md'],
        'DATA_MODEL': ['Workplan/compiled/DATA_MODEL.md'], 'PRIOR_DECISION': ['Workplan/compiled/DECISIONS.md'],
        'ACTIVE_UNIT': [f'Workplan/work/{wid}/RESUME.md'], 'FAILURE_EVIDENCE': [f'Workplan/work/{wid}/evidence'], 'WORKTREE': []
    }
    paths = mapping[reason][:]
    if task and reason in {'REQUIREMENT', 'ACTIVE_UNIT'}:
        paths.insert(0, f'Workplan/tasks/{task}.md')
    meta['context_paths'] = sorted(set(meta.get('context_paths', [])) | set(paths))
    ticket = _issue_current_ticket(meta, st) if meta.get('role') == 'BUILDER' else None
    atomic_write_json(p / 'WORK.json', meta)
    save_state(st, event='CONTEXT_GRANTED', actor='machine:work', details={'work_id': wid, 'attempt_id': meta.get('attempt_id'), 'reason': reason, 'paths': paths})
    return {'reason': reason, 'level': 'L1', 'paths': paths, 'granted_context': meta['context_paths'], 'authority_unchanged': True, 'ticket': ticket}
