#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _core.approval import submit
args=sys.argv[1:]
if args and args[0]=='--': args=args[1:]
if len(args)!=1 or not args[0].isdigit():
    raise SystemExit('USAGE: python Workplan/scripts/approve.py -- <6-digit-challenge>')
status,rec,new=submit(args[0])
print('APPROVAL:',status)
print('id:',rec['approval_id'])
if status=='GRANTED': print('requested_action:',rec['requested_action'])
elif status=='REJECTED': print('new_challenge:',new)
elif status=='STALE': print('reason: STALE_APPROVAL_BINDING')
