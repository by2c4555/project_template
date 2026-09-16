#!/usr/bin/env python3
from pathlib import Path
import argparse, json, re
ROOT=Path(__file__).resolve().parents[1]
ROLES={
 'ProjectManager500K':('.github/agents/project-manager.agent.md',512000),
 'Builder100K':('.github/agents/builder100k.agent.md',102400),
}
def pin(path, model):
 p=ROOT/path; t=p.read_text(encoding='utf-8')
 if re.search(r'^model:',t,re.M): t=re.sub(r'^model:.*$',f"model: '{model}'",t,count=1,flags=re.M)
 else: t=t.replace('target: vscode\n',f"target: vscode\nmodel: '{model}'\n",1)
 p.write_text(t,encoding='utf-8')
def main():
 ap=argparse.ArgumentParser()
 for key in ('manager','builder'):
  ap.add_argument(f'--{key}-model',required=True); ap.add_argument(f'--{key}-provider',required=True); ap.add_argument(f'--{key}-context',required=True,type=int)
 a=ap.parse_args(); vals={
 'ProjectManager500K':(a.manager_model,a.manager_provider,a.manager_context),
 'Builder100K':(a.builder_model,a.builder_provider,a.builder_context)}
 data=json.loads((ROOT/'EXECUTE/MODEL_BINDINGS.json').read_text())
 for role,(base,prov,cap) in vals.items():
  floor=ROLES[role][1]
  if cap<floor: raise SystemExit(f'{role}: {cap} < required {floor}')
  qual=f'{base} ({prov})'
  data['roles'][role].update(base_model=base,provider=prov,model=qual,documented_context_tokens=cap)
  pin(ROLES[role][0],qual)
 (ROOT/'EXECUTE/MODEL_BINDINGS.json').write_text(json.dumps(data,indent=2)+'\n')
 print('v4.1 local model bindings configured.')
if __name__=='__main__': main()
