#!/usr/bin/env python3
"""Run potentially verbose commands while persisting full output and returning bounded output to the agent."""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path
from workflow_state import ROOT, load_state, utc_now

ap=argparse.ArgumentParser(description='Bound command output to protect agent context while preserving full logs.')
ap.add_argument('--label',required=True)
ap.add_argument('--chars',type=int,default=None,help='maximum combined characters printed back; defaults to runtime policy')
ap.add_argument('command',nargs=argparse.REMAINDER)
a=ap.parse_args()
cmd=a.command
if cmd and cmd[0]=='--': cmd=cmd[1:]
if not cmd: raise SystemExit('SAFE_EXEC: FAIL\nmissing command after --')
if not all(ch.isalnum() or ch in '._-' for ch in a.label): raise SystemExit('SAFE_EXEC: FAIL\nlabel may contain only letters, digits, dot, underscore, hyphen')
state=load_state(); maxchars=a.chars or int(state.get('runtime_policy',{}).get('safe_exec_stdout_chars',12000))
proc=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,errors='replace')
out=proc.stdout or ''
logdir=ROOT/'EXECUTE/execution/logs'; logdir.mkdir(parents=True,exist_ok=True)
log=logdir/f'{a.label}.log'; log.write_text(f'# {utc_now()}\n# command: {cmd!r}\n# exit_code: {proc.returncode}\n\n{out}',encoding='utf-8')
print('SAFE_EXEC')
print(f'exit_code: {proc.returncode}')
print(f'full_log: {log.relative_to(ROOT)}')
print(f'full_output_chars: {len(out)}')
if len(out)<=maxchars:
    print('--- bounded output ---'); print(out,end='' if out.endswith('\n') else '\n')
else:
    head=maxchars//2; tail=maxchars-head
    print(f'--- bounded output: first {head} + last {tail} chars ---')
    print(out[:head]); print('\n... [output truncated; inspect full log only if justified] ...\n'); print(out[-tail:])
raise SystemExit(proc.returncode)
