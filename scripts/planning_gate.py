#!/usr/bin/env python3
"""Machine-governed planning interaction and package-expansion gate for v4.4.0."""
from __future__ import annotations
import argparse
from copy import deepcopy
from workflow_state import (
    active_cycle, append_transition, build_package_manifest, load_state, next_id,
    save_state, write_json, CONTROL, ensure_scope_integrity, require_external_work_complete,
)


def planning(state):
    cid, cycle = active_cycle(state)
    if cycle.get('status') not in {'PLANNING'}:
        raise SystemExit(f'PLANNING_GATE: BLOCKED\ncycle {cid} status {cycle.get("status")} is not PLANNING')
    ensure_scope_integrity(cycle)
    return cid, cycle, cycle['planning']


def cmd_status(_a):
    state = load_state(); cid, cycle, p = planning(state)
    for k in ['version','revision_label','status','based_on_scope_revision','based_on_scope_digest','material_unknowns','package_status','task_expansion_allowed','interaction_gate','invocation_stop_required','candidate_scope_digest','candidate_package_digest']:
        print(f'{k}: {p.get(k)}')
    print(f'cycle_id: {cid}')
    return 0


def cmd_hold(a):
    if a.unknowns < 1:
        raise SystemExit('PLANNING_GATE: FAIL\n--unknowns must be >= 1')
    state = load_state(); cid, cycle, p = planning(state)
    p.update({
        'status':'AWAITING_MATERIAL_FEEDBACK', 'material_unknowns':a.unknowns,
        'package_status':'NOT_COMPILED', 'task_expansion_allowed':False,
        'interaction_gate':'USER_FEEDBACK_REQUIRED', 'invocation_stop_required':True,
        'candidate_scope_digest':None,'candidate_package_digest':None,
    })
    cycle['next_action'] = 'USER_FEEDBACK_THEN_RESUME_PLANNING'
    save_state(state); append_transition('PLANNING_MATERIAL_FEEDBACK_REQUIRED', actor='agent:planning_gate', cycle_id=cid, details={'unknowns':a.unknowns})
    print('PLANNING_GATE: PASS\nHARD_STOP_REQUIRED: true\nReason: material decisions remain. Ask focused questions and end the invocation.')
    return 0


def cmd_resume(_a):
    state = load_state(); cid, cycle, p = planning(state)
    if p.get('status') not in {'AWAITING_MATERIAL_FEEDBACK','PLAN_READY'}:
        raise SystemExit(f'PLANNING_GATE: BLOCKED\nresume-feedback not valid from {p.get("status")}')
    p.update({'status':'IN_PROGRESS','interaction_gate':'NONE','invocation_stop_required':False,'task_expansion_allowed':False,'package_status':'NOT_COMPILED','candidate_scope_digest':None,'candidate_package_digest':None})
    cycle['next_action']='RUN_EXTERNAL_AGENT_PLANNING'
    save_state(state); append_transition('PLANNING_FEEDBACK_RESUMED', actor='agent:planning_gate', cycle_id=cid)
    print('PLANNING_GATE: PASS\nstate: IN_PROGRESS\nTask expansion remains locked until authorize-expansion.')
    return 0


def cmd_revision(a):
    state = load_state(); cid, cycle, p = planning(state)
    if cycle.get('approval'):
        raise SystemExit('PLANNING_GATE: BLOCKED\napproved planning cannot be revised in place; use start_replan.py')
    cycle.setdefault('planning_history', []).append(deepcopy(p))
    p['revision'] = int(p.get('revision',1)) + 1
    p['revision_label'] = f'Revision_{p["revision"]}'
    scope=cycle.get('scope') or {}
    p.update({'status':'IN_PROGRESS','based_on_scope_revision':scope.get('revision_label'),'based_on_scope_digest':scope.get('digest'),'material_unknowns':None,'package_status':'NOT_COMPILED','task_expansion_allowed':False,'interaction_gate':'NONE','invocation_stop_required':False,'candidate_scope_digest':None,'candidate_package_digest':None})
    cycle['next_action']='RUN_EXTERNAL_AGENT_PLANNING'
    state['active_external_work']=None
    save_state(state); append_transition('PLANNING_REVISION_STARTED', actor='agent:planning_gate', cycle_id=cid, details={'revision':p['revision_label'],'reason':a.reason})
    print('PLANNING_GATE: PASS')
    print(f'planning_revision: {p["revision_label"]}')
    print('Old draft is historical; regenerate all current package artifacts with the new revision metadata.')
    return 0


def cmd_zero(_a):
    state = load_state(); cid, cycle, p = planning(state)
    if p.get('status') != 'IN_PROGRESS':
        raise SystemExit(f'PLANNING_GATE: BLOCKED\nset-material-zero requires IN_PROGRESS, found {p.get("status")}')
    p['material_unknowns'] = 0
    save_state(state); append_transition('PLANNING_MATERIAL_UNKNOWNS_ZERO', actor='agent:planning_gate', cycle_id=cid)
    print('PLANNING_GATE: PASS\nmaterial_unknowns: 0')
    return 0


def cmd_authorize(_a):
    state = load_state(); cid, cycle, p = planning(state)
    errors=[]
    if p.get('status') != 'IN_PROGRESS': errors.append('planning status must be IN_PROGRESS')
    if p.get('material_unknowns') != 0: errors.append('material_unknowns must be exactly 0')
    if p.get('interaction_gate') != 'NONE': errors.append('interaction gate must be NONE')
    scope=cycle.get('scope') or {}
    if p.get('based_on_scope_revision') != scope.get('revision_label'): errors.append('planning is not bound to the active scope revision')
    if p.get('based_on_scope_digest') != scope.get('digest'): errors.append('planning is not bound to the active scope digest')
    if errors:
        raise SystemExit('PLANNING_GATE: FAIL\n'+'\n'.join('FAIL: '+e for e in errors))
    p['task_expansion_allowed']=True
    save_state(state); append_transition('PLANNING_PACKAGE_EXPANSION_AUTHORIZED', actor='python:planning_gate', cycle_id=cid, details={'planning':p['version'],'revision':p['revision_label']})
    print('PLANNING_GATE: PASS\nTask/package compilation is authorized for the current Planning revision only.')
    return 0


def cmd_ready(_a):
    state = load_state(); cid, cycle, p = planning(state)
    require_external_work_complete(state, cycle, 'PLANNING')
    if p.get('status') != 'IN_PROGRESS' or p.get('material_unknowns') != 0 or not p.get('task_expansion_allowed'):
        raise SystemExit('PLANNING_GATE: BLOCKED\nrequires IN_PROGRESS + material_unknowns=0 + task_expansion_allowed=true')
    scope=cycle.get('scope') or {}
    if p.get('based_on_scope_revision') != scope.get('revision_label') or p.get('based_on_scope_digest') != scope.get('digest'):
        raise SystemExit('PLANNING_GATE: BLOCKED\nactive Scope Snapshot changed; import/revision planning before PLAN_READY')
    try:
        manifest = build_package_manifest(p['version'], p['revision_label'])
    except ValueError as exc:
        raise SystemExit('PLANNING_GATE: FAIL\n'+str(exc))
    candidate = CONTROL / 'manifests' / f'{cid}_{p["version"]}_{p["revision_label"]}_CANDIDATE.json'
    write_json(candidate, manifest)
    p.update({'status':'PLAN_READY','package_status':'READY_FOR_APPROVAL','task_expansion_allowed':False,'interaction_gate':'USER_REVIEW_OR_APPROVAL','invocation_stop_required':True,'candidate_scope_digest':scope['digest'],'candidate_package_digest':manifest['package_digest']})
    cycle['next_action']='REVIEW_PLAN_OR_RUN_APPROVE_PLAN'
    save_state(state); append_transition('PLAN_READY', actor='python:planning_gate', cycle_id=cid, details={'planning':p['version'],'revision':p['revision_label'],'scope_revision':scope['revision_label'],'scope_digest':scope['digest'],'package_digest':manifest['package_digest'],'task_count':manifest['task_count']})
    print('PLANNING_GATE: PASS')
    print('planning_status: PLAN_READY')
    print(f'scope_revision: {scope["revision_label"]}')
    print(f'scope_digest: {scope["digest"]}')
    print(f'package_digest: {manifest["package_digest"]}')
    print(f'task_count: {manifest["task_count"]}')
    print('HARD_STOP_REQUIRED: true')
    print('Any chat message is feedback/question only. Implementation requires the user to run scripts/approve_plan.py manually.')
    return 0


def main():
    ap=argparse.ArgumentParser(description='v4.3 planning state/cost gate')
    sub=ap.add_subparsers(dest='cmd',required=True)
    s=sub.add_parser('status'); s.set_defaults(func=cmd_status)
    h=sub.add_parser('hold-material-feedback'); h.add_argument('--unknowns',type=int,required=True); h.set_defaults(func=cmd_hold)
    r=sub.add_parser('resume-feedback'); r.set_defaults(func=cmd_resume)
    n=sub.add_parser('begin-revision'); n.add_argument('--reason',required=True); n.set_defaults(func=cmd_revision)
    z=sub.add_parser('set-material-zero'); z.set_defaults(func=cmd_zero)
    e=sub.add_parser('authorize-expansion'); e.set_defaults(func=cmd_authorize)
    m=sub.add_parser('mark-plan-ready'); m.set_defaults(func=cmd_ready)
    a=ap.parse_args(); return a.func(a)

if __name__=='__main__': raise SystemExit(main())
