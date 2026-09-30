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
2. Call `review_org_identity` with `{}`. Require a `VERIFIED` result with
   `completeness.complete: true`, and compare `target.alias` exactly with the selected alias.
   Record `target.organizationId`, the reported environment and
   `sources.rest.retrievedAt`; compare an expected Org ID when supplied, accounting for
   Salesforce's 15- and 18-character forms. Use the reported `environmentType` and identity
   facts; `isSandbox: false` alone does not establish production. If identity cannot be
   established or the alias differs, stop before object or record reads and report that
   the connection must be restarted for the selected alias. Do not change authentication
   or fall back to a shell command.
3. Keep that target for subsequent calls. The custom MCP freezes its target at startup;
   individual read tools accept no org alias, username, or workspace directory. An alias
   supplied in chat cannot rebind the server. When the user asks which orgs are configured,
   `review_configured_orgs` with `{}` lists only locally configured aliases if scoped
   enumeration is enabled; it does not authenticate, switch target, or verify live identity.
4. Inspect an object's fields and relationships with `review_object_contract`, passing only
   `objectApiName`. Read `facts.object`, including `contestedProperties` and
   `sourceExclusive.rest`, and use only verified, uncontested properties. Use
   `review_installed_packages` with `{}` when package identity matters; its results are
   limited by the configured namespace scope. If further metadata is needed, compose a
   bounded `review_soql_query` with `query` and optional `useToolingApi: true` for the
   Tooling API. When component definitions are needed, use
   [retrieve-metadata](../retrieve-metadata/SKILL.md) after establishing identity;
   that skill owns local writes and completion checks. Report unavailable fields or
   definitions instead of inventing an object contract.
5. Check each evidence envelope's status, target, completeness, warnings, and observation
   time. `MISMATCH`, `INCOMPLETE`, and `BLOCKED` are not confirmed facts. Stop dependent
   reads on a failed contract or identity check; disclose permission and completeness gaps.
   For `RESULT_TRUNCATED`, discard the incomplete result and narrow the query; never
   silently widen scope or use raw output as a complete dataset. Stop if identity changes.

Use `explain_query` only when query-plan feedback is needed, with `query` and optional
`useToolingApi`; it does not execute the query. Use `org_limits` with `{}` only when API
budget information is relevant. These return timestamped diagnostics, not evidence envelopes
or proof of configuration behavior.

Return the verified target, available relevant capabilities, retrieval time, and limitations.
Discovery does not deploy, mutate records, create local Salesforce source, or manage orgs.
