#!/usr/bin/env python3
"""Check constitution navigation and consistency, not runtime conformance."""
from pathlib import Path
import re
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
HEADER = '> PROJECT TEMPLATE DEVELOPMENT CONSTITUTION 1.2 — Human owned. AI may read and apply this guidance; modification requires explicit authorization from a trusted repository-owner channel covering the change.'
DOCUMENTS = {
    'README.md', 'OBJECTIVE.md', 'REFERENCE_ARCHITECTURE.md',
    'DEVELOPMENT_PROMPT.md', 'CONFORMANCE.md', 'PLANNING_MODEL.md',
    'RESEARCH_AND_SCOPE_MODEL.md',
    *('architecture/' + name + '.md' for name in (
        'AGENT_ADAPTER_BOUNDARIES', 'AUTHORITY_MODEL', 'CONTEXT_AND_COST_MODEL',
        'DIAGNOSIS_AND_RECOVERY', 'EVALUATION_CLOSURE_AND_NEXT_VERSION',
        'EXECUTION_MODEL', 'FAILURE_AND_REPAIR_MODEL', 'REPORTING_AND_HUMAN_REVIEW',
        'RESEARCH_REVISION_AND_CARRY_FORWARD', 'RUNTIME_LIFECYCLE_AND_TRANSITIONS',
        'STATE_BINDING_AND_RESUME', 'TASK_AND_PHASE_GATES',
        'TRUST_AND_INPUT_BOUNDARIES', 'USER_APPROVAL_AND_COST_CONTROL',
    )),
}
LINK = re.compile(r'(?<!!)\[[^\]\n]+\]\(([^\s)]+)\)')


def link_errors(path, text, root):
    errors = []
    for target in LINK.findall(text):
        parsed = urlsplit(target)
        if parsed.scheme in {'https', 'http', 'mailto'}:
            continue
        if parsed.scheme or target.startswith(('/', '\\')):
            errors.append(f'{path.name}: non-portable link: {target}')
            continue
        destination = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        if not destination.is_relative_to(root.resolve()) or not destination.is_file():
            errors.append(f'{path.name}: missing or out-of-repository link: {target}')
    return errors


def check_documents(root=ROOT):
    directory = root / 'Workplan/development_constitution'
    errors = []
    actual = {p.relative_to(directory).as_posix() for p in directory.rglob('*.md')}
    if missing := DOCUMENTS - actual:
        errors.append('missing constitutional owners: ' + ', '.join(sorted(missing)))
    readme_path = directory / 'README.md'
    readme = readme_path.read_text(encoding='utf-8') if readme_path.is_file() else ''
    indexed = set(LINK.findall(readme))
    # Constitution v1.2: architecture docs are catalogued in REFERENCE_ARCHITECTURE.md
    # (concern-ownership table) rather than linked directly from README. Accept either.
    refarch_path = directory / 'REFERENCE_ARCHITECTURE.md'
    refarch = refarch_path.read_text(encoding='utf-8') if refarch_path.is_file() else ''
    all_indexed = indexed | set(LINK.findall(refarch))
    # Entry-point organizer docs are exempt: requiring them to self-appear is circular.
    ENTRY_DOCS = {'README.md', 'REFERENCE_ARCHITECTURE.md', 'GOVERNANCE_AND_TERMINOLOGY.md'}
    for name in sorted(actual):
        path = directory / name
        text = path.read_text(encoding='utf-8')
        lines = text.splitlines()
        if not lines or lines[0] != HEADER:
            errors.append(f'{name}: missing owner-authorization notice')
        if not re.search(r'^# .+', text, re.M):
            errors.append(f'{name}: missing document title')
        if len(re.findall(r'^```', text, re.M)) % 2:
            errors.append(f'{name}: unclosed fenced block')
        if name not in ENTRY_DOCS and name not in all_indexed:
            errors.append(f'{name}: absent from entry-point reading map')
        errors.extend(link_errors(path, text, root))
    for name, prefix in [('CONFORMANCE.md', 'C'), ('architecture/RUNTIME_LIFECYCLE_AND_TRANSITIONS.md', 'L')]:
        path = directory / name
        if not path.is_file():
            continue
        text = path.read_text(encoding='utf-8')
        ids = re.findall(r'^\| `?(' + prefix + r'-\d{3})`? \|', text, re.M)
        if not ids or len(ids) != len(set(ids)):
            errors.append(f'{name}: missing or duplicate canonical IDs')
    entry = root / 'AGENTS.md'
    if not entry.is_file():
        errors.append('missing agent entry point: AGENTS.md')
    else:
        text = entry.read_text(encoding='utf-8')
        errors.extend(link_errors(entry, text, root))
        if 'Workplan/development_constitution/README.md' not in LINK.findall(text):
            errors.append('AGENTS.md does not link to the constitution entry point')
    if (root / 'Workplan/Objective_dev.md').exists():
        errors.append('obsolete Objective_dev.md must not remain')
    return errors


def main():
    # Verify that link validation rejects broken and escaping references.
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        page = root / 'page.md'
        page.write_text('# Page\n', encoding='utf-8')
        assert not link_errors(page, '[valid](page.md)', root)
        assert link_errors(page, '[missing](missing.md)', root)
        assert link_errors(page, '[escape](../outside.md)', root)
        assert link_errors(page, '[absolute](/page.md)', root)
    problems = check_documents()
    if problems:
        raise SystemExit('CONSTITUTION_HARDENING_VALID: FAIL\n' + '\n'.join(problems))
    print('CONSTITUTION_HARDENING_VALID: PASS (documents only; runtime conformance not assessed)')


if __name__ == '__main__':
    main()
