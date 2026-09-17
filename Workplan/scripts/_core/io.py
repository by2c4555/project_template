from __future__ import annotations
import json, os, tempfile
from pathlib import Path

def atomic_write_text(path:Path, text:str):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=path.name+'.', dir=str(path.parent))
    try:
        with os.fdopen(fd,'w',encoding='utf-8',newline='\n') as f: f.write(text)
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def atomic_write_json(path:Path, obj):
    atomic_write_text(path, json.dumps(obj,indent=2,sort_keys=True)+'\n')
