#!/usr/bin/env python3
"""Bind provider-qualified VS Code custom-agent models to v4.0.1 roles.

The binding is intentionally explicit about provider/vendor so a model with the
same display name from GitHub Copilot and OpenRouter cannot be confused.

Example:
  python scripts/configure_models.py \\
    --planner-model "Claude Opus 4.7" --planner-provider openrouter --planner-context 1048576 \\
    --builder128-model "Qwen3 Coder Next" --builder128-provider openrouter --builder128-context 262144 \\
    --builder256-model "Qwen3 Coder Next" --builder256-provider openrouter --builder256-context 262144

This writes qualified model references such as:
  Claude Opus 4.7 (openrouter)
  Claude Opus 4.7 (copilot)

Use the vendor/provider identifier exposed by VS Code. Do not guess it from a
provider display label. This script never guesses model context capacity.
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
PROVIDER_RE=re.compile(r'^[A-Za-z0-9._-]+$')
QUALIFIED_RE=re.compile(r'^(?P<base>.+?)\s+\((?P<provider>[A-Za-z0-9._-]+)\)$')

def yaml_quote(s:str)->str:
    return "'" + s.replace("'", "''") + "'"

def normalize_binding(model:str, provider:str):
    model=model.strip(); provider=provider.strip().lower()
    if not model:
        raise ValueError('model name is empty')
    if not provider or not PROVIDER_RE.fullmatch(provider):
        raise ValueError(f'invalid provider/vendor identifier: {provider!r}')
    m=QUALIFIED_RE.fullmatch(model)
    if m:
        embedded=m.group('provider').lower()
        if embedded != provider:
            raise ValueError(f'model already names provider {embedded!r}, but --provider is {provider!r}')
        base=m.group('base').strip()
        qualified=f'{base} ({provider})'
    else:
        base=model
        qualified=f'{base} ({provider})'
    return base,provider,qualified

def bind_agent(rel:str, qualified_model:str):
    p=ROOT/rel; t=p.read_text(encoding='utf-8')
    if not t.startswith('---\n'):
        raise RuntimeError(f'{rel}: missing YAML frontmatter')
    if re.search(r'^model:\s*.*$',t,re.M):
        t=re.sub(r'^model:\s*.*$', 'model: '+yaml_quote(qualified_model), t, count=1, flags=re.M)
    elif re.search(r'^target:\s*.*$',t,re.M):
        t=re.sub(r'^(target:\s*.*)$', r'\1\nmodel: '+yaml_quote(qualified_model), t, count=1, flags=re.M)
    else:
        t=t.replace('---\n','---\nmodel: '+yaml_quote(qualified_model)+'\n',1)
    p.write_text(t,encoding='utf-8')

def main():
    ap=argparse.ArgumentParser(description='Bind exact model + provider/vendor to each v4.0.1 execution role.')
    ap.add_argument('--planner-model',required=True)
    ap.add_argument('--planner-provider',required=True)
    ap.add_argument('--planner-context',required=True,type=int)
    ap.add_argument('--builder128-model',required=True)
    ap.add_argument('--builder128-provider',required=True)
    ap.add_argument('--builder128-context',required=True,type=int)
    ap.add_argument('--builder256-model',required=True)
    ap.add_argument('--builder256-provider',required=True)
    ap.add_argument('--builder256-context',required=True,type=int)
    a=ap.parse_args()
    raw={
      'Planner512K':(a.planner_model,a.planner_provider,a.planner_context),
      'Builder128K':(a.builder128_model,a.builder128_provider,a.builder128_context),
      'Builder256K':(a.builder256_model,a.builder256_provider,a.builder256_context),
    }
    values={}; errors=[]; warnings=[]
    for role,(model,provider,cap) in raw.items():
        minimum=ROLES[role][1]
        try:
            base,vendor,qualified=normalize_binding(model,provider)
            values[role]=(base,vendor,qualified,cap)
        except ValueError as e:
            errors.append(f'{role}: {e}')
            continue
        if cap < minimum:
            errors.append(f'{role}: documented context {cap} < required {minimum}')
        if vendor == 'customendpoint':
            warnings.append(
                f'{role}: provider is customendpoint. If multiple same-name models share this vendor, '
                'current VS Code qualified-name routing may not distinguish their groups/IDs. '
                'Prefer a distinct vendor such as openrouter when available.'
            )
    if errors:
        for e in errors: print('FAIL:',e,file=sys.stderr)
        return 2
    data=json.loads(BIND.read_text(encoding='utf-8'))
    data['binding_schema_version']=2
    data['provider_qualified_models_required']=True
    data['qualified_model_format']='Model Name (vendor)'
    for role,(base,vendor,qualified,cap) in values.items():
        bind_agent(ROLES[role][0],qualified)
        r=data['roles'][role]
        r['base_model']=base
        r['provider']=vendor
        r['model']=qualified
        r['documented_context_tokens']=cap
    BIND.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    for w in warnings: print('WARN:',w)
    print('PASS: provider-qualified model bindings written and agent frontmatter pinned.')
    for role,(_,vendor,qualified,cap) in values.items():
        print(f'  {role}: {qualified} | provider={vendor} | context={cap}')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
