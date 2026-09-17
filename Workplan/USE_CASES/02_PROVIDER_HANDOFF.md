# Provider Handoff

Codex checkpoints a completed topic and becomes unavailable. A fresh Claude/other provider runs the same Planning prompt. `work.py begin` returns RESUME for the same Work, updates provider metadata, loads the latest resume capsule, and continues the next unit without replaying completed valid research. No human approval is required.
