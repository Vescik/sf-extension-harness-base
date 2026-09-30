---
name: retrieve-metadata
description: Retrieve explicitly scoped Salesforce metadata into this SFDX project for an admin investigation or review, preserving existing local work.
user-invocable: false
---

# Retrieve metadata for review

Follow the [shared instructions](../../copilot-instructions.md). This is a read of
the selected org that can create or overwrite local source files. It is available
to `config-investigator` and `admin-reviewer`; it does not deploy or fix configuration.

## Establish the target and scope

1. Resolve this workspace's SFDX root from `sfdx-project.json`, its package directories,
   default package, and API version. Use the absolute root as the tool's `directory`.
   Verify the explicit org via the identity steps in [org-discovery](../org-discovery/SKILL.md).
   A request for an offline review does not authorize a live retrieve.
2. Accept an existing manifest, named metadata components, or specific existing source
   paths. For a live review, select the minimum components needed for the stated scope.
   Ask only if the target or scope is materially ambiguous. A vague request to review
   an org is not permission to retrieve every component or all remote changes.
3. Read a supplied manifest before using it: check its metadata types, members, API
   version, and actual scope. The starter `manifest/package.xml` selects every
   `CustomObject`; never treat it as an automatically approved review scope.
   Use wildcards only when the user requested all components of those exact types.
4. When component names are supplied, write a small manifest to a new, unused
   `output/retrieval/<descriptive-name>.xml` using the standard Metadata API namespace
   and the project's API version. Group members by metadata type and XML-escape
   names. Reuse an existing manifest only if its contents match; do not overwrite an
   unrelated manifest. This temporary input file is part of the requested retrieval,
   not a review report or a maintained registry.

## Protect local files and retrieve

5. Inspect the selected local components in all package directories and any available
   working-tree changes, including relevant untracked and ignored files. Do not silently overwrite
   local edits or mix metadata from different orgs. If affected existing files cannot
   be shown to be safe to refresh, have the user preserve them or explicitly authorize
   their replacement. Reuse authorization already given for that exact scope; empty
   destinations do not need this question. Never reset, delete, or stash user work.
6. Call `salesforce/retrieve_metadata` using its actual schema:
   - `directory`: the absolute SFDX project root;
   - `usernameOrAlias`: the verified explicit target;
   - exactly one of `manifest` (absolute XML path) or `sourceDir` (a nonempty array of
     absolute paths to the selected existing components);
   - `ignoreConflicts: false`.
   Do not supply invented `metadata`, `outputDir`, or job-resume arguments. Keep paths
   within this workspace. Never omit both selectors: upstream's default can include
   remote deletions and broader source-tracked changes. Do not select the whole source
   root when only named components were requested.
7. The tool writes source into the project and can merge existing components. Its
   conflict check depends on source tracking; `ignoreConflicts: false` is not proof
   that every org protects local edits. Do not enable conflict bypass or treat a
   warning, partial result, or transport error as success.

## Verify the result

8. Check the returned success/status, component messages, and actual resulting files.
   Match files and components to the requested scope; account for decomposed metadata
   and companion files. A success flag does not prove that every requested property
   was returned. Report missing members and retrieval-dependent omissions, including
   profile permissions whose coverage depends on the other components retrieved.
9. The pinned tool waits up to ten minutes. If it times out or completion is uncertain,
   report the operation as incomplete, preserving any returned job ID and known file
   state. Do not blindly retry. The core `resume_tool_operation` tool does not support
   retrieves and is intentionally excluded from these agents. Further completion
   checking needs the admin's normal Salesforce tooling; never invent a completed job.

Return the org alias and observed Org ID, retrieval time, manifest or source selection,
result status, changed files, missing components, and remaining uncertainty in chat.
Use [inventory-force-app](../inventory-force-app/SKILL.md) when a component summary
helps the next review step. Save a separate report only if requested. Do not create
an automatic knowledge store, source snapshot ledger, or publish retrieved content.
