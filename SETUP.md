# Setup

## Prerequisites

- VS Code with GitHub Copilot Chat and support for custom agents, prompts, skills, and MCP.
- Node.js 22.12+ on the 22.x line or Node.js 24 LTS, with `node` and `npx` on VS Code's PATH.
- Python 3.11+ with `venv` and `pip`.
- Salesforce CLI 2.136.8+ on the 2.x line and one authenticated org with an explicit alias.
  Sign in yourself using your team's normal procedure; a username is not a valid
  MCP alias. Aliases contain 1–80 letters, digits, dots, underscores, or hyphens and
  start with a letter or digit.
- Access to an Azure DevOps organization and project when using the ADO agent.

Open this repository folder directly. Parent customization discovery is disabled
in [.vscode/settings.json](.vscode/settings.json). This folder is also the SFDX root.
No Salesforce data or local authorization is included in the template.

## Install the Salesforce MCP runtime

The server is the custom review MCP from `sf-extension-harness`. It uses six local
scripts and hash-pinned Python dependencies; it does not launch `@salesforce/mcp`.
There is no package-level npm install. ADO starts through its pinned npm package.

On macOS or Linux, run from the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements-mcp.lock
cp config/harness.example.json config/harness.local.json
```

On Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --require-hashes -r requirements-mcp.lock
Copy-Item config/harness.example.json config/harness.local.json
```

Edit the ignored `config/harness.local.json` and set `salesforce.review.enabled`
to `true` when ready to connect. The generic example starts disabled. Configure:

| Setting | Meaning |
| --- | --- |
| `salesforce.orgs` | Optional alias/environment entries; an empty list permits an explicitly selected authenticated alias after live identity proof. This list is not an org allowlist. |
| `salesforce.review.deniedOrganizationIds` | Org IDs to deny before serving tools. |
| `salesforce.review.apiVersion` | REST API version, initially `67.0`; keep the SFDX project and manifest compatible with your org. |
| `salesforce.review.allowedObjectApiNames` | Nonempty scope for object contracts and parsed SOQL/EXPLAIN `FROM` targets, or `["*"]` for all. |
| `salesforce.review.allowedPackageNamespaces` | `["*"]` for all installed packages, specific namespace names, or `[]` to omit package discovery. |
| `salesforce.review.maxFieldsPerObject` | Object-contract field bound, from 1 to 500. |
| `safety.allowScopedEnumeration` | Allows listing configured aliases/environments when `true`; never lists all locally authenticated orgs. Defaults to `false`. |

Optional entries in `salesforce.orgs` contain `alias` and `environment` (`dev`, `uat`,
`stage`, or `prod`). `expectedInstanceHost` and `expectedOrganizationId` can pin the
identity; supply both together using independently verified values. The server still
checks live identity. Configured labels do not replace live environment evidence.
The [local configuration schema](schemas/harness-config.schema.json) provides editor
validation; runtime checks remain in the server.

The launcher searches `SALESFORCE_MCP_PYTHON`, the repository `.venv`, `py -3`,
`python3`, then `python`, probing both `requests` and `jsonschema`. An optional
`SALESFORCE_MCP_PYTHON` value must be an executable path, not a shell command.
Missing or disabled configuration blocks startup before Salesforce access.
Do not commit local config, tokens, passwords, session exports, or retrieved business data.

## Start the two connections

1. Open [.vscode/mcp.json](.vscode/mcp.json) and start `ado`. Enter the organization
   slug, not a URL, project name, or token. Complete its interactive sign-in. Supply
   the project in chat; it is not a server startup argument.
2. Start `salesforce` and enter exactly one authenticated CLI alias. Do not use a
   username, wildcard, comma-separated list, or default-target sentinel. Startup
   reads CLI authorization and proves the live host and Org ID before tool discovery.
   It supports sandbox, production, scratch, and Developer Edition targets.
3. Select the relevant agent and supply the same org alias or ADO project in the task.
   The Salesforce server binds one alias for its entire session; tools have no
   per-call org, username, or workspace-directory argument.
4. To change the target, update the corresponding VS Code input and restart that
   MCP server. If the host caches the value, change the input's `id` and matching
   `${input:...}` reference together to prompt again. Verify the new identity.

These prompt inputs use VS Code's extension-host MCP support. For a host that does
not support interactive inputs, replace the `${input:...}` arguments in your team's
copy with explicit non-secret identifiers, remove `inputs`, and verify discovery.

## Tool surface

| Server | Implementation | Surface |
| --- | --- | --- |
| `ado` | `@azure-devops/mcp@2.10.0` | `work-items`, `wiki`, and `search` domains |
| `salesforce` | `node scripts/start_salesforce_mcp.mjs --mode review --org <alias>` | Seven custom read tools below |

The ADO analyst selects `search_wiki`, `search_workitem`, `wiki`, and `wit_work_item`.
Wiki and work-item operations use an `action` argument. These are agent selections;
the upstream ADO server also includes write operations. Another agent can expose a
different selection. Account permissions and host approval controls still apply.

| Salesforce tool | Arguments | Purpose |
| --- | --- | --- |
| `review_org_identity` | `{}` | Verify the bound target and return identity evidence. |
| `review_installed_packages` | `{}` | Read packages within configured namespace scope. |
| `review_configured_orgs` | `{}` | Read locally configured aliases/environments when enabled. |
| `review_object_contract` | `{"objectApiName":"Account"}` | Reconcile REST describe and Tooling API field evidence. |
| `review_soql_query` | `{"query":"SELECT Id FROM Account LIMIT 5","useToolingApi":false}` | Read bounded SOQL results; `useToolingApi` is optional. |
| `org_limits` | `{}` | Read org limits. |
| `explain_query` | `{"query":"SELECT Id FROM Account LIMIT 5","useToolingApi":false}` | Read query plans when requested; `useToolingApi` is optional. |

The first five tools return structured evidence including target, time, status,
completeness, and warnings. Limits and query plans return diagnostic objects, not
those evidence envelopes. Agents must distinguish `VERIFIED`, `MISMATCH`,
`INCOMPLETE`, and `BLOCKED` and keep unresolved properties explicit.

The object allowlist checks object contracts and parsed `FROM` targets in SOQL and
query plans. It is not a complete field or relationship authorization boundary. The
namespace list scopes package discovery only. SOQL returns actual record values
and is not a data-redaction service. Use only
necessary fields, filters, and a small explicit `LIMIT`; sanitize reports. A sample
cannot prove org-wide behavior. Object-contract reconciliation marks contested
properties instead of silently preferring one source. The runtime bounds responses
and rejects unsupported calls. It exposes no metadata retrieval, deploy, test,
Apex-execution, record-write, terminal, or arbitrary HTTP tool.

## Prepare metadata for review

The complete SFDX scaffold remains available, with source API `67.0`. Install the
recommended Salesforce and XML extensions. `/retrieve-metadata` verifies the selected
org with our MCP, examines relevant local files, and prepares a narrow Salesforce CLI
command or manifest for an admin to run manually. It does not execute retrieval.

```text
/retrieve-metadata org=team-sandbox components=Flow:Case_Routing,PermissionSet:Support_User
```

An example manual command, from this project root, is:

```sh
sf project retrieve start --metadata 'Flow:Case_Routing' --metadata 'PermissionSet:Support_User' --target-org team-sandbox --wait 10
```

Replace the sample names and alias with the intended scope. Alternatively, use one
reviewed manifest selector:

```sh
sf project retrieve start --manifest output/retrieval/review.xml --target-org team-sandbox --wait 10
```

Prepare that manifest first. Do not blindly run the inherited `manifest/package.xml`:
its `CustomObject:*` entry is a broad starter and does not select every metadata type.
Review existing local source before retrieval because the CLI can merge or overwrite
files. Preserve unrelated changes; do not bypass conflicts with force flags.

After the command finishes, check the CLI result and resulting files. Supply the
org identity, retrieval time, selected components, and any failures to the agent.
A timeout, failed component, or partial file tree remains incomplete; inspect the
reported operation with your normal Salesforce tooling before retrying. A manifest
and a prepared command are not evidence that retrieval ran successfully.

Use `/inventory-force-app` to inspect the local snapshot, then `/review-org` for a
scoped review. An explicitly offline review requires no live MCP calls. Scratch-org
configuration and Apex Replay Debugger support remain available, but opening this
package does not create or modify an org.

## Verification

Run local checks using the installed environment:

```sh
.venv/bin/python -m unittest discover -s tests
node --check scripts/start_salesforce_mcp.mjs
```

On Windows use `.\.venv\Scripts\python.exe` for the first command. The tests drive
the actual Python server and Node launcher against a fake CLI and localhost HTTP
fixtures. They check identity, tool contracts, bounds, refresh, and startup policy
without authenticating or contacting Salesforce.

For your team's authenticated VS Code setup:

- Check discovery of four agents, seven prompts, nine skills, and both MCP servers.
  Seven skills use `user-invocable: false` because their prompts supply slash commands.
- Fetch a known ADO item and verify its project/ID; try a bounded wiki search.
- Verify the selected Salesforce alias/Org ID, inspect a known object contract, and
  run a minimal query. Check status, completeness, filters, and observation time.
- Manually retrieve one named component into a clean local source location, inspect
  the CLI result and files, and run inventory plus a scoped review.
- Check offline review and requested report saving. Permission failures, partial
  evidence, and unsupported checks must remain visible; no report is saved by default.

Passing offline tests does not establish authenticated VS Code, ADO, or live-org
acceptance. Keep those verification results separate.
