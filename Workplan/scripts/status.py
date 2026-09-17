#!/usr/bin/env python3
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _core.state import load_state,compact
for k,v in compact(load_state()).items(): print(f'{k}: {v}')
