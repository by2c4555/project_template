#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _core.command import execute
p=argparse.ArgumentParser(description='Project Template v5.2 exact human workflow command interface')
p.add_argument('command')
p.add_argument('--surface',required=True,choices=['EXTERNAL_AI','VS_CODE'])
p.add_argument('--tool',default='unknown')
p.add_argument('--model',default='unknown')
a=p.parse_args(); r=execute(a.command,a.surface,a.tool,a.model)
print(json.dumps(r,indent=2,sort_keys=True))
raise SystemExit(0 if r.get('status') in {'OK','ACCEPTED','APPROVAL_REQUIRED'} else 2)
