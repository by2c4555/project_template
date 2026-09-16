#!/usr/bin/env python3
"""User-operated implementation approval gate for v4.2.1 Planning Vx -> Execution Vx."""
from pathlib import Path
import argparse
import re
from datetime import datetime, timezone

R = Path(__file__).resolve().parents[1]
CONFIRM = 'I_APPROVE_IMPLEMENTATION'


def replace_yamlish(text, key, value):
    pat = rf'^(\s*{re.escape(key)}:\s*).*$'
    if re.search(pat, text, re.M):
        return re.sub(pat, rf'\g<1>{value}', text, count=1, flags=re.M)
    return text


def value_of(text, key):
    m = re.search(rf'^\s*{re.escape(key)}:\s*(.*?)\s*$', text, re.M)
    return m.group(1).strip().strip('"\'') if m else None


def read(rel):
    p = R / rel
    if not p.is_file():
        raise SystemExit(f'missing required approval artifact: {rel}')
    return p.read_text(encoding='utf-8', errors='replace')


def require_package(planning, revision):
    errors = []
    for rel in ['EXECUTE/plan/IMPLEMENTATION_PLAN.md', 'EXECUTE/tasks/TASK_INDEX.md']:
        t = read(rel)
        if value_of(t, 'planning_version') != planning:
            errors.append(f'{rel} is not bound to {planning}')
        if value_of(t, 'planning_revision') != revision:
            errors.append(f'{rel} is not bound to {revision}')
        if value_of(t, 'artifact_status') not in {'COMPILED', 'READY_FOR_APPROVAL'}:
            errors.append(f'{rel} artifact_status must be COMPILED or READY_FOR_APPROVAL')
    tasks = [p for p in (R/'EXECUTE/tasks').glob('TASK_*.md') if p.name not in {'TASK_INDEX.md','TASK_TEMPLATE.md'} and re.fullmatch(r'TASK_\d+.*\.md',p.name)]
    if not tasks:
        errors.append('no atomic TASK_NNN.md files exist for approval')
    for p in tasks:
        t=p.read_text(encoding='utf-8',errors='replace')
        if value_of(t,'planning_version') == planning and value_of(t,'status') not in {'PENDING','READY'}:
            errors.append(f'{p.relative_to(R)} has invalid pre-execution status')
    return errors


def main():
    ap = argparse.ArgumentParser(description='USER/OPERATOR ONLY: bind one reviewed Planning Vx to an Execution Vx after explicit implementation authorization.')
    ap.add_argument('--planning', required=True, help='e.g. Planning_V1')
    ap.add_argument('--execution', required=True, help='e.g. Execution_V1')
    ap.add_argument('--approved-by', default='user')
    ap.add_argument('--confirm-explicit-user-approval', required=True, help=f'must equal {CONFIRM}')
    a = ap.parse_args()

    if a.confirm_explicit_user_approval != CONFIRM:
        raise SystemExit(f'implementation approval blocked: --confirm-explicit-user-approval must equal {CONFIRM}')
    if not re.fullmatch(r'Planning_V[1-9][0-9]*', a.planning):
        raise SystemExit('invalid --planning')
    if not re.fullmatch(r'Execution_V[1-9][0-9]*', a.execution):
        raise SystemExit('invalid --execution')

    planning_status_path = R / 'EXECUTE/plan/PLANNING_STATUS.md'
    project_status_path = R / 'EXECUTE/PROJECT_STATUS.md'
    execution_state_path = R / 'EXECUTE/execution/EXECUTION_STATE.md'

    planning = read('EXECUTE/plan/PLANNING_STATUS.md')
    required = {
        'planning_status': 'AWAITING_USER_APPROVAL',
        'planning_version': a.planning,
        'material_unknowns': '0',
        'feedback_reason': 'none',
        'plan_review_status': 'ACCEPTED',
        'package_status': 'READY_FOR_APPROVAL',
        'interaction_gate': 'USER_APPROVAL_REQUIRED',
        'invocation_stop_required': 'true',
        'task_expansion_allowed': 'true',
        'implementation_approval_requested': 'true',
        'execution_locked': 'true',
    }
    errors=[]
    for k,v in required.items():
        if value_of(planning,k) != v:
            errors.append(f'{k} must be {v!r}, found {value_of(planning,k)!r}')
    revision = value_of(planning, 'planning_revision') or 'none'
    errors.extend(require_package(a.planning, revision))
    if errors:
        print('IMPLEMENTATION_APPROVAL: BLOCKED')
        for e in errors:
            print('FAIL:',e)
        raise SystemExit(1)

    approved_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    for k,v in {
        'planning_status':'APPROVED','package_status':'APPROVED','interaction_gate':'NONE',
        'invocation_stop_required':'false','approved_by':a.approved_by,'approved_at':approved_at,
        'execution_locked':'false'
    }.items():
        planning=replace_yamlish(planning,k,v)
    planning_status_path.write_text(planning,encoding='utf-8')

    project = read('EXECUTE/PROJECT_STATUS.md')
    updates = [
        ('lifecycle_stage', 'EXECUTION'), ('project_validation_status', 'NOT_VALIDATED'),
        ('planning_version', a.planning), ('planning_revision', revision), ('planning_status', 'APPROVED'),
        ('material_unknowns', '0'), ('implementation_approval_requested', 'true'),
        ('approved_planning_version', a.planning), ('execution_version', a.execution),
        ('execution_status', 'READY'), ('execution_bound_planning_version', a.planning),
        ('active_task', 'none'), ('active_issue', 'none'), ('recovery_status', 'NOT_ACTIVE'),
        ('resume_authorized', 'false'), ('evaluation_version', 'none'), ('evaluation_status', 'NOT_STARTED'),
        ('latest_evaluation_result', 'none'), ('completion_report', 'none'), ('scope_clarification_status', 'NOT_REQUIRED'),
    ]
    for k,v in updates:
        project=replace_yamlish(project,k,v)
    project=replace_yamlish(project,'next_action','>\n  Start VS Code ProjectManager500K with EXECUTE_PROJECT_PROMPT.md.')
    project_status_path.write_text(project,encoding='utf-8')

    execution_state_path.write_text(f'''# Execution State\n\n```yaml\nexecution_version: {a.execution}\nexecution_status: READY\nexecution_bound_planning_version: {a.planning}\n\ncompleted_tasks: []\nrecovered_tasks: []\nactive_task: none\nblocked_tasks: []\n\nactive_issue: none\nlast_resolved_issue: none\n\nrecovery:\n  status: NOT_ACTIVE\n  owner: none\n  diagnosis: none\n  resolution: none\n  verification: none\n  resume_authorized: false\n  recovery_baseline: none\n  next_task: none\n\nreplan_required: false\nscope_clarification_required: false\nevaluation_required: false\n```\n\n## Execution Status State Machine\n\nAllowed primary execution states:\n\n- `LOCKED`\n- `READY`\n- `IN_PROGRESS`\n- `ISSUE_DETECTED`\n- `PAUSED_FOR_DIAGNOSIS`\n- `PAUSED_FOR_EXTERNAL_REPAIR`\n- `RECOVERY_VERIFICATION`\n- `READY_TO_RESUME`\n- `COMPLETE`\n- `AWAITING_EVALUATION`\n\nLocal Manager/Builder execution is permitted only in `READY`, `IN_PROGRESS`, or `READY_TO_RESUME`.\n\nAny `PAUSED_*` or `RECOVERY_VERIFICATION` state is a hard stop for normal Builder dispatch.\n''',encoding='utf-8')

    print(f'APPROVED FOR IMPLEMENTATION: {a.planning} -> bound {a.execution}')
    print('Explicit user/operator confirmation recorded by command invocation.')
    print('Next: run EXECUTE_PROJECT_PROMPT.md with ProjectManager500K in VS Code.')


if __name__ == '__main__':
    main()
