# Migration v5.3.2 to v5.4.0

v5.4.0 separates immutable Research import, Planning A, bound Scope approval, Planning B, and bound execution approval. It changes the state schema from 6 to 7.

Run `python Workplan/scripts/migrate_v532_to_v540.py` only while v5.3.2 has no active Cycle, Work, or pending approval. Active authority cannot be transformed safely because its old lifecycle created Scope at import; finish, cancel, or reconcile it under v5.3.2 first. The migration preserves historical cycles and starts the new ingress control plane at `BOOTSTRAP` / `AWAITING_RESEARCH`.
