---
name: org-discovery
description: Establish the selected Salesforce org and available read-only MCP capabilities before answering an org-specific question.
---

# Discover a Salesforce org

Follow the [shared instructions](../../copilot-instructions.md). Use only read capabilities
exposed by the `salesforce` MCP server; inspect its actual tool schemas.

1. State the question and minimum evidence needed. Reuse the explicitly selected org from this
   session unless the user changes it. If no target is selected, ask for the org alias or
   identifier; do not silently choose a default or another authenticated org.
2. Use `run_soql_query` with the explicit `usernameOrAlias` and absolute workspace `directory`.
   When the username is unclear, `get_username` can resolve the single allowed org using that
   `directory`; keep `defaultTargetOrg` and `defaultDevHub` false. It does not accept an org
   argument and is not a live identity check. Verify identity with
   `SELECT Id, Name, IsSandbox FROM Organization LIMIT 1` using `useToolingApi: false`.
   Compare an expected Org ID when supplied. Record the returned identity; `IsSandbox=false`
   alone does not establish production. If the target differs or its identity cannot be
   established, report the gap before reading business data. Do not change authentication or
   fall back to a shell command.
3. Keep the same verified target for subsequent calls. If the server binds its target at startup,
   report when a connection change is needed; an alias supplied in chat does not rebind it.
4. Inspect relevant objects and fields through bounded metadata queries, such as
   `EntityDefinition` or `FieldDefinition`, where the tool and API support them. Check the real
   `run_soql_query` schema before choosing API options. Use `useToolingApi: true` for Tooling
   API metadata queries and constrain `FieldDefinition` to the selected entity. There is no
   general runtime describe tool in this base. When component definitions are needed,
   use [retrieve-metadata](../retrieve-metadata/SKILL.md) after establishing identity;
   that skill owns local writes and completion checks. If available metadata cannot
   establish the fields or relationships required for a record query, report that
   limitation instead of inventing the object contract.
5. Treat observations as specific to the retrieval time and current access. Disclose permission
   gaps and incomplete results. Stop if target identity changes during the investigation.

Return the verified target, available relevant capabilities, retrieval time, and limitations.
Discovery does not deploy, mutate records, create local Salesforce source, or manage orgs.
