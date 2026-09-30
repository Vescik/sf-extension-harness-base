---
name: investigate-object
description: Investigate one Salesforce object's metadata and bounded record evidence.
argument-hint: "objectApiName=<API name> question=<question> [org=<alias>]"
agent: config-investigator
---

Use the [investigate-object skill](../skills/investigate-object/SKILL.md).
Require an object and question. Reuse the session's selected org or verify the explicitly
requested target. Use available read capabilities only and report capability gaps, evidence,
and limits. Respond in chat; save a report only when requested.
