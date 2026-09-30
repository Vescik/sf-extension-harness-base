---
name: review-org
description: Review scoped Salesforce configuration for admin teams using live read evidence or a local metadata snapshot.
user-invocable: false
---

# Review Salesforce configuration

Follow the [shared instructions](../../copilot-instructions.md). Review existing
configuration against the user's question and stated intended behavior. Keep
recommendations advisory; review does not authorize implementation.

## Choose the evidence mode

- **Local snapshot:** use the supplied files, directory, or manifest. No live org
  connection is required. Record the known source org and retrieval time; otherwise
  mark them unknown. File timestamps do not establish retrieval time. A manifest
  states requested scope, not proof that its components were retrieved.
- **Live org:** reuse the explicitly selected target and establish its identity with
  [org-discovery](../org-discovery/SKILL.md). Use bounded read queries and, where XML
  is needed, [retrieve-metadata](../retrieve-metadata/SKILL.md) for the minimum
  selected components. That skill prepares a command for an admin to run manually;
  continue metadata analysis only when its result and source files are available. Do not silently replace an inaccessible org with another.
- **Comparison:** identify each source and its observation time separately. Compare
  only overlapping components; do not present an old or mixed snapshot as live state.

If the question or scope is missing, ask only for what is needed to select evidence.
Review available local evidence while reporting any live evidence gap. Do not expand
into an entire-org audit because a referenced component is unavailable.

## Review

1. Use [inventory-force-app](../inventory-force-app/SKILL.md) when the selected files
   need an inventory or dependency summary. Distinguish selected, available, examined,
   and unresolved components. Absence from a snapshot is not absence from the org.
2. Apply only relevant sections of the [admin checklist](references/admin-checklist.md).
   Explain the behavior from concrete metadata or query evidence, including version,
   activation, assignments, and runtime context when they matter. Record unknowns.
3. Trace only dependencies needed to assess the selected behavior. Mark inferred
   references as inferred; missing targets may reflect partial retrieval or packages.
   Include Apex only when it materially explains an in-scope dependency, as read-only
   analysis. Do not turn this into a code implementation or test workflow.
4. For each material finding, give the condition, expected behavior or applicable
   rule, exact evidence, affected scenario, impact, and recommendation. Use high,
   medium, or low severity with a short impact rationale; do not invent an occurrence
   rate. Put unproven risks and questions in open items rather than confirmed defects.
5. Distinguish static configuration observations from demonstrated runtime behavior
   and effective access. Cite source paths and line numbers or bounded query results.
   Cite relevant official Salesforce documentation for platform rules; guidance alone
   is not evidence of an org defect. If a rule cannot be verified, qualify it.

## Result

Return a concise review in chat with scope, source identity and observation time,
material findings, open items, and limits. State which requested checks were actually
performed. “No findings in the examined scope” does not certify the org as safe or
prove successful execution, deployment readiness, or complete security coverage.

When the user requests a saved report, adapt [review-report.md](assets/review-report.md)
under ignored `output/` unless another destination is requested. Replace its placeholders
with evidence or explicit unknowns, omit irrelevant sections, and sanitize values.
Use a new filename; overwrite an existing report only when requested. Do not save a
report automatically or create supporting caches and registries.
