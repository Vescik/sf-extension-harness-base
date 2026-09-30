---
name: investigate-config-records
description: Inspect a bounded set of Salesforce configuration or reference records, such as statuses, settings, templates, or routing rules.
user-invocable: false
---

# Investigate configuration records

Follow the [shared instructions](../../copilot-instructions.md) and
[org-discovery](../org-discovery/SKILL.md). Require one object API name and a specific question;
accept optional field names and reuse the selected session target.

1. Call `salesforce/review_object_contract` with the exact `objectApiName` and inspect
   `facts.object`. Confirm that requested fields exist and are not contested; choose only
   those needed to explain the configuration. Preserve missing or access-dependent traits.
   When metadata consumers are needed to explain behavior, inspect the relevant
   local source or use [retrieve-metadata](../retrieve-metadata/SKILL.md) for that scope.
2. Use `salesforce/review_soql_query` with `query` and optional `useToolingApi` only.
   Include an explicit `LIMIT`, bounded filters, and deterministic ordering where supported.
   Start with at most 5 rows; expand toward 20 only when the question requires it and explain
   the expansion. The MCP returns unredacted rows in `facts.soqlQuery.records`; select only
   useful values for the answer. Follow discovery's envelope and truncation checks.
   Report unavailable capabilities without substituting CLI calls.
3. Inspect related configuration only when it explains the selected records, with at most
   5 lookup edges and depth 2. Do not enumerate unrelated objects or export complete datasets.
4. Distinguish configured values from verified behavior. A setting's label or value alone does
   not prove what automation consumes it. Report missing evidence, permissions, and incomplete
   pagination; zero visible records does not prove the configuration is absent.

Return the verified org, object, retrieval time, field selection and bounds, findings, sources,
and limitations. Omit secrets and unnecessary personal data. Respond in chat; save a sanitized
report under `output/` only when requested. Do not change configuration or records.
