#!/usr/bin/env python3
from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2]


def run(root: Path, rel: str):
    env = dict(os.environ); env['PYTHONDONTWRITEBYTECODE'] = '1'
    return subprocess.run([sys.executable, str(root / rel)], cwd=root, text=True, capture_output=True, env=env, timeout=10)


def write_state(root: Path, version: str, *, active_work=None, pending_approval=None):
    p = root / 'Workplan/control/STATE.json'
    st = json.loads(p.read_text(encoding='utf-8'))
    st['workflow_version'] = version
    st['schema_version'] = 6
    st['active_work'] = active_work
    st['pending_approval'] = pending_approval
    p.write_text(json.dumps(st, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return p


def main():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / 'repo'; shutil.copytree(SOURCE, root)
        state = write_state(root, '5.3.0')
        r = run(root, 'Workplan/scripts/migrate_v530_to_v531.py')
        assert r.returncode == 0, r.stdout + r.stderr
        assert json.loads(state.read_text())['workflow_version'] == '5.3.1'
        r = run(root, 'Workplan/scripts/migrate_v531_to_v532.py')
        assert r.returncode == 0, r.stdout + r.stderr
        migrated = json.loads(state.read_text())
        assert migrated['workflow_version'] == '5.3.2' and migrated['schema_version'] == 6

    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / 'repo'; shutil.copytree(SOURCE, root)
        write_state(root, '5.3.1', active_work='WORK_9999')
        r = run(root, 'Workplan/scripts/migrate_v531_to_v532.py')
        assert r.returncode != 0 and 'active_work must be null' in (r.stdout + r.stderr)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / 'repo'; shutil.copytree(SOURCE, root)
        write_state(root, '5.3.1', pending_approval={'approval_id':'APPROVAL_9999'})
        r = run(root, 'Workplan/scripts/migrate_v531_to_v532.py')
        assert r.returncode != 0 and 'pending_approval must be null' in (r.stdout + r.stderr)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / 'repo'; shutil.copytree(SOURCE, root)
        state = write_state(root, '5.3.0')
        r = run(root, 'Workplan/scripts/migrate_v531_to_v532.py')
        assert r.returncode != 0 and 'expected workflow=5.3.1' in (r.stdout + r.stderr)
        assert json.loads(state.read_text())['workflow_version'] == '5.3.0'

    print('MIGRATION_REGRESSIONS_VALID: PASS')


if __name__ == '__main__':
    main()
