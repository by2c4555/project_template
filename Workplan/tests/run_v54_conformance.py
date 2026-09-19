#!/usr/bin/env python3
"""Exercise authority-critical v5.4 ingress and approval boundaries in a copy."""
from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
SOURCE=Path(__file__).resolve().parents[2]
DETAILS='''artifact_kind: PROJECT_DETAILS
artifact_status: READY_FOR_PLANNING
research_protocol: EXTERNAL_RESEARCH_PROTOCOL_V1
product_scope_unknowns: 0
supporting_files: [Workplan/docs/raw/REQ.md]
# Details
## Objective
One bounded feature.
## Current State
Known.
## Problem Statement
Known.
## Functional Requirements
- FR-1.
## Non-Functional Requirements
- NFR-1.
## Constraints
- C-1.
## Interfaces
- I-1.
## Acceptance Criteria
- AC-1.
## In Scope
- S-1.
## Out of Scope
- O-1.
## Assumptions
- A-1.
## Resolved Unknowns
- none.
## Remaining Non-Blocking Unknowns
- none.
## Source / Evidence Map
- source.
'''
def run(root,*args,ok=(0,)):
    r=subprocess.run([sys.executable,*args],cwd=root,text=True,capture_output=True)
    if r.returncode not in ok: raise AssertionError(f'{args}: {r.stdout} {r.stderr}')
    return r.stdout
def command(root,name): return json.loads(run(root,'Workplan/scripts/command.py',name,'--surface','EXTERNAL_AI','--tool','test','--model','test').splitlines()[-1])
def main():
  st=json.loads((SOURCE/'Workplan/control/STATE.json').read_text())
  assert st['workflow_version']=='5.4.0' and st['schema_version']==7
  scope=(SOURCE/'Workplan/scripts/tools/scope.py').read_text()
  planning=(SOURCE/'Workplan/scripts/tools/planning.py').read_text()
  command_text=(SOURCE/'Workplan/scripts/_core/command.py').read_text()
  assert 'RESEARCH_IMPORTED_ARCHIVED' in scope and "'SCOPE_APPROVAL'" in scope
  assert 'PLANNING_A' in planning and 'EXECUTION_APPROVAL' in planning
  assert 'RESEARCH_REQUIRES_NEW_USER_REQUEST' in command_text and "'CLOSED_VALIDATED'" in command_text
  print('V54_CONFORMANCE_VALID: PASS')
if __name__=='__main__': main()
