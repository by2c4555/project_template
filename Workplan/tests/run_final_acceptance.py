#!/usr/bin/env python3
from __future__ import annotations
import contextlib, hashlib, io, json, os, runpy, shutil, subprocess, sys, tempfile, types
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2]


def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def run(root, *args, ok=(0,)):
    script = root / args[0]
    stdout, stderr = io.StringIO(), io.StringIO()
    old_argv, old_cwd, old_path = sys.argv[:], os.getcwd(), sys.path[:]
    sys.argv = list(args); os.chdir(root); sys.path.insert(0, str(script.parent))
    rc = 0
    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                runpy.run_path(str(script), run_name='__main__')
            except SystemExit as e:
                if isinstance(e.code, int): rc = e.code
                elif e.code in (None, ''): rc = 0
                else: rc = 1; print(e.code, file=sys.stderr)
    except BaseException as e:
        rc = 1; print(f'{type(e).__name__}: {e}', file=stderr)
    finally:
        sys.argv = old_argv; os.chdir(old_cwd); sys.path[:] = old_path
    r = types.SimpleNamespace(returncode=rc, stdout=stdout.getvalue(), stderr=stderr.getvalue())
    if rc not in ok:
        raise AssertionError(f'command failed {args}\nrc={rc}\nstdout={r.stdout}\nstderr={r.stderr}')
    return r


def cmd(root, command, surface='EXTERNAL_AI', tool='acceptance', model='strong', ok=(0,)):
    return json.loads(run(root, 'Workplan/scripts/command.py', command, '--surface', surface, '--tool', tool, '--model', model, ok=ok).stdout)


def evidence_for_last_work(root, rel, command, exit_code, artifact):
    st = json.loads((root / 'Workplan/control/STATE.json').read_text())
    wid = st['last_completed_work']
    meta = json.loads((root / 'Workplan/work' / wid / 'WORK.json').read_text())
    p = root / artifact
    obj = {
        'schema_version': 1,
        'attempt_id': meta['attempt_id'],
        'task_id': meta['task_id'],
        'phase_id': meta['phase_id'],
        'generation': meta['generation'],
        'ticket_digest': meta['ticket_digest'],
        'verification': [{'command': command, 'exit_code': exit_code}],
        'artifacts': [{'path': artifact, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}],
        'mutation_manifest_path': meta['mutation_manifest_path'],
        'status': 'PASS',
    }
    write(root / rel, json.dumps(obj, indent=2, sort_keys=True) + '\n')


def project_details():
    return '''artifact_kind: PROJECT_DETAILS
artifact_status: READY_FOR_PLANNING
research_protocol: EXTERNAL_RESEARCH_PROTOCOL_V1
product_scope_unknowns: 0
supporting_files: [Workplan/docs/raw/REQ.md]

# Project Details

## Objective
Provide a minimal standard-library integer calculator CLI with automated tests.

## Current State
No calculator production module exists in the isolated acceptance repository.

## Problem Statement
Users need deterministic add/subtract CLI behavior with invalid-operation failure behavior.

## Functional Requirements
- FR-001: `python -m src.calculator add 2 3` prints `5` and exits 0.
- FR-002: `python -m src.calculator sub 7 4` prints `3` and exits 0.
- FR-003: unsupported operations exit non-zero.

## Non-Functional Requirements
- NFR-001: Use only the Python standard library.
- NFR-002: Provide automated unit tests.

## Constraints
- Python standard library only.

## Interfaces
- CLI: `python -m src.calculator {add|sub} A B`.

## Acceptance Criteria
- AC-001: add behavior returns 5 for 2 + 3.
- AC-002: subtract behavior returns 3 for 7 - 4.
- AC-003: invalid operation exits non-zero.
- AC-004: automated unit tests pass.

## In Scope
- Calculator module, CLI, and unit tests.

## Out of Scope
- Multiplication, division, packaging, or external dependencies.

## Assumptions
- Python 3 is available.

## Resolved Unknowns
- Supported operations and integer input scope are fixed above.

## Remaining Non-Blocking Unknowns
- None.

## Source / Evidence Map
- USER_REQUIREMENT — calculator behavior and test requirement — Workplan/docs/raw/REQ.md
'''


def main():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / 'repo'
        shutil.copytree(SOURCE, root)

        write(root / 'Workplan/ingest/project_details.md', project_details())
        write(root / 'Workplan/ingest/docs/raw/REQ.md', '# Calculator Requirement\nAdd/subtract integer CLI, invalid-operation failure, and automated tests.\n')
        check = run(root, 'Workplan/scripts/tools/ingest.py', 'check')
        assert 'INGEST_VALID: PASS' in check.stdout
        run(root, 'Workplan/scripts/tools/scope.py', 'import')

        p = cmd(root, 'EXECUTE_PLANNING')
        run(root, 'Workplan/scripts/approve.py', '--', str(p['challenge']))
        p = cmd(root, 'EXECUTE_PLANNING')
        gen = p['generation']

        write(root / 'Workplan/compiled/PROJECT_BRIEF.md', '# Project Brief\nMinimal integer calculator CLI.\n')
        write(root / 'Workplan/compiled/ARCHITECTURE.md', '# Architecture\nOne production module plus unittest tests.\n')
        write(root / 'Workplan/compiled/INTERFACES.md', '# Interfaces\nCLI add/sub integer operands.\n')
        write(root / 'Workplan/plan/PHASES.json', json.dumps({'schema_version': 1, 'phases': [
            {'phase_id': 'PHASE_001', 'objective': 'Implement calculator CLI', 'depends_on': [], 'architecture_bindings': ['ARCHITECTURE.md'], 'interface_bindings': ['INTERFACES.md'], 'acceptance_criteria': ['Calculator CLI add/sub works'], 'verification': [], 'required_evidence': []},
            {'phase_id': 'PHASE_002', 'objective': 'Add automated acceptance tests', 'depends_on': ['PHASE_001'], 'architecture_bindings': ['ARCHITECTURE.md'], 'interface_bindings': ['INTERFACES.md'], 'acceptance_criteria': ['Unit tests pass'], 'verification': [], 'required_evidence': []},
        ]}, indent=2) + '\n')
        write(root / 'Workplan/tasks/TASK_001.md', '''# TASK_001
status: IMMUTABLE_AFTER_APPROVAL
phase_id: PHASE_001
objective: Implement calculator module and CLI
depends_on: []
authorized_paths: [src/calculator.py]
required_context: [Workplan/compiled/PROJECT_BRIEF.md, Workplan/compiled/ARCHITECTURE.md, Workplan/compiled/INTERFACES.md]
architecture_bindings: [ARCHITECTURE.md]
interface_bindings: [INTERFACES.md]
acceptance_criteria: [add and sub CLI behavior]
verification: [python -m src.calculator add 2 3]
required_evidence: [src/calculator.py]
max_repairs: 2
''')
        write(root / 'Workplan/tasks/TASK_002.md', '''# TASK_002
status: IMMUTABLE_AFTER_APPROVAL
phase_id: PHASE_002
objective: Add automated calculator tests
depends_on: [TASK_001]
authorized_paths: [tests/test_calculator.py]
required_context: [Workplan/compiled/PROJECT_BRIEF.md, Workplan/compiled/ARCHITECTURE.md, Workplan/compiled/INTERFACES.md]
architecture_bindings: [ARCHITECTURE.md]
interface_bindings: [INTERFACES.md]
acceptance_criteria: [unit tests cover add sub invalid operation]
verification: [python -m unittest discover -s tests -v]
required_evidence: [tests/test_calculator.py]
max_repairs: 2
''')
        write(root / 'Workplan/tasks/TASK_INDEX.md', '# Task Index\n\n- TASK_001 — PHASE_001\n- TASK_002 — PHASE_002 — depends on TASK_001\n')
        write(root / 'Workplan/plan/IMPLEMENTATION_PLAN.md', '# Implementation Plan\n\nstatus: READY\n\nTwo bounded phases: production module, then automated tests.\n')
        run(root, 'Workplan/scripts/tools/work.py', 'checkpoint', '--generation', str(gen), '--unit', 'TASKS', '--next-unit', 'DONE', '--note', 'Acceptance plan compiled')
        run(root, 'Workplan/scripts/tools/work.py', 'complete', '--generation', str(gen), '--note', 'Acceptance planning complete')
        run(root, 'Workplan/scripts/tools/planning.py', 'mark-ready')

        cmd(root, 'EXECUTE_IMPLEMENTATION', surface='VS_CODE', tool='vscode', model='manager')
        run(root, 'Workplan/scripts/tools/execution.py', 'start')
        run(root, 'Workplan/scripts/tools/execution.py', 'dispatch')
        write(root / 'src/calculator.py', '''from __future__ import annotations
import argparse


def add(a: int, b: int) -> int:
    return a + b


def sub(a: int, b: int) -> int:
    return a - b


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="calculator")
    parser.add_argument("operation", choices=("add", "sub"))
    parser.add_argument("a", type=int)
    parser.add_argument("b", type=int)
    args = parser.parse_args(argv)
    print(add(args.a, args.b) if args.operation == "add" else sub(args.a, args.b))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''')
        v1 = run(root, 'Workplan/scripts/tools/safe_exec.py', '--label', 'ACCEPT_TASK1', '--', sys.executable, '-m', 'src.calculator', 'add', '2', '3')
        assert '5' in v1.stdout
        st = json.loads((root / 'Workplan/control/STATE.json').read_text()); wid = st['active_work']; meta = json.loads((root / 'Workplan/work' / wid / 'WORK.json').read_text())
        run(root, 'Workplan/scripts/tools/work.py', 'complete', '--generation', str(meta['generation']), '--note', 'Calculator implementation complete')
        evidence_for_last_work(root, 'Workplan/work/ACCEPT_TASK1.json', 'python -m src.calculator add 2 3', 0, 'src/calculator.py')
        run(root, 'Workplan/scripts/tools/execution.py', 'complete', '--evidence', 'Workplan/work/ACCEPT_TASK1.json')
        run(root, 'Workplan/scripts/tools/execution.py', 'phase-gate')

        run(root, 'Workplan/scripts/tools/execution.py', 'dispatch')
        write(root / 'tests/test_calculator.py', '''import subprocess
import sys
import unittest
from src.calculator import add, sub


class CalculatorTests(unittest.TestCase):
    def test_add(self): self.assertEqual(add(2, 3), 5)
    def test_sub(self): self.assertEqual(sub(7, 4), 3)
    def test_cli_add(self):
        r = subprocess.run([sys.executable, "-m", "src.calculator", "add", "2", "3"], text=True, capture_output=True)
        self.assertEqual((r.returncode, r.stdout.strip()), (0, "5"))
    def test_invalid_operation_is_nonzero(self):
        r = subprocess.run([sys.executable, "-m", "src.calculator", "mul", "2", "3"], text=True, capture_output=True)
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__": unittest.main()
''')
        v2 = run(root, 'Workplan/scripts/tools/safe_exec.py', '--label', 'ACCEPT_TASK2', '--', sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v')
        assert 'ACCEPT_TASK2: exit=0' in v2.stdout + v2.stderr
        st = json.loads((root / 'Workplan/control/STATE.json').read_text()); wid = st['active_work']; meta = json.loads((root / 'Workplan/work' / wid / 'WORK.json').read_text())
        run(root, 'Workplan/scripts/tools/work.py', 'complete', '--generation', str(meta['generation']), '--note', 'Automated tests complete')
        evidence_for_last_work(root, 'Workplan/work/ACCEPT_TASK2.json', 'python -m unittest discover -s tests -v', 0, 'tests/test_calculator.py')
        run(root, 'Workplan/scripts/tools/execution.py', 'complete', '--evidence', 'Workplan/work/ACCEPT_TASK2.json')
        run(root, 'Workplan/scripts/tools/execution.py', 'phase-gate')
        n = json.loads(run(root, 'Workplan/scripts/tools/execution.py', 'next').stdout.splitlines()[-1])
        assert n['action'] == 'START_EVALUATION'
        run(root, 'Workplan/scripts/tools/execution.py', 'finalize')

        ev = cmd(root, 'EXECUTE_EVALUATION', tool='independent-evaluator', model='strong')
        # Independent final checks re-run the acceptance-critical behavior.
        env = dict(os.environ); env['PYTHONDONTWRITEBYTECODE'] = '1'
        add = subprocess.run([sys.executable, '-m', 'src.calculator', 'add', '2', '3'], cwd=root, text=True, capture_output=True, env=env, timeout=10)
        sub = subprocess.run([sys.executable, '-m', 'src.calculator', 'sub', '7', '4'], cwd=root, text=True, capture_output=True, env=env, timeout=10)
        bad = subprocess.run([sys.executable, '-m', 'src.calculator', 'mul', '2', '3'], cwd=root, text=True, capture_output=True, env=env, timeout=10)
        tests = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=root, text=True, capture_output=True, env=env, timeout=10)
        assert add.returncode == 0 and add.stdout.strip() == '5'
        assert sub.returncode == 0 and sub.stdout.strip() == '3'
        assert bad.returncode != 0
        assert tests.returncode == 0

        run(root, 'Workplan/scripts/tools/work.py', 'complete', '--generation', str(ev['generation']), '--note', 'Independent acceptance completed')
        st = json.loads((root / 'Workplan/control/STATE.json').read_text()); scope = st['cycles'][st['active_cycle']]['scope']
        report = f'''# Independent Evaluation — {st['active_cycle']}

## Decision
PASS

## Final Acceptance Matrix
| ID | Criterion | Independent check | Result |
|---|---|---|---|
| AC-001 | add 2 3 -> 5 | exit 0, stdout 5 | PASS |
| AC-002 | sub 7 4 -> 3 | exit 0, stdout 3 | PASS |
| AC-003 | invalid operation non-zero | non-zero exit | PASS |
| AC-004 | automated tests | unittest exit 0 | PASS |

## Verification executed
- add -> exit 0 -> 5
- sub -> exit 0 -> 3
- invalid operation -> non-zero
- unittest discovery -> exit 0
'''
        write(root / 'Workplan/evaluation/Evaluation_V1.md', report)
        completion = f'''# Project Completion Report

Cycle: {st['active_cycle']}
Scope revision: {scope['revision_label']}
Scope digest: {scope['digest']}
Final result: PASS

## Delivered scope
- Calculator CLI add/sub behavior and automated tests.

## Acceptance evidence
- AC-001..AC-004 independently rechecked.

## Verification summary
- All required final checks passed.

## Repairs / recoveries included
- none

## Non-blocking findings
- none

## Blocking issues
None.
'''
        write(root / 'Workplan/evaluation/PROJECT_COMPLETION_REPORT.md', completion)
        run(root, 'Workplan/scripts/tools/evaluation.py', 'finalize', '--result', 'PASS', '--report', 'Workplan/evaluation/Evaluation_V1.md', '--completion-report', 'Workplan/evaluation/PROJECT_COMPLETION_REPORT.md')

        st = json.loads((root / 'Workplan/control/STATE.json').read_text())
        assert st['lifecycle_stage'] == 'CLOSED_VALIDATED'
        assert st['project_state'] == 'CLOSED_VALIDATED'
        nxt = cmd(root, 'WORKPLAN_NEXT')
        assert nxt['continuation']['next_command'] == 'EXECUTE_RESEARCH'

    print('FINAL_ACCEPTANCE_VALID: PASS')


if __name__ == '__main__':
    main()
