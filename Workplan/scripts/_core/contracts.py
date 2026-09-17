from __future__ import annotations
import json
from pathlib import Path, PurePosixPath
from .paths import ROOT, WORKPLAN, TASK_DIR, PLAN_DIR
from .integrity import field, inline_list, sha256_file

DEFAULT_MAX_REPAIRS = 2
MAX_REPAIRS_RANGE = range(0, 6)
PHASES_PATH = PLAN_DIR / 'PHASES.json'


def _present(text, key):
    return field(text, key) is not None


def normalize_relpath(value: str) -> str:
    raw = value.replace('\\', '/').strip()
    p = PurePosixPath(raw)
    if not raw or p.is_absolute() or '..' in p.parts or '.' in p.parts or raw.startswith('/'):
        raise ValueError(f'unsafe path: {value}')
    norm = str(p)
    if norm == 'Workplan' or norm.startswith('Workplan/') or norm == '.git' or norm.startswith('.git/'):
        raise ValueError(f'control path cannot be production authority: {value}')
    return norm.rstrip('/') + ('/' if raw.endswith('/') else '')


def _task(fp: Path):
    text = fp.read_text(encoding='utf-8')
    required_keys = ['objective', 'depends_on', 'authorized_paths', 'acceptance_criteria']
    missing = [k for k in required_keys if not _present(text, k)]
    verification_key = 'verification' if _present(text, 'verification') else 'verification_commands' if _present(text, 'verification_commands') else None
    evidence_key = 'required_evidence' if _present(text, 'required_evidence') else None
    if not verification_key:
        missing.append('verification')
    if not evidence_key:
        missing.append('required_evidence')
    if missing:
        raise ValueError(f'{fp.stem}: missing fields: {", ".join(missing)}')
    raw_max_repairs = field(text, 'max_repairs')
    max_repairs = DEFAULT_MAX_REPAIRS if raw_max_repairs is None else int(raw_max_repairs)
    if max_repairs not in MAX_REPAIRS_RANGE:
        raise ValueError(f'{fp.stem}: max_repairs must be 0..5')
    paths = [normalize_relpath(x) for x in inline_list(text, 'authorized_paths')]
    required_context = inline_list(text, 'required_context') or inline_list(text, 'context_manifest')
    explicit_phase_id = field(text, 'phase_id')
    phase_id = explicit_phase_id or 'PHASE_001'
    return {
        'task_id': fp.stem,
        'phase_id': phase_id,
        'phase_id_explicit': explicit_phase_id is not None,
        'objective': field(text, 'objective') or '',
        'depends_on': inline_list(text, 'depends_on'),
        'authorized_paths': paths,
        'required_context': required_context,
        'architecture_bindings': inline_list(text, 'architecture_bindings'),
        'interface_bindings': inline_list(text, 'interface_bindings'),
        'acceptance_criteria': inline_list(text, 'acceptance_criteria'),
        'verification': inline_list(text, verification_key),
        'required_evidence': inline_list(text, evidence_key),
        'max_repairs': max_repairs,
        'contract': str(fp.relative_to(ROOT)).replace('\\', '/'),
        'digest': sha256_file(fp),
    }


def _implicit_phase(tasks):
    return {
        'phase_id': 'PHASE_001', 'objective': 'Implicit phase for bounded implementation',
        'depends_on': [], 'architecture_bindings': [], 'interface_bindings': [],
        'acceptance_criteria': [], 'verification': [], 'required_evidence': [], 'implicit': True,
    }


def _load_phases(tasks):
    if not PHASES_PATH.is_file():
        return {'PHASE_001': _implicit_phase(tasks)}
    obj = json.loads(PHASES_PATH.read_text(encoding='utf-8'))
    rows = obj.get('phases') if isinstance(obj, dict) else None
    if not isinstance(rows, list) or not rows:
        raise ValueError('PHASES.json: phases must be a non-empty list')
    out = {}
    for raw in rows:
        pid = raw.get('phase_id')
        if not pid or pid in out:
            raise ValueError(f'PHASES.json: duplicate or missing phase_id: {pid}')
        req = ['objective', 'depends_on', 'architecture_bindings', 'interface_bindings', 'acceptance_criteria', 'verification', 'required_evidence']
        missing = [k for k in req if k not in raw]
        if missing:
            raise ValueError(f'{pid}: missing phase fields: {", ".join(missing)}')
        out[pid] = {k: raw[k] for k in ['phase_id'] + req}
        out[pid]['implicit'] = False
    return out


def _acyclic(nodes, deps, label):
    visiting, done = set(), set()
    def visit(n):
        if n in done:
            return
        if n in visiting:
            raise ValueError(f'{label} dependency cycle at {n}')
        visiting.add(n)
        for d in deps(n):
            if d not in nodes:
                raise ValueError(f'{label} {n} references missing dependency {d}')
            visit(d)
        visiting.remove(n); done.add(n)
    for n in nodes:
        visit(n)


def _resolve_binding(binding):
    p = WORKPLAN / 'compiled' / binding
    if p.is_file():
        return True
    q = ROOT / binding
    return q.is_file()


def load_contract_package(validate=True):
    fps = sorted(p for p in TASK_DIR.glob('TASK_*.md') if p.name not in {'TASK_INDEX.md', 'TASK_TEMPLATE.md'})
    tasks = {}
    for fp in fps:
        t = _task(fp)
        if t['task_id'] in tasks:
            raise ValueError(f'duplicate task id: {t["task_id"]}')
        tasks[t['task_id']] = t
    phases = _load_phases(tasks)
    if validate:
        _acyclic(set(phases), lambda p: phases[p].get('depends_on', []), 'phase')
        _acyclic(set(tasks), lambda t: tasks[t].get('depends_on', []), 'task')
        for tid, t in tasks.items():
            if PHASES_PATH.is_file() and not t.get('phase_id_explicit'):
                raise ValueError(f'{tid}: phase_id is required when PHASES.json exists')
            if t['phase_id'] not in phases:
                raise ValueError(f'{tid}: missing phase {t["phase_id"]}')
            for dep in t['depends_on']:
                dp = tasks[dep]['phase_id']
                if dp != t['phase_id'] and dp not in phases[t['phase_id']].get('depends_on', []):
                    raise ValueError(f'{tid}: cross-phase dependency {dep} requires phase dependency {dp}')
            for b in t['architecture_bindings'] + t['interface_bindings']:
                if not _resolve_binding(b):
                    raise ValueError(f'{tid}: unresolved binding {b}')
        for pid, p in phases.items():
            for b in p.get('architecture_bindings', []) + p.get('interface_bindings', []):
                if not _resolve_binding(b):
                    raise ValueError(f'{pid}: unresolved binding {b}')
    return {'phases': phases, 'tasks': tasks}
