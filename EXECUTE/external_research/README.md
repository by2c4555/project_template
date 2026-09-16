# External Research Pack — v4.3.2

This folder is for **ChatGPT Projects or any other web-AI project/workspace** used outside the controlled VS Code runtime.

Its job is to turn an idea/change/debug intent into a concise implementation-ready scope plus useful evidence for Codex.

## Files

```text
EXECUTE/external_research/
├── README.md
├── RESEARCH_GUIDE.md
└── setup/
    ├── CHATGPT_INSTRUCTIONS.txt
    └── EXTERNAL_INSTRUCTIONS_1000.txt
```

## Setup — ChatGPT

1. Create/open a Project.
2. Add `RESEARCH_GUIDE.md` as Project knowledge/resource.
3. Paste `setup/CHATGPT_INSTRUCTIONS.txt` into Project Instructions.
4. Add only the baseline/reference files needed for the current research.
5. Describe the project/change/debug request naturally and continue the research conversation.

## Setup — other Web AI

1. Create/open a Project/Workspace when supported.
2. Upload `RESEARCH_GUIDE.md` as knowledge/resource/reference material.
3. Paste `setup/EXTERNAL_INSTRUCTIONS_1000.txt` into the instruction field.
4. Upload only the relevant baseline/reference files.
5. Describe the request naturally.

`EXTERNAL_INSTRUCTIONS_1000.txt` is intentionally <= 1,000 characters. The detailed behavior lives in `RESEARCH_GUIDE.md`.

If the service has no project/workspace feature, attach/paste `RESEARCH_GUIDE.md` at the start of the conversation.

## Long research conversations

Do not depend on one 100k–200k-token chat lasting forever. Periodically checkpoint confirmed research into user-saved working files such as:

```text
research_workspace/RESEARCH_INDEX.md
research_workspace/topics/TOPIC-NNN-*.md
research_workspace/sources/SOURCE-NNN-*.md
```

Start a fresh web chat with the Guide + Index + only the relevant topic/source files. A good checkpoint must let the new chat continue without the old conversation.

These working files are **not** the Codex handoff.

## Final handoff

Only after material product/scope readiness is complete, produce:

```text
EXECUTE/project_details.md
EXECUTE/docs/raw/*        # only useful supporting evidence
```

If important product/scope information is still missing, do not create the final handoff. Summarize what is confirmed, what is unresolved, why it matters, and the recommended next research/questions.

There is no `Research_Vx.md` in v4.3.2.

After copying the final handoff into the repository, start a local change cycle:

```bash
python scripts/start_cycle.py --title "..."
```

Python validates the handoff and captures an immutable Scope Snapshot before Codex Planning begins.
