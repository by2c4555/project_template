# Prepared Project Knowledge Index

Knowledge status: NOT_REFINED
Knowledge revision: 0

This index stores durable **scope/repository/architecture knowledge compiled by External Agent Planning for the current Planning package**.

It is distinct from `EXECUTE/knowledge/KNOWLEDGE_INDEX.md`, which indexes verified reusable lessons from resolved execution/evaluation incidents.

## Allowed Status Values

- USER_STATED
- VERIFIED
- INFERRED
- UNKNOWN
- DISPUTED
- SUPERSEDED

## Entry Schema

```text
ID:
Title:
Status:
Source / Provenance:
Confidence:
Summary:
Implications:
Supersedes:
Revision:
```

## Entries

None yet.

## Rules

- Create stable IDs for important durable facts.
- Preserve provenance.
- Do not silently overwrite contradictory facts.
- Mark replaced facts SUPERSEDED when historical reasoning matters.
- Builders treat this index as read-only.
- Recovery lessons belong in `EXECUTE/knowledge/**`, not here.
