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
There is no `npm install`, Python environment, build, SFDX project, or setup script
for this package. The first MCP startup uses `npx` to download the vendor servers.

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

## Tool surface

The top-level npm versions are pinned in the MCP configuration:

| Server | Package | Configuration |
| --- | --- | --- |
| `ado` | `@azure-devops/mcp@2.10.0` | `work-items`, `wiki`, and `search` domains |
| `salesforce` | `@salesforce/mcp@0.30.15` | One explicit org; `run_soql_query`; telemetry disabled |

The ADO analyst exposes four read tools: `search_wiki`, `search_workitem`, `wiki`,
and `wit_work_item`. In this version, wiki and work-item operations use an `action`
argument on the consolidated tool. Earlier individual tool names are not compatible.

The Salesforce investigator exposes `get_username` and `run_soql_query`. Queries
require `query`, `usernameOrAlias`, and the absolute workspace `directory`;
`useToolingApi` selects Tooling API queries. The server also registers a core
`resume_tool_operation` tool, which this agent does not expose.

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

- Check that all three agents, four prompts, and six skills are discovered without
  customization errors. Four skills are hidden from the slash menu because their
  prompt files already provide the corresponding command.
- Check that both MCP servers start and that every tool named in the agent files
  exists. Do not replace missing tool names with a server-wide wildcard.
- With `ado-analyst`, fetch a known work item in the intended project. Verify its
  ID and project in the result. Try a bounded wiki search in the same project.
- With `config-investigator`, verify the selected org identity, then inspect a known
  object with a bounded query. Check alias, Org ID, filters, and returned fields.
- Check that reports are returned in chat by default and that permission failures
  or incomplete results remain visible.

A JSON/frontmatter check or unauthenticated MCP handshake verifies configuration
and discovery only. Your authenticated VS Code, ADO, and Salesforce checks are still
required before treating the package as verified for your team.

## Vendor references

Configuration follows the [Azure DevOps MCP documentation](https://github.com/microsoft/azure-devops-mcp)
and [Salesforce DX MCP documentation](https://github.com/salesforcecli/mcp).
See [VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
and [Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
for host behavior. Recheck tool names and startup discovery when changing versions.
