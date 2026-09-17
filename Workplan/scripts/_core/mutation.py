from __future__ import annotations
from pathlib import Path, PurePosixPath
from .paths import ROOT, WORKPLAN
from .integrity import sha256_file

EXCLUDED_DIRS = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.cache', '.pytest_cache', '.mypy_cache', '.idea', '.vscode'}
EXCLUDED_SUFFIXES = {'.pyc', '.pyo', '.tmp', '.swp'}


def _excluded(p: Path):
    try:
        rel = p.relative_to(ROOT)
    except ValueError:
        return True
    if WORKPLAN == p or WORKPLAN in p.parents:
        return True
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return True
    if p.suffix in EXCLUDED_SUFFIXES or p.name.endswith('~'):
        return True
    return False


def snapshot_production():
    import os
    out = {}
    root_s = str(ROOT)
    for dirpath, dirnames, filenames in os.walk(root_s):
        dp = Path(dirpath)
        rel_dir = dp.relative_to(ROOT)
        if dp == ROOT:
            dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS and d not in {'Workplan', '.git'}]
        else:
            dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for name in filenames:
            p = dp / name
            if _excluded(p):
                continue
            rel = str(p.relative_to(ROOT)).replace('\\', '/')
            out[rel] = sha256_file(p)
    return out


def diff_snapshots(before, after):
    out = []
    for rel in sorted(set(before) | set(after)):
        a, b = before.get(rel), after.get(rel)
        if a == b:
            continue
        kind = 'CREATE' if a is None else 'DELETE' if b is None else 'MODIFY'
        out.append({'path': rel, 'kind': kind, 'before_sha256': a, 'after_sha256': b})
    return out


def _safe_auth(raw):
    text = raw.replace('\\', '/').strip()
    p = PurePosixPath(text)
    if not text or p.is_absolute() or '..' in p.parts or text.startswith('Workplan/') or text == 'Workplan' or text.startswith('.git/') or text == '.git':
        raise ValueError(f'unsafe authorized path: {raw}')
    return str(p).rstrip('/') + ('/' if text.endswith('/') else '')


def path_authorized(path, authorized_paths):
    for raw in authorized_paths:
        auth = _safe_auth(raw)
        if auth.endswith('/'):
            if path.startswith(auth):
                return True
        elif path == auth:
            return True
    return False


def validate_mutations(mutations, authorized_paths):
    unauthorized = [m for m in mutations if not path_authorized(m['path'], authorized_paths)]
    return {'status': 'PASS' if not unauthorized else 'FAIL', 'unauthorized': unauthorized, 'mutations': mutations}
