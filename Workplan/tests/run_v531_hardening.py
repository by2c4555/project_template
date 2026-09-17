#!/usr/bin/env python3
from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2]


def write(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def expect_block(fn, marker: str):
    try:
        fn()
    except (SystemExit, ValueError) as e:
        assert marker in str(e), (marker, str(e))
        return
    raise AssertionError(f'expected block containing {marker!r}')


def valid_project_details():
    return '''artifact_kind: PROJECT_DETAILS
artifact_status: READY_FOR_PLANNING
research_protocol: EXTERNAL_RESEARCH_PROTOCOL_V1
product_scope_unknowns: 0
supporting_files: [Workplan/docs/raw/REQ.md]

# Project Details

## Objective
Deliver the requested demo behavior.

## Current State
The demo behavior is not implemented yet.

## Problem Statement
A bounded implementation is required.

## Functional Requirements
- FR-001: Implement the demo behavior.

## Non-Functional Requirements
- NFR-001: Preserve deterministic authority.

## Constraints
- Use only declared interfaces and paths.

## Interfaces
- CLI/repository interface described by the requirement.

## Acceptance Criteria
- AC-001: The declared behavior is independently observable.

## In Scope
- Demo behavior.

## Out of Scope
- Unrelated refactors.

## Assumptions
- None.

## Resolved Unknowns
- Target behavior is fixed by REQ.md.

## Remaining Non-Blocking Unknowns
- None.

## Source / Evidence Map
- USER_REQUIREMENT — demo behavior — Workplan/docs/raw/REQ.md
'''


def frontmatter(text: str):
    assert text.startswith('---\n')
    end = text.index('\n---\n', 4)
    return text[4:end]


def main():
    # Workspace agent policy is a cost/capability boundary, not prompt-only advice.
    manager = (SOURCE / '.github/agents/manager.agent.md').read_text(encoding='utf-8')
    builder = (SOURCE / '.github/agents/builder.agent.md').read_text(encoding='utf-8')
    mf = frontmatter(manager)
    bf = frontmatter(builder)
    assert 'model:' not in mf, 'ExecutionManager must inherit the user-selected chat model'
    assert "tools: ['read','search','execute','agent']" in mf
    assert "agents: ['Builder']" in mf
    assert "'edit'" not in mf
    assert "model: 'Project Builder Local'" in bf
    assert "user-invocable: false" in bf
    assert "agents: []" in bf
    assert not (SOURCE / '.github/agents/builder100k.agent.md').exists()
    assert (SOURCE / 'Workplan/external_agent/RESEARCH_INSTRUCTION.md').is_file()
    assert (SOURCE / 'Workplan/external_agent/RESEARCH_POTOCAL_PROMPT.md').is_file()
    assert not (SOURCE / 'Workplan/external_agent/RESEARCH_PROMPT.md').exists()
    assert not (SOURCE / 'Workplan/external_agent/EXTERNAL_RESEARCH_PROTOCOL.md').exists()

    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / 'repo'
        shutil.copytree(SOURCE, root)
        sys.path.insert(0, str(root / 'Workplan/scripts'))
        from _core.ingest import validate, revalidate_bound, RESEARCH_PROTOCOL

        ingest = root / 'Workplan/ingest'
        for p in sorted(ingest.rglob('*'), reverse=True):
            if p.is_file() and p.name != '.gitkeep':
                p.unlink()
        write(ingest / 'project_details.md', valid_project_details())
        write(ingest / 'docs/raw/REQ.md', '# Requirement\nBuild demo.\n')

        receipt = validate(ingest, write_receipt=False)
        assert receipt['schema_version'] == 2
        assert receipt['research_protocol'] == RESEARCH_PROTOCOL

        # New handoffs fail closed when the protocol marker or canonical sections are missing.
        good = (ingest / 'project_details.md').read_text(encoding='utf-8')
        write(ingest / 'project_details.md', good.replace('research_protocol: EXTERNAL_RESEARCH_PROTOCOL_V1\n', ''))
        expect_block(lambda: validate(ingest, write_receipt=False), 'research_protocol must be')
        write(ingest / 'project_details.md', good.replace('## Acceptance Criteria\n- AC-001: The declared behavior is independently observable.\n\n', ''))
        expect_block(lambda: validate(ingest, write_receipt=False), 'missing required sections: Acceptance Criteria')
        write(ingest / 'project_details.md', good.replace('supporting_files: [Workplan/docs/raw/REQ.md]', 'supporting_files: Workplan/docs/raw/REQ.md'))
        expect_block(lambda: validate(ingest, write_receipt=False), 'supporting_files must be an inline list')

        # Already-accepted v5.3.0-style ingest remains digest-revalidatable after the patch.
        legacy = '''artifact_kind: PROJECT_DETAILS\nartifact_status: READY_FOR_PLANNING\nproduct_scope_unknowns: 0\nsupporting_files: [Workplan/docs/raw/REQ.md]\n'''
        write(ingest / 'project_details.md', legacy)
        binding = validate(ingest, write_receipt=False, strict_research=False)
        binding['source_root'] = 'Workplan/ingest'
        rebound = revalidate_bound(binding)
        assert rebound['package_digest'] == binding['package_digest']
        assert rebound['scope_digest'] == binding['scope_digest']

        # Deterministic 5.3.0 -> 5.3.1 state migration succeeds only at a safe boundary.
        sp = root / 'Workplan/control/STATE.json'
        st = json.loads(sp.read_text(encoding='utf-8'))
        st['workflow_version'] = '5.3.0'
        st['active_work'] = None
        st['pending_approval'] = None
        sp.write_text(json.dumps(st, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        env = dict(os.environ)
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        r = subprocess.run([sys.executable, str(root / 'Workplan/scripts/migrate_v530_to_v531.py')], cwd=root, text=True, capture_output=True, env=env, timeout=10)
        assert r.returncode == 0, r.stdout + r.stderr
        migrated = json.loads(sp.read_text(encoding='utf-8'))
        assert migrated['workflow_version'] == '5.3.1' and migrated['schema_version'] == 6

        migrated['workflow_version'] = '5.3.0'
        migrated['active_work'] = 'WORK_9999'
        sp.write_text(json.dumps(migrated, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        r = subprocess.run([sys.executable, str(root / 'Workplan/scripts/migrate_v530_to_v531.py')], cwd=root, text=True, capture_output=True, env=env, timeout=10)
        assert r.returncode != 0 and 'active_work must be null' in (r.stdout + r.stderr)

    print('V531_HARDENING_VALID: PASS')


if __name__ == '__main__':
    main()
