#!/usr/bin/env python3
"""Capture an updated external handoff as a new immutable Scope revision inside the active Cycle."""
from __future__ import annotations

import argparse
from copy import deepcopy
from workflow_state import (
    active_cycle, append_transition, build_scope_manifest, load_state,
    reset_package_workspace, save_state, snapshot_scope,
)

ap = argparse.ArgumentParser(description='Import updated project_details/docs/raw as SCOPE_N+1 for the active Cycle.')
ap.add_argument('--reason', required=True, help='Why the scope changed/was clarified')
a = ap.parse_args()

state = load_state()
cid, cycle = active_cycle(state)
if cycle.get('status') == 'CLOSED_VALIDATED':
    raise SystemExit('IMPORT_SCOPE: BLOCKED\nvalidated cycles are immutable; use start_cycle.py for new post-validation scope')

old_scope = cycle.get('scope') or {}
old_n = int(old_scope.get('revision', 0))
new_n = old_n + 1
revision = f'SCOPE_{new_n:03d}'
try:
    manifest = build_scope_manifest(revision)
except ValueError as exc:
    raise SystemExit('IMPORT_SCOPE: BLOCKED\n' + str(exc))
if manifest['scope_digest'] == old_scope.get('digest'):
    raise SystemExit('IMPORT_SCOPE: BLOCKED\nexternal handoff is identical to the active Scope Snapshot; no new revision needed')
try:
    snapshot = snapshot_scope(cid, manifest)
except ValueError as exc:
    raise SystemExit('IMPORT_SCOPE: BLOCKED\n' + str(exc))

if old_scope:
    historic = deepcopy(old_scope)
    historic['status'] = 'SUPERSEDED'
    cycle.setdefault('scope_history', []).append(historic)

cycle['scope'] = {
    'revision': new_n,
    'revision_label': revision,
    'status': 'ACTIVE',
    'digest': manifest['scope_digest'],
    'title': manifest['scope_title'],
    'baseline_ref': manifest['baseline_ref'],
    'snapshot_path': snapshot,
    'source_handoff_path': manifest['source_handoff_path'],
    'supporting_files': manifest['supporting_files'],
    'captured_at': manifest['created_at'],
    'reason': a.reason,
}

state['active_external_work'] = None

planning = cycle.get('planning') or {}
was_approved = bool(cycle.get('approval') or cycle.get('execution'))

if not was_approved and cycle.get('status') == 'PLANNING':
    if planning:
        cycle.setdefault('planning_history', []).append(deepcopy(planning))
        planning['revision'] = int(planning.get('revision', 1)) + 1
        planning['revision_label'] = f'Revision_{planning["revision"]}'
        planning.update({
            'status': 'IN_PROGRESS',
            'based_on_scope_revision': revision,
            'based_on_scope_digest': manifest['scope_digest'],
            'material_unknowns': None,
            'package_status': 'NOT_COMPILED',
            'task_expansion_allowed': False,
            'interaction_gate': 'NONE',
            'invocation_stop_required': False,
            'candidate_scope_digest': None,
            'candidate_package_digest': None,
        })
        reset_package_workspace(planning['version'], planning['revision_label'])
    cycle['lifecycle_stage'] = 'PLANNING'
    cycle['next_action'] = 'RUN_EXTERNAL_AGENT_PLANNING'
    state['project_state'] = 'PLANNING'
    route = 'PLANNING_REVISION_REQUIRED'; state['active_external_work']=None
else:
    if cycle.get('approval'):
        old_approval = deepcopy(cycle['approval'])
        old_approval['status'] = 'SUPERSEDED_BY_SCOPE_CHANGE'
        cycle.setdefault('approval_history', []).append(old_approval)
        cycle['approval'] = None
    ex = cycle.get('execution') or {}
    if ex:
        ex['status'] = 'PAUSED_FOR_REPLAN'
        rec = ex.get('recovery') or {}
        rec['status'] = 'REPLAN_REQUIRED'
        rec['resume_authorized'] = False
        ex['recovery'] = rec
    cycle['status'] = 'REPLAN_REQUIRED'
    cycle['lifecycle_stage'] = 'REPLAN_REQUIRED'
    cycle['next_action'] = 'RUN_START_REPLAN'
    state['project_state'] = 'REPLAN_REQUIRED'
    route = 'REPLAN_REQUIRED'; state['active_external_work']=None

save_state(state)
append_transition(
    'SCOPE_REVISION_IMPORTED', actor='user:import_scope', cycle_id=cid,
    details={
        'scope_revision': revision,
        'scope_digest': manifest['scope_digest'],
        'snapshot_path': snapshot,
        'reason': a.reason,
        'route': route,
    },
)
print('IMPORT_SCOPE: PASS')
print(f'scope_revision: {revision}')
print(f'scope_digest: {manifest["scope_digest"]}')
print(f'route: {route}')
if route == 'PLANNING_REVISION_REQUIRED':
    print(f'planning_revision: {planning.get("revision_label")}')
    print('Next: resume External Agent Planning against the new Scope Snapshot.')
else:
    print('All prior implementation authority is superseded. Next: run python scripts/start_replan.py')
