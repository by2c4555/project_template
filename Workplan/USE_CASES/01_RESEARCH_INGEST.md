# Research -> Ingest -> Scope

External Research produces `project_details.md` plus declared logical `Workplan/docs/raw/*` files. The user places them in `Workplan/ingest/`. `ingest.py check` validates metadata, path safety, declarations and dual digests. `scope.py import` accepts only validated current input and snapshots canonical logical Scope.
