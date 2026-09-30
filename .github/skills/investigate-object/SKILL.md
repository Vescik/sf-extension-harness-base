---
name: investigate-object
description: Explain a Salesforce object's available metadata and bounded record evidence for a specific question.
user-invocable: false
---

# Investigate a Salesforce object

Follow the [shared instructions](../../copilot-instructions.md) and
[org-discovery](../org-discovery/SKILL.md). Require one object API name and a question; use the
org already selected in the session or the user's explicit target.

1. Call `salesforce/review_object_contract` with the exact `objectApiName` and inspect
   `facts.object`. Confirm field and relationship names before using them; do not treat
   null or contested properties as established values. Read describe-only traits from
   `sourceExclusive.rest` with their access context. Use `review_installed_packages`
   with `{}` when package identity is relevant, preserving its configured namespace scope.
   Explain inaccessible definitions or package details rather than assuming behavior.
   If the question needs full component definitions, read the relevant local source
   or use [retrieve-metadata](../retrieve-metadata/SKILL.md) for the minimum current
   metadata needed. State whether the evidence is local or freshly retrieved.
2. If records are needed, use `salesforce/review_soql_query` with `query` and optional
   `useToolingApi` only. Select a few fields that answer the question and include an explicit
   `LIMIT`: start with at most 5 rows and increase toward 20 only when useful, explaining
   the reason. Use filters and ordering supported by the verified schema. The MCP runs
   the query verbatim and returns unredacted rows in `facts.soqlQuery.records`; select
   only useful values for the answer. Follow discovery's envelope and truncation checks.
3. Follow relationships only when they materially answer the question, with at most 5 relevant
   lookup edges and depth 2. Stop when required read capabilities are unavailable.
4. Separate metadata facts, record observations, and inferred business meaning. A small sample
   or zero visible rows does not establish universal behavior or global absence.

Return findings, verified org and object, retrieval time, selected fields and query bounds,
sources, and limitations. Prefer counts or categorical summaries when actual record values are
unnecessary. Respond in chat; save a sanitized report under `output/` only when requested.
