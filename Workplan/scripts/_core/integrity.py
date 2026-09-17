import hashlib, json, re
from pathlib import Path
from .paths import ROOT, WORKPLAN

def sha256_file(p:Path):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def digest_files(paths):
    h=hashlib.sha256(); rows=[]
    for p in sorted(paths,key=lambda x:str(x)):
        rel=str(p.relative_to(ROOT)).replace('\\','/')
        d=sha256_file(p); rows.append({'path':rel,'sha256':d,'bytes':p.stat().st_size}); h.update(rel.encode()); h.update(b'\0'); h.update(d.encode()); h.update(b'\n')
    return h.hexdigest(),rows

def field(text,key):
    m=re.search(rf'^\s*{re.escape(key)}:\s*(.*?)\s*$',text,re.M); return m.group(1).strip().strip('"\'') if m else None

def build_package_manifest():
    files=[]
    for p in [WORKPLAN/'plan'/'IMPLEMENTATION_PLAN.md', WORKPLAN/'tasks'/'TASK_INDEX.md']:
        if p.is_file(): files.append(p)
    files += sorted((WORKPLAN/'compiled').glob('*.md'))
    files += sorted(p for p in (WORKPLAN/'tasks').glob('TASK_*.md') if p.name not in {'TASK_INDEX.md','TASK_TEMPLATE.md'})
    digest,rows=digest_files(files)
    return {'package_digest':digest,'task_count':sum(1 for p in files if p.parent.name=='tasks' and p.name.startswith('TASK_') and p.name not in {'TASK_INDEX.md','TASK_TEMPLATE.md'}),'files':rows}
