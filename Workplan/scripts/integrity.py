#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _core.integrity import write_release_manifest, validate_release_manifest, release_files

p=argparse.ArgumentParser(description='Project Template v5.3 deterministic release manifest')
p.add_argument('command', choices=['generate','check'])
a=p.parse_args()
if a.command=='generate':
    write_release_manifest()
ok, problems=validate_release_manifest()
if not ok:
    print('RELEASE_INTEGRITY: FAIL')
    for problem in problems: print('FAIL:', problem)
    raise SystemExit(1)
print('RELEASE_INTEGRITY: PASS')
print('release_files:', len(release_files()))
