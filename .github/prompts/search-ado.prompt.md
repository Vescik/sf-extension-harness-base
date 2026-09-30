---
name: search-ado
description: Search Azure DevOps wiki pages and work items in the selected organization and project.
argument-hint: "query=<text> [project=<name>] [target=wiki|workitems|both] [top=10]"
agent: ado-analyst
---

Use the [search-ado skill](../skills/search-ado/SKILL.md).
Accept a natural-language question or the hinted arguments. Reuse established organization and
project scope; ask only for missing input. Return sourced findings in chat with search limits
and incomplete results disclosed. Save a report only when requested.
