# Setup

## Prerequisites

- VS Code with GitHub Copilot Chat and access to custom agents, prompts, skills, and MCP.
- Node.js 22.12 or later on the 22.x line, or Node.js 24 LTS, with `npx` available
  on the PATH used by VS Code.
- Access to one Azure DevOps organization and project.
- Salesforce CLI, with the intended org already authenticated under an explicit
  alias or username. Perform sign-in yourself using your team's normal procedure.

Open this repository folder directly. Do not open its parent workspace. Parent
repository customization discovery is disabled in [.vscode/settings.json](.vscode/settings.json).
The repository root contains the SFDX project. There is no package-level `npm install`,
Python environment, build, or setup script. The first MCP startup uses `npx` to
download the vendor servers.

The input prompts in this configuration use VS Code's extension-host MCP support.
For an Agent Host session, replace the two `${input:...}` arguments in your team's
copy with explicit non-secret org identifiers and remove `inputs`, then verify that
both servers are available. VS Code does not forward interactive-input servers to
Agent Host; see the [MCP configuration reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

## Start the two connections

1. Open [.vscode/mcp.json](.vscode/mcp.json) in VS Code and start `ado`.
   Enter the organization slug, not a full URL, project name, or token. Complete the
   vendor's interactive sign-in. The project is supplied in chat or prompt arguments;
   it is not a server command-line argument.
2. Start `salesforce` and enter exactly one authenticated Salesforce alias or username.
   Avoid default-target sentinels, comma-separated lists, or wildcard org selection.
3. Select the matching custom agent. Include the ADO project and organization, or
   Salesforce alias, in the task context. Reuse that scope for the conversation.
4. When changing organization or org, update the corresponding input value and
   restart the affected MCP server. If the host keeps the old value, rename that
   input's `id` and its matching `${input:...}` reference together so it prompts
   again. Establish the new scope before further reads.

Authentication belongs to the vendor tools and the host. Do not store tokens,
passwords, or auth exports in this repository. The two input values are identifiers,
not credentials.

## Prepare local metadata for an admin review

Install the recommended Salesforce and XML extensions. Open this folder directly
so the Salesforce extension finds [sfdx-project.json](sfdx-project.json).
The restored project retains source API version `67.0`; select a compatible version
for your target org if required, keeping the project and manifest aligned.

Use `/retrieve-metadata` with the already authenticated org's explicit alias and
named components, or an existing manifest. The skill verifies identity, inspects
local files, prepares a small manifest when needed, and calls `retrieve_metadata`.
For example:

```text
/retrieve-metadata org=team-sandbox components=Flow:Case_Routing,PermissionSet:Support_User
```

Replace the sample alias and names with the intended target and scope. The MCP tool
accepts an absolute `manifest` path or a `sourceDir` array, never both. There is no
component-name or output-directory parameter. A generated manifest goes under
ignored `output/retrieval/`; retrieved metadata goes into the SFDX source tree.
Review relevant existing files before retrieval: the tool can overwrite or merge
local source, and `ignoreConflicts: false` only protects tracked conflicts where
source tracking is supported. Preserve local work if its safety cannot be established.
The skill never calls retrieve without an explicit selector.

After completion, check component messages and resulting files. The current vendor
tool waits up to ten minutes. A timeout or uncertain result stays incomplete: the
registered core `resume_tool_operation` does not handle retrieves and is excluded
from the bundled agents. Do not blindly retry or infer success from partial files.
An admin can check the operation using their normal Salesforce tooling.

For manual retrieval, edit [manifest/package.xml](manifest/package.xml) to select
components needed for the review. The inherited `CustomObject:*` entry is a broad starter, not a complete
org manifest. Include other required metadata types and prefer named components
when the review is narrower. Then run this manually from the project root:

```sh
sf project retrieve start --manifest manifest/package.xml --target-org YOUR_ORG_ALIAS
```

Replace `YOUR_ORG_ALIAS` with the intended target. This reads org metadata into the
local project; review existing local files before retrieval because they can change.
Check the CLI result and pass the target, retrieval time, component scope, and any
gaps to the investigator. Do not treat a partial retrieve as a complete org snapshot.
The [Salesforce retrieve reference](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_project_retrieve_start.html)
describes supported flags and local conflict behavior.

The bundled agents can read the resulting files and use only MCP for external
calls. The investigator and reviewer can retrieve within the selected scope; an
explicitly offline review performs no live calls. The scratch-org
definition is retained for teams that need a disposable environment, and the Apex
Replay Debugger launch configuration is available for existing logs. No org is
created, retrieved, or changed by opening this template.

## Tool surface

The top-level npm versions are pinned in the MCP configuration:

| Server | Package | Configuration |
| --- | --- | --- |
| `ado` | `@azure-devops/mcp@2.10.0` | `work-items`, `wiki`, and `search` domains |
| `salesforce` | `@salesforce/mcp@0.30.15` | One explicit org; `run_soql_query,retrieve_metadata`; telemetry disabled |

The ADO analyst exposes four read tools: `search_wiki`, `search_workitem`, `wiki`,
and `wit_work_item`. In this version, wiki and work-item operations use an `action`
argument on the consolidated tool. Earlier individual tool names are not compatible.

The Salesforce investigator and admin reviewer expose `get_username`,
`run_soql_query`, and `retrieve_metadata`. Queries require `query`,
`usernameOrAlias`, and the absolute workspace `directory`; `useToolingApi` selects
Tooling API queries. Retrieve uses the same target/root plus exactly one selector
and `ignoreConflicts: false`.

The server also registers the always-on core `resume_tool_operation` tool. It supports
other operation types, not retrieves; neither bundled Salesforce agent exposes it.
This allowlist is client-side selection, not a server-side authorization boundary.

Object analysis can use bounded `EntityDefinition` and `FieldDefinition` queries
when the authenticated user has access. This does not expose all metadata properties.
For an identity check, query `Organization` and report the returned ID and sandbox
flag. `IsSandbox = false` alone does not prove that the org is production.

The ADO server domains include write tools, even though the bundled analyst does
not select them. Neither upstream server is wrapped by this package. Use the supplied
agents and review host tool selections; another agent or user configuration can
expose a different tool set. Actual access is governed by the account's permissions.
Do not broadly auto-approve server tools.

## Verify in your host

- Check that all four agents, seven prompts, and nine skills are discovered without
  customization errors. Seven skills are hidden from the slash menu because their
  prompt files already provide the corresponding command.
- Check that both MCP servers start and that every tool named in the agent files
  exists. Do not replace missing tool names with a server-wide wildcard.
- With `ado-analyst`, fetch a known work item in the intended project. Verify its
  ID and project in the result. Try a bounded wiki search in the same project.
- With `config-investigator`, verify the selected org identity, then inspect a known
  object with a bounded query. Check alias, Org ID, filters, and returned fields.
- Retrieve one known, named component into a clean local source location. Verify
  the manifest, target Org ID, tool result, and returned files. Do not test by widening
  to all metadata. Check that deploy, tests, and resume are absent from agent tool lists.
- Run `/inventory-force-app` on that component and check its logical name and path.
  Run `/review-org` with an explicit question, then test an offline snapshot review.
- Request a saved review and inspect the Markdown report: scope, source/time,
  evidence, findings, open items, and unverified checks must agree with the observations.
  Reports stay in chat when saving was not requested; local modifications are preserved.
- Check that permission failures, partial retrieval, and unsupported checks remain
  visible and do not produce an org-wide safety verdict.

A JSON/frontmatter check or unauthenticated MCP handshake verifies configuration
and discovery only. Your authenticated VS Code, ADO, and Salesforce checks are still
required before treating the package as verified for your team.

## Vendor references

Configuration follows the [Azure DevOps MCP documentation](https://github.com/microsoft/azure-devops-mcp)
and [Salesforce DX MCP documentation](https://github.com/salesforcecli/mcp).
See the [core Salesforce tool reference](https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-mcp-use-core-tools.html)
for available operations; exact retrieve/resume behavior above was checked against
the pinned package's published implementation.
See [VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
and [Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
for host behavior. Recheck tool names and startup discovery when changing versions.
