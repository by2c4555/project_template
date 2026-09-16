#!/usr/bin/env python3
from pathlib import Path
import argparse
import configparser
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / 'EXECUTE' / 'MODEL_CONFIG.ini'
ROLES = {
    'ProjectManager500K': ('.github/agents/project-manager.agent.md', 512000),
    'Builder100K': ('.github/agents/builder100k.agent.md', 102400),
}
PLACEHOLDERS = {'', 'CHANGE_ME', '<MODEL>', '<PROVIDER>', 'NONE', 'NULL'}


def pin(path, model):
    p = ROOT / path
    t = p.read_text(encoding='utf-8')
    safe_model = model.replace("'", "''")
    if re.search(r'^model:', t, re.M):
        t = re.sub(r'^model:.*$', f"model: '{safe_model}'", t, count=1, flags=re.M)
    else:
        t = t.replace('target: vscode\n', f"target: vscode\nmodel: '{safe_model}'\n", 1)
    p.write_text(t, encoding='utf-8')


def read_ini(path):
    if not path.exists():
        return {}
    cp = configparser.ConfigParser(interpolation=None)
    try:
        with path.open('r', encoding='utf-8') as f:
            cp.read_file(f)
    except configparser.Error as e:
        raise SystemExit(f'ERROR: cannot parse {path}: {e}')

    values = {}
    for section in ('manager', 'builder'):
        if cp.has_section(section):
            values[section] = {
                'model': cp.get(section, 'model', fallback='').strip(),
                'provider': cp.get(section, 'provider', fallback='').strip(),
                'context': cp.get(section, 'context', fallback='').strip(),
            }
    return values


def choose(cli_value, config_value):
    return cli_value if cli_value is not None else config_value


def parse_context(value, label):
    if value is None or str(value).strip() == '':
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        raise SystemExit(f'ERROR: {label} context must be an integer, got: {value!r}')


def incomplete_message(config_path, missing):
    lines = [
        'ERROR: Model configuration is incomplete.',
        '',
        f'Edit: {config_path}',
        '',
        'Missing or placeholder fields:',
    ]
    lines.extend(f'  - {item}' for item in missing)
    lines += [
        '',
        'Then run:',
        '  python scripts/configure_models.py',
        '',
        'CLI flags are still supported as optional overrides.',
    ]
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(
        description='Configure v4.1.1 local model bindings from EXECUTE/MODEL_CONFIG.ini. CLI flags optionally override file values.'
    )
    ap.add_argument('--config', default=str(DEFAULT_CONFIG), help='Path to INI config (default: EXECUTE/MODEL_CONFIG.ini)')
    for key in ('manager', 'builder'):
        ap.add_argument(f'--{key}-model')
        ap.add_argument(f'--{key}-provider')
        ap.add_argument(f'--{key}-context', type=int)
    a = ap.parse_args()

    config_path = Path(a.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    cfg = read_ini(config_path)

    raw = {
        'manager': {
            'model': choose(a.manager_model, cfg.get('manager', {}).get('model')),
            'provider': choose(a.manager_provider, cfg.get('manager', {}).get('provider')),
            'context': choose(a.manager_context, cfg.get('manager', {}).get('context')),
        },
        'builder': {
            'model': choose(a.builder_model, cfg.get('builder', {}).get('model')),
            'provider': choose(a.builder_provider, cfg.get('builder', {}).get('provider')),
            'context': choose(a.builder_context, cfg.get('builder', {}).get('context')),
        },
    }

    missing = []
    for section in ('manager', 'builder'):
        for field in ('model', 'provider'):
            value = raw[section][field]
            if value is None or str(value).strip().upper() in PLACEHOLDERS:
                missing.append(f'[{section}] {field}')
        raw[section]['context'] = parse_context(raw[section]['context'], section)
        if raw[section]['context'] is None:
            missing.append(f'[{section}] context')

    if missing:
        raise SystemExit(incomplete_message(config_path, missing))

    vals = {
        'ProjectManager500K': (raw['manager']['model'].strip(), raw['manager']['provider'].strip(), raw['manager']['context']),
        'Builder100K': (raw['builder']['model'].strip(), raw['builder']['provider'].strip(), raw['builder']['context']),
    }

    bindings_path = ROOT / 'EXECUTE' / 'MODEL_BINDINGS.json'
    data = json.loads(bindings_path.read_text(encoding='utf-8'))
    data['schema_version'] = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()

    for role, (base, prov, cap) in vals.items():
        floor = ROLES[role][1]
        if cap < floor:
            raise SystemExit(f'ERROR: {role} context {cap} < required minimum {floor}')
        qual = f'{base} ({prov})'
        data['roles'][role].update(
            base_model=base,
            provider=prov,
            model=qual,
            documented_context_tokens=cap,
        )
        pin(ROLES[role][0], qual)

    bindings_path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print('v4.1.1 local model bindings configured.')
    print(f'  Manager: {data["roles"]["ProjectManager500K"]["model"]} / {data["roles"]["ProjectManager500K"]["documented_context_tokens"]} tokens')
    print(f'  Builder: {data["roles"]["Builder100K"]["model"]} / {data["roles"]["Builder100K"]["documented_context_tokens"]} tokens')
    print('  Updated: EXECUTE/MODEL_BINDINGS.json and VS Code agent model pins')


if __name__ == '__main__':
    main()
