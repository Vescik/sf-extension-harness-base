# Admin review checklist

Select checks that answer the review question. For each selected area, distinguish
observed behavior, a contextual recommendation, and evidence still needed. An
unchecked item or missing artifact is not automatically a defect.

## Access: CRUD, fields, and records

- Identify the relevant users or personas, objects, fields, and operations. Read the
  available profiles, permission sets, groups, assignments, and license constraints.
  A single permission-set file cannot establish a user's effective access.
- Review object/field grants separately from record access: ownership, sharing
  defaults, rules, role/group membership, and applicable access overrides. Report
  assignment, record, or runtime context that is unavailable.
- Compare observed grants with the stated access requirement. Do not infer security
  enforcement from a layout or infer all-user access from the integration user's query.

Source: [Salesforce Platform Sharing Architecture](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture).

## Flow and automation

- Establish the inspected version/status and, if known, active version. Examine trigger
  object, timing, entry criteria, decisions, and conditions on changed values against
  the requested scenarios. A local active status is not proof of current org activation.
- Trace queries, record writes, loops, subflows, and invocable actions for the relevant
  volume. Flag an evidenced limit risk; source inspection does not prove bulk execution.
- Inspect failure handling where supported and explain the effect of unhandled errors
  in context. Missing fault paths alone are not a universal defect.
- Follow updates that can re-enter automation. Consider existing entry guards and
  changed-value checks before alleging recursion; identify unresolved cross-automation
  edges and ordering assumptions.

Source: [Salesforce Record-Triggered Automation](https://architect.salesforce.com/docs/architect/decision-guides/guide/record-triggered).

## Objects, fields, validation, record types, and layouts

- Compare field types, required/default values, relationships, and picklist choices
  with the selected process. Identify formulas or validation rules whose conditions,
  bypasses, or error messages conflict with a specific expected scenario.
- Inspect relevant record types, available values, and layout assignments together.
  Describe what is visible in the inspected configuration; identify missing assignment
  context and distinguish UI presentation from access control.
- Treat inactive rules, unused-looking fields, or duplicate-looking configuration as
  review questions unless evidence establishes the expected use and actual impact.

## Dependencies and integrations

- Record relevant field, object, Flow, action, and Apex references with their source.
  State whether each target was inspected, merely referenced, or unresolved.
- For integration dependencies, inspect only the configuration needed to explain the
  selected path. Do not expose credentials or treat endpoint configuration as proof
  of connectivity, successful execution, or the external system's current contract.
- Report the boundary of the inspected graph. Local references are not a complete
  dependency map; dynamic references and unavailable managed-package internals may
  leave gaps. Recommend the smallest follow-up evidence that resolves the question.
