# Provider Handoff

A Planning provider checkpoints a semantic unit. A fresh provider submits the same exact `EXECUTE_PLANNING` command. Workplan detects compatible active Planning Work, recalculates immutable bindings, increments generation, fences the old session, and returns a Resume Ticket. Prior chat replay is not required.
