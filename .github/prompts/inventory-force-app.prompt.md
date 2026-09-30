---
name: inventory-force-app
description: List local Salesforce metadata and visible references for an admin review.
argument-hint: "[scope=<types, objects, or folders>] [question=<review question>]"
agent: config-investigator
---

Use the [inventory-force-app skill](../skills/inventory-force-app/SKILL.md).
Inspect the configured local SFDX source within the requested scope. Report logical
components, source paths, visible references, snapshot provenance, and missing evidence.
Local inventory works offline. Compare with an org only when explicitly requested.
Respond in chat; save a report only when requested.
