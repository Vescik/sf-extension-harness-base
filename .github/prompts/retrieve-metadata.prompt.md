---
name: retrieve-metadata
description: Retrieve selected Salesforce metadata into the local SFDX project for review.
argument-hint: "org=<alias> components=<Type:Name,...> or manifest=<path>"
agent: config-investigator
---

Use the [retrieve-metadata skill](../skills/retrieve-metadata/SKILL.md).
Resolve the exact org and component scope from the request. For named components,
prepare a small manifest; the MCP tool does not accept component names directly.
Protect existing local work, retrieve through MCP, and report actual completion and
gaps. A retrieve can update local files but never changes configuration in the org.
