# Control State

`STATE.json` is authoritative internal workflow state. Agents should use bounded CLI projections instead of reading it directly during normal operation. `TRANSITIONS.jsonl` is append-only audit history and is not workflow authority.
