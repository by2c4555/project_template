# External Research UI Pack — v4.3.1

Use this folder with **ChatGPT Project or any other web AI project/workspace**. It replaces the older ChatGPT-only multi-prompt pack.

The goal is simple: one durable knowledge file + one short project instruction + one universal start prompt.

## Files

```text
EXECUTE/external_research/
├── RESEARCH_PROTOCOL.md
├── RUN_RESEARCH.md
├── chatgpt/
│   └── PROJECT_INSTRUCTIONS.txt
└── generic/
    └── INSTRUCTIONS_1000.txt
```

## ChatGPT setup

1. Create/open a ChatGPT Project.
2. Add `RESEARCH_PROTOCOL.md` as project knowledge/resource.
3. Paste `chatgpt/PROJECT_INSTRUCTIONS.txt` into Project Instructions.
4. Add the files relevant to this research round, for example the latest verified `PROJECT_COMPLETION_REPORT_Vx.md` for a next-version/debug round.
5. Send `RUN_RESEARCH.md` plus your actual request.

No separate Initial / Next Version / Scope Clarification prompt is required. The AI infers the mode from the inputs.

## Generic web AI setup

For Claude/Gemini/other project-style web chats:

1. Create/open a Project/Workspace if the service supports one.
2. Upload `RESEARCH_PROTOCOL.md` as knowledge/resource/reference material.
3. Paste `generic/INSTRUCTIONS_1000.txt` into the service's project/system instruction field.
4. Upload the relevant baseline/scope files.
5. Send `RUN_RESEARCH.md` plus your actual request.

`INSTRUCTIONS_1000.txt` is intentionally below 1,000 characters so it can fit restrictive instruction fields. The detailed behavior lives in `RESEARCH_PROTOCOL.md`.

If the service has no project/workspace feature, attach/paste `RESEARCH_PROTOCOL.md` in the conversation, then send `RUN_RESEARCH.md` and your request.

## What to provide by mode

### New project

Normally provide only your idea/requirements and any useful external references.

### Next version / new feature / debug after a validated release

Prefer providing:

```text
latest EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_Vx.md
current EXECUTE/project_details.md (optional but useful)
your new feature/change/debug intent
relevant external evidence
```

### Scope clarification requested by Codex

Provide:

```text
EXECUTE/scope/SCOPE_CLARIFICATION_REQUIRED_Vx.md
referenced Diagnosis when useful
current project_details.md / Research version
your decision or additional requirements
```

## Expected handoff

The external AI returns:

```text
EXECUTE/project_details.md
EXECUTE/research/Research_Vx.md
EXECUTE/docs/raw/**   # only useful evidence
```

Copy those artifacts into the repository. Then the controlled VS Code workflow starts with:

```bash
python scripts/start_cycle.py --scope Research_Vx --title "..."
```

Old implementation approval never carries into the new cycle.
