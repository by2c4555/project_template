from pathlib import Path
WORKPLAN = Path(__file__).resolve().parents[2]
ROOT = WORKPLAN.parent
CONTROL = WORKPLAN / 'control'
STATE_PATH = CONTROL / 'STATE.json'
TRANSITIONS_PATH = CONTROL / 'TRANSITIONS.jsonl'
WORK_DIR = WORKPLAN / 'work'
APPROVAL_DIR = CONTROL / 'approvals'
INGEST_DIR = WORKPLAN / 'ingest'
INGEST_RECEIPT_DIR = CONTROL / 'ingest'
ARCHIVE_DIR = WORKPLAN / 'archive'
HISTORY_DIR = WORKPLAN / 'history'
TASK_DIR = WORKPLAN / 'tasks'
COMPILED_DIR = WORKPLAN / 'compiled'
PLAN_DIR = WORKPLAN / 'plan'
