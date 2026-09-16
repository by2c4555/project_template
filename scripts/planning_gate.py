#!/usr/bin/env python3
"""Planning interaction/cost-control gate for Project Template v4.2.1."""
from __future__ import annotations

from pathlib import Path
import argparse
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / 'EXECUTE/plan/PLANNING_STATUS.md'


def read_text(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f'PLANNING_GATE: FAIL\nmissing: {path.relative_to(ROOT)}')
    return path.read_text(encoding='utf-8', errors='replace')


def value_of(text: str, key: str):
    m = re.search(rf'^\s*{re.escape(key)}:\s*(.*?)\s*$', text, re.M)
    return m.group(1).strip().strip('"\'') if m else None


def replace_value(text: str, key: str, value: str) -> str:
    pat = rf'^(\s*{re.escape(key)}:\s*).*$'
    if not re.search(pat, text, re.M):
        raise SystemExit(f'PLANNING_GATE: FAIL\nPLANNING_STATUS missing field: {key}')
    return re.sub(pat, rf'\g<1>{value}', text, count=1, flags=re.M)


def parse_unknowns(raw):
    if raw is None or raw.lower() == 'unknown':
        return None
    try:
        n = int(raw)
    except ValueError:
        return None
    return n if n >= 0 else None


def require_identity(status: str, planning: str, revision: str):
    errors = []
    if value_of(status, 'planning_version') != planning:
        errors.append(f'planning_version must be {planning}')
    if value_of(status, 'planning_revision') != revision:
        errors.append(f'planning_revision must be {revision}')
    return errors


def generated_task_paths():
    task_dir = ROOT / 'EXECUTE/tasks'
    if not task_dir.exists():
        return []
    return sorted(p for p in task_dir.glob('TASK_*.md') if p.name not in {'TASK_INDEX.md', 'TASK_TEMPLATE.md'} and re.fullmatch(r'TASK_\d+.*\.md', p.name))


def task_plan(path: Path):
    return value_of(read_text(path), 'planning_version')


def check_no_current_tasks(planning: str):
    bad = []
    for p in generated_task_paths():
        pv = task_plan(p)
        if pv in {planning, None, '', 'none'}:
            bad.append(str(p.relative_to(ROOT)))
    return bad


def cmd_authorize(a):
    status = read_text(STATUS_PATH)
    errors = require_identity(status, a.planning, a.revision)
    if value_of(status, 'planning_status') != 'IN_PROGRESS':
        errors.append('planning_status must be IN_PROGRESS')
    if parse_unknowns(value_of(status, 'material_unknowns')) != 0:
        errors.append('material_unknowns must be exactly 0')
    if value_of(status, 'interaction_gate') != 'NONE':
        errors.append('interaction_gate must be NONE')
    if value_of(status, 'invocation_stop_required') != 'false':
        errors.append('invocation_stop_required must be false')
    if value_of(status, 'implementation_approval_requested') != 'false':
        errors.append('implementation_approval_requested must be false')
    if value_of(status, 'execution_locked') != 'true':
        errors.append('execution_locked must be true')
    if errors:
        print('PLANNING_GATE: FAIL')
        for e in errors:
            print('FAIL:', e)
        return 1
    status = replace_value(status, 'task_expansion_allowed', 'true')
    STATUS_PATH.write_text(status, encoding='utf-8')
    print('PLANNING_GATE: PASS')
    print(f'Expansion authorized for {a.planning} {a.revision}; material_unknowns=0.')
    return 0


def cmd_hold_material(a):
    if a.unknowns < 1:
        print('PLANNING_GATE: FAIL\nFAIL: --unknowns must be >= 1 for MATERIAL_DECISION')
        return 1
    status = read_text(STATUS_PATH)
    errors = require_identity(status, a.planning, a.revision)
    current_tasks = check_no_current_tasks(a.planning)
    if current_tasks:
        errors.append('current-Planning Tasks already exist while material decisions remain: ' + ', '.join(current_tasks))
    if errors:
        print('PLANNING_GATE: FAIL')
        for e in errors:
            print('FAIL:', e)
        return 1
    updates = {
        'planning_status': 'AWAITING_USER_FEEDBACK',
        'material_unknowns': str(a.unknowns),
        'feedback_reason': 'MATERIAL_DECISION',
        'plan_review_status': 'NOT_STARTED',
        'package_status': 'NOT_COMPILED',
        'interaction_gate': 'USER_FEEDBACK_REQUIRED',
        'invocation_stop_required': 'true',
        'task_expansion_allowed': 'false',
        'implementation_approval_requested': 'false',
        'execution_locked': 'true',
    }
    for k, v in updates.items():
        status = replace_value(status, k, v)
    STATUS_PATH.write_text(status, encoding='utf-8')
    print('PLANNING_GATE: PASS')
    print('HARD_STOP_REQUIRED: true')
    print('Reason: MATERIAL_DECISION. Ask focused questions and end the current invocation.')
    return 0


def cmd_status(_a):
    status = read_text(STATUS_PATH)
    keys = [
        'planning_version', 'planning_revision', 'planning_status', 'material_unknowns',
        'feedback_reason', 'plan_review_status', 'package_status', 'interaction_gate',
        'invocation_stop_required', 'task_expansion_allowed', 'implementation_approval_requested',
        'execution_locked'
    ]
    print('PLANNING_GATE: STATUS')
    for key in keys:
        print(f'{key}: {value_of(status, key)}')
    return 0


def main():
    ap = argparse.ArgumentParser(description='Machine-checkable planning interaction and cost-control gate.')
    sub = ap.add_subparsers(dest='command', required=True)

    s = sub.add_parser('status')
    s.set_defaults(func=cmd_status)

    e = sub.add_parser('authorize-expansion')
    e.add_argument('--planning', required=True)
    e.add_argument('--revision', required=True)
    e.set_defaults(func=cmd_authorize)

    h = sub.add_parser('hold-material-feedback')
    h.add_argument('--planning', required=True)
    h.add_argument('--revision', required=True)
    h.add_argument('--unknowns', required=True, type=int)
    h.set_defaults(func=cmd_hold_material)

    a = ap.parse_args()
    if getattr(a, 'planning', None) and not re.fullmatch(r'Planning_V[1-9][0-9]*', a.planning):
        raise SystemExit('PLANNING_GATE: FAIL\ninvalid --planning')
    if getattr(a, 'revision', None) and not re.fullmatch(r'Revision_[1-9][0-9]*', a.revision):
        raise SystemExit('PLANNING_GATE: FAIL\ninvalid --revision')
    return a.func(a)


if __name__ == '__main__':
    raise SystemExit(main())
