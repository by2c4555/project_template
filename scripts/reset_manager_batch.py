#!/usr/bin/env python3
"""Human-operated context-reset acknowledgment after a Manager dispatch batch is exhausted."""
from workflow_state import active_cycle, append_transition, human_tty_challenge, load_state, save_state
state=load_state(); cid,cycle=active_cycle(state); ex=cycle.get('execution') or {}; b=ex.get('manager_batch') or {}
if not b.get('reset_required'):
    raise SystemExit('MANAGER_BATCH_RESET: BLOCKED\nno manager context reset is currently required')
human_tty_challenge('MANAGER CONTEXT RESET',[f'Cycle: {cid}',f'Completed Manager batch: {b.get("number")}',f'Dispatches in batch: {b.get("dispatches")}'])
b['number']=int(b.get('number',0))+1; b['dispatches']=0; b['reset_required']=False; cycle['next_action']='START_FRESH_VSCODE_PROJECT_MANAGER'
save_state(state); append_transition('MANAGER_BATCH_RESET',actor='user:reset_manager_batch',cycle_id=cid,details={'new_batch':b['number']})
print('MANAGER_BATCH_RESET: PASS')
print(f'new_batch: {b["number"]}')
print('Start a fresh ProjectManager500K chat; do not continue the old Manager conversation.')
