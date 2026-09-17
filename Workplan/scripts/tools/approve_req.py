#!/usr/bin/env python3
import argparse
from _bootstrap import *
from _core.approval import get_pending
p=argparse.ArgumentParser(); p.add_argument('--id'); a=p.parse_args(); st,r=get_pending(a.id); print('APPROVAL_REQUEST'); print('id:',r['approval_id']); print('risk:',r['risk_kind']); print('action:',r['requested_action']); print('subject:',r.get('subject','')); print('challenge:',r['challenge'])
