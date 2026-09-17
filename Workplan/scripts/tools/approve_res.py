#!/usr/bin/env python3
import argparse,json
from _bootstrap import *
from _core.state import load_state
from _core.paths import APPROVAL_DIR
p=argparse.ArgumentParser(); p.add_argument('--id',required=True); a=p.parse_args(); st=load_state(); cur=st.get('pending_approval')
if cur and cur.get('approval_id')==a.id:
    print('APPROVAL_STATE: WAITING_HUMAN'); print('id:',a.id); print('challenge:',cur['challenge']); print('generation:',cur['challenge_generation']); print(f'human_command: python Workplan/scripts/approve.py -- {cur["challenge"]}'); print('STOP'); raise SystemExit
fp=APPROVAL_DIR/f'{a.id}.json'
if fp.is_file():
    r=json.loads(fp.read_text()); print('APPROVAL_STATE:',r.get('status')); print('id:',a.id); print('requested_action:',r.get('requested_action')); raise SystemExit
print('APPROVAL_STATE: UNKNOWN')
