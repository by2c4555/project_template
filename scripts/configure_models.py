#!/usr/bin/env python3
"""Bind provider-specific VS Code custom-agent model names to v4.0.1 roles.

Example:
  python scripts/configure_models.py \
    --planner-model "<model id>" --planner-context 524288 \
    --builder128-model "<model id>" --builder128-context 131072 \
    --builder256-model "<model id>" --builder256-context 262144

The supplied capacities must come from provider/host documentation or another
trusted runtime source. This script does not guess model context sizes.
"""
from pathlib import Path
import argparse, json, re, sys

ROOT=Path(__file__).resolve().parents[1]
BIND=ROOT/'EXECUTE/MODEL_BINDINGS.json'
ROLES={
 'Planner512K': ('.github/agents/planner512k.agent.md',524288),
 'Builder128K': ('.github/agents/builder128k.agent.md',131072),
 'Builder256K': ('.github/agents/builder256k.agent.md',262144),
}

def yaml_quote(s:str)->str:
    return "'" + s.replace("'", "''") + "'"

def bind_agent(rel:str, model:str):
    p=ROOT/rel; t=p.read_text(encoding='utf-8')
    if not t.startswith('---\n'):
        raise RuntimeError(f'{rel}: missing YAML frontmatter')
    # Replace existing model field or insert after target.
    if re.search(r'^model:\s*.*$',t,re.M):
        t=re.sub(r'^model:\s*.*$', 'model: '+yaml_quote(model), t, count=1, flags=re.M)
    elif re.search(r'^target:\s*.*$',t,re.M):
        t=re.sub(r'^(target:\s*.*)$', r'\1\nmodel: '+yaml_quote(model), t, count=1, flags=re.M)
    else:
        t=t.replace('---\n','---\nmodel: '+yaml_quote(model)+'\n',1)
    p.write_text(t,encoding='utf-8')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--planner-model',required=True); ap.add_argument('--planner-context',required=True,type=int)
    ap.add_argument('--builder128-model',required=True); ap.add_argument('--builder128-context',required=True,type=int)
    ap.add_argument('--builder256-model',required=True); ap.add_argument('--builder256-context',required=True,type=int)
    a=ap.parse_args()
    values={
      'Planner512K':(a.planner_model,a.planner_context),
      'Builder128K':(a.builder128_model,a.builder128_context),
      'Builder256K':(a.builder256_model,a.builder256_context),
    }
    errors=[]
    for role,(model,cap) in values.items():
        minimum=ROLES[role][1]
        if not model.strip(): errors.append(f'{role}: model name is empty')
        if cap < minimum: errors.append(f'{role}: {cap} < required {minimum}')
    if errors:
        for e in errors: print('FAIL:',e,file=sys.stderr)
        return 2
    data=json.loads(BIND.read_text(encoding='utf-8'))
    for role,(model,cap) in values.items():
        bind_agent(ROLES[role][0],model.strip())
        data['roles'][role]['model']=model.strip()
        data['roles'][role]['documented_context_tokens']=cap
    BIND.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('PASS: model bindings written and agent frontmatter pinned.')
    return 0
if __name__=='__main__': raise SystemExit(main())
