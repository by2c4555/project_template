#!/usr/bin/env python3
"""Initialize v4.4.2 machine state. Safe to run on a fresh template only."""
from workflow_state import STATE_PATH, append_transition, initial_state, save_state

if STATE_PATH.exists():
    raise SystemExit(f"INIT_V43: BLOCKED\n{STATE_PATH} already exists")
state = initial_state()
save_state(state)
append_transition("WORKFLOW_INITIALIZED", actor="python:init_v44", cycle_id=None, details={"version": "4.3.2"})
print("INIT_V43: PASS")
print("State: AWAITING_SCOPE_IMPORT")
print("Next: copy READY_FOR_PLANNING project_details.md + declared docs/raw evidence, then run python scripts/start_cycle.py --title \"...\"")
