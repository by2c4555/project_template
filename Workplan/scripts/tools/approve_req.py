#!/usr/bin/env python3
import argparse
from _bootstrap import *
from _core.approval import get_pending
p=argparse.ArgumentParser(); p.add_argument('--id',required=True); a=p.parse_args()
st,r=get_pending(a.id)
print('APPROVAL_REQUEST: READY'); print('id:',r['approval_id']); print('risk:',r['risk_kind']); print('requested_action:',r['requested_action']); print('challenge:',r['challenge']); print('generation:',r['challenge_generation']); print(f'human_command: python Workplan/scripts/approve.py -- {r["challenge"]}'); print('STOP')
