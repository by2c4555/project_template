#!/usr/bin/env python3
"""Compatibility adapter. v5.3 public entry is Workplan/scripts/command.py."""
import argparse,json
from _bootstrap import *
from _core.state import load_state
from _core.command import ROLE_COMMAND, execute
p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True); a=sp.add_parser('acquire'); a.add_argument('--tool',default='unknown'); a.add_argument('--model',default='unknown'); ns=p.parse_args(); st=load_state(); role=st.get('lifecycle_stage'); command=ROLE_COMMAND.get(role)
if not command: raise SystemExit('EXTERNAL_ENTRY: BLOCKED\ncurrent stage is not an external reasoning role')
r=execute(command,'EXTERNAL_AI',ns.tool,ns.model)
print('EXTERNAL_ENTRY:',r.get('status')); print(json.dumps(r,sort_keys=True))
raise SystemExit(0 if r.get('status') in {'ACCEPTED','APPROVAL_REQUIRED'} else 2)
