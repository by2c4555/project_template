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
PLACEHOLDERS = {'', 'CHANGE_ME', '<MODEL>', '<MODEL_ID>', '<MODEL_NAME>', '<PROVIDER>', '<VENDOR>', 'NONE', 'NULL'}


def pin(path, qualified_model_name):
    p = ROOT / path
    t = p.read_text(encoding='utf-8')
    safe_model = qualified_model_name.replace("'", "''")
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
            # Backward-compatible fallbacks for v4.1.1 config files:
            #   model -> vscode_model_name
            #   provider -> vendor
            values[section] = {
                'model_id': cp.get(section, 'model_id', fallback='').strip(),
                'vscode_model_name': cp.get(
                    section,
                    'vscode_model_name',
                    fallback=cp.get(section, 'model', fallback='')
                ).strip(),
                'vendor': cp.get(
                    section,
                    'vendor',
                    fallback=cp.get(section, 'provider', fallback='')
                ).strip(),
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


def is_placeholder(value):
    return value is None or str(value).strip().upper() in PLACEHOLDERS


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
        'In VS Code open: Chat: Manage Language Models',
        'Record the model ID, VS Code model name, vendor, and context size.',
        '',
        'Then run:',
        '  python scripts/configure_models.py',
        '',
        'Legacy --*-model / --*-provider flags are still accepted as aliases',
        'for VS Code model name / vendor, but model_id should be recorded in the INI.',
    ]
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(
        description='Configure v4.3.2 local model bindings from EXECUTE/MODEL_CONFIG.ini. CLI flags optionally override file values.'
    )
    ap.add_argument('--config', default=str(DEFAULT_CONFIG), help='Path to INI config (default: EXECUTE/MODEL_CONFIG.ini)')

    for key in ('manager', 'builder'):
        ap.add_argument(f'--{key}-model-id')
        ap.add_argument(f'--{key}-vscode-model-name')
        ap.add_argument(f'--{key}-vendor')
        ap.add_argument(f'--{key}-context', type=int)

        # v4.1.1 compatibility aliases. These do not represent API model IDs.
        ap.add_argument(f'--{key}-model', help=argparse.SUPPRESS)
        ap.add_argument(f'--{key}-provider', help=argparse.SUPPRESS)

    a = ap.parse_args()

    config_path = Path(a.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    cfg = read_ini(config_path)

    raw = {}
    for section in ('manager', 'builder'):
        legacy_model = getattr(a, f'{section}_model')
        legacy_provider = getattr(a, f'{section}_provider')
        cli_name = getattr(a, f'{section}_vscode_model_name')
        cli_vendor = getattr(a, f'{section}_vendor')

        raw[section] = {
            'model_id': choose(getattr(a, f'{section}_model_id'), cfg.get(section, {}).get('model_id')),
            'vscode_model_name': choose(cli_name if cli_name is not None else legacy_model, cfg.get(section, {}).get('vscode_model_name')),
            'vendor': choose(cli_vendor if cli_vendor is not None else legacy_provider, cfg.get(section, {}).get('vendor')),
            'context': choose(getattr(a, f'{section}_context'), cfg.get(section, {}).get('context')),
        }

    missing = []
    for section in ('manager', 'builder'):
        for field in ('model_id', 'vscode_model_name', 'vendor'):
            if is_placeholder(raw[section][field]):
                missing.append(f'[{section}] {field}')
        raw[section]['context'] = parse_context(raw[section]['context'], section)
        if raw[section]['context'] is None:
            missing.append(f'[{section}] context')

    if missing:
        raise SystemExit(incomplete_message(config_path, missing))

    vals = {
        'ProjectManager500K': raw['manager'],
        'Builder100K': raw['builder'],
    }

    bindings_path = ROOT / 'EXECUTE' / 'MODEL_BINDINGS.json'
    data = json.loads(bindings_path.read_text(encoding='utf-8'))
    data['schema_version'] = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    data['binding_schema_version'] = 4
    data['qualified_model_format'] = 'Model Name (vendor)'

    for role, value in vals.items():
        floor = ROLES[role][1]
        cap = value['context']
        if cap < floor:
            raise SystemExit(f'ERROR: {role} context {cap} < required minimum {floor}')

        name = value['vscode_model_name'].strip()
        vendor = value['vendor'].strip()
        model_id = value['model_id'].strip()
        qualified = f'{name} ({vendor})'

        data['roles'][role].update(
            model_id=model_id,
            vscode_model_name=name,
            vendor=vendor,
            model=qualified,
            documented_context_tokens=cap,
        )
        # Remove obsolete fields if present from v4.1.1 bindings.
        data['roles'][role].pop('base_model', None)
        data['roles'][role].pop('provider', None)

        pin(ROLES[role][0], qualified)

    bindings_path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print('v4.3.2 local model bindings configured.')
    for role in ('ProjectManager500K', 'Builder100K'):
        r = data['roles'][role]
        print(f'  {role}:')
        print(f'    VS Code model: {r["model"]}')
        print(f'    Model ID:      {r["model_id"]}')
        print(f'    Context:       {r["documented_context_tokens"]} tokens')
    print('  Updated: EXECUTE/MODEL_BINDINGS.json and VS Code agent model pins')


if __name__ == '__main__':
    main()
