#!/usr/bin/env python3
import argparse
from _bootstrap import *
from _core import work as W
p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
a=sp.add_parser('acquire'); a.add_argument('--role',required=True); a.add_argument('--tool',default='unknown'); a.add_argument('--model',default='unknown'); a.add_argument('--task')
sp.add_parser('status')
c=sp.add_parser('checkpoint'); c.add_argument('--generation',type=int,required=True); c.add_argument('--unit',required=True); c.add_argument('--next-unit',required=True); c.add_argument('--note',required=True)
x=sp.add_parser('complete'); x.add_argument('--generation',type=int,required=True); x.add_argument('--note',default='')
q=sp.add_parser('request-context'); q.add_argument('--reason',required=True)
ns=p.parse_args()
if ns.cmd=='acquire':
    mode,m,t=W.acquire(ns.role,ns.tool,ns.model,ns.task); print('WORK:',mode); print('ticket:',t)
elif ns.cmd=='status':
    m=W.status(); print('WORK: NONE' if not m else 'WORK: ACTIVE');
    if m: print('work_id:',m['work_id']); print('role:',m['role']); print('generation:',m['generation']); print('checkpoint_seq:',m['checkpoint_seq']); print('next_unit:',m['next_unit']); print('reconciliation:',W.reconcile(m))
elif ns.cmd=='checkpoint':
    cp=W.checkpoint(ns.unit,ns.next_unit,ns.note,ns.generation); print('WORK_CHECKPOINT: PASS'); print('checkpoint_seq:',cp['checkpoint_seq'])
elif ns.cmd=='complete':
    m=W.complete(ns.note,ns.generation); print('WORK_COMPLETE: PASS'); print('work_id:',m['work_id'])
elif ns.cmd=='request-context': print(W.request_context(ns.reason))
