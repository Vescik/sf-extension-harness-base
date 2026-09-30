---
name: search-ado
description: Search Azure DevOps wiki pages and work items within one selected organization and project, and summarize relevant source evidence.
user-invocable: false
---

# Search Azure DevOps

Follow the [shared instructions](../../copilot-instructions.md). Use only read capabilities
exposed by the `ado` MCP server.

Accept a question or search text, a target (`wiki`, `workitems`, or `both`; default `both`),
and optional result limit (default 10, maximum 25). Reuse the organization and project already
selected in this session; ask only for missing or ambiguous scope. Reject invalid limits and
unknown targets before a call.

1. Use `search_wiki` and/or `search_workitem` after inspecting their actual argument schemas.
   In the pinned version, both search tools take `project` as an array with one selected project,
   plus `searchText` and bounded `top`. The `wiki` read tool takes a project string instead;
   use `wikiIdentifier`, `path`, and a read action such as `get_page_content`. Omit `url`, which
   overrides those scope arguments. Keep every read within the selected organization/project. If that
   scope cannot be established, report the missing capability instead of widening the search.
2. Return relevant hits with title, source link or ID, type, and a short snippet. Fetch page
   content only when needed to answer the question. For deeper work-item context, use
   [fetch-ado-item](../fetch-ado-item/SKILL.md) with the relevant ID.
3. Separate source statements from your interpretation. Preserve source language in quotations;
   remove active markup and omit sensitive material from excerpts.
4. Report the query, scope, retrieval time, and material gaps. Disclose limits, failed reads,
   and incomplete pagination. Zero hits mean no matches in this search, not proof that the
   documentation or work item does not exist.

Respond in chat by default. Save a sanitized report under `output/` only when requested.
Do not create caches, edit wiki pages or work items, or start a delivery workflow.
