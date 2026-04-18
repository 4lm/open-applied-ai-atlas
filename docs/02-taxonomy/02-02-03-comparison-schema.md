# 2.2.3 Comparison Schema

_Page Type: Reference Sheet | Maturity: Review-Ready_

_Page Type: Reference Sheet | Maturity: Review-Ready_

This schema is the atlas default for comparing tools, vendors, projects, platforms, patterns, and architecture options. It exists to keep chapter-local tables useful without letting every author invent a different comparison logic.

## Core Rule

Use the smallest comparison surface that still makes the decision legible. Do not force every field into every table, but do not omit the control, portability, and dependence questions when they materially change the recommendation.

## Required Fields

| Field | Why it is required |
| --- | --- |
| Entity type | Prevents tools, vendors, standards, and patterns from collapsing into one list |
| Primary purpose | Makes the job of the thing explicit |
| Deployment or control posture | Shows whether the organization operates it, rents it, or inherits it indirectly |
| Openness posture | Separates open source, open weights, mixed, and proprietary positions |
| Main lock-in or dependence note | Forces the comparison to name where dependence actually sits |
| Primary source | Keeps the row traceable |

## Extended Fields

Add these when they change the decision in a meaningful way:

| Field | Use when |
| --- | --- |
| Stack layer | The same category appears in multiple layers |
| Data boundary implications | Data placement, residency, secrecy, retention, or permissioning matter materially |
| Portability implications | Exit posture or migration burden is a real concern |
| Observability implications | Traceability, telemetry export, or incident evidence matters |
| Security implications | Threat surface or control design differs meaningfully across options |
| Governance implications | Approval, audit, or management-system evidence differs across options |
| Operational complexity | The burden of running the option is a major trade-off |
| Fit by organization type | The same option fits startups, SMEs, public sector, and regulated enterprises differently |
| Strengths | A concise summary of where the option is strongest |
| Weaknesses | A concise summary of where the option is weakest |

## Comparison Writing Rules

- Compare like with like first. If the table spans mixed entity types, make that distinction explicit in the first column.
- Do not treat convenience as a neutral default. Managed speed often changes control and exit posture.
- Avoid hidden scoring. If a ranking is implied, explain the decision logic in prose or an evidence note.
- Keep chapter-specific trade-offs visible instead of pretending one global ranking exists.

## Evidence Notes Pattern

Comparison-heavy pages should include an `Evidence Notes` section when they:

- make a recommendation
- summarize vendor claims
- rely on editorial judgment to collapse many trade-offs into one table
- compare standards or regulatory anchors beyond raw legal text

Use the section to separate:

- primary-source-backed facts
- atlas synthesis
- explicit editorial judgment

## Minimum Table Example

| Option | Entity type | Primary purpose | Deployment or control posture | Openness posture | Main lock-in note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| Example A | Open-source framework | Retrieval orchestration | Self-hosted | Open source | Local ops burden and framework coupling | Official docs |
| Example B | Managed platform | End-to-end app delivery | Vendor-managed | Proprietary | Data-plane and workflow dependence | Official docs |

Back to [2.2 Applying The Taxonomy](02-02-00-applying-the-taxonomy.md).
