---
name: investigate-config-records
description: Inspect bounded Salesforce configuration or reference records for a specific question.
argument-hint: "objectApiName=<API name> question=<question> [org=<alias>] [fields=<A,B,C>]"
agent: config-investigator
---

Use the [investigate-config-records skill](../skills/investigate-config-records/SKILL.md).
Require an object and question. Verify the selected org and requested fields before reading a
small relevant sample. Return observations separately from inferred behavior, including
capability gaps and limits. Respond in chat; save a report only when requested.
