# DEPRECATED COMBINED RECOVERY PROMPT — v4.3.2

**STOP. Do not diagnose and repair in one invocation.**

v4.3 intentionally splits this high-cost workflow:

1. Diagnosis only: `EXECUTE/codex/ISSUE_DIAGNOSIS_PROMPT.md`
2. Human gate: `python scripts/approve_recovery.py`
3. Authorized repair only: `EXECUTE/codex/RECOVERY_PROMPT.md`
4. Machine verification: `scripts/recovery_gate.py`
5. Human resume or re-evaluation gate.

This separation is a token-safety boundary and must not be bypassed for convenience.
