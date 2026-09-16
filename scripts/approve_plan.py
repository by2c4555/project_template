#!/usr/bin/env python3
"""Explicit user approval gate for v4.1 Planning Vx -> Execution Vx."""
from pathlib import Path
import argparse, re, sys
R=Path(__file__).resolve().parents[1]
def replace_yamlish(text,key,value):
 pat=rf'^(\s*{re.escape(key)}:\s*).*$'
 if re.search(pat,text,re.M): return re.sub(pat,rf'\g<1>{value}',text,flags=re.M)
 return text

def main():
 ap=argparse.ArgumentParser(description='Approve one Planning Vx and bind an Execution Vx to it.')
 ap.add_argument('--planning',required=True,help='e.g. Planning_V1')
 ap.add_argument('--execution',required=True,help='e.g. Execution_V1')
 ap.add_argument('--approved-by',default='user')
 a=ap.parse_args()
 if not re.fullmatch(r'Planning_V[1-9][0-9]*',a.planning): raise SystemExit('invalid --planning')
 if not re.fullmatch(r'Execution_V[1-9][0-9]*',a.execution): raise SystemExit('invalid --execution')
 ps=R/'EXECUTE/plan/PLANNING_STATUS.md'; st=R/'EXECUTE/PROJECT_STATUS.md'; es=R/'EXECUTE/execution/EXECUTION_STATE.md'
 pt=ps.read_text();
 if 'AWAITING_USER_APPROVAL' not in pt:
  raise SystemExit('Planning status is not AWAITING_USER_APPROVAL; approval blocked.')
 if not re.search(rf'planning_version:\s*{re.escape(a.planning)}\b',pt):
  raise SystemExit(f'Planning status does not identify {a.planning}; approval blocked.')
 pt=replace_yamlish(pt,'planning_status','APPROVED'); pt=replace_yamlish(pt,'approved_by',a.approved_by); pt=replace_yamlish(pt,'execution_locked','false'); ps.write_text(pt)
 t=st.read_text();
 for k,v in [('lifecycle_stage','EXECUTION'),('planning_version',a.planning),('planning_status','APPROVED'),('approved_planning_version',a.planning),('execution_version',a.execution),('execution_status','READY'),('execution_bound_planning_version',a.planning),('evaluation_status','NOT_STARTED')]: t=replace_yamlish(t,k,v)
 t=replace_yamlish(t,'next_action','>\n  Start VS Code ProjectManager500K with EXECUTE_PROJECT_PROMPT.md.')
 st.write_text(t)
 e=es.read_text();
 for k,v in [('execution_version',a.execution),('execution_status','READY'),('execution_bound_planning_version',a.planning),('active_task','none'),('replan_required','false'),('evaluation_required','false')]: e=replace_yamlish(e,k,v)
 es.write_text(e)
 print(f'APPROVED: {a.planning} -> bound {a.execution}')
 print('Next: run EXECUTE_PROJECT_PROMPT.md with ProjectManager500K in VS Code.')
if __name__=='__main__': main()
