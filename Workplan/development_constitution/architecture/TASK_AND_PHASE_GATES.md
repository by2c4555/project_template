> PROJECT TEMPLATE DEVELOPMENT CONSTITUTION 1.2 — Human owned. AI may read and apply this guidance; modification requires explicit authorization from a trusted repository-owner channel covering the change.

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
- actual mutation manifest, including indirect/generated/rename/delete effects;
- normalized/symlink-resolved authorized-path compliance;
- artifact integrity;
- blocking issue state.

### 2.1 Minimum Verification Evidence

For each required check, retain the applicable:

- requirement/check identity and bound acceptance criterion;
- Task/Attempt/generation and authority bindings;
- relevant repository baseline and verification-input identity;
- actual command/tool invocation, working directory, and relevant toolchain/environment identity;
- execution time, exit status or tool outcome, and whether execution completed;
- durable output/artifact references and integrity metadata;
- collector provenance and any limitations, skipped checks, or incomplete output.

Capture secrets by reference or redaction, not as raw command/environment values. Record only environment details needed to interpret or reproduce the check.

Planning binds an assurance profile from `CONFORMANCE.md` to the work. Evidence detail scales to that profile and risk: an editorial check need not imitate a security release, while authority/security/migration work MUST include the applicable negative, interruption, replay, and recovery evidence. “Applicable” MUST be justified by the Task/Phase contract, not selected after seeing a result.

The gate must validate evidence against observations collected through the trusted runtime path. Builder summaries, self-authored success files, and self-reported mutation manifests are insufficient on their own. Mutation accounting must reconcile actual relevant before/after state, including generated or otherwise untracked effects.

### 2.2 Verification Outcomes

Distinguish successful, failed, not-run/skipped, interrupted/timed-out, and unknown checks. Only a completed check satisfying its bound acceptance criterion counts as successful. A zero exit code alone does not establish that required tests ran or assertions were evaluated.

Required checks that are unavailable, skipped, or inconclusive prevent PASS and route to repair, environment resolution, or authority revision as appropriate. Do not weaken the acceptance contract after failure to manufacture success.

Retries must follow the bound retry policy and preserve prior results. Do not repeatedly rerun a failing or flaky check until one success conceals the unresolved failure.

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

### 3.1 Fail-Closed Task Gate

Task Gate must reject rather than infer PASS when any authority-critical requirement is:

- missing;
- stale;
- ambiguous;
- mismatched;
- unverifiable.

An incomplete mutation manifest or uncertain mutation target cannot be treated as authorized.

Evidence must still apply to the state being accepted. A later edit to checked content or verification inputs requires affected checks to run again or a recorded justification that the change cannot affect those results. Keep historical PASS records as history; do not use stale results as current eligibility.

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

Gate PASS means the required bounded checks and evidence contract were satisfied. It is not proof of all product behavior or of the quality of the checks themselves. Independent Evaluation remains responsible for acceptance against Accepted Scope.

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
- mismatched Recovery binding;
- unknown/uncertain actual mutation boundary;
- unauthorized indirect or symlink-resolved mutation;
- evidence bound to the wrong repository/generation state;
- required checks skipped, timed out, never executed, or with unknown outcome;
- evidence or gate status self-issued by the Builder;
- relevant content changed after verification;
- acceptance weakened merely to convert a failed result into PASS.

## 8. Phase Progression

Only Phase Gate PASS makes dependent Phases eligible.

## 9. Phase Gate Fail-Closed Rule

Phase Gate must not infer integration/Phase PASS from partial Task success, missing evidence, or stale bindings.

If required Phase-level evidence cannot be positively validated, Phase does not PASS.

## 10. Evaluation Eligibility

Independent Evaluation is eligible only after all required Phase Gates PASS.

Conformance coverage: `C-005`, `C-008`, `C-010`, `C-011`, `C-016`.
