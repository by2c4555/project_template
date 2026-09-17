from pathlib import Path
WORKPLAN = Path(__file__).resolve().parents[2]
ROOT = WORKPLAN.parent
CONTROL = WORKPLAN / "control"
STATE_PATH = CONTROL / "STATE.json"
TRANSITIONS_PATH = CONTROL / "TRANSITIONS.jsonl"
WORK_DIR = WORKPLAN / "work"
APPROVAL_DIR = CONTROL / "approvals"
