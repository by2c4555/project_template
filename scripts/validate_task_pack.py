#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TASK_DIR = ROOT / "EXECUTE" / "tasks"
AGENT_DIR = ROOT / ".github" / "agents"

REQUIRED_SECTIONS = [
    "## Objective",
    "## Definition of Done",
    "## Plan References",
    "## Knowledge References",
    "## Builder / Context Budget",
    "## Exploration Budget",
    "## External I/O Budget",
    "## Environment Contract",
    "## Context Manifest",
    "## Required Evidence",
    "## Acceptance Criteria",
    "## Test Ownership",
    "## Verification Matrix",
    "## Exploration Stop Conditions",
    "## Completion Condition",
    "## Current Result",
]

def profile_max(agent_text):
    m = re.search(r"Maximum planned task:\s*<=\s*([0-9]+)K", agent_text)
    return int(m.group(1)) * 1024 if m else None

def main():
    tasks = sorted(
        p for p in TASK_DIR.glob("TASK_*.md")
        if p.name not in {"TASK_INDEX.md", "TASK_TEMPLATE.md"}
    )
    if not tasks:
        print("RESULT: PASS (0 generated tasks; template state)")
        return 0
    profiles = {}
    for p in AGENT_DIR.glob("builder*.agent.md"):
        lim = profile_max(p.read_text(encoding="utf-8"))
        if lim:
            profiles[p.name] = lim
    errors = []
    for task in tasks:
        text = task.read_text(encoding="utf-8")
        for sec in REQUIRED_SECTIONS:
            if sec not in text:
                errors.append(f"{task.name}: missing {sec}")
        src = re.search(r"builder_profile_source:\s*([^\n]+)", text)
        planned = re.search(r"planned_context_tokens:\s*([0-9]+)", text)
        assessment = re.search(r"context_assessment:\s*([A-Z_]+)", text)
        if not (src and planned and assessment):
            errors.append(f"{task.name}: incomplete Builder/context metadata")
            continue
        source_name = Path(src.group(1).strip()).name
        if source_name not in profiles:
            errors.append(f"{task.name}: unknown Builder profile source {source_name}")
            continue
        if int(planned.group(1)) > profiles[source_name]:
            errors.append(f"{task.name}: planned context exceeds {source_name} maximum")
        if assessment.group(1) != "SAFE":
            errors.append(f"{task.name}: context_assessment must be SAFE")
    if errors:
        print("TASK PACK VALIDATION")
        for err in errors:
            print(f"- {err}")
        print(f"RESULT: FAIL ({len(errors)} errors)")
        return 1
    print(f"RESULT: PASS ({len(tasks)} generated tasks)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
