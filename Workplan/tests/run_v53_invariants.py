#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, sys, tempfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2]

def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding='utf-8')

def expect_block(fn, marker):
    try: fn()
    except (SystemExit, ValueError) as e:
        assert marker in str(e), (marker, str(e)); return
    raise AssertionError(f'expected block containing {marker!r}')

def main():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / 'repo'; shutil.copytree(SOURCE, root)
        sys.path.insert(0, str(root / 'Workplan/scripts'))
        from _core.contracts import load_contract_package
        from _core.mutation import snapshot_production, diff_snapshots, validate_mutations
        from _core.state import load_state, save_state
        from _core.integrity import write_release_manifest, validate_release_manifest
        from _core import work as W

        # Contract defaults + implicit phase.
        task = root/'Workplan/tasks/TASK_001.md'
        write(task, '# TASK_001\nobjective: Demo\ndepends_on: []\nauthorized_paths: [src/a.txt]\nrequired_context: []\narchitecture_bindings: []\ninterface_bindings: []\nacceptance_criteria: [done]\nverification: []\nrequired_evidence: []\n')
        phasep = root/'Workplan/plan/PHASES.json'
        if phasep.exists(): phasep.unlink()
        pkg = load_contract_package(validate=True)
        assert list(pkg['phases']) == ['PHASE_001'] and pkg['tasks']['TASK_001']['max_repairs'] == 2

        # Explicit multi-phase plans require explicit task phase_id.
        write(phasep, json.dumps({'phases':[{'phase_id':'PHASE_A','objective':'A','depends_on':[],'architecture_bindings':[],'interface_bindings':[],'acceptance_criteria':[],'verification':[],'required_evidence':[]}]}))
        expect_block(lambda: load_contract_package(validate=True), 'phase_id is required')
        text = task.read_text().replace('objective: Demo', 'phase_id: PHASE_A\nobjective: Demo')
        task.write_text(text)
        pkg = load_contract_package(validate=True); assert pkg['tasks']['TASK_001']['phase_id'] == 'PHASE_A'
        task.write_text(text + 'max_repairs: 6\n'); expect_block(lambda: load_contract_package(validate=True), 'max_repairs must be 0..5')
        task.write_text(text + 'max_repairs: 0\n'); assert load_contract_package(validate=True)['tasks']['TASK_001']['max_repairs'] == 0

        # Graph cycle rejected.
        write(phasep, json.dumps({'phases':[
            {'phase_id':'PHASE_A','objective':'A','depends_on':['PHASE_B'],'architecture_bindings':[],'interface_bindings':[],'acceptance_criteria':[],'verification':[],'required_evidence':[]},
            {'phase_id':'PHASE_B','objective':'B','depends_on':['PHASE_A'],'architecture_bindings':[],'interface_bindings':[],'acceptance_criteria':[],'verification':[],'required_evidence':[]}
        ]}))
        expect_block(lambda: load_contract_package(validate=True), 'dependency cycle')

        # Mutation accounting sees create/modify/delete across the full production tree.
        phasep.unlink(); task.write_text(text.replace('phase_id: PHASE_A\n',''))
        write(root/'src/existing.txt', 'before\n'); write(root/'src/delete.txt', 'remove\n')
        before = snapshot_production(); write(root/'src/existing.txt','after\n'); write(root/'rogue.txt','x\n'); (root/'src/delete.txt').unlink(); after = snapshot_production()
        muts = diff_snapshots(before, after); kinds = {m['path']:m['kind'] for m in muts}
        assert kinds['src/existing.txt']=='MODIFY' and kinds['rogue.txt']=='CREATE' and kinds['src/delete.txt']=='DELETE'
        auth = validate_mutations(muts, ['src/']); assert auth['status']=='FAIL' and [x['path'] for x in auth['unauthorized']] == ['rogue.txt']
        assert validate_mutations(muts, ['src/','rogue.txt'])['status']=='PASS'

        # Stale state object is fenced.
        a = load_state(); b = load_state(); save_state(a, event='TEST_A'); expect_block(lambda: save_state(b, event='TEST_B'), 'stale state object')

        # Reasoning-only Work cannot complete after production mutation.
        st = load_state(); st['lifecycle_stage']='DIAGNOSIS'; st['project_state']='DIAGNOSIS'; save_state(st, event='TEST_DIAG_STAGE')
        _, meta, _ = W.acquire('DIAGNOSIS','test','strong'); write(root/'src/diag_illegal.txt','x\n')
        expect_block(lambda: W.complete('illegal', meta['generation']), 'REASONING_ONLY_MUTATION')
        (root/'src/diag_illegal.txt').unlink()
        # Complete cleanly so Recovery can start as a distinct Work.
        W.complete('diagnosis clean', meta['generation'])
        st=load_state(); st['lifecycle_stage']='RECOVERY'; st['project_state']='RECOVERY'; save_state(st,event='TEST_REC_STAGE')
        _, rmeta, _=W.acquire('RECOVERY','test','strong'); write(root/'src/recovery_illegal.txt','x\n')
        expect_block(lambda: W.complete('illegal', rmeta['generation']), 'REASONING_ONLY_MUTATION')
        (root/'src/recovery_illegal.txt').unlink(); W.complete('recovery clean', rmeta['generation'])

        # Release manifest excludes caches and detects a stale tracked file.
        cache = root/'Workplan/scripts/__pycache__/junk.pyc'; write(cache, 'junk')
        write_release_manifest(); ok, problems = validate_release_manifest(); assert ok, problems
        assert '__pycache__' not in (root/'Workplan/FILE_SHA256SUMS.txt').read_text()
        readme = root/'README.md'; readme.write_text(readme.read_text()+'\nSTALE_TEST\n')
        ok, problems = validate_release_manifest(); assert not ok and any('README.md' in x and 'digest mismatch' in x for x in problems)

    print('V53_INVARIANTS_VALID: PASS')

if __name__ == '__main__': main()
