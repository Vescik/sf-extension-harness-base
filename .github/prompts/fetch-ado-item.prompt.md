---
name: fetch-ado-item
description: Read an Azure DevOps work item and optionally its immediate parent and children.
argument-hint: "itemId=<ID> [project=<name>] [mode=single|hierarchy]"
agent: ado-analyst
---

Use the [fetch-ado-item skill](../skills/fetch-ado-item/SKILL.md).
Require a positive work-item ID, reuse established organization/project scope, and default to
`mode=single`. Return source requirements separately from interpretation, with revision,
retrieval time, and gaps. Save a report only when requested; do not start a delivery workflow.
