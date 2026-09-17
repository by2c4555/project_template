# Migration from v4.4.0

v5 is a breaking structural redesign. Do not manually rename a live v4.4 workspace and assume bindings remain valid. Preserve the original workspace, validate v4.4 state/package/scope first, then translate artifacts/state with a reviewed migration procedure. Any active in-progress Work requires explicit reconciliation because v4.4 lacks v5 Builder universal checkpoint semantics.
