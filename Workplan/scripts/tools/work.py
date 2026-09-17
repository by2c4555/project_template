#!/usr/bin/env python3
import argparse
from _bootstrap import *
from _core import work as W
p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
b=sp.add_parser('begin'); b.add_argument('--role',required=True); b.add_argument('--tool',default='unknown'); b.add_argument('--model',default='unknown'); b.add_argument('--task')
s=sp.add_parser('status')
c=sp.add_parser('checkpoint'); c.add_argument('--unit',required=True); c.add_argument('--next-unit',required=True); c.add_argument('--note',required=True)
x=sp.add_parser('complete'); x.add_argument('--note',default='')
a=p.parse_args()
if a.cmd=='begin':
    mode,m=W.begin(a.role,a.tool,a.model,a.task); print('WORK:',mode); [print(f'{k}: {m.get(k)}') for k in ['work_id','role','task_id','checkpoint_seq','next_unit']]
elif a.cmd=='status':
    m=W.status(); print('WORK: NONE' if not m else 'WORK: ACTIVE');
    if m: [print(f'{k}: {m.get(k)}') for k in ['work_id','role','task_id','status','checkpoint_seq','current_unit','next_unit']]
elif a.cmd=='checkpoint':
    cp=W.checkpoint(a.unit,a.next_unit,a.note); print('WORK_CHECKPOINT: PASS'); print('checkpoint_seq:',cp['checkpoint_seq']); print('next_unit:',cp['next_unit'])
elif a.cmd=='complete':
    m=W.complete(a.note); print('WORK_COMPLETE: PASS'); print('work_id:',m['work_id'])
