---
name: investigate-object
description: Explain a Salesforce object's available metadata and bounded record evidence for a specific question.
user-invocable: false
---

# Investigate a Salesforce object

Follow the [shared instructions](../../copilot-instructions.md) and
[org-discovery](../org-discovery/SKILL.md). Require one object API name and a question; use the
org already selected in the session or the user's explicit target.

1. Inspect the object's available metadata and relevant fields through bounded metadata SOQL
   supported by `salesforce/run_soql_query`, such as `EntityDefinition` or `FieldDefinition`.
   Confirm field and relationship names before using them. Explain any inaccessible
   definitions or package details rather than assuming their behavior.
   If the question needs full component definitions, read the relevant local source
   or use [retrieve-metadata](../retrieve-metadata/SKILL.md) for the minimum current
   metadata needed. State whether the evidence is local or freshly retrieved.
2. If records are needed and a read tool exists, select a few fields that answer the question.
   Start with at most 5 rows; increase toward 20 only when useful and explain the reason. Use
   filters and ordering supported by the actual schema, and preserve pagination limitations.
3. Follow relationships only when they materially answer the question, with at most 5 relevant
   lookup edges and depth 2. Stop when required read capabilities are unavailable.
4. Separate metadata facts, record observations, and inferred business meaning. A small sample
   or zero visible rows does not establish universal behavior or global absence.

Return findings, verified org and object, retrieval time, selected fields and query bounds,
sources, and limitations. Prefer counts or categorical summaries when actual record values are
unnecessary. Respond in chat; save a sanitized report under `output/` only when requested.
