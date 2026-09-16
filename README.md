# Project Template v4.3.2
## Machine-Governed Workflow & Token-Safety Architecture

Project Template v4.3.2 is a controlled, restartable engineering workflow for large AI-assisted software projects operated primarily inside **VS Code + Codex**.

The v4.3 design goal is not merely “better prompts”. It is to reduce the blast radius of an agent misunderstanding by moving workflow authority into Python state transitions and explicit human gates.

> **Agents produce work and evidence. Python grants authority. Natural-language chat never unlocks an expensive phase.**

Disk state is authoritative. Chat history is disposable.

---

# 1. Controlled boundary

ChatGPT Web UI or another external research surface may still be used to define product scope, future-version scope, or post-validation debug scope. That layer is intentionally manual and is **outside** the v4.3 controlled runtime.

```text
External Research / New Scope / Debug Scope
                │
                │ manual user handoff
                ▼
════════════════════════════════════════════
          v4.3 VS Code / Codex boundary
════════════════════════════════════════════
                │
          Change Cycle N
                │
          Codex Planning
                │
             PLAN_READY
                │
      human approve_plan.py
                │
        Local Execution
   Manager -> fresh Builder/Task
                │
        issue? hard pause
                │
      Codex Diagnosis only
                │
   human approve_recovery.py
                │
       Codex Recovery only
                │
       recovery_gate.py
                │
 human resume_execution.py
                │
       execution complete
                │
 human start_evaluation.py
                │
       Codex Evaluation
                │
   finalize_evaluation.py
                │
        CLOSED_VALIDATED
════════════════════════════════════════════
                │
        new external scope
                ▼
          Change Cycle N+1
```

A validated Cycle is never reopened for new work. New feature/version/refactor/newly discovered post-validation bug starts a new Cycle and receives a new Planning package and new approval.

---

# 2. Required tools

| Tool | Use |
|---|---|
| **Visual Studio Code** | Repository/workspace, terminal, Manager/Builder agents |
| **Codex** | Repository research, Planning, Diagnosis, Recovery, Evaluation |
| **VS Code Chat / Copilot custom-agent support** | `ProjectManager500K`, `Builder100K` |
| **Other Models / BYOK / Ollama / OpenRouter** | Optional local Manager/Builder model provider |
| **Python 3** | Authoritative workflow gates and validators |
| **Git** | Strongly recommended for baselines, diff review and audit |
| **ChatGPT Project or other Web AI (optional)** | External product/scope research using `EXECUTE/external_research/**` |

## External research setup (outside controlled runtime)

v4.3.2 uses a vendor-neutral **checkpointed External Research** layer. The web AI produces only the mutable handoff; Python creates local versioned Scope Snapshots.

```text
EXECUTE/external_research/RESEARCH_GUIDE.md
EXECUTE/external_research/setup/CHATGPT_INSTRUCTIONS.txt
EXECUTE/external_research/setup/EXTERNAL_INSTRUCTIONS_1000.txt
```

Use `RESEARCH_GUIDE.md` as the Project/Workspace knowledge resource. Paste the platform instruction appropriate for the service. The generic instruction is deliberately under 1,000 characters.

External Research should understand the problem, define requirements/scope/constraints/success criteria, collect high-value external/reference evidence, maintain resumable topic checkpoints when context grows, and refuse finalization while material product/scope gaps remain.

Final repository handoff only when ready:

```text
EXECUTE/project_details.md
EXECUTE/docs/raw/*        # only useful evidence
```

There is no `Research_Vx.md` in the v4.3.2 handoff. Web-chat working checkpoints such as `RESEARCH_INDEX.md`, topic files, and source notes are external working memory and do not automatically become Codex context.

Local model bindings are configured with:

```bash
python scripts/configure_models.py
python scripts/validate_v4.py
```

Minimum documented context floors:

```text
ProjectManager500K : 512000
Builder100K        : 102400
```

---

# 3. Authoritative state

The single authoritative workflow state is:

```text
EXECUTE/control/STATE.json
```

Every authoritative transition is appended to:

```text
EXECUTE/control/TRANSITIONS.jsonl
```

Human-readable files such as:

```text
EXECUTE/PROJECT_STATUS.md
EXECUTE/plan/PLANNING_STATUS.md
EXECUTE/execution/EXECUTION_STATE.md
EXECUTE/evaluation/EVALUATION_STATUS.md
```

are **generated views**. Editing those Markdown files does not grant authority.

Never hand-edit `STATE.json` to bypass a gate.

---

# 4. Human gates vs machine gates

v4.3 intentionally does **not** ask the user to approve every Task. Routine transitions remain automated, but expensive phase boundaries require an explicit operator action.

## Human-operated hard gates

| Boundary | Script |
|---|---|
| `PLAN_READY -> implementation authorized` | `python scripts/approve_plan.py` |
| Manager context batch exhausted -> fresh Manager | `python scripts/reset_manager_batch.py` |
| confirmed implementation defect -> broad Recovery authorized | `python scripts/approve_recovery.py` |
| verified execution recovery -> local Execution resume | `python scripts/resume_execution.py` |
| execution complete / re-evaluation -> one Evaluation attempt | `python scripts/start_evaluation.py` |

These scripts require a live interactive terminal challenge. There is no `--yes` flag and no static phrase such as `I_APPROVE_IMPLEMENTATION` that an agent can copy from source and submit non-interactively.

This is an accidental-flow/token-runaway barrier, not a security sandbox against a malicious process with full local-machine control.

## Machine gates

| Purpose | Script |
|---|---|
| Scope capture / revision | `start_cycle.py` / `import_scope.py` |
| Planning interaction / expansion / PLAN_READY | `planning_gate.py` |
| Task dispatch / repair counter / PASS / Issue / execution completion | `execution_gate.py` |
| Diagnosis registration + routing | `diagnosis_gate.py` |
| Recovery verification | `recovery_gate.py` |
| Evaluation result + Cycle close/Issue creation | `finalize_evaluation.py` |
| Builder context preflight | `context_guard.py` |
| Bounded command output | `safe_exec.py` |
| Template/state/invariant validation | `validate_v4.py` |

---

# 5. Initial template state

A fresh v4.3 package already contains initialized:

```text
EXECUTE/control/STATE.json
project_state = AWAITING_SCOPE_IMPORT
```

`init_v43.py` exists only to reconstruct state if creating a template manually; do not run it over an existing state file.

After External Research has produced a **READY_FOR_CODEX** handoff, copy:

```text
EXECUTE/project_details.md
EXECUTE/docs/raw/* declared in supporting_files
```

Then start the Cycle:

```bash
python scripts/start_cycle.py --title "Initial implementation"
```

`start_cycle.py` validates readiness and supporting files, then captures the mutable handoff into immutable history:

```text
EXECUTE/history/cycles/CYCLE_001/scope/SCOPE_001/
```

The Scope Snapshot receives a SHA-256 digest. Codex Planning is bound to that exact scope revision/digest. Editing root `project_details.md` later does not mutate the active Scope Snapshot.

For a material clarification/change **inside an open Cycle**, update the external handoff and capture it with:

```bash
python scripts/import_scope.py --reason "<why scope changed>"
```

This creates `SCOPE_002+`. If implementation was already approved, prior approval is superseded and replan/new approval is required.

A new Cycle can start only when the previous active Cycle is `CLOSED_VALIDATED`.

---

# 6. Step 1 — Codex Planning

**Tool:** Codex

Run:

```text
EXECUTE/codex/IMPLEMENTATION_RESEARCH_AND_PLANNING_PROMPT.md
```

Codex researches the repository against the active immutable Scope Snapshot. It reads the snapshot `project_details.md` first and follows its `Codex Context Map` so raw evidence is loaded selectively rather than wholesale.

## Material decision gate

If one or more material decisions remain:

```bash
python scripts/planning_gate.py hold-material-feedback --unknowns N
```

Codex asks focused questions and **ends the invocation**.

When the user later replies in Codex chat:

```bash
python scripts/planning_gate.py resume-feedback
```

If the existing draft must change materially:

```bash
python scripts/planning_gate.py begin-revision --reason "user feedback"
```

## Compile only after zero material unknowns

```bash
python scripts/planning_gate.py set-material-zero
python scripts/planning_gate.py authorize-expansion
```

Codex then compiles:

```text
EXECUTE/compiled/**
EXECUTE/plan/IMPLEMENTATION_PLAN.md
EXECUTE/tasks/TASK_INDEX.md
EXECUTE/tasks/TASK_NNN.md
```

Each generated Task is an **immutable contract**, not runtime state.

Runtime fields such as:

```text
PENDING
IN_PROGRESS
PASS
BLOCKED
PASS_RECOVERED
repair_attempts
dispatch_count
```

exist only in `STATE.json` after approval.

## PLAN_READY

When compilation is complete:

```bash
python scripts/planning_gate.py mark-plan-ready
```

This validates package metadata, creates a candidate SHA-256 manifest, changes state to `PLAN_READY`, and requires Codex to STOP.

### Important semantic change from v4.2.1

There is no separate:

```text
PLAN_REVIEW -> user accepts -> AWAITING_USER_APPROVAL
```

loop.

Instead:

```text
PLAN_READY
  ├─ user chat -> feedback/question/revision only
  └─ user runs approve_plan.py -> APPROVED
```

Even messages such as:

```text
approved
go ahead
looks good
implement it
continue
start now
```

remain ordinary feedback and carry **zero execution authority**.

---

# 7. Step 2 — Human implementation approval

**Tool:** VS Code terminal / user

Run manually:

```bash
python scripts/approve_plan.py
```

The script displays:

- active Cycle;
- Planning version/revision;
- Task count;
- exact package SHA-256;
- random interactive challenge.

On success it creates immutable approval/manifest records under:

```text
EXECUTE/control/approvals/
EXECUTE/control/manifests/
```

Approval is bound to one exact Cycle and package.

Before every later execution/recovery/evaluation transition, the package digest is rechecked. If an approved Plan/Task/compiled artifact changes:

```text
PACKAGE_INTEGRITY: FAIL
```

and work stops.

---

# 8. Step 3 — Local Execution

**Tool:** VS Code `ProjectManager500K`

Use:

```text
EXECUTE_PROJECT_PROMPT.md
```

Manager first runs:

```bash
python scripts/execution_gate.py status
```

For each ready Task:

```bash
python scripts/execution_gate.py begin-task TASK_001
python scripts/context_guard.py EXECUTE/tasks/TASK_001.md
```

Then Manager invokes exactly one **fresh Builder100K**.

## Task success

Builder writes:

```text
EXECUTE/execution/evidence/TASK_001.md
```

Manager checks evidence, then:

```bash
python scripts/execution_gate.py complete-task TASK_001 \
  --evidence EXECUTE/execution/evidence/TASK_001.md
```

Only Python records PASS.

## Local repair budget

After failed verification, Builder must obtain one repair authorization per code-repair attempt:

```bash
python scripts/execution_gate.py authorize-repair TASK_001
```

The machine counter enforces the Task's repair limit. A denied repair token is a hard stop.

## Ordinary dispatch is one-time

An approved Task may be ordinarily dispatched only once. Recovery uses the separate Recovery contract rather than spawning repeated ordinary Builders for the same Task.

---

# 9. Manager context circuit breaker

Even though Builders are fresh, a Manager chat can accumulate context across many Tasks.

Default policy:

```text
manager_max_task_dispatches_per_batch = 10
```

When the batch is exhausted, `begin-task` returns:

```text
MANAGER_CONTEXT_RESET_REQUIRED
```

Manager must STOP.

User then ends the old Manager conversation, manually runs:

```bash
python scripts/reset_manager_batch.py
```

and starts a **fresh** ProjectManager500K conversation.

This is not a new implementation approval. It is a token/context circuit breaker.

Policy is stored in:

```text
EXECUTE/control/STATE.json -> runtime_policy
```

---

# 10. Bounded tool output

Large build/test/compiler logs can consume context even when file input is well controlled.

Use:

```bash
python scripts/safe_exec.py --label TASK_001_TEST -- pytest -vv
```

Full output is persisted under:

```text
EXECUTE/execution/logs/TASK_001_TEST.log
```

The agent receives only a bounded head/tail summary plus exit code and log path.

Agents should load the full log only when evidence justifies it.

---

# 11. Step 4 — Execution incident

If Builder cannot complete after the machine-counted local repair budget, Manager calls:

```bash
python scripts/execution_gate.py fail-task TASK_017 \
  --evidence EXECUTE/execution/evidence/TASK_017.md \
  --reason "verified failure summary"
```

Python:

- marks runtime Task BLOCKED;
- allocates `ISSUE_NNNN`;
- sets execution `PAUSED_FOR_DIAGNOSIS`;
- blocks all normal dispatch;
- routes to Codex Diagnosis.

Manager then STOPs.

---

# 12. Step 5 — Diagnosis only

**Tool:** Codex

Run:

```text
EXECUTE/codex/ISSUE_DIAGNOSIS_PROMPT.md
```

Diagnosis may reproduce, inspect, analyze and propose. It **must not repair production code**.

Create immutable:

```text
EXECUTE/diagnostics/Diagnosis_Vx.md
```

Then register:

```bash
python scripts/diagnosis_gate.py \
  --issue ISSUE_NNNN \
  --diagnosis EXECUTE/diagnostics/Diagnosis_Vx.md \
  --classification IMPLEMENTATION_DEFECT
```

Classifications:

```text
IMPLEMENTATION_DEFECT
TASK_DEFECT
PLAN_DEFECT
EVALUATION_DEFECT
SCOPE_AMBIGUITY
EXTERNAL_BLOCKER
UNKNOWN
```

The old combined `ISSUE_DIAGNOSIS_AND_RECOVERY_PROMPT.md` is deliberately deprecated and hard-stops.

---

# 13. Step 6 — Human Recovery approval

For confirmed `IMPLEMENTATION_DEFECT`, user manually runs:

```bash
python scripts/approve_recovery.py
```

Approval binds to the immutable Diagnosis digest and active Issue.

Only then may Codex run:

```text
EXECUTE/codex/RECOVERY_PROMPT.md
```

Recovery performs the minimum complete root-cause repair and durable Resolution knowledge.

When verified:

```bash
python scripts/recovery_gate.py \
  --issue ISSUE_NNNN \
  --resolution EXECUTE/knowledge/resolutions/RESOLUTION_NNNN.md \
  --baseline "<verified baseline>" \
  --verification RECOVERY_PASS
```

Recovery verification **does not** set `resume_authorized: true`.

For an execution-origin issue, user manually runs:

```bash
python scripts/resume_execution.py
```

then starts a fresh Manager conversation.

For an evaluation-origin issue, successful Recovery returns to `AWAITING_EVALUATION_AUTHORIZATION`; it does not resume local Task execution.

---

# 14. TASK_DEFECT / PLAN_DEFECT

A defect in an approved Task/Plan cannot be silently patched into the approved package.

Diagnosis routes to replan. Run:

```bash
python scripts/start_replan.py
```

This:

- archives/supersedes old approval/execution authority;
- creates a new `Planning_Vx` inside the same open Cycle;
- returns to Codex Planning;
- requires a brand-new `approve_plan.py` after the new package reaches PLAN_READY.

Any approved package mutation therefore invalidates old execution authority by design.

---

# 15. Step 7 — Execution complete

When all approved Tasks are machine-state `PASS` or `PASS_RECOVERED`, Manager updates the Execution Summary and runs:

```bash
python scripts/execution_gate.py finalize-execution
```

Result:

```text
execution_status: AWAITING_EVALUATION
cycle: EXECUTION_COMPLETE
HARD STOP
```

Manager cannot start Evaluation.

---

# 16. Step 8 — Human Evaluation authorization

User manually runs:

```bash
python scripts/start_evaluation.py
```

One authorization creates exactly one Evaluation version/attempt.

Then run Codex with:

```text
EXECUTE/codex/EVALUATION_PROMPT.md
```

Evaluation is read-only with respect to production code and approved Planning artifacts.

Allowed results:

```text
PASS
PASS_WITH_FINDINGS
DIAGNOSIS_REQUIRED
```

Evaluation creates the authorized report and, for PASS/PASS_WITH_FINDINGS, a detailed Project Completion Report.

Then it calls the **machine** finalizer:

```bash
python scripts/finalize_evaluation.py \
  --evaluation Evaluation_Vx \
  --completion-report EXECUTE/evaluation/PROJECT_COMPLETION_REPORT_Vx.md
```

## PASS

The finalizer closes the Cycle:

```text
CLOSED_VALIDATED
AWAITING_NEW_SCOPE
```

The approval is recorded as consumed historical authority.

## DIAGNOSIS_REQUIRED

The finalizer creates an Evaluation-origin Issue and hard-stops to Diagnosis. There is no automatic repair or automatic re-evaluation chain.

After any correction, every new Evaluation attempt again requires the user to run `start_evaluation.py`.

---

# 17. Next version / post-validation debug

After Cycle N passes Evaluation, do **not** modify/reopen its Planning/Execution/Scope history.

Use the prior Completion Report as baseline context in External Research, combine it with the new feature/change/debug intent, and produce a new cumulative:

```text
EXECUTE/project_details.md
EXECUTE/docs/raw/*
```

Then start the next Cycle:

```bash
python scripts/start_cycle.py --title "Next version"
```

or:

```bash
python scripts/start_cycle.py --title "Post-validation defect fix"
```

The new Cycle captures a new `SCOPE_001` under its own cycle namespace and begins with:

```text
approval = none
execution = none
planning = new Planning_Vx
```

No approval or execution authority carries forward.

This distinction is critical:

```text
Evaluation has not passed yet -> stay in same Cycle through Diagnosis/Recovery/Replan/Re-evaluate
Evaluation already passed      -> new scope/debug = NEW EXTERNAL SCOPE -> NEW CYCLE
```

---

# 18. Package integrity model

Before Planning, Python captures and verifies the immutable Scope Snapshot. At `PLAN_READY`, Python binds the candidate package to the active Scope digest and computes a package manifest from:

```text
EXECUTE/compiled/**
EXECUTE/plan/IMPLEMENTATION_PLAN.md
EXECUTE/tasks/TASK_INDEX.md
all generated EXECUTE/tasks/TASK_NNN.md
```

At approval, the exact package manifest is stored under `EXECUTE/control/manifests/`. The approval record binds **both** the active `scope_digest` and exact `package_digest`.

Scope Snapshot integrity and package integrity are checked before Task execution, recovery verification, resume and evaluation.

Task contracts therefore must not contain mutable runtime fields.

---

# 19. Durable learning

Material execution/evaluation implementation defects preserve:

```text
ISSUE
  -> Diagnosis
  -> human Recovery approval
  -> verified Resolution
  -> Knowledge Index
```

History is evidence for future Planning/Evaluation, not permission to bypass current-cycle gates.

---

# 20. Validation and regression tests

Run:

```bash
python scripts/validate_v4.py
python -m unittest discover -s test/regression -p 'test_*.py'
```

A clean template should report:

```text
TEMPLATE_VALID: PASS (v4.3.2)
```

`validate_v4.py` checks structural v4.3 invariants, state schema, required scripts/prompts, human TTY gate markers, generated Task contract rules, package-integrity infrastructure and deprecated combined-recovery protection.

Regression tests exercise the machine state/package/gate helpers in isolated temporary copies rather than consuming the live project state.

---

# 21. Core v4.3 rules

```text
External Research owns WHAT / WHY / REQUIREMENTS / SCOPE / EVIDENCE / SUCCESS.
Python owns Scope versioning / snapshot / digest / authority.
Codex owns HOW / repository truth / implementation planning / Tasks.
```

- Incomplete external scope produces questions/research recommendations, not final artifacts.
- External Research is checkpointable; a fresh web chat must be able to resume from saved Index/Topic/Source files without the old conversation.
- `project_details.md` is the distilled mutable handoff; `docs/raw/*` is selective evidence, not a bulk dump.
- `start_cycle.py`/`import_scope.py` convert that handoff into an immutable `SCOPE_NNN` snapshot.
- `PLAN_READY` and implementation approval bind both exact Scope digest and exact package digest.
- Chat is feedback, never implementation authority.
- LLMs may produce artifacts/evidence; Python grants authoritative transitions.
- No approval or execution authority carries forward across Cycle boundaries.
- Expensive phases have machine/human circuit breakers and bounded retries/context.
