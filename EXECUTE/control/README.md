# Control State — v4.4.0

`STATE.json` is the single workflow authority. `TRANSITIONS.jsonl` is the append-only transition ledger. Approval/manifests bind immutable scope/package authority.

`AGENT_WORK.json` is provider-neutral resumable working state for the currently active expensive External Agent role. It is subordinate to the authoritative `active_external_work` pointer/status/checkpoint sequence in `STATE.json`.

Never hand-edit these files to bypass a gate. Use deterministic scripts.
