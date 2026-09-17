#!/usr/bin/env python3
import argparse, json
from _bootstrap import *
from _core.ingest import validate
p=argparse.ArgumentParser(); p.add_argument('cmd',choices=['check']); a=p.parse_args()
r=validate(); print('INGEST_VALID: PASS'); print('ingest_id:',r['ingest_id']); print('package_digest:',r['package_digest']); print('scope_digest:',r['scope_digest'])
