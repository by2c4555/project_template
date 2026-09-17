# External Agent Protocol — v4.4.0

Provider-neutral role prompts for repository-capable expensive agents such as Codex, Claude Code, OpenCode, Antigravity, or future providers.

Authority remains in `EXECUTE/control/STATE.json` + deterministic scripts. Agent identity is audit metadata only.

For every role invocation:

1. read `STATE.json`;
2. run `python scripts/agent_work.py begin --role <ROLE> --tool "<tool>" --model "<model>"`;
3. if it returns RESUME, read the referenced resume capsule before any broad repository research;
4. perform one bounded work unit at a time;
5. checkpoint verified facts/decisions/evidence/open items and exact next unit;
6. never persist hidden chain-of-thought; persist conclusions and evidence only;
7. mark External Agent work complete before the role's deterministic finalizer/gate.

A valid checkpoint must be sufficient for a fresh compatible agent with zero conversation history to continue safely.
