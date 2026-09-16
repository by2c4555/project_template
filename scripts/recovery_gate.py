#!/usr/bin/env python3
"""Validate the v4.2.1 durable recovery contract before local execution resumes."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    p = ROOT / rel
    if not p.is_file():
        raise SystemExit(f'RECOVERY_GATE: FAIL\nmissing: {rel}')
    return p.read_text(encoding='utf-8', errors='replace')


def value(text, key):
    m = re.search(rf'^\s*{re.escape(key)}:\s*(.*?)\s*$', text, re.M)
    return m.group(1).strip().strip('"\'') if m else None


def find_task(task_id):
    candidates = list((ROOT / 'EXECUTE/tasks').glob(f'{task_id}*.md'))
    candidates = [p for p in candidates if p.name not in {'TASK_INDEX.md', 'TASK_TEMPLATE.md'}]
    return candidates[0] if candidates else None


def main():
    es = read('EXECUTE/execution/EXECUTION_STATE.md')
    ps = read('EXECUTE/PROJECT_STATUS.md')

    errors = []
    if value(es, 'execution_status') != 'READY_TO_RESUME':
        errors.append('EXECUTION_STATE execution_status must be READY_TO_RESUME')
    if value(es, 'resume_authorized') != 'true':
        errors.append('EXECUTION_STATE recovery.resume_authorized must be true')
    if value(ps, 'resume_authorized') != 'true':
        errors.append('PROJECT_STATUS resume_authorized must be true')

    issue_id = value(es, 'last_resolved_issue') or value(ps, 'last_resolved_issue')
    if not issue_id or issue_id == 'none':
        errors.append('last_resolved_issue is missing')
        issue_text = ''
    else:
        issue_path = ROOT / 'EXECUTE/issues' / f'{issue_id}.md'
        if not issue_path.is_file():
            errors.append(f'missing resolved issue artifact: {issue_path.relative_to(ROOT)}')
            issue_text = ''
        else:
            issue_text = issue_path.read_text(encoding='utf-8', errors='replace')
            if value(issue_text, 'status') != 'RESOLVED':
                errors.append(f'{issue_id} status must be RESOLVED')
            if value(issue_text, 'resume_authorized') != 'true':
                errors.append(f'{issue_id} resume_authorized must be true')

    resolution = value(es, 'resolution')
    diagnosis = value(es, 'diagnosis')
    verification = value(es, 'verification')
    baseline = value(es, 'recovery_baseline')

    if not diagnosis or diagnosis == 'none':
        errors.append('recovery diagnosis reference missing')
    elif diagnosis.startswith('Diagnosis_'):
        if not (ROOT / 'EXECUTE/diagnostics' / f'{diagnosis}.md').is_file():
            errors.append(f'diagnosis artifact missing: EXECUTE/diagnostics/{diagnosis}.md')

    if not resolution or resolution == 'none':
        errors.append('recovery resolution reference missing')
    elif resolution.startswith('RESOLUTION_'):
        if not (ROOT / 'EXECUTE/knowledge/resolutions' / f'{resolution}.md').is_file():
            errors.append(f'resolution artifact missing: EXECUTE/knowledge/resolutions/{resolution}.md')

    if verification not in {'PASS', 'VERIFIED', 'RECOVERY_PASS'}:
        errors.append('recovery verification must be PASS, VERIFIED, or RECOVERY_PASS')
    if not baseline or baseline == 'none':
        errors.append('recovery_baseline must be recorded')

    task_id = None
    if issue_text:
        task_id = value(issue_text, 'origin_task')
    if not task_id or task_id == 'none':
        # A recovered task may also be identified in the list/text, but require issue provenance for deterministic resume.
        errors.append('resolved Issue must identify origin_task')
    else:
        task_path = find_task(task_id)
        if not task_path:
            errors.append(f'recovered Task artifact not found for {task_id}')
        else:
            task_text = task_path.read_text(encoding='utf-8', errors='replace')
            if value(task_text, 'status') != 'PASS_RECOVERED':
                errors.append(f'{task_id} status must be PASS_RECOVERED')

    if errors:
        print('RECOVERY_GATE: FAIL')
        for e in errors:
            print('FAIL:', e)
        return 1

    print('RECOVERY_GATE: PASS')
    print(f'last_resolved_issue: {issue_id}')
    print(f'recovered_task: {task_id}')
    print(f'diagnosis: {diagnosis}')
    print(f'resolution: {resolution}')
    print(f'recovery_baseline: {baseline}')
    print(f'next_task: {value(es, "next_task") or "derive_from_task_graph"}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
