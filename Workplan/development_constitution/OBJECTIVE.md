> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Project Template Development Objective

## 1. Product Identity

Project Template is an **AI-assisted software-development control plane**.

Its purpose is to convert externally prepared product/research information into reliable software-development authority, then coordinate high-quality repository implementation, verification, recovery, and final acceptance.

Project Template runtime coordinates:

- Research Handoff import and structural validation;
- Research Investigation & Finalization by Planning;
- authoritative Scope finalization;
- user approval of material Scope and execution envelopes;
- architecture and implementation planning;
- bounded source-code implementation;
- CLI/tool execution;
- controlled file operations;
- software debugging and repair;
- verification and regression checking;
- recovery from failed implementation;
- independent final acceptance;
- deterministic closure;
- durable next-version knowledge output;
- cross-session continuation.

Project Template does **not** perform or govern the external user-facing Research conversation.

External Research may be performed by ChatGPT, another web chat, another AI system, a human researcher, or another preparation process.

Project Template may provide Research prompts, protocols, instructions, and templates. Those helpers do not make Research a runtime lifecycle stage, Work item, Cycle, or authority source.

Project Template is not a general-purpose autonomous-agent framework.

## 2. Core Objective

Maximize:

```text
engineering quality / token / cost
```

while keeping authority:

- deterministic;
- durable;
- auditable;
- bounded;
- resumable;
- stale-safe;
- provider-neutral;
- independently verifiable.

## 3. Capability Allocation

```text
External Research AI
    -> broad/deep preparation
    -> user clarification
    -> repository/technical research
    -> candidate Scope
    -> candidate architecture/design
    -> evidence

Planning AI
    -> strongest normal runtime reasoning
    -> Research Investigation & Finalization
    -> selective independent verification
    -> Accepted Scope synthesis
    -> implementation authority design

Manager
    -> execution coordination
    -> Task-local debugging
    -> bounded repair reasoning

Builder
    -> lower-cost bounded implementation

Deterministic Workplan
    -> import integrity
    -> state
    -> routing
    -> approvals
    -> tickets
    -> bindings
    -> generations
    -> gates
    -> retry limits
    -> validation
    -> finalization

Repository/filesystem state
    -> durable truth

Chat/session state
    -> disposable context
```

## 4. Engineering Principles

1. Deterministic mechanisms before prompt complexity.
2. Durable repository state before conversational memory.
3. Bounded contracts before open-ended autonomy.
4. Strong reasoning only where it materially improves decision quality.
5. Use the lowest-cost capable Builder for routine implementation.
6. Executed verification before claimed completion.
7. Immutable execution bindings.
8. Explicit escalation instead of unbounded retries.
9. Resumability across sessions, models, providers, and machines.
10. Selective context instead of repository-wide context by default.
11. Negative-path validation for authority boundaries.
12. One source of truth per concern.
13. Preserve existing valid work before rewriting.
14. Fix root causes rather than accumulating compensating mechanisms.
15. Internal rigor may increase, but normal user workflow should become simpler.
16. External preparation must not be confused with runtime authority.
17. Research should maximize useful information, not authority.
18. Planning must finalize Research before Scope becomes runtime authority.
19. Planning should reuse strong Research rather than blindly repeat it.
20. Material claims should be independently verified when wrongness would materially affect architecture, compatibility, acceptance, security, irreversible behavior, or major cost/risk.
21. Planning must not invent unresolved material product requirements.
22. Technical HOW belongs to Planning unless it changes product WHAT/WHY.
23. User approval should protect meaningful cost/authority/rework boundaries, not every routine step.
24. An approval applies only to the exact approved envelope and becomes stale when that envelope materially changes.
25. `CLOSED_VALIDATED` must produce durable output for future external Research.
26. Completion knowledge is not automatically the next Scope.

## 5. Authority Model

Workflow authority comes from deterministic Workplan state and accepted runtime contracts.

Authority does not come from:

- model capability;
- model price;
- provider identity;
- model confidence;
- chat context;
- prompt self-assertion;
- external Research conversation;
- Research Handoff by itself;
- candidate architecture;
- implementation summary;
- model claim of PASS.

External Research is **high-value, non-authoritative input**.

Planning creates semantic authority only through controlled finalization and deterministic binding.

User approval authorizes only explicit material envelopes.

Deterministic software owns runtime authority transitions and PASS/finalization gates.

## 6. Canonical Lifecycle

```text
OUTSIDE RUNTIME
External Research
    ↓
Research Handoff

RUNTIME
Import
    ↓
Planning A — Research Investigation & Finalization
    ↓
User Scope Approval
    ↓
Accepted Scope
    ↓
Planning B — Implementation Planning
    ↓
User Execution Approval
    ↓
PLAN_READY
    ↓
Execution
    ↓
Independent Evaluation
    ↓
CLOSED_VALIDATED
    ↓
Completion Knowledge Package

OUTSIDE RUNTIME AGAIN
Next-Version External Research
```

Diagnosis, Recovery, and Change Re-Approval are controlled exception paths.

## 7. Runtime Hierarchy

```text
Cycle -> Phase -> Task -> Attempt
```

Required invariants:

- no production Task authority before Accepted Scope and valid approved Planning authority;
- every Task belongs to exactly one Phase;
- every Builder dispatch creates a fresh Attempt;
- Attempt kinds include `INITIAL`, `REPAIR`, and `RECOVERY`;
- a simple project may use an implicit Phase;
- normal users should not manually manage IDs, generations, digests, tickets, or repair counters.

## 8. External Research Principle

Research should produce maximum useful information with minimum irrelevant context.

Research may provide:

- product requirements;
- repository findings;
- technical evidence;
- compatibility findings;
- risks;
- candidate architecture;
- preliminary interfaces/data;
- verification ideas;
- unresolved questions.

Research may recommend conclusions.

Planning must finalize them.

## 9. Planning Principle

Planning is the strongest normal runtime reasoning stage.

Planning has two mandatory logical responsibilities:

```text
A. Research Investigation & Finalization
B. Implementation Planning
```

Planning A produces Draft Finalized Scope and Finalized Research Knowledge.

After material Scope review, User Scope Approval converts the finalized Scope into Accepted Scope authority.

Planning B produces the Planning Package.

User Execution Approval authorizes entry into execution.

## 10. User Approval Principle

Approval is required where a new material:

- product-Scope commitment;
- execution cost;
- authority expansion;
- destructive effect;
- rework envelope;
- compatibility break;
- migration risk

is introduced.

Do not require approval for routine Task/Phase progression or bounded repair already covered by an approved envelope.

## 11. Execution Principle

Normal production implementation uses the VS Code Copilot Agent execution environment.

```text
Manager
    -> reasoning, coordination, local debugging, repair strategy

Builder
    -> bounded repository mutation

Deterministic Workplan
    -> routing, authority, retry control, gates
```

## 12. Manager Principle

Manager is the local execution reasoning layer.

Manager coordinates and diagnoses.

Manager is not the normal production editor.

## 13. Builder Principle

Builder is the lower-cost bounded implementation worker.

Builder must not:

- expand Scope;
- expand write authority;
- invent new lifecycle authority;
- decide deterministic PASS;
- enter open-ended debug/edit/retry loops.

## 14. Gate Principle

Only deterministic Task Gate logic may mark Task PASS.

Only deterministic Phase Gate logic may mark Phase PASS.

A model statement never replaces evidence.

## 15. Local Repair Principle

Ordinary Task-local failure uses:

```text
Builder failure
    ↓
durable failure evidence
    ↓
Manager diagnosis
    ↓
Manager-defined repair
    ↓
fresh Builder REPAIR Attempt
    ↓
Task Gate
```

Hard maximum:

```text
5 local Repair Attempts per failure chain
```

No sixth local repair.

## 16. Durable Failure Principle

Every authoritative runtime failure must leave enough durable evidence for a fresh capable model/session to diagnose, repair, recover, or resume.

Failed strategies must not be silently overwritten.

## 17. Escalation Principle

External strong reasoning is used when local execution reasoning is insufficient.

Escalation may be required for:

- exhausted local repair;
- structural defect;
- Task defect;
- Plan defect;
- Scope defect;
- environment/tooling defect;
- verification defect;
- external blocker;
- correctness uncertainty.

## 18. Diagnosis and Recovery Principle

External Diagnosis is reasoning-only.

External Recovery is reasoning-only.

Recovery cannot directly mark implementation PASS.

Recovery cannot silently broaden Task authority or create product Scope.

## 19. Context Principle

Context expansion is read authority only.

Additional context must never silently expand Scope, Task objective, write paths, or repair authority.

## 20. Binding and Resume Principle

Original authority bindings must remain durable.

Generation fencing must prevent stale sessions from completing newer authority.

A fresh session must be able to continue without replaying prior chat.

External Research conversation history must not be required.

## 21. Independent Evaluation Principle

Independent Evaluation occurs after required execution gates pass.

It verifies actual repository outcomes against Accepted Scope and Planning authority.

Evaluation is acceptance, not production repair.

## 22. CLOSED_VALIDATED Principle

`CLOSED_VALIDATED` means:

- required Accepted Scope was satisfied;
- required implementation completed;
- required Task/Phase Gates passed;
- Independent Evaluation accepted the result;
- deterministic finalization completed;
- final repository baseline is durably identifiable;
- Completion Knowledge Package was produced.

It does not claim perfection outside Scope.

## 23. Cross-Cycle Principle

A completed Cycle must produce durable knowledge for future external Research.

The output may include:

- Completion Report;
- final repository/version baseline;
- verified architecture state;
- Scope outcome;
- accepted decisions;
- known limitations;
- deferred work;
- repair/recovery lessons;
- next-version Research seed.

This package is knowledge, not next Scope.

## 24. Provider and Model Neutrality

Model capability affects cost and reasoning quality.

It does not grant workflow authority.

Core authority must remain provider-neutral.

## 25. Human Ownership Principle

This Development Constitution is human-owned.

AI may read and use it.

AI must not change it unless the repository owner explicitly authorizes protected-area modification.

## 26. Change Governance

Material changes must consider:

- constitution impact;
- authority impact;
- architecture impact;
- token/cost impact;
- user approval impact;
- context impact;
- reliability;
- recovery/resume;
- migration;
- tests;
- docs.

Do not add roles, lifecycle stages, authority paths, prompts, aliases, or sources of truth merely because they simplify one local patch.

## 27. Direction of Travel

Project Template should move toward:

- richer but focused Research handoffs;
- stronger Planning finalization;
- less duplicated expensive reasoning;
- explicit user cost/authority gates;
- more deterministic execution authority;
- bounded low-cost implementation;
- durable failure evidence;
- safe resume/recovery;
- strong independent acceptance;
- durable next-version handoff;
- simpler user workflow.
