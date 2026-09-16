# ChatGPT Research Workspace

## Purpose

This workspace is used to manually research, verify, compare, and organize project information before moving the resulting Markdown files into a separate VS Code project.

ChatGPT is used here as a **research assistant**, not as the implementation planner or coding agent.

The user controls the research process manually.

The final outputs of this workspace are normally:

```text
project_details.md

docs/
├── <TOPIC>_RESEARCH.md
├── <TOPIC>_RESEARCH.md
└── ...
```

The user then manually copies these files into the target VS Code project.

---

## Scope

ChatGPT Research is responsible for:

- researching technologies, frameworks, libraries, APIs, protocols, standards, products, and platforms;
- checking current documentation and compatibility information;
- comparing technical alternatives;
- analyzing source material provided by the user;
- identifying constraints, limitations, risks, assumptions, and unknowns;
- helping the user refine requirements;
- turning completed research discussions into reusable Markdown documents;
- consolidating confirmed user requirements and decisions into `project_details.md`.

ChatGPT Research is **not** responsible for:

- creating the implementation plan;
- defining implementation phases;
- compiling coding tasks;
- generating Builder/Subagent instructions;
- managing VS Code agents;
- creating curated Planner reference knowledge;
- creating `KNOWLEDGE_INDEX.md`;
- executing the implementation.

Those activities belong to the separate VS Code workflow.

---

## Workflow

```text
USER IDEA / USER DATA
        │
        ▼
ChatGPT Project
        │
        │ Manual research
        │
        ├── Ask questions
        ├── Search and verify information
        ├── Compare alternatives
        ├── Upload source material
        ├── Discuss constraints
        ├── Make user decisions
        └── Refine requirements
        │
        ▼
RAW KNOWLEDGE DOCUMENTS
        │
        ├── API_RESEARCH.md
        ├── DATABASE_RESEARCH.md
        ├── SECURITY_RESEARCH.md
        ├── DEPLOYMENT_RESEARCH.md
        ├── PLATFORM_RESEARCH.md
        └── ...
        │
        ▼
project_details.md
        │
        │ User manually exports/copies files
        ▼
══════════════════════════════════════
VS CODE PROJECT BOUNDARY
══════════════════════════════════════
        │
        ▼
EXECUTE/
├── project_details.md
└── docs/
    ├── API_RESEARCH.md
    ├── DATABASE_RESEARCH.md
    ├── SECURITY_RESEARCH.md
    └── ...
        │
        ▼
VS Code Planning / Execution Workflow
```

The ChatGPT Project does not need to know how the VS Code planner, task generator, or subagents operate internally.

Its job ends when the research documents and `project_details.md` are ready for the user to export.

---

## Setup

Create one ChatGPT Project for each software or engineering project you want to research.

Place the contents of:

```text
RESEARCH_PROMPT.md
```

into the ChatGPT Project Instructions.

Then use the Project normally.

There is no mandatory kickoff command.

You can begin with a normal research question such as:

> I want to build a Windows desktop application for managing local AI models. Help me research suitable technology stacks first.

or:

> Research authentication options for this project. Compare the practical tradeoffs and use current official documentation where possible.

---

## Manual Research Model

Research is intentionally user-driven.

A typical topic proceeds like this:

```text
User asks a research question
        │
        ▼
ChatGPT investigates
        │
        ▼
Findings + sources + uncertainties
        │
        ▼
User asks follow-up questions
        │
        ▼
More research / comparison
        │
        ▼
User makes or postpones a decision
        │
        ▼
User decides the topic is sufficiently researched
        │
        ▼
User explicitly requests a Markdown document
```

ChatGPT should not automatically declare the research complete.

ChatGPT should not automatically create all possible research documents.

The user determines which topics require deeper research and when a document should be created.

---

## RAW KNOWLEDGE

RAW KNOWLEDGE files contain supporting research and evidence.

They are not implementation plans.

They may contain:

- verified technical facts;
- documentation findings;
- supported versions;
- compatibility information;
- platform limitations;
- API constraints;
- protocol information;
- licensing information;
- deployment constraints;
- security findings;
- alternatives;
- factual tradeoffs;
- unresolved questions;
- risks and limitations;
- source links.

A project may have one RAW KNOWLEDGE file or many.

For example:

```text
docs/
├── WINDOWS_PLATFORM_RESEARCH.md
├── DOTNET_RESEARCH.md
├── DATABASE_RESEARCH.md
├── AUTHENTICATION_RESEARCH.md
├── API_PROVIDER_RESEARCH.md
├── PACKAGING_RESEARCH.md
├── AUTO_UPDATE_RESEARCH.md
├── SECURITY_RESEARCH.md
└── TESTING_RESEARCH.md
```

Splitting research by coherent topic is usually better than creating one extremely large document.

---

## Recommended RAW KNOWLEDGE Structure

When the user asks ChatGPT to turn research into a Markdown document, a useful default structure is:

```markdown
# <Research Topic>

## Research Scope

## Context

## Findings

## Verified Facts

## Constraints

## Alternatives Investigated

## Tradeoffs

## Compatibility / Version Information

## Risks and Limitations

## Unknowns / Open Questions

## Sources
```

Only include sections that are relevant.

Research documents should remain evidence-oriented.

Do not silently turn recommendations into requirements.

---

## Evidence Labels

When useful, distinguish information using the following labels:

```text
VERIFIED
Supported by reliable external evidence.

USER_STATED
Explicitly provided or decided by the user.

INFERRED
A reasoned conclusion that is not directly confirmed.

UNKNOWN
Not yet established.

DISPUTED
Reliable sources, requirements, or evidence conflict.
```

These labels help prevent assumptions from being mistaken for facts.

---

## Source Quality

For technical research, prefer sources in approximately this order:

1. official standards and specifications;
2. official vendor or platform documentation;
3. official API documentation;
4. official release notes;
5. authoritative repositories and maintained technical documentation;
6. primary research or official regulatory documentation;
7. reliable secondary technical sources when primary sources are insufficient.

For information that can change over time, ChatGPT should verify current information before presenting it as current.

Examples include:

- versions;
- pricing;
- supported operating systems;
- API limits;
- model capabilities;
- service availability;
- compatibility;
- licensing;
- package support;
- deployment requirements.

Important claims should preserve useful provenance whenever practical.

---

## User Decisions

Research and requirements are different.

Research may show that several options are valid.

For example:

```text
SQLite
PostgreSQL
SQL Server
```

A research document may explain all three.

That does **not** mean one automatically becomes a project requirement.

Only a confirmed user decision should become authoritative project input.

Example:

```text
USER:
Use SQLite for the local application database.

RESULT:
This can now be recorded in project_details.md as a user decision.
```

---

## project_details.md

`project_details.md` contains the actual project requirements, constraints, goals, and confirmed decisions.

It should not be a dump of all research.

A recommended structure is:

```markdown
# Project Name

## Purpose

## Success Criteria

## In Scope

## Out of Scope

## Critical User / System Workflows

## Functional Requirements

## Non-Functional Requirements

## Runtime and Target Platform

## Existing System / Repository Constraints

## Database / Persistence

## External APIs / Services

## Security Constraints

## Packaging / Deployment / Installation

## Testing Expectations

## Release Expectations

## Known Risks / Unknowns

## Source Documents

## User Decisions
```

If an architecture-relevant issue remains unresolved, use:

```text
UNKNOWN
```

rather than inventing an answer.

---

## Creating project_details.md

Do not create `project_details.md` simply because research has started.

Create or update it when the user requests it.

A useful request is:

> Review the confirmed information and decisions in this ChatGPT Project and create `project_details.md`. Include only requirements and decisions I have actually confirmed. Do not convert unselected research options into requirements. Mark unresolved architecture-relevant items as UNKNOWN and list the supporting research documents under Source Documents.

The user should review the result before exporting it.

---

## Suggested Research Sequence

There is no mandatory sequence, but the following areas often deserve investigation:

- project purpose and success criteria;
- users and critical workflows;
- runtime and target platforms;
- existing-system constraints;
- technology stack;
- data and persistence;
- external APIs and services;
- authentication and authorization;
- security and compliance;
- protocols and interoperability;
- packaging and installation;
- deployment and hosting;
- updates and migration;
- performance and resource constraints;
- testing strategy;
- compatibility requirements;
- release requirements.

Only research topics that are relevant to the project.

---

## Export to VS Code

When research is sufficiently mature, manually export or copy:

```text
project_details.md
docs/*.md
```

into the target VS Code project:

```text
EXECUTE/
├── project_details.md
└── docs/
    ├── <RAW_KNOWLEDGE>.md
    └── ...
```

The VS Code system should treat these files as prepared user input.

The ChatGPT Research workspace should not attempt to create the downstream planner outputs.

---

## Boundary Rule

Keep this separation clear:

```text
ChatGPT Project
=
Manual Research
Evidence Collection
Requirement Refinement
RAW KNOWLEDGE
project_details.md
```

```text
VS Code Project
=
Planning
Reference Curation
Implementation Plan
Task Generation
Subagent Execution
Integration
```

The user is the bridge between the two systems.

---

## Recommended Final Export

A mature research package may look like:

```text
research-export/
├── project_details.md
└── docs/
    ├── PLATFORM_RESEARCH.md
    ├── TECHNOLOGY_STACK_RESEARCH.md
    ├── DATABASE_RESEARCH.md
    ├── API_RESEARCH.md
    ├── SECURITY_RESEARCH.md
    ├── DEPLOYMENT_RESEARCH.md
    └── TESTING_RESEARCH.md
```

The exact number and names of research documents are project-dependent.

There is no requirement to create every example file.

---

## Core Principle

**Research first. Decide explicitly. Document the evidence. Keep requirements separate from alternatives. Let the user control when information becomes authoritative.**
