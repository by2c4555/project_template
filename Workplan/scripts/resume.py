#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _core.resume import project_resume
r=project_resume()
print('RESUME_STATUS:',r.pop('resume_status'))
for k,v in r.items():
    if v is not None: print(f'{k}: {v}')
if r.get('human_approval_required'):
    print(f"human_command: python Workplan/scripts/approve.py -- {r['challenge']}")
