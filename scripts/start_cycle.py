#!/usr/bin/env python3
"""Start a new immutable change cycle after external scope has been manually imported."""
from __future__ import annotations
import argparse
from workflow_state import active_cycle, append_transition, load_state, next_id, reset_package_workspace, save_state, utc_now

ap = argparse.ArgumentParser(description='Start a new v4.3 change cycle from an external scope reference.')
ap.add_argument('--scope', required=True, help='Scope/research reference, e.g. Research_V2 or docs/new_feature_scope.md')
ap.add_argument('--title', default='Change cycle')
a = ap.parse_args()
state = load_state()
if state.get('active_cycle'):
    cid, current = active_cycle(state)
    if current.get('status') != 'CLOSED_VALIDATED':
        raise SystemExit(f'START_CYCLE: BLOCKED\nactive cycle {cid} is {current.get("status")}; only CLOSED_VALIDATED cycles may be followed by a new scope')
cycle_id = next_id(state, 'cycle', 'CYCLE_')
planning_version = next_id(state, 'planning', 'Planning_V', width=1)
cycle = {
    'cycle_id': cycle_id,
    'title': a.title,
    'scope_ref': a.scope,
    'created_at': utc_now(),
    'closed_at': None,
    'status': 'PLANNING',
    'lifecycle_stage': 'PLANNING',
    'next_action': 'RUN_CODEX_PLANNING',
    'planning': {
        'version': planning_version,
        'revision': 1,
        'revision_label': 'Revision_1',
        'status': 'IN_PROGRESS',
        'material_unknowns': None,
        'package_status': 'NOT_COMPILED',
        'task_expansion_allowed': False,
        'interaction_gate': 'NONE',
        'invocation_stop_required': False,
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
state['project_state'] = 'PLANNING'
reset_package_workspace(planning_version, 'Revision_1')
save_state(state)
append_transition('CHANGE_CYCLE_STARTED', actor='user:start_cycle', cycle_id=cycle_id, details={'scope_ref': a.scope, 'planning_version': planning_version})
print('START_CYCLE: PASS')
print(f'cycle_id: {cycle_id}')
print(f'planning_version: {planning_version}')
print('execution_authorized: false')
print('Next: run Codex with EXECUTE/codex/IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md')
