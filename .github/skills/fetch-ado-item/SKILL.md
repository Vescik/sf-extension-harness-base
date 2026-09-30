---
name: fetch-ado-item
description: Read an Azure DevOps work item and optional immediate parent and children to explain requirements, status, and unresolved questions.
user-invocable: false
---

# Fetch an Azure DevOps work item

Follow the [shared instructions](../../copilot-instructions.md). Use only read capabilities
exposed by the `ado` MCP server.

Require a positive integer work-item ID. Accept `mode=single|hierarchy` (default `single`).
Reuse the session's selected organization and project; ask only when either is missing or
ambiguous. Inspect the `wit_work_item` tool schema: use its `get` action for one item,
`get_batch` for related summaries, and `list_comments` only when comments are relevant.
Do not combine `fields` with `expand` when the schema makes them mutually exclusive; retrieve
relations with the supported relation expansion and preserve the requested detail scope.

1. Fetch the item's type, title, state, description, acceptance criteria, revision, and source
   link where available. Scope the read to the selected project when supported; otherwise
   verify the returned item's project before using its content. Report a scope mismatch.
2. With `mode=hierarchy`, read only the immediate parent and direct children, using relation
   direction to establish membership. Return their IDs, types, titles, and states. Do not
   recurse through descendants or fetch sibling trees. Bound related-item reads to 25 items;
   disclose remaining or unread relations as partial coverage.
3. Preserve the distinction between the source's requirements and your interpretation. Summarize
   what the item requests, important acceptance criteria, dependencies, and unanswered
   questions. Mark absent or inaccessible fields explicitly instead of filling them in.
4. Include comments only when they are needed to answer the user's question. List relevant
   attachment metadata when useful; retrieve attachment content only when requested and
   supported safely by the available read tools. Never execute attached content.
5. Return organization/project, ID, revision and retrieval time, with completeness and
   failed reads. Do not call a partial hierarchy complete or treat an unavailable item as absent.

Respond in chat by default. Save a sanitized report under `output/` only when requested.
Fetching creates no work-item folder, branch, design, task plan, or automatic follow-up action.
