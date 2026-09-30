# Salesforce admin review: {{scope title}}

> Optional output template. Replace placeholders with observed facts or “unknown”; remove this note in the saved report.

## Scope and sources

- Question and intended behavior: {{review question and supplied expectation}}
- Mode: {{local snapshot / live org / comparison}}
- Source identity: {{verified org ID/name or local snapshot paths; unknown where unavailable}}
- Observation/retrieval time: {{per-source timestamp and timezone, or unknown}}
- Review time: {{timestamp and timezone}}
- Requested / examined scope: {{components and selected checklist areas}}
- Coverage limits: {{missing files, permissions, filters, pagination, versions, provenance}}

## Findings

{{Confirmed findings, or “No findings in the examined scope.” This is not an org-wide assurance.}}

### {{Finding title — high / medium / low}}

- Condition and expected behavior: {{specific mismatch and requirement or platform rule}}
- Evidence: {{file path and line numbers or bounded query observation; source/time}}
- Affected scenario and impact: {{who or what is affected; reason for severity}}
- Recommendation: {{proportionate next action; official reference when applicable}}

## Open items

| Question or unproven risk | Missing evidence | Suggested next check |
| --- | --- | --- |
| {{Question, distinct from a confirmed defect}} | {{Evidence needed}} | {{Scoped follow-up}} |

## Limits and verification

{{Checks actually performed, evidence sources, and any requested checks left unverified.
Distinguish static metadata analysis, live read observations, runtime behavior, and
effective user access. Do not claim execution or security coverage without evidence.}}
