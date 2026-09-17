# Bounded Local Repair

Each immutable Task carries `max_repairs`. `execution.py repair` increments the machine counter. Once exhausted, another repair request creates a diagnosis issue and routes to DIAGNOSIS instead of allowing open-ended Builder loops.
