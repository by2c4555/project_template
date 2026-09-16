#!/usr/bin/env python3
"""Explicit user implementation-approval gate for v4.1.3 Planning Vx -> Execution Vx."""
from pathlib import Path
import argparse, re
from datetime import datetime, timezone
R=Path(__file__).resolve().parents[1]

def replace_yamlish(text,key,value):
    pat=rf'^(\s*{re.escape(key)}:\s*).*$'
    if re.search(pat,text,re.M):
        return re.sub(pat,rf'\g<1>{value}',text,flags=re.M)
    return text

def value_of(text,key):
    m=re.search(rf'^\s*{re.escape(key)}:\s*(.*?)\s*$',text,re.M)
    return m.group(1).strip() if m else None

def main():
    ap=argparse.ArgumentParser(description='Record explicit user authorization and bind one execution-ready Planning Vx to an Execution Vx.')
    ap.add_argument('--planning',required=True,help='e.g. Planning_V1')
    ap.add_argument('--execution',required=True,help='e.g. Execution_V1')
    ap.add_argument('--approved-by',default='user')
    a=ap.parse_args()
    if not re.fullmatch(r'Planning_V[1-9][0-9]*',a.planning): raise SystemExit('invalid --planning')
    if not re.fullmatch(r'Execution_V[1-9][0-9]*',a.execution): raise SystemExit('invalid --execution')

    ps=R/'EXECUTE/plan/PLANNING_STATUS.md'; st=R/'EXECUTE/PROJECT_STATUS.md'; es=R/'EXECUTE/execution/EXECUTION_STATE.md'
    pt=ps.read_text(encoding='utf-8')
    if value_of(pt,'planning_status') != 'AWAITING_USER_APPROVAL':
        raise SystemExit('Planning status is not AWAITING_USER_APPROVAL; implementation approval blocked.')
    if value_of(pt,'planning_version') != a.planning:
        raise SystemExit(f'Planning status does not identify {a.planning}; implementation approval blocked.')
    if value_of(pt,'material_unknowns') != '0':
        raise SystemExit('material_unknowns must be 0 before implementation approval.')
    if value_of(pt,'implementation_approval_requested') != 'true':
        raise SystemExit('Codex has not marked implementation_approval_requested: true; approval blocked.')

    revision=value_of(pt,'planning_revision') or 'none'
    approved_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
    pt=replace_yamlish(pt,'planning_status','APPROVED')
    pt=replace_yamlish(pt,'approved_by',a.approved_by)
    pt=replace_yamlish(pt,'approved_at',approved_at)
    pt=replace_yamlish(pt,'execution_locked','false')
    ps.write_text(pt,encoding='utf-8')

    t=st.read_text(encoding='utf-8')
    for k,v in [
        ('lifecycle_stage','EXECUTION'),('planning_version',a.planning),('planning_revision',revision),('planning_status','APPROVED'),
        ('material_unknowns','0'),('implementation_approval_requested','true'),('approved_planning_version',a.planning),('execution_version',a.execution),('execution_status','READY'),
        ('execution_bound_planning_version',a.planning),('evaluation_status','NOT_STARTED')
    ]: t=replace_yamlish(t,k,v)
    t=replace_yamlish(t,'next_action','>\n  Start VS Code ProjectManager500K with EXECUTE_PROJECT_PROMPT.md.')
    st.write_text(t,encoding='utf-8')

    e=es.read_text(encoding='utf-8')
    for k,v in [('execution_version',a.execution),('execution_status','READY'),('execution_bound_planning_version',a.planning),('active_task','none'),('replan_required','false'),('evaluation_required','false')]:
        e=replace_yamlish(e,k,v)
    es.write_text(e,encoding='utf-8')
    print(f'APPROVED FOR IMPLEMENTATION: {a.planning} -> bound {a.execution}')
    print('Next: run EXECUTE_PROJECT_PROMPT.md with ProjectManager500K in VS Code.')

if __name__=='__main__': main()
