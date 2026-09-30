---
name: review-org
description: Review selected Salesforce configuration for an admin team.
argument-hint: "question=<review question> scope=<components, local paths, or manifest> [org=<alias>]"
agent: admin-reviewer
---

Use the [review-org skill](../skills/review-org/SKILL.md). Review the selected org
configuration or local snapshot for the stated question. Reuse explicit scope;
local review does not require a live connection. Return findings, evidence, open
items, and limits in chat. Save a report only when requested.
