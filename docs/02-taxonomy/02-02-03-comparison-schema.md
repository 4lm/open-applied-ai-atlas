# 2.2.3 Comparison Schema

_Page Type: Reference Sheet | Maturity: Review-Ready_

Use this page when a chapter needs a comparison table and you want that table to support a real decision instead of becoming a shallow inventory. The atlas default is not “add more columns.” The atlas default is “make the comparison honest, readable, and decision-grade.”

## What A Good Comparison Page Must Do

A good comparison page should let the reader answer questions like these quickly:

* what kind of entities are being compared
* why these entities were selected
* what decision the table is helping with
* where control, dependence, and exit posture differ
* which row claims come from primary sources and which judgments come from atlas synthesis

If the table cannot do that work, either deepen it, split it, or replace it with prose.

## Step 1: Decide Whether A Table Is Justified

Use a table only when side-by-side reading genuinely helps.

| Use a table when... | Prefer prose or bullets when... |
| --- | --- |
| the reader needs to compare several entities on the same decision surface | the page is mainly defining a concept or warning against a mistake |
| the key trade-offs become clearer when rows are aligned | only one option is being described in depth |
| the entities can be compared on a shared set of fields without hiding major differences | the entities are so mixed that the table would flatten unlike things into false equivalence |
| the page can name why the listed entities belong together | the page would only list names without enough row depth to help a decision |

## Step 2: Choose The Right Entities

Entity selection quality matters as much as table formatting.

### Include An Entity Only If It Improves The Decision

Keep a row only if at least one of these is true:

* it represents a major lane the reader is likely to consider
* it reveals a materially different control posture, sourcing posture, or operating burden
* it changes how the reader should think about dependence, portability, privacy, or governance
* it is a canonical public anchor the reader genuinely needs to see in the chapter

### Exclude Or Remove An Entity If It Fails These Tests

Remove the row when:

* it is present only because the name is familiar
* it duplicates a stronger representative row without adding new decision value
* it belongs to a different entity class and the mixed comparison is not explained clearly
* the row would be too thin to stay trustworthy
* the row weakens the chapter by turning the page into a broad list rather than a useful comparison

## Step 3: Compare Like With Like First

Like-with-like comparison is the default.

| If the page is comparing... | Compare directly with... | Usually split away from... |
| --- | --- | --- |
| tools, frameworks, or projects | peers at the same stack layer and with similar operating roles | vendors, standards, and full architectures |
| managed platforms or services | services with similar scope and control posture | isolated open-source projects or standards anchors |
| vendors or organizations | suppliers, stewarding bodies, or ecosystem actors | product rows unless the page explicitly separates supplier and product logic |
| laws, standards, or frameworks | anchors in the same family first | products, platforms, or architecture options |
| architecture patterns or reference stacks | other architecture shapes serving similar jobs | single tools presented as if they settle the whole design |

Mixed-class comparison is allowed only when the mixed view is itself the point. If you keep a mixed table, state that clearly in the first paragraph and in the first column.

## Step 4: Use The Minimum Required Fields

Every comparison-heavy page should make these fields visible unless the page has a very strong reason not to.

| Field | Why it is required |
| --- | --- |
| Entity type | Prevents tools, vendors, standards, and patterns from collapsing into one list |
| Primary purpose | Makes the job of the thing explicit |
| Deployment or control posture | Shows whether the organization operates it, rents it, or inherits it indirectly |
| Openness posture | Separates open source, open weights, mixed, and proprietary positions |
| Main lock-in or dependence note | Forces the comparison to name where dependence actually sits |
| Primary source | Keeps the row traceable |

## Step 5: Add Extended Fields Only When They Change The Decision

Do not widen the table mechanically. Add fields when they materially improve the comparison.

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

## Step 6: Make Each Row Deep Enough To Matter

A row should do more than name the category.

| Weak row shape | Stronger row shape |
| --- | --- |
| product name plus one vague fit phrase | purpose, control posture, dependence note, and one or two decision-shaping trade-offs |
| “open” or “managed” with no consequence | the openness or managed posture plus why it changes portability, control, or operating burden |
| source link only | source link plus a row description clear enough that the reader can use the source intelligently |
| marketing-style strength summary | chapter-specific strength and weakness phrased in atlas language |

## Comparison Writing Rules

* State what the page helps the reader decide before the first table.
* Compare like with like first. If the table spans mixed entity types, make that distinction explicit in the first column and surrounding prose.
* Do not treat convenience as a neutral default. Managed speed often changes control, evidence, and exit posture.
* Do not hide ranking logic. If a ranking is implied, explain the decision logic in prose or an evidence note.
* Keep chapter-specific trade-offs visible instead of pretending one global ranking exists.
* Delete weak rows before adding decorative fields.

## Evidence Notes Pattern

Comparison-heavy pages should include an `Evidence Notes` section when they:

* make a recommendation
* summarize vendor claims
* rely on editorial judgment to collapse many trade-offs into one table
* compare standards or regulatory anchors beyond raw legal text

Use the section to separate:

* primary-source-backed facts
* atlas synthesis
* explicit editorial judgment

Do not add `Evidence Notes` mechanically.

## Pre-Publish Review Checks

Run these checks before keeping a comparison table:

* Does each row answer the same question?
* Are the selected entities the ones that actually shape the reader's decision?
* Is the table still useful if the reader knows nothing about the named entities already?
* Is the row depth strong enough that the table helps with real planning, implementation, governance, sourcing, or operations work?
* Would splitting the table by entity class make it more honest and more readable?

## Minimum Table Example

| Option | Entity type | Primary purpose | Deployment or control posture | Openness posture | Main lock-in note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| Example A | Open-source framework | Retrieval orchestration | Self-hosted | Open source | Local ops burden and framework coupling | Official docs |
| Example B | Managed platform | End-to-end app delivery | Vendor-managed | Proprietary | Data-plane and workflow dependence | Official docs |

Back to [2.2 Applying The Taxonomy](02-02-00-applying-the-taxonomy.md).
