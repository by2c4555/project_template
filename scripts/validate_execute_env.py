#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / "EXECUTE" / ".env.execute"

FORBIDDEN_KEY_PARTS = (
    "PASSWORD", "PASSWD", "SECRET", "TOKEN", "API_KEY", "ACCESS_KEY",
    "PRIVATE_KEY", "CLIENT_SECRET", "AUTHORIZATION", "COOKIE", "SESSION",
    "CREDENTIAL",
)

PLACEHOLDERS = {"__REQUIRED__", "<REQUIRED>", "CHANGEME"}

def parse_env(path: Path):
    values = {}
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"line {n}: expected KEY=VALUE")
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values

def main():
    if not ENV.exists():
        print("RESULT: FAIL")
        print("Missing EXECUTE/.env.execute")
        return 1
    try:
        values = parse_env(ENV)
    except Exception as exc:
        print("RESULT: FAIL")
        print(exc)
        return 1
    errors = []
    for key, value in values.items():
        upper = key.upper()
        if any(part in upper for part in FORBIDDEN_KEY_PARTS):
            errors.append(f"{key}: forbidden secret-bearing key name")
        if value in PLACEHOLDERS:
            errors.append(f"{key}: placeholders are not allowed in .env.execute")
        if re.search(r"://[^/@:\s]+:[^/@\s]+@", value):
            errors.append(f"{key}: URL appears to contain embedded credentials")
    print("EXECUTE environment validation")
    if errors:
        for err in errors:
            print(f"- {err}")
        print("RESULT: FAIL")
        return 1
    print(f"Keys checked: {len(values)}")
    print("RESULT: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
