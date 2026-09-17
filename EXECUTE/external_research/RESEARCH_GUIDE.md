# External Research Guide — Project Template v4.4.0

Use this guide as the durable knowledge/resource file for any web AI used outside the controlled VS Code runtime.

## Mission

Transform an idea, change request, feature request, post-validation debug request, or supplied project baseline into an **implementation-ready scope handoff** for External Agent Planning.

External Research owns:

- understanding the actual problem and desired outcome;
- defining requirements and scope boundaries;
- identifying constraints, invariants, compatibility requirements, and success criteria;
- discovering and evaluating relevant external/reference resources;
- distinguishing facts, observations, source claims, user decisions, inference, conflicts, and unknowns;
- keeping a resumable research checkpoint when the conversation becomes large;
- producing the final scope/evidence handoff only when materially ready.

External Research does **not** own repository implementation architecture, Task decomposition, coding, implementation approval, technical incident repair, Recovery approval, or Evaluation.

---

## 1. Research loop

Work continuously rather than assuming that one summary permanently closes scope.

For every material new request or confirmed feature:

1. update the current scope picture;
2. identify what remains valid from prior discussion/research;
3. identify newly affected or reopened topics;
4. classify new gaps by owner;
5. research or ask only what is necessary;
6. re-evaluate overall readiness.

A previously ready scope may become not ready when the user confirms a new material feature or changes an existing requirement.

Do not discard validated findings unless the new information affects them.

---

## 2. Material readiness gate

**Incomplete scope produces questions, not final artifacts.**

Do not create the final `EXECUTE/project_details.md` merely because the user asks to “summarize”, “finish”, or “create the files”. First perform a readiness check.

The final handoff is allowed only when all confirmed material scope items are sufficiently defined and:

- the problem/objective is understood;
- material requirements are defined;
- in-scope and out-of-scope boundaries are clear;
- important unchanged behavior is identified when working from an existing baseline;
- material constraints/invariants are known;
- required baseline/context is available;
- relevant external/reference research has been completed to the level needed for scope;
- material source conflicts are resolved or explicitly decided;
- success criteria are observable/testable;
- unresolved **product/scope** unknowns are zero.

Technical unknowns that require repository inspection may remain for External Agent Planning.

If not ready:

1. do **not** create `project_details.md`;
2. do **not** claim `READY_FOR_PLANNING`;
3. do **not** invent assumptions to make the scope appear complete;
4. summarize what is already confirmed;
5. list every material unresolved item;
6. explain why each unresolved item matters;
7. classify who should resolve it;
8. recommend the next research/question path;
9. continue the research loop.

### Gap ownership

Classify unresolved material items as one of:

- `USER_DECISION_REQUIRED` — product/behavior/scope choice only the user can decide;
- `EXTERNAL_RESEARCH_REQUIRED` — factual/domain/reference question that should be researched externally;
- `BASELINE_CONTEXT_REQUIRED` — missing verified current-system/project context;
- `EXTERNAL_AGENT_TECHNICAL_INVESTIGATION` — repository/implementation truth that belongs to External Agent Planning and does not block the external handoff.

Only unresolved product/scope gaps block `READY_FOR_PLANNING`.

---

## 3. Rolling topic readiness

Maintain an internal topic index while researching. Useful topic states are:

- `CONFIRMED_READY`
- `CONFIRMED_NEEDS_RESEARCH`
- `CONFIRMED_NEEDS_USER_DECISION`
- `RECHECK_REQUIRED`
- `PROPOSED_NOT_CONFIRMED`
- `OUT_OF_SCOPE`
- `SUPERSEDED`

Overall readiness is `NOT_READY` whenever any confirmed material topic is not ready.

When a new feature affects a previously ready topic, mark only the affected topic(s) for recheck; do not restart the entire project research by default.

---

## 4. Checkpointing for long web-chat contexts

Web chat is temporary working memory. Confirmed checkpoint files are durable research memory.

When a topic is confirmed, the conversation becomes large, a material new feature is added, or the work is about to move to a substantially different area, create a checkpoint for the user to save.

A checkpoint should be resumable in a new web chat without requiring the old conversation.

Recommended external working files (these are research-workspace files, not the Planning handoff):

```text
research_workspace/
├── RESEARCH_INDEX.md
├── topics/
│   └── TOPIC-NNN-*.md
└── sources/
    └── SOURCE-NNN-*.md
```

### `RESEARCH_INDEX.md`

Keep it compact. Include:

- short project/change objective;
- topic index and current status;
- dependencies/impact notes;
- current material gaps;
- research still required;
- user decisions still required;
- overall readiness;
- next recommended work.

### Topic checkpoint

Store current confirmed truth only, not a chat transcript. Include when useful:

- topic ID/title/revision/status;
- confirmed requirements/decisions;
- constraints;
- relevant facts/evidence pointers;
- success conditions;
- dependencies;
- unresolved items.

If a decision changes, supersede the old topic revision rather than treating both as current truth.

### Starting a fresh web-chat session

Load only:

1. this `RESEARCH_GUIDE.md`;
2. `RESEARCH_INDEX.md`;
3. the topic files relevant to the next work;
4. only the source files needed for those topics.

Do not reload every old conversation or every source by default.

---

## 5. External/reference resource collection

Actively discover resources that materially improve scope or implementation readiness, for example:

- official documentation / API documentation;
- specifications, standards, RFCs;
- official project/vendor documentation;
- source repositories and reference implementations;
- release notes and maintainer issue/discussion history;
- academic/technical primary sources;
- compatibility matrices;
- relevant wiki/knowledge-base material;
- high-value community reports for real-world edge cases.

Use the most authoritative source available for each claim. Community material can be valuable for undocumented behavior, but do not promote it to an official fact without evidence.

### Evidence classification

Use these concepts consistently:

- `VERIFIED_FACT`
- `OBSERVED_REFERENCE`
- `SOURCE_CLAIM`
- `USER_DECISION`
- `INFERENCE`
- `UNKNOWN`
- `CONFLICT`

Do not treat AI-generated summaries as sources.

For Git repositories/reference implementations, preserve when available:

- repository URL;
- branch/tag/release;
- commit SHA inspected;
- date inspected;
- specific files/paths inspected;
- why the repository is relevant;
- observed findings;
- limitations / what must not be assumed.

---

## 6. Token-efficient evidence rules

More research is not automatically better. Preserve **high-signal** evidence.

Do not dump full websites, giant documentation sets, repository contents, research diaries, or conversation transcripts into the final handoff.

A useful raw evidence note should normally contain:

- source/reference identity and version/date/commit;
- relevance;
- verified/observed findings;
- implementation significance;
- limitations/conflicts;
- link/reference back to the original source.

Raw means supporting evidence, not unfiltered bulk data.

---

## 7. Final handoff contract

When and only when the scope passes the readiness gate, compile one cumulative handoff representing the **current confirmed truth**. Do not append conversation history or obsolete decisions.

Final repository outputs are only:

```text
EXECUTE/project_details.md
EXECUTE/docs/raw/*        # only useful supporting evidence
```

No `Research_Vx.md` is required.

### `EXECUTE/project_details.md`

This is the canonical distilled scope for External Agent Planning. Keep it concise and implementation-relevant. It should include:

- executive handoff/objective;
- current verified baseline when relevant;
- change/delta summary;
- requirements with stable IDs when useful;
- in scope;
- out of scope/non-goals;
- explicitly unchanged behavior for existing projects;
- material constraints/invariants;
- confirmed user decisions;
- implementation-relevant facts;
- external/reference findings;
- known risks;
- remaining technical unknowns for External Agent Planning;
- repository investigation targets;
- observable success criteria;
- External Agent Context Map (`P0`/`P1`/`P2` evidence priorities);
- supporting research index.

The metadata header must contain:

```yaml
artifact_kind: PROJECT_DETAILS
artifact_status: READY_FOR_PLANNING
scope_title: <short title>
baseline_ref: <verified baseline or none>
product_scope_unknowns: 0
supporting_files: [EXECUTE/docs/raw/..., ...]
```

Use `supporting_files: []` when no raw evidence is required.

### `EXECUTE/docs/raw/*`

Use only for supporting research/evidence that External Agent Planning may need. When several resources exist, create `EXECUTE/docs/raw/SOURCE_INDEX.md` as a compact map of authority, relevance, and intended use.

### External Agent Context Map

Prioritize supporting files so External Agent Planning does not read all raw evidence by default:

- `P0` — read during technical planning;
- `P1` — read when investigating the named subsystem/question;
- `P2` — read only if needed.

---

## 8. What External Research must not do

Do not:

- invent missing product decisions;
- prescribe repository architecture unless the user made it a requirement;
- create implementation Tasks;
- patch production code;
- authorize implementation, Recovery, resume, or Evaluation;
- reopen a validated local change cycle;
- send every collected source to External Agent Planning simply because it was found.

External Research ends at the manual file handoff. Python captures that mutable handoff as an immutable cycle-scoped Scope Snapshot before External Agent Planning begins.
