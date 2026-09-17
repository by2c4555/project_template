#!/usr/bin/env python3
from _bootstrap import *
from _core.approval import get_pending
st,r=get_pending(); print('APPROVAL_PENDING'); print('id:',r['approval_id']); print('status:',r['status']); print('generation:',r['challenge_generation'])
