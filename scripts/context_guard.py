#!/usr/bin/env python3
"""Conservative Builder100K context preflight for v4.3.0. Standard-library only."""
from pathlib import Path
import argparse, math, re, sys, json
ROOT=Path(__file__).resolve().parents[1]
TARGET=40000; MAX=52000; RESERVE=5000
PATH_RE=re.compile(r"`([^`]+)`")
def tok(n): return math.ceil(n/4)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('task'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
 p=(ROOT/a.task).resolve() if not Path(a.task).is_absolute() else Path(a.task).resolve()
 try: p.relative_to(ROOT.resolve())
 except ValueError: print('CONTEXT_BLOCKED: task outside workspace'); return 30
 if not p.is_file(): print('CONTEXT_BLOCKED: task not found'); return 30
 txt=p.read_text(encoding='utf-8',errors='replace')
 if not re.search(r'^builder:\s*Builder100K\s*$',txt,re.M): print('CONTEXT_BLOCKED: Builder100K profile missing'); return 30
 m=re.search(r'## Context Manifest\s*(.*?)(?=\n## Allowed Scope|\Z)',txt,re.S)
 paths=[]
 if m:
  for x in PATH_RE.findall(m.group(1)):
   x=x.strip()
   if '*' in x: continue
   q=(ROOT/x).resolve()
   try: q.relative_to(ROOT.resolve())
   except ValueError: continue
   if q.is_file() and x not in paths: paths.append(x)
 chars=len(txt); det=[]
 for x in paths:
  q=ROOT/x; n=len(q.read_text(encoding='utf-8',errors='replace')); chars+=n; det.append({'path':x,'tokens_est':tok(n)})
 total=tok(chars)+RESERVE
 decision='PASS' if total<=TARGET else ('WARN' if total<=MAX else 'SPLIT_REQUIRED')
 code={'PASS':0,'WARN':10,'SPLIT_REQUIRED':20}[decision]
 out={'task':str(p.relative_to(ROOT)),'builder':'Builder100K','controlled_tokens_est':total,'target':TARGET,'max':MAX,'files':det,'decision':decision}
 print(json.dumps(out,indent=2) if a.json else f'{decision}: Builder100K controlled≈{total} target={TARGET} max={MAX} files={len(det)}')
 return code
if __name__=='__main__': raise SystemExit(main())
