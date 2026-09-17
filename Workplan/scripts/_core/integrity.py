from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from .paths import ROOT, WORKPLAN

RELEASE_MANIFEST = WORKPLAN / 'FILE_SHA256SUMS.txt'
RELEASE_EXCLUDED_DIRS = {'.git', '__pycache__', '.venv', 'venv', '.cache', '.pytest_cache', '.mypy_cache', '.idea', '.vscode'}
RELEASE_EXCLUDED_SUFFIXES = {'.pyc', '.pyo', '.tmp', '.swp', '.zip'}
RUNTIME_PREFIXES = (
    'Workplan/work/', 'Workplan/control/approvals/', 'Workplan/control/ingest/',
    'Workplan/history/', 'Workplan/diagnosis/', 'Workplan/recovery/', 'Workplan/evaluation/',
    'Workplan/ingest/', 'Workplan/archive/'
)
RUNTIME_FILES = {'Workplan/control/TRANSITIONS.jsonl'}


def sha256_file(p: Path):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def digest_rows(rows):
    h = hashlib.sha256()
    for r in sorted(rows, key=lambda x: x['path']):
        h.update(r['path'].encode()); h.update(b'\0'); h.update(r['sha256'].encode()); h.update(b'\n')
    return h.hexdigest()


def digest_files(paths):
    rows = []
    for p in sorted(paths, key=lambda x: str(x)):
        rel = str(p.relative_to(ROOT)).replace('\\', '/')
        rows.append({'path': rel, 'sha256': sha256_file(p), 'bytes': p.stat().st_size})
    return digest_rows(rows), rows


def field(text, key):
    m = re.search(rf'^\s*{re.escape(key)}:\s*(.*?)\s*$', text, re.M)
    return m.group(1).strip().strip('"\'') if m else None


def inline_list(text, key):
    raw = field(text, key) or '[]'
    inner = raw[1:-1].strip() if raw.startswith('[') and raw.endswith(']') else ''
    return [x.strip().strip('"\'') for x in inner.split(',') if x.strip()]


def build_package_manifest():
    files = []
    for p in [WORKPLAN / 'plan' / 'IMPLEMENTATION_PLAN.md', WORKPLAN / 'plan' / 'PHASES.json', WORKPLAN / 'tasks' / 'TASK_INDEX.md']:
        if p.is_file():
            files.append(p)
    files += sorted((WORKPLAN / 'compiled').glob('*.md'))
    files += sorted(p for p in (WORKPLAN / 'tasks').glob('TASK_*.md') if p.name not in {'TASK_INDEX.md', 'TASK_TEMPLATE.md'})
    digest, rows = digest_files(files)
    task_rows = [r for r in rows if '/tasks/TASK_' in r['path'] and not r['path'].endswith(('TASK_INDEX.md', 'TASK_TEMPLATE.md'))]
    phase_digests = {}
    phase_path = WORKPLAN / 'plan' / 'PHASES.json'
    if phase_path.is_file():
        try:
            obj = json.loads(phase_path.read_text(encoding='utf-8'))
            for phase in obj.get('phases', []):
                pid = phase.get('phase_id')
                if pid:
                    payload = json.dumps(phase, sort_keys=True, separators=(',', ':')).encode('utf-8')
                    phase_digests[pid] = hashlib.sha256(payload).hexdigest()
        except Exception:
            # Contract validation owns malformed JSON errors; manifest remains deterministic.
            phase_digests['PHASES_INVALID'] = sha256_file(phase_path)
    else:
        implicit = {'phase_id':'PHASE_001','objective':'Implicit phase for bounded implementation','depends_on':[],
                    'architecture_bindings':[],'interface_bindings':[],'acceptance_criteria':[],
                    'verification':[],'required_evidence':[],'implicit':True}
        payload = json.dumps(implicit, sort_keys=True, separators=(',', ':')).encode('utf-8')
        phase_digests['PHASE_001'] = hashlib.sha256(payload).hexdigest()
    return {
        'package_digest': digest,
        'task_count': len(task_rows),
        'files': rows,
        'phase_digests': phase_digests,
        'task_digests': {Path(r['path']).stem: r['sha256'] for r in task_rows},
    }


def _release_excluded(p: Path):
    rel = str(p.relative_to(ROOT)).replace('\\', '/')
    if p == RELEASE_MANIFEST:
        return True
    if rel in RUNTIME_FILES or any(rel.startswith(prefix) for prefix in RUNTIME_PREFIXES):
        if p.name == '.gitkeep':
            return False
        return True
    if any(part in RELEASE_EXCLUDED_DIRS for part in p.relative_to(ROOT).parts):
        return True
    if p.suffix in RELEASE_EXCLUDED_SUFFIXES or p.name.endswith('~'):
        return True
    return False


def release_files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and not _release_excluded(p))


def render_release_manifest():
    return ''.join(f'{sha256_file(p)}  {str(p.relative_to(ROOT)).replace(chr(92), "/")}\n' for p in release_files())


def write_release_manifest():
    RELEASE_MANIFEST.write_text(render_release_manifest(), encoding='utf-8', newline='\n')


def validate_release_manifest():
    if not RELEASE_MANIFEST.is_file():
        return False, ['manifest missing']
    expected = {}
    problems = []
    for line in RELEASE_MANIFEST.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        try:
            digest, rel = line.split('  ', 1)
        except ValueError:
            problems.append(f'malformed manifest line: {line}')
            continue
        if '__pycache__' in rel or rel.endswith(('.pyc', '.pyo')) or rel == 'Workplan/FILE_SHA256SUMS.txt':
            problems.append(f'forbidden manifest entry: {rel}')
        expected[rel] = digest
    actual = {str(p.relative_to(ROOT)).replace('\\', '/'): sha256_file(p) for p in release_files()}
    for rel in sorted(set(expected) - set(actual)):
        problems.append(f'manifest tracks missing/excluded file: {rel}')
    for rel in sorted(set(actual) - set(expected)):
        problems.append(f'manifest omits release file: {rel}')
    for rel in sorted(set(actual) & set(expected)):
        if actual[rel] != expected[rel]:
            problems.append(f'manifest digest mismatch: {rel}')
    return not problems, problems
