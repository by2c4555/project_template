#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _core.approval import submit
args=[x for x in sys.argv[1:] if x!='--']
if len(args)!=1: raise SystemExit('usage: python Workplan/scripts/approve.py -- <challenge>')
status,rec,new=submit(args[0]); print('APPROVAL:',status); print('id:',rec['approval_id'])
if new: print('new_challenge:',new)
raise SystemExit(0 if status=='GRANTED' else 2)
