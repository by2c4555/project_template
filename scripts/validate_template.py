#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "EXECUTE_PROJECT_PROMPT.md",
    ".gitignore",
    "EXECUTE/PROJECT_CONFIG.md",
    "EXECUTE/PROJECT_STATUS.md",
    "EXECUTE/.env.execute",
    "EXECUTE/project_details.md",
    "EXECUTE/reference/KNOWLEDGE_INDEX.md",
    "EXECUTE/plan/IMPLEMENTATION_PLAN.md",
    "EXECUTE/tasks/TASK_INDEX.md",
    "EXECUTE/tasks/TASK_TEMPLATE.md",
    "EXECUTE/issues/ISSUE_INDEX.md",
    "EXECUTE/issues/ISSUE_TEMPLATE.md",
    ".github/agents/project-manager.agent.md",
    ".github/skills/project-orchestration/SKILL.md",
    ".github/skills/builder-task-execution/SKILL.md",
]

BUILDERS = [32, 64, 128, 200, 500]

def main():
    errors = []
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            errors.append(f"missing {rel}")
    for size in BUILDERS:
        if not (ROOT / f".github/agents/builder{size}k.agent.md").exists():
            errors.append(f"missing Builder{size}K agent")
    if (ROOT / ".env.user").exists():
        errors.append("template must not ship with .env.user; workflow creates it when needed")
    for script in ("validate_execute_env.py", "validate_task_pack.py"):
        p = ROOT / "scripts" / script
        if p.exists():
            r = subprocess.run([sys.executable, str(p)], cwd=ROOT, text=True, capture_output=True)
            if r.returncode != 0:
                errors.append(f"{script} failed: {r.stdout.strip()}")
    if errors:
        print("TEMPLATE VALIDATION")
        for e in errors:
            print(f"- {e}")
        print(f"RESULT: FAIL ({len(errors)} errors)")
        return 1
    print("RESULT: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
