---
name: retrieve-metadata
description: Prepare a scoped manual retrieval command and inspect the resulting Salesforce metadata for review.
argument-hint: "org=<alias> components=<Type:Name,...> or manifest=<path>"
agent: config-investigator
---

Use the [retrieve-metadata skill](../skills/retrieve-metadata/SKILL.md).
Verify the selected MCP-bound org and resolve the exact component scope. Protect
existing local work, then prepare a narrow `sf project retrieve start` command with
explicit metadata names or a vetted manifest, the target alias, and `--wait 10`.
The admin runs the command manually; these agents have no retrieval or terminal
tool. After the admin supplies the result, inspect available files and report
completion evidence and gaps. Do not claim retrieval from command preparation.
