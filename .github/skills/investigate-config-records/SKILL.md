---
name: investigate-config-records
description: Inspect a bounded set of Salesforce configuration or reference records, such as statuses, settings, templates, or routing rules.
user-invocable: false
---

# Investigate configuration records

Follow the [shared instructions](../../copilot-instructions.md) and
[org-discovery](../org-discovery/SKILL.md). Require one object API name and a specific question;
accept optional field names and reuse the selected session target.

1. Check the object's metadata through bounded metadata SOQL supported by
   `salesforce/run_soql_query`, such as `EntityDefinition` or `FieldDefinition`. Confirm that
   requested fields exist and choose only those needed to explain the configuration.
2. If a record-read capability is available, use bounded filters and deterministic ordering
   where supported. Start with at most 5 rows; expand toward 20 only when the question requires
   it and explain the expansion. Report unavailable capabilities without substituting CLI calls.
3. Inspect related configuration only when it explains the selected records, with at most
   5 lookup edges and depth 2. Do not enumerate unrelated objects or export complete datasets.
4. Distinguish configured values from verified behavior. A setting's label or value alone does
   not prove what automation consumes it. Report missing evidence, permissions, and incomplete
   pagination; zero visible records does not prove the configuration is absent.

Return the verified org, object, retrieval time, field selection and bounds, findings, sources,
and limitations. Omit secrets and unnecessary personal data. Respond in chat; save a sanitized
report under `output/` only when requested. Do not change configuration or records.
