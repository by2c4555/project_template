from __future__ import annotations
import json, re, shutil
from pathlib import Path
from .paths import ROOT, WORKPLAN, INGEST_DIR, INGEST_RECEIPT_DIR, ARCHIVE_DIR
from .integrity import field, inline_list, sha256_file, digest_rows
from .io import atomic_write_json
from .state import now

PROJECT_DETAILS_LOGICAL = 'Workplan/project_details.md'
RAW_PREFIX = 'Workplan/docs/raw/'
RESEARCH_PROTOCOL = 'EXTERNAL_RESEARCH_PROTOCOL_V1'
REQUIRED_PROJECT_DETAIL_SECTIONS = (
    'Objective',
    'Current State',
    'Problem Statement',
    'Functional Requirements',
    'Non-Functional Requirements',
    'Constraints',
    'Interfaces',
    'Acceptance Criteria',
    'In Scope',
    'Out of Scope',
    'Assumptions',
    'Resolved Unknowns',
    'Remaining Non-Blocking Unknowns',
    'Source / Evidence Map',
)


def _physical_for(logical: str, source_root: Path):
    if logical == PROJECT_DETAILS_LOGICAL:
        return source_root / 'project_details.md'
    if logical.startswith(RAW_PREFIX):
        return source_root / 'docs' / 'raw' / logical[len(RAW_PREFIX):]
    raise SystemExit(f'INGEST: BLOCKED\ninvalid logical path {logical}')


def _section_body(text: str, heading: str):
    m = re.search(
        rf'(?ms)^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)',
        text,
    )
    return m.group(1).strip() if m else None


def _validate_project_details_text(text: str, strict_research: bool):
    if field(text, 'artifact_kind') != 'PROJECT_DETAILS':
        raise SystemExit('INGEST: BLOCKED\nartifact_kind must be PROJECT_DETAILS')
    if field(text, 'artifact_status') != 'READY_FOR_PLANNING':
        raise SystemExit('INGEST: BLOCKED\nartifact_status must be READY_FOR_PLANNING')
    if field(text, 'product_scope_unknowns') != '0':
        raise SystemExit('INGEST: BLOCKED\nproduct_scope_unknowns must be 0')

    raw_supporting = field(text, 'supporting_files')
    if raw_supporting is None or not (raw_supporting.startswith('[') and raw_supporting.endswith(']')):
        raise SystemExit('INGEST: BLOCKED\nsupporting_files must be an inline list')

    if not strict_research:
        return

    if field(text, 'research_protocol') != RESEARCH_PROTOCOL:
        raise SystemExit(f'INGEST: BLOCKED\nresearch_protocol must be {RESEARCH_PROTOCOL}')

    missing = []
    empty = []
    for heading in REQUIRED_PROJECT_DETAIL_SECTIONS:
        body = _section_body(text, heading)
        if body is None:
            missing.append(heading)
        elif not body.strip():
            empty.append(heading)
    if missing:
        raise SystemExit('INGEST: BLOCKED\nmissing required sections: ' + ', '.join(missing))
    if empty:
        raise SystemExit('INGEST: BLOCKED\nempty required sections: ' + ', '.join(empty))


def validate(source_root: Path | None = None, write_receipt=True, allow_accepted=False, strict_research=True):
    # Resolve to canonical long path so relative_to(ROOT) succeeds on Windows
    # even when source_root originates from tempfile (which may use 8.3 short names).
    source_root = Path(source_root or INGEST_DIR).resolve()
    pd = source_root / 'project_details.md'
    if not pd.is_file():
        raise SystemExit('INGEST: BLOCKED\nmissing project_details.md')
    text = pd.read_text(encoding='utf-8')
    _validate_project_details_text(text, strict_research=strict_research)

    supporting = inline_list(text, 'supporting_files')
    if len(supporting) != len(set(supporting)):
        raise SystemExit('INGEST: BLOCKED\nduplicate supporting_files')
    logical = [PROJECT_DETAILS_LOGICAL] + supporting
    physical_rows = []
    logical_rows = []
    for rel in logical:
        if rel != PROJECT_DETAILS_LOGICAL and not rel.startswith(RAW_PREFIX):
            raise SystemExit(f'INGEST: BLOCKED\ninvalid supporting path {rel}')
        if '..' in Path(rel).parts:
            raise SystemExit(f'INGEST: BLOCKED\npath traversal {rel}')
        p = _physical_for(rel, source_root)
        if not p.is_file():
            raise SystemExit(f'INGEST: BLOCKED\nmissing declared file {rel}')
        d = sha256_file(p)
        logical_rows.append({'path': rel, 'sha256': d, 'bytes': p.stat().st_size})
        physical_rows.append({
            'path': str(p.relative_to(source_root)).replace('\\', '/'),
            'sha256': d,
            'bytes': p.stat().st_size,
        })
    package_digest = digest_rows(physical_rows)
    scope_digest = digest_rows(logical_rows)
    iid = 'INGEST_' + package_digest[:16]
    receipt = {
        'schema_version': 2 if strict_research else 1,
        'ingest_id': iid,
        'status': 'VALIDATED',
        'source_root': str(source_root.relative_to(ROOT)).replace('\\', '/'),
        'package_digest': package_digest,
        'scope_digest': scope_digest,
        'research_protocol': RESEARCH_PROTOCOL if strict_research else 'LEGACY_V530',
        'logical_files': logical_rows,
        'physical_files': physical_rows,
        'validated_at': now(),
    }
    rp = INGEST_RECEIPT_DIR / f'{iid}.json'
    if rp.is_file():
        old = json.loads(rp.read_text())
        if old.get('status') == 'ACCEPTED' and source_root.resolve() == INGEST_DIR.resolve() and not allow_accepted:
            raise SystemExit('INGEST: BLOCKED\nduplicate already accepted ingest')
    if write_receipt:
        atomic_write_json(rp, receipt)
    return receipt


def revalidate_bound(binding):
    source = ROOT / binding['source_root']
    # v5.3.1 preserves already-accepted v5.3.0 ingest authority by digest.
    # New handoffs must satisfy EXTERNAL_RESEARCH_PROTOCOL_V1.
    strict = binding.get('research_protocol') == RESEARCH_PROTOCOL or int(binding.get('schema_version', 1)) >= 2
    r = validate(source, write_receipt=False, allow_accepted=True, strict_research=strict)
    if r['package_digest'] != binding['package_digest'] or r['scope_digest'] != binding['scope_digest']:
        raise SystemExit('INGEST_BINDING: BLOCKED\nauthoritative ingest changed')
    return r


def archive_for_cycle(cycle_id, binding):
    source = ROOT / binding['source_root']
    dest = ARCHIVE_DIR / 'cycles' / cycle_id / 'ingest' / binding['ingest_id']
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, dest)
    test = dict(binding)
    test['source_root'] = str(dest.relative_to(ROOT)).replace('\\', '/')
    revalidate_bound(test)
    return test


def mark_accepted(binding):
    rp = INGEST_RECEIPT_DIR / f"{binding['ingest_id']}.json"
    rec = json.loads(rp.read_text()) if rp.is_file() else dict(binding)
    rec.update(binding)
    rec['status'] = 'ACCEPTED'
    rec['accepted_at'] = now()
    atomic_write_json(rp, rec)
    return rec


def normalize_active_ingest():
    if not INGEST_DIR.exists():
        return
    for p in sorted(INGEST_DIR.rglob('*'), reverse=True):
        if p.is_file() and p.name != '.gitkeep':
            p.unlink()
        elif p.is_dir() and p != INGEST_DIR:
            try:
                p.rmdir()
            except OSError:
                pass
    (INGEST_DIR / 'docs' / 'raw').mkdir(parents=True, exist_ok=True)
    (INGEST_DIR / '.gitkeep').touch(exist_ok=True)
    (INGEST_DIR / 'docs' / 'raw' / '.gitkeep').touch(exist_ok=True)
