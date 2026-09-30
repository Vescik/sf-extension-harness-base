# Adapt the base for your team

Keep the base small. Put shared rules in
[.github/copilot-instructions.md](.github/copilot-instructions.md), task procedures
in a skill, and only role/tool selection in an agent. Prompt files should delegate
to a skill instead of repeating its procedure.

## Add team context

Create a focused `.github/instructions/<team>.instructions.md` file with VS Code
instruction frontmatter, for example:

```yaml
---
applyTo: "**"
---
```

Below it, document the actual domain vocabulary, source systems, and working rules.
Use a narrower file pattern where appropriate. Do not copy old vendor assumptions,
credentials, production records, or another team's process into the shared base.
For reliable discovery from a particular agent, link the instruction file there.

## Add a capability

1. Define the task and evidence needed. Extend an existing skill when it already
   owns that procedure; otherwise add `.github/skills/<name>/SKILL.md` with `name`
   and `description` frontmatter.
2. Add a custom agent only for a distinct role or tool set. Select explicit MCP read
   tools from the connected server's actual schema. Keep procedures in the skill.
3. Add a prompt when a short command helps users. Match its `agent` to an existing
   agent and link its skill. When prompt and skill share a name, set
   `user-invocable: false` on the skill to avoid duplicate slash commands.
4. Update the README and setup when entry points or required capabilities change.

The base includes an SFDX project, the ADO connector, our Salesforce review MCP,
and read-only analysis. Teams can build
specialized layers in their own repository, but must explicitly define any new
access or write workflow and verify the corresponding host controls.

Keep `sfdx-project.json`, `manifest/package.xml`, and the source directory structure
coherent when adapting the Salesforce project. Local retrieved metadata is evidence
from a named org and time, not proof of the current state of every environment.

## Review and validation

Check JSON syntax, YAML frontmatter, relative links, prompt-to-agent routing, and
actual MCP tool names. Search for references to files or tools that you remove.
Check Git's diff for unintended changes, local credentials, or captured business data.
Run the host checks in [SETUP.md](SETUP.md) after changing tool configuration.
Report static checks, MCP discovery, and authenticated host checks separately.

The custom Salesforce MCP has a focused offline test suite. After installing the
locked dependencies from [SETUP.md](SETUP.md), run:

```sh
python -m unittest discover -s tests
node --check scripts/start_salesforce_mcp.mjs
```

Use the configured virtual environment's Python. Tests use a fake CLI and local HTTP
fixtures; they do not authenticate or contact Salesforce. Run them after runtime or
policy changes. Keep dependency versions and hashes in `requirements-mcp.lock`.
Do not restore Knowledge, deployment workflows, or unrelated validation machinery
as incidental dependencies of a review feature.
