#!/usr/bin/env python3
"""Explicit user implementation-approval gate for v4.2.0 Planning Vx -> Execution Vx."""
from pathlib import Path
import argparse
import re
from datetime import datetime, timezone

R = Path(__file__).resolve().parents[1]


def replace_yamlish(text, key, value):
    pat = rf'^(\s*{re.escape(key)}:\s*).*$'
    if re.search(pat, text, re.M):
        return re.sub(pat, rf'\g<1>{value}', text, count=1, flags=re.M)
    return text


def value_of(text, key):
    m = re.search(rf'^\s*{re.escape(key)}:\s*(.*?)\s*$', text, re.M)
    return m.group(1).strip() if m else None


def main():
    ap = argparse.ArgumentParser(description='Record explicit user authorization and bind one execution-ready Planning Vx to an Execution Vx.')
    ap.add_argument('--planning', required=True, help='e.g. Planning_V1')
    ap.add_argument('--execution', required=True, help='e.g. Execution_V1')
    ap.add_argument('--approved-by', default='user')
    a = ap.parse_args()

    if not re.fullmatch(r'Planning_V[1-9][0-9]*', a.planning):
        raise SystemExit('invalid --planning')
    if not re.fullmatch(r'Execution_V[1-9][0-9]*', a.execution):
        raise SystemExit('invalid --execution')

    planning_status_path = R / 'EXECUTE/plan/PLANNING_STATUS.md'
    project_status_path = R / 'EXECUTE/PROJECT_STATUS.md'
    execution_state_path = R / 'EXECUTE/execution/EXECUTION_STATE.md'

    planning = planning_status_path.read_text(encoding='utf-8')
    if value_of(planning, 'planning_status') != 'AWAITING_USER_APPROVAL':
        raise SystemExit('Planning status is not AWAITING_USER_APPROVAL; implementation approval blocked.')
    if value_of(planning, 'planning_version') != a.planning:
        raise SystemExit(f'Planning status does not identify {a.planning}; implementation approval blocked.')
    if value_of(planning, 'material_unknowns') != '0':
        raise SystemExit('material_unknowns must be 0 before implementation approval.')
    if value_of(planning, 'implementation_approval_requested') != 'true':
        raise SystemExit('Codex has not marked implementation_approval_requested: true; approval blocked.')

    revision = value_of(planning, 'planning_revision') or 'none'
    approved_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')

    planning = replace_yamlish(planning, 'planning_status', 'APPROVED')
    planning = replace_yamlish(planning, 'approved_by', a.approved_by)
    planning = replace_yamlish(planning, 'approved_at', approved_at)
    planning = replace_yamlish(planning, 'execution_locked', 'false')
    planning_status_path.write_text(planning, encoding='utf-8')

    project = project_status_path.read_text(encoding='utf-8')
    updates = [
        ('lifecycle_stage', 'EXECUTION'),
        ('project_validation_status', 'NOT_VALIDATED'),
        ('planning_version', a.planning),
        ('planning_revision', revision),
        ('planning_status', 'APPROVED'),
        ('material_unknowns', '0'),
        ('implementation_approval_requested', 'true'),
        ('approved_planning_version', a.planning),
        ('execution_version', a.execution),
        ('execution_status', 'READY'),
        ('execution_bound_planning_version', a.planning),
        ('active_task', 'none'),
        ('active_issue', 'none'),
        ('recovery_status', 'NOT_ACTIVE'),
        ('resume_authorized', 'false'),
        ('evaluation_version', 'none'),
        ('evaluation_status', 'NOT_STARTED'),
        ('latest_evaluation_result', 'none'),
        ('completion_report', 'none'),
        ('scope_clarification_status', 'NOT_REQUIRED'),
    ]
    for k, v in updates:
        project = replace_yamlish(project, k, v)
    project = replace_yamlish(project, 'next_action', '>\n  Start VS Code ProjectManager500K with EXECUTE_PROJECT_PROMPT.md.')
    project_status_path.write_text(project, encoding='utf-8')

    execution_state_path.write_text(
        f'''# Execution State\n\n```yaml\nexecution_version: {a.execution}\nexecution_status: READY\nexecution_bound_planning_version: {a.planning}\n\ncompleted_tasks: []\nrecovered_tasks: []\nactive_task: none\nblocked_tasks: []\n\nactive_issue: none\nlast_resolved_issue: none\n\nrecovery:\n  status: NOT_ACTIVE\n  owner: none\n  diagnosis: none\n  resolution: none\n  verification: none\n  resume_authorized: false\n  recovery_baseline: none\n  next_task: none\n\nreplan_required: false\nscope_clarification_required: false\nevaluation_required: false\n```\n\n## Execution Status State Machine\n\nAllowed primary execution states:\n\n- `LOCKED`\n- `READY`\n- `IN_PROGRESS`\n- `ISSUE_DETECTED`\n- `PAUSED_FOR_DIAGNOSIS`\n- `PAUSED_FOR_EXTERNAL_REPAIR`\n- `RECOVERY_VERIFICATION`\n- `READY_TO_RESUME`\n- `COMPLETE`\n- `AWAITING_EVALUATION`\n\nLocal Manager/Builder execution is permitted only in `READY`, `IN_PROGRESS`, or `READY_TO_RESUME`.\n\nAny `PAUSED_*` or `RECOVERY_VERIFICATION` state is a hard stop for normal Builder dispatch.\n''',
        encoding='utf-8'
    )

    print(f'APPROVED FOR IMPLEMENTATION: {a.planning} -> bound {a.execution}')
    print('Recovery state reset for the new Execution version.')
    print('Next: run EXECUTE_PROJECT_PROMPT.md with ProjectManager500K in VS Code.')


if __name__ == '__main__':
    main()
