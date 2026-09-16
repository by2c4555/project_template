# PROCESS ISSUE

Run the Project Template v4.1 Research process in `ISSUE_DRIVEN_RESEARCH` mode.

Treat the supplied issue as an observation that requires investigation.

The issue may be:

- runtime error
- stack trace
- failed test
- production incident
- user-reported bug
- unexpected workflow behavior
- performance regression
- security report
- dependency incompatibility
- changed external API behavior
- deployment failure
- new platform constraint
- user feedback
- other real-world evidence

Follow `MASTER_RESEARCH_PROMPT.md`.

First capture the issue as unprocessed evidence under the conceptual `EXECUTE/research/inbox/**` layer.

Do not directly convert the reported symptom into a new requirement or technical solution.

Investigate:

1. What exactly happened?
2. Is the issue reproducible?
3. What evidence exists?
4. Which current requirement(s), assumption(s), interface(s), or environment constraints are affected?
5. Is the current project knowledge incorrect, incomplete, or still valid?
6. Does authoritative external documentation clarify the behavior?
7. Is a user product decision required?
8. Does the issue require:
   - no knowledge change
   - corrected raw knowledge
   - requirement clarification
   - new requirement
   - architecture reconsideration
   - Planning revision
   - implementation-only correction

Assign a stable issue identifier when useful, for example:

`ISSUE-001`

Record:

- issue type
- source
- observed behavior
- expected behavior, if verified
- reproducibility
- evidence
- affected requirements
- knowledge impact
- research result
- disposition

Disposition must be one of:

- resolved by new evidence
- resolved by user decision
- corrected prior knowledge
- still unresolved
- rejected as not applicable

If the issue changes authoritative knowledge, create the next:

`Research Vx+1`

Update:

- `EXECUTE/project_details.md`
- `EXECUTE/docs/raw/**`

Create immutable:

- `EXECUTE/research/Research_Vx+1.md`

If the issue does not require a Research revision, explain why and preserve it as issue evidence without manufacturing a new requirement.

Do not patch source code.
Do not create an Implementation Plan.
Do not automatically start Planning.
