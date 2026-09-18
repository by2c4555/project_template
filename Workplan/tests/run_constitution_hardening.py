#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / 'Workplan/development_constitution'
WARNING = '> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.'
FILES = ['README.md','OBJECTIVE.md','REFERENCE_ARCHITECTURE.md','DEVELOPMENT_PROMPT.md']


def main():
    assert D.is_dir()
    assert not (ROOT / 'Workplan/Objective_dev.md').exists(), 'obsolete Objective_dev.md must not remain'
    for name in FILES:
        p = D / name
        assert p.is_file(), name
        lines = p.read_text(encoding='utf-8').splitlines()
        assert lines and lines[0] == WARNING, f'first-line constitution warning mismatch: {name}'

    readme = (D / 'README.md').read_text(encoding='utf-8')
    objective = (D / 'OBJECTIVE.md').read_text(encoding='utf-8')
    architecture = (D / 'REFERENCE_ARCHITECTURE.md').read_text(encoding='utf-8')
    prompt = (D / 'DEVELOPMENT_PROMPT.md').read_text(encoding='utf-8')

    assert 'HUMAN OWNED' in readme and 'AI NON-MUTABLE' in readme
    assert 'AI-assisted software-development control plane' in objective
    assert 'Cycle -> Phase -> Task -> Attempt' in objective
    assert 'hard maximum is **5 local Repair Attempts' in objective
    assert 'VS CODE COPILOT AGENT ONLY' in architecture
    assert 'Manager Diagnosis #5' in architecture and 'Builder REPAIR #5' in architecture
    assert 'CONSTITUTION_CHANGE_REQUIRED' in prompt
    assert 'must not edit' in prompt.lower() and 'repository owner' in prompt.lower()

    # Current operational documentation must reference the package, not the obsolete monolithic file.
    operational = [
        ROOT / 'Workplan/README.md', ROOT / 'Workplan/CHATGPT_PROJECT_INSTRUCTIONS.md',
        *(ROOT / 'Workplan/external_agent').glob('*.md'),
    ]
    for p in operational:
        if p.is_file():
            assert 'Workplan/Objective_dev.md' not in p.read_text(encoding='utf-8'), p

    print('CONSTITUTION_HARDENING_VALID: PASS')


if __name__ == '__main__':
    main()
