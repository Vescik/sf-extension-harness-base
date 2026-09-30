---
name: inventory-force-app
description: Inventory local Salesforce metadata and visible dependency references for a scoped admin review.
user-invocable: false
---

# Inventory Salesforce metadata

Follow the [shared instructions](../../copilot-instructions.md). A local inventory is
valid offline; it does not require org access, terminal commands, or a generated index.

1. Resolve the SFDX project root and read `sfdx-project.json`. Use its
   `packageDirectories` as source roots; the starter has only `force-app`.
   Keep the user's requested types, objects, folders, and review question as scope.
   If scope is unspecified, first summarize locally available types and ask which
   area to inspect when a detailed inventory would be too large. State any bounds.
2. Use built-in file reading and search to inspect the selected metadata. Derive
   logical component types and names from metadata XML and source layout, not file
   counts alone. Include parent object names for decomposed fields, validation
   rules, record types, and other object children. A component may span files.
   Exclude `.gitkeep` and other scaffold placeholders from component counts.
3. Cover relevant available metadata, including objects and their children, Flow,
   permission sets and groups, profiles, layouts, FlexiPages, custom metadata
   records, and integration configuration. Report unfamiliar formats as unclassified;
   do not silently drop them or invent component identities. Never extract secrets.
4. Record explicit references visible in inspected contents, such as a Flow's
   subflow or object reference, a layout field, an assigned permission set, or a
   named credential reference. Identify the source path and referenced API name;
   mark unresolved targets without declaring them absent from the org.
5. State the snapshot's supplied org and retrieval time, or `unknown` when unavailable.
   Local presence proves only presence in this snapshot. Missing files do not prove
   org absence. Manifest members and wildcards express requested retrieval scope;
   they do not establish a complete org snapshot or a complete dependency graph.
   Dynamic references, unavailable metadata, access limits, and profile retrieval
   scope can leave gaps. Keep those limits distinct from what was actually inspected.
6. Compare with live state only when explicitly requested. Start with
   [org-discovery](../org-discovery/SKILL.md), then use relevant exposed MCP reads or
   [retrieve-metadata](../retrieve-metadata/SKILL.md) within the requested scope.
   Do not automatically retrieve metadata or broaden the org review.

Return the inspected scope and provenance, a concise table of **type / component
name / source path**, visible references with their source paths, and material gaps.
Separate observed references from inferred relationships. Keep results in chat;
save a sanitized report under `output/` only when requested.
