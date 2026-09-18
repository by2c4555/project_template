> HUMAN-OWNED DEVELOPMENT CONSTITUTION — AI may read and use this file as development guidance, but MUST NOT edit, modify, rewrite, move, rename, or delete it.

# Task and Phase Gates

## 1. Purpose

Defines deterministic PASS authority.

## 2. Task Gate

Task Gate owns Task PASS.

Applicable validation:

- Task/Phase/Attempt identity;
- current generation;
- current valid ticket;
- Scope binding;
- Planning binding;
- Task binding;
- Recovery binding where applicable;
- verification result;
- evidence;
- mutation manifest;
- authorized-path compliance;
- artifact integrity;
- blocking issue state.

## 3. Task Gate PASS

Conceptually:

```text
valid authority
+
valid mutation boundary
+
successful required verification
+
required evidence
+
no blocking defect
=
Task PASS
```

## 4. Task Gate FAIL

Task Gate FAIL must produce durable failure evidence.

The failure may route to:

- Manager local repair;
- External Diagnosis;
- authority revision;
- owner action.

## 5. Phase Gate

Phase Gate owns Phase PASS.

Applicable validation:

- dependencies;
- all required Tasks PASS;
- Phase verification;
- Phase evidence;
- integration behavior;
- regression behavior;
- unresolved issues.

## 6. Gate Independence

Neither Manager nor Builder may grant PASS.

User approval does not grant PASS.

Planning does not grant PASS.

## 7. Negative Cases

Reject:

- stale generation;
- stale ticket;
- wrong Task/Attempt;
- verification missing;
- required evidence missing;
- unauthorized mutation;
- stale Scope/Planning binding;
- unresolved blocking issue;
- mismatched Recovery binding.

## 8. Phase Progression

Only Phase Gate PASS makes dependent Phases eligible.

## 9. Evaluation Eligibility

Independent Evaluation is eligible only after all required Phase Gates PASS.
