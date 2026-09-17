# Project Template v5.0.0

This repository separates the **user project** from the AI-development control plane.

- `Workplan/` is the control plane used to plan, build, diagnose, recover, evaluate, resume, and govern AI work.
- Files outside `Workplan/` are user-project space, except thin platform adapters such as `.github/agents/`.

Normal human commands:

```bash
python Workplan/scripts/resume.py
python Workplan/scripts/approve.py -- 583194
```

Read `Workplan/README.md` for the canonical workflow.
