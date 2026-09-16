#!/usr/bin/env python3
"""
Lightweight deterministic validator for the v4 template.

Checks:
- required files exist;
- low-context Builder agent names are absent;
- .env.user is ignored;
- EXECUTE/.env.execute does not obviously contain secret-bearing variable names;
- hard context floors are present in PROJECT_CONFIG.md.

This validator intentionally uses only the Python standard library.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "VERSION",
    ".gitignore",
    "EXECUTE_PROJECT_PROMPT.md",
    ".github/agents/project-manager.agent.md",
    ".github/agents/planner512k.agent.md",
    ".github/agents/builder128k.agent.md",
    ".github/agents/builder256k.agent.md",
    ".github/skills/project-planning/SKILL.md",
    ".github/skills/builder-task-execution/SKILL.md",
    "EXECUTE/.env.execute",
    "EXECUTE/PROJECT_CONFIG.md",
    "EXECUTE/PROJECT_STATUS.md",
    "EXECUTE/project_details.md",
    "EXECUTE/reference/KNOWLEDGE_INDEX.md",
    "EXECUTE/plan/IMPLEMENTATION_PLAN.md",
    "EXECUTE/tasks/TASK_INDEX.md",
    "EXECUTE/tasks/TASK_TEMPLATE.md",
    "EXECUTE/issues/ISSUE_INDEX.md",
    "EXECUTE/issues/ISSUE_TEMPLATE.md",
]

SECRET_KEY_RE = re.compile(
    r"(^|_)(PASSWORD|PASSWD|TOKEN|SECRET|API_KEY|ACCESS_KEY|PRIVATE_KEY|CLIENT_SECRET|SESSION|COOKIE|AUTHORIZATION)($|_)",
    re.IGNORECASE,
)

def fail(message):
    print(f"FAIL: {message}")
    return False

ok = True

for rel in REQUIRED:
    if not (ROOT / rel).exists():
        ok = fail(f"missing required file: {rel}") and ok

version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
if version != "4.0.0":
    ok = fail(f"VERSION must be 4.0.0, got {version!r}") and ok

gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
if ".env.user" not in gitignore:
    ok = fail(".gitignore must ignore .env.user") and ok

agents_dir = ROOT / ".github" / "agents"
for p in agents_dir.glob("*.agent.md"):
    lower = p.name.lower()
    if "32k" in lower or "64k" in lower:
        ok = fail(f"unsupported low-context Builder agent present: {p.name}") and ok

config = (ROOT / "EXECUTE" / "PROJECT_CONFIG.md").read_text(encoding="utf-8")
for required_number in ("524288", "131072", "262144"):
    if required_number not in config:
        ok = fail(f"PROJECT_CONFIG.md is missing hard context value {required_number}") and ok

env_path = ROOT / "EXECUTE" / ".env.execute"
for line_no, raw in enumerate(env_path.read_text(encoding="utf-8").splitlines(), 1):
    line = raw.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    key = line.split("=", 1)[0].strip()
    if SECRET_KEY_RE.search(key):
        ok = fail(f".env.execute contains secret-bearing key {key!r} at line {line_no}") and ok

if ok:
    print("PASS: v4 template validation succeeded.")
    sys.exit(0)

sys.exit(1)
