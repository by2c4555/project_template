#!/usr/bin/env python3
import argparse,subprocess
p=argparse.ArgumentParser(); p.add_argument('--label',default='CMD'); p.add_argument('cmd',nargs=argparse.REMAINDER); a=p.parse_args(); cmd=a.cmd[1:] if a.cmd[:1]==['--'] else a.cmd
if not cmd: raise SystemExit('safe_exec: command required')
r=subprocess.run(cmd,text=True,capture_output=True); print(f'{a.label}: exit={r.returncode}'); print('STDOUT:'); print((r.stdout or '')[-12000:]); print('STDERR:'); print((r.stderr or '')[-12000:]); raise SystemExit(r.returncode)
