#!/usr/bin/env python3
import argparse,json
from _bootstrap import *
from _core.approval import create_pending
from _core.paths import WORKPLAN
p=argparse.ArgumentParser(); p.add_argument('--risk',required=True); p.add_argument('--action',required=True); p.add_argument('--subject',default=''); a=p.parse_args()
r=create_pending(a.risk,a.action,a.subject)
print('TOKEN_RISK_APPROVAL_REQUIRED'); print('id:',r['approval_id']); print('challenge:',r['challenge']); print(f'next: python Workplan/scripts/tools/approve_req.py --id {r["approval_id"]}')
