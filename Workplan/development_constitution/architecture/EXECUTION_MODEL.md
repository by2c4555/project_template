> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Execution Model

## 1. Purpose

Defines production execution after:

```text
Accepted Scope
+
Validated Planning Package
+
valid User Execution Approval
+
PLAN_READY
```

## 2. Environment

```text
VS Code
+
Copilot Agent
+
ExecutionManager
+
Builder
```

## 3. Execution Hierarchy

```text
Cycle
  └─ Phase
      └─ Task
          └─ Attempt
```

Attempt kinds:

```text
INITIAL
REPAIR
RECOVERY
```

## 4. Manager

Manager owns:

- deterministic route invocation;
- execution coordination;
- Task-local reasoning;
- local debugging;
- failure interpretation;
- repair strategy;
- Builder supervision;
- escalation recognition.

Manager is not the normal production editor.

## 5. Builder

Builder owns bounded execution:

- CLI;
- authorized file operations;
- straightforward code changes;
- configuration edits;
- Manager-defined repairs;
- verification commands;
- evidence production.

Builder must stop on unexpected failure.

## 6. Builder Prohibitions

Builder must not:

- expand Scope;
- expand Task objective;
- expand write paths;
- choose lifecycle stage;
- grant PASS;
- self-authorize retry;
- create open-ended repair loops;
- invoke unrestricted subagents.

## 7. Ticket Model

A Builder dispatch should bind applicable:

- Cycle;
- Phase;
- Task;
- Attempt;
- generation;
- Scope revision/digest;
- Planning revision/digest;
- approval envelope;
- authorized paths;
- required context;
- verification;
- evidence.

## 8. Fresh Attempt Rule

Every Builder dispatch creates a fresh Attempt.

Never overwrite previous failed Attempt evidence.

## 9. Completion

Builder completion is input to Task Gate.

```text
Builder done
≠
Task PASS
```

## 10. Execution Exit

Execution completes only when all required Phase Gates pass and no blocking issue remains.

Then Independent Evaluation becomes eligible.
