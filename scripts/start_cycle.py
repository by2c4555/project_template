#!/usr/bin/env python3
"""Start a new v4.4.0 change cycle by capturing the external handoff as SCOPE_001."""
from __future__ import annotations

import argparse
from workflow_state import (
    active_cycle, append_transition, build_scope_manifest, load_state, next_id,
    reset_package_workspace, save_state, snapshot_scope, utc_now,
)

ap = argparse.ArgumentParser(description='Start a new v4.4.0 change cycle from EXECUTE/project_details.md + declared docs/raw evidence.')
ap.add_argument('--title', default='Change cycle')
a = ap.parse_args()

state = load_state()
if state.get('active_cycle'):
    cid, current = active_cycle(state)
    if current.get('status') != 'CLOSED_VALIDATED':
        raise SystemExit(
            f'START_CYCLE: BLOCKED\nactive cycle {cid} is {current.get("status")}; '
            'only CLOSED_VALIDATED cycles may be followed by a new scope'
        )

cycle_id = next_id(state, 'cycle', 'CYCLE_')
planning_version = next_id(state, 'planning', 'Planning_V', width=1)
scope_revision = 'SCOPE_001'
try:
    scope_manifest = build_scope_manifest(scope_revision)
    scope_snapshot = snapshot_scope(cycle_id, scope_manifest)
except ValueError as exc:
    raise SystemExit('START_CYCLE: BLOCKED\n' + str(exc))

scope = {
    'revision': 1,
    'revision_label': scope_revision,
    'status': 'ACTIVE',
    'digest': scope_manifest['scope_digest'],
    'title': scope_manifest['scope_title'],
    'baseline_ref': scope_manifest['baseline_ref'],
    'snapshot_path': scope_snapshot,
    'source_handoff_path': scope_manifest['source_handoff_path'],
    'supporting_files': scope_manifest['supporting_files'],
    'captured_at': scope_manifest['created_at'],
    'reason': 'NEW_CHANGE_CYCLE',
}

cycle = {
    'cycle_id': cycle_id,
    'title': a.title,
    'created_at': utc_now(),
    'closed_at': None,
    'status': 'PLANNING',
    'lifecycle_stage': 'PLANNING',
    'next_action': 'RUN_EXTERNAL_AGENT_PLANNING',
    'scope': scope,
    'scope_history': [],
    'planning': {
        'version': planning_version,
        'revision': 1,
        'revision_label': 'Revision_1',
        'status': 'IN_PROGRESS',
        'based_on_scope_revision': scope_revision,
        'based_on_scope_digest': scope_manifest['scope_digest'],
        'material_unknowns': None,
        'package_status': 'NOT_COMPILED',
        'task_expansion_allowed': False,
        'interaction_gate': 'NONE',
        'invocation_stop_required': False,
        'candidate_scope_digest': None,
        'candidate_package_digest': None,
    },
    'planning_history': [],
    'approval': None,
    'approval_history': [],
    'execution': None,
    'execution_history': [],
    'evaluation': {'status': 'NOT_STARTED', 'active': None, 'attempts': [], 'latest_result': None, 'next_route': None},
    'issues': [],
    'active_issue': None,
    'completion_report': None,
}
state['cycles'][cycle_id] = cycle
state['active_cycle'] = cycle_id
state['project_state'] = 'PLANNING'; state['active_external_work']=None
reset_package_workspace(planning_version, 'Revision_1')
save_state(state)
append_transition(
    'CHANGE_CYCLE_STARTED', actor='user:start_cycle', cycle_id=cycle_id,
    details={
        'scope_revision': scope_revision,
        'scope_digest': scope_manifest['scope_digest'],
        'scope_snapshot': scope_snapshot,
        'planning_version': planning_version,
    },
)
print('START_CYCLE: PASS')
print(f'cycle_id: {cycle_id}')
print(f'scope_revision: {scope_revision}')
print(f'scope_digest: {scope_manifest["scope_digest"]}')
print(f'scope_snapshot: {scope_snapshot}')
print(f'planning_version: {planning_version}')
print('execution_authorized: false')
print('Next: run an External Agent with EXECUTE/external_agent/PLANNING_PROMPT.md')
