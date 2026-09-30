# Salesforce & Azure DevOps Base

A small, independent starting point for admin teams that review Salesforce orgs
with GitHub Copilot in VS Code and Azure DevOps. Adapted from `sf-extension-harness`.

The package contains Markdown agents, prompts, and skills, a Salesforce DX project,
and direct configuration for two vendor MCP servers. There is no package-owned
runtime to install or maintain.

## Included

| Agent | Purpose | Entry points |
| --- | --- | --- |
| `ado-analyst` | Find requirements, work items, and wiki documentation | `/search-ado`, `/fetch-ado-item` |
| `config-investigator` | Investigate objects and records, retrieve metadata, and inventory local source | `/investigate-object`, `/investigate-config-records`, `/retrieve-metadata`, `/inventory-force-app` |
| `admin-reviewer` | Review selected org configuration or an offline snapshot | `/review-org` |
| `workspace-maintainer` | Adapt the local package for a team | Select the agent and describe the change |

Nine skills provide the procedures: `search-ado`, `fetch-ado-item`, `org-discovery`,
`investigate-object`, `investigate-config-records`, `retrieve-metadata`,
`inventory-force-app`, `review-org`, and `maintain-workspace`.
External operations are reads. Metadata retrieval writes scoped local source files;
analysis stays in chat unless a report is requested. `output/` is ignored by Git.

The Salesforce connection exposes bounded SOQL and metadata retrieval. The ADO
connection supports project-scoped wiki and work-item reads. The package adds no
terminal access, deployment, record-write, or test-execution tools to its agents.

## Admin review

For a live review, select an org and the components or behavior to examine. The
reviewer checks identity, reads the relevant evidence, and can retrieve the minimum
needed metadata. For an offline review, supply local files or a manifest; an org
connection is not required and unknown source provenance remains explicit.

The [admin checklist](.github/skills/review-org/references/admin-checklist.md) covers
access and sharing, Flow and automation, objects and validation, record types and
layouts, and relevant dependencies. Only the selected areas are reviewed. Findings
include evidence, impact, severity, and recommendations; missing evidence is listed
separately from confirmed defects. Review does not apply fixes.

When requested, save a report using the
[review report template](.github/skills/review-org/assets/review-report.md). The
report records the source org or snapshot, observation time, examined scope,
findings, open items, and checks that remain unverified.

## Salesforce DX project

The repository root is the SFDX project root. The complete source project's scaffold
is restored: [sfdx-project.json](sfdx-project.json), [force-app/](force-app/),
[manifest/package.xml](manifest/package.xml), [.forceignore](.forceignore),
[scratch-org definition](config/project-scratch-def.json), and the Apex Replay
Debugger launch configuration. VS Code recommends the Salesforce and XML extensions.

The source tree contains empty component directories, as in the original package;
it does not contain a snapshot of any org. Admins can retrieve scoped metadata into
it for local review. The starter manifest currently selects all `CustomObject`
members, not all org metadata; tailor it to the review. API version `67.0` is retained
from the source project. See [SETUP.md](SETUP.md) for MCP and manual retrieval.

## Start

Open this folder directly in VS Code and follow [SETUP.md](SETUP.md). Then select
one of the custom agents and provide the project or org and a concrete question.
For example:

```text
/search-ado project=Support query="case routing" target=both
/fetch-ado-item project=Support itemId=123 mode=hierarchy
/investigate-object objectApiName=Account org=team-sandbox question="Which fields identify customer ownership?"
/investigate-config-records objectApiName=RoutingRule__c org=team-sandbox question="Which rules route urgent cases?"
/retrieve-metadata org=team-sandbox components=Flow:Case_Routing,PermissionSet:Support_User
/inventory-force-app scope=Flow,PermissionSet
/review-org org=team-sandbox scope=Flow:Case_Routing question="Review routing and error handling."
/review-org scope=force-app/main/default/permissionsets question="Review this local snapshot against our stated support-access requirements and save a report in output/."
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
evals, test infrastructure, CI workflows, development delivery workflows, delivery
work items, and business-specific configuration. The SFDX project and its
standard editor support are retained.
The new repository starts with its own local history and no remote.

Tool lists and instructions are not server-side authorization. See the access limits
and host verification steps in [SETUP.md](SETUP.md).
