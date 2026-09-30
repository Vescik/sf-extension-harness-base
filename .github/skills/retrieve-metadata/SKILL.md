---
name: retrieve-metadata
description: Prepare a scoped manual Salesforce CLI retrieval for admin review, then inspect the reported result and local files.
user-invocable: false
---

# Retrieve metadata for review

Follow the [shared instructions](../../copilot-instructions.md). The custom
Salesforce MCP exposes seven read tools and does not retrieve metadata. This skill
prepares a command for the admin to run manually, then inspects the available
result and local source. Neither agent has terminal access or a retrieval tool.
A retrieve reads the org but can create or overwrite local source files; it does
not deploy or fix configuration.

## Establish the target and scope

1. Resolve this workspace's SFDX root from `sfdx-project.json`, its package directories,
   default package, and API version. State the absolute root as the directory where
   the admin must run the command. Follow [org-discovery](../org-discovery/SKILL.md):
   call `review_org_identity` with `{}`, require a complete `VERIFIED` result, and
   match `target.alias` exactly to the requested alias before preparing a command
   for execution. Record the returned Org ID and observation time. A different alias
   requires restarting the MCP connection for that target; do not use manual CLI as
   a workaround for a failed identity check. An offline review needs no live retrieve.
2. Accept an existing manifest, named metadata components, or specific existing source
   paths. For a live review, select the minimum components needed for the stated scope.
   Ask only if the target or scope is materially ambiguous. A vague request to review
   an org is not permission to retrieve every component or all remote changes.
3. Read a supplied manifest before using it: check its metadata types, members, API
   version, and actual scope. The starter `manifest/package.xml` selects every
   `CustomObject`; never treat it as an automatically approved review scope.
   Use wildcards only when the user requested all components of those exact types.
4. For a few named components, prepare one `--metadata 'Type:Member'` argument per
   component. Resolve supplied source paths to exact component types and names before
   using them; do not replace a narrow path with the entire source root. If a manifest
   is clearer, write a small one to a new, unused
   `output/retrieval/<descriptive-name>.xml` using the standard Metadata API namespace
   and the project's API version. Group members by metadata type and XML-escape names.
   Reuse a manifest only if its contents match; do not overwrite an unrelated one.
   This temporary input file is part of the requested preparation, not a review report.

## Protect local files and prepare the command

5. Inspect the selected local components in all package directories and any available
   working-tree changes, including relevant untracked and ignored files. Do not silently overwrite
   local edits or mix metadata from different orgs. If affected existing files cannot
   be shown to be safe to refresh, have the user preserve them or explicitly authorize
   their replacement. Reuse authorization already given for that exact scope; empty
   destinations do not need this question. Never reset, delete, or stash user work.
6. Show one command for the admin to run from the verified SFDX root, with the exact
   alias, one selector mode, and an explicit wait limit:

   ```sh
   sf project retrieve start --metadata 'Flow:Case_Routing' --metadata 'PermissionSet:Support_User' --target-org 'team-sandbox' --wait 10
   ```

   Or use `--manifest '/absolute/project/output/retrieval/review.xml'` instead of
   all `--metadata` arguments when the vetted manifest defines the scope. Replace
   every example value with the verified target and requested components. Shell-quote
   literal arguments safely; never interpolate unchecked text as shell syntax.
   Include `--api-version` with the project's declared version when needed to make
   the API version explicit. Keep manifest paths within the workspace. Never omit
   the selector, rely on the default org, add `--ignore-conflicts`, or select all
   metadata merely because the starter manifest contains a wildcard.
7. State that the command is prepared and must be run by the admin. Do not execute it
   through a terminal, raw HTTP request, another connector, or an invented MCP tool.
   Salesforce CLI can merge or overwrite existing source. Its conflict protection
   depends on source tracking and does not protect all orgs, including production.
   Present unresolved local-file risks before execution; retain the protections in
   step 5. Ask the admin to return the command result and make the resulting files
   available for inspection. Preparation alone is not successful retrieval.

## Verify the result

8. After the admin reports execution, inspect the supplied status and component
   messages, then read the actual resulting files using available local read tools.
   Match files and components to the requested scope; account for decomposed metadata
   and companion files. A success flag does not prove that every requested property
   was returned. Report missing members and retrieval-dependent omissions, including
   profile permissions whose coverage depends on the other components retrieved.
   Distinguish admin-reported completion from files independently inspected. Existing
   files alone do not prove this retrieval completed or establish its org provenance.
9. `--wait 10` lets the CLI return before a long job finishes. On timeout, partial
   results, errors, or missing completion evidence, report the operation as incomplete
   and retain any returned job ID and known file state. Do not blindly prepare a retry.
   The admin must check completion using their Salesforce tooling and provide the
   result. Never invent a completed job or infer retrieval time from file presence.

Return the org alias and observed Org ID, identity-check time, exact component or
manifest selection, and prepared command in chat. Once execution is reported, add
its reported retrieval time and status, inspected files, missing components, and
remaining uncertainty; keep unknown values explicit.
Use [inventory-force-app](../inventory-force-app/SKILL.md) when a component summary
helps the next review step. Save a separate report only if requested. Do not create
an automatic knowledge store, source snapshot ledger, or publish retrieved content.
