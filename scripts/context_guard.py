#!/usr/bin/env python3
"""Conservative Task context preflight for project template v4.0.1.

This tool estimates controlled Task payload without injecting file contents into the
model. It is deliberately simple and standard-library-only; it is not a tokenizer.
Exit codes: 0 PASS, 10 WARN, 20 SPLIT_REQUIRED, 30 CONTEXT_BLOCKED/ERROR.
"""
from __future__ import annotations
from pathlib import Path
import argparse, json, math, re, sys

ROOT = Path(__file__).resolve().parents[1]
PROFILES = {
    "Builder128K": {"target": 49152, "max": 65536, "tool_reserve": 6000, "runtime_floor": 131072},
    "Builder256K": {"target": 98304, "max": 131072, "tool_reserve": 12000, "runtime_floor": 262144},
}
PATH_RE = re.compile(r"`([^`]+)`")
BUILDER_RE = re.compile(r"^builder:\s*(Builder(?:128|256)K)\s*$", re.M)


def approx_tokens(chars: int) -> int:
    return math.ceil(chars / 4)


def extract_context_paths(text: str) -> list[str]:
    # Only scan the Context section, stopping before Context Budget/Verified Facts.
    m = re.search(r"## Context\s*(.*?)(?=\n## (?:Context Budget|Verified Facts|Required Change)|\Z)", text, re.S)
    if not m:
        return []
    out=[]
    for candidate in PATH_RE.findall(m.group(1)):
        c=candidate.strip()
        # Symbols/commands are ignored; only workspace paths that exist are counted.
        p=(ROOT/c).resolve()
        try:
            p.relative_to(ROOT.resolve())
        except ValueError:
            continue
        if p.is_file() and c not in out:
            out.append(c)
    return out


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('task', help='Task markdown file')
    ap.add_argument('--json', action='store_true')
    args=ap.parse_args()
    task=(ROOT/args.task).resolve() if not Path(args.task).is_absolute() else Path(args.task).resolve()
    try:
        task.relative_to(ROOT.resolve())
    except ValueError:
        print('CONTEXT_BLOCKED: task must be inside workspace', file=sys.stderr); return 30
    if not task.is_file():
        print(f'CONTEXT_BLOCKED: task not found: {task}', file=sys.stderr); return 30

    text=task.read_text(encoding='utf-8', errors='replace')
    bm=BUILDER_RE.search(text)
    if not bm or bm.group(1) not in PROFILES:
        print('CONTEXT_BLOCKED: valid builder profile missing', file=sys.stderr); return 30
    profile=bm.group(1); pol=PROFILES[profile]
    files=extract_context_paths(text)
    missing=[]; file_chars=0; details=[]
    for rel in files:
        p=ROOT/rel
        if not p.is_file():
            missing.append(rel); continue
        n=len(p.read_text(encoding='utf-8', errors='replace'))
        file_chars += n; details.append({'path': rel, 'chars': n, 'tokens_est': approx_tokens(n)})

    task_chars=len(text)
    controlled = approx_tokens(task_chars + file_chars) + pol['tool_reserve']
    if controlled <= pol['target']:
        decision='PASS'; code=0
    elif controlled <= pol['max']:
        decision='WARN'; code=10
    else:
        decision='SPLIT_REQUIRED'; code=20

    result={
        'task': str(task.relative_to(ROOT)), 'builder': profile,
        'runtime_floor_tokens': pol['runtime_floor'],
        'target_tokens': pol['target'], 'max_tokens': pol['max'],
        'tool_output_reserve_tokens': pol['tool_reserve'],
        'task_contract_tokens_est': approx_tokens(task_chars),
        'listed_file_tokens_est': approx_tokens(file_chars),
        'controlled_total_tokens_est': controlled,
        'files_counted': details, 'missing_listed_files': missing,
        'decision': decision,
        'note': 'Estimate uses 4 chars/token and excludes host/system/tool-schema overhead; role runtime floor still applies.'
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{decision}: {profile} controlled≈{controlled} tokens target={pol['target']} max={pol['max']} files={len(details)}")
        if missing:
            print('NOTE: listed paths not counted because they do not exist yet: ' + ', '.join(missing[:10]))
    return code

if __name__ == '__main__':
    raise SystemExit(main())
