---
name: maintain-workspace
description: Adapt this base package's agents, prompts, skills, instructions, and documentation for a team's requested workflow.
---

# Maintain the base package

Follow the [shared instructions](../../copilot-instructions.md). Use the
`workspace-maintainer` agent for local package changes.

1. Read the affected files and find their references before editing. Preserve unrelated team
   changes and clarify only missing decisions that would materially change the request.
2. Make the smallest coherent update across agents, prompts, skills, instructions, and setup
   documentation. Keep common rules in the shared instructions and task procedures in skills;
   prompts should remain short entry points to those procedures.
3. Keep this base limited to the `ado` and `salesforce` MCP integrations and read-only external
   workflows. Do not add a runtime, scripts, hooks, another integration, or a development workflow
   as an incidental part of maintaining the package.
4. Check edited frontmatter, relative links, agent references, and tool names against the files
   and configured integrations. Check JSON syntax when configuration changes. A static check
   does not prove that VS Code loads a customization or that a live MCP connection works.
5. Report the changed behavior, files, checks actually performed, and any runtime verification
   still needed. Do not claim host or external-system validation without observed results.

Ordinary requested edits need no extra confirmation. Do not modify credentials, external
systems, or Git history, or publish changes as part of this maintenance workflow.
