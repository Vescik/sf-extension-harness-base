# Salesforce & Azure DevOps Base

A small, independent starting point for teams that use GitHub Copilot in VS Code
with Azure DevOps and Salesforce. Adapted from `sf-extension-harness`.

The package contains Markdown agents, prompts, and skills, plus direct configuration
for two vendor MCP servers. There is no package-owned runtime to install or maintain.

## Included

| Agent | Purpose | Entry points |
| --- | --- | --- |
| `ado-analyst` | Find requirements, work items, and wiki documentation | `/search-ado`, `/fetch-ado-item` |
| `config-investigator` | Investigate Salesforce objects and configuration records | `/investigate-object`, `/investigate-config-records` |
| `workspace-maintainer` | Adapt the local package for a team | Select the agent and describe the change |

Six skills provide the procedures: `search-ado`, `fetch-ado-item`, `org-discovery`,
`investigate-object`, `investigate-config-records`, and `maintain-workspace`.
Analysis is read-only in external systems. Results stay in chat unless a report is
requested; `output/` is ignored by Git.

The Salesforce connection exposes bounded SOQL, including available Tooling API
schema information. It does not provide a full object describe or metadata retrieval
workflow. The ADO connection supports project-scoped wiki and work-item reads.

## Start

Open this folder directly in VS Code and follow [SETUP.md](SETUP.md). Then select
one of the custom agents and provide the project or org and a concrete question.
For example:

```text
/search-ado project=Support query="case routing" target=both
/fetch-ado-item project=Support itemId=123 mode=hierarchy
/investigate-object objectApiName=Account org=team-sandbox question="Which fields identify customer ownership?"
/investigate-config-records objectApiName=RoutingRule__c org=team-sandbox question="Which rules route urgent cases?"
```

These are examples; replace their project, ID, object, and alias with your own.

## Extend

- Shared behavior: [.github/copilot-instructions.md](.github/copilot-instructions.md).
- Agent roles and tool lists: [.github/agents/](.github/agents/).
- Reusable task procedures: [.github/skills/](.github/skills/).
- Short user entry points: [.github/prompts/](.github/prompts/).
- The two MCP registrations: [.vscode/mcp.json](.vscode/mcp.json).

See [CONTRIBUTING.md](CONTRIBUTING.md) for adding team instructions and capabilities.
No company names, org IDs, package namespaces, or credentials are preconfigured.

## Removed from the source package

Knowledge MCP and its stores, custom Salesforce proxies, scripts, hooks, schemas,
evals, test infrastructure, CI workflows, development/design/review/QA/release agents,
application source, delivery work items, and project-specific configuration.
The new repository starts with its own local history and no remote.

Tool lists and instructions are not server-side authorization. See the access limits
and host verification steps in [SETUP.md](SETUP.md).
