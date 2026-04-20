# 2.2.3 Comparison Schema

_Page Type: Reference Sheet | Maturity: Review-Ready_

Use this page when a chapter needs a comparison table and you want that table to support a real decision instead of becoming a shallow inventory. The atlas default is not "add more columns." The atlas default is "make the comparison honest, readable, and decision-grade."

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

Before adding names, write the first question the table is supposed to answer. If the candidate rows stop answering that same question, the problem is usually the comparison surface, not the formatting.

### Include An Entity Only If It Improves The Decision

Keep a row only if at least one of these is true:

* it represents a real lane the reader is likely to compare on the current surface
* it reveals a materially different control posture, sourcing posture, workflow scope, or operating burden
* it changes how the reader should think about dependence, portability, privacy, sovereignty, or governance
* it is a canonical public anchor the reader genuinely needs to see in the chapter

### Exclude Or Remove An Entity If It Fails These Tests

Remove the row when:

* it is present only because the name is familiar
* it duplicates a stronger representative row without adding new decision value
* it belongs to a different entity class and the mixed comparison is not the point of the page
* the row would be too thin to stay trustworthy
* the row weakens the chapter by turning the page into a broad list rather than a useful comparison

## Step 3: Compare Like With Like First

Like-with-like comparison is the default.

| If the page is comparing... | Compare directly with... | Usually split away from... |
| --- | --- | --- |
| models or model families | peer models with similar modality, lifecycle, and serving assumptions | managed services or APIs, managed platforms, and full applications |
| tools, frameworks, or projects | peers at the same stack layer and with similar operating roles | vendors, standards, and full architectures |
| managed services or APIs | services with similar capability scope, data posture, and support-path evidence | models in isolation, managed platforms, or supplier rows |
| managed platforms | platforms with similar workflow scope, control-plane coverage, and operating posture | managed services or APIs, isolated tools, or supplier rows |
| vendors or organizations | suppliers, stewarding bodies, or ecosystem actors | product rows unless the page explicitly separates supplier and product logic |
| laws, standards, or frameworks | anchors in the same family first | products, platforms, or architecture options |
| architecture patterns or reference stacks | other architecture shapes serving similar jobs | single tools presented as if they settle the whole design |

Mixed-class comparison is allowed only when the mixed view is itself the point. If you keep a mixed table, state that clearly in the first paragraph and in the first column.

Split the table before it goes further when:

* a model row is standing in for a managed service or API decision
* a managed platform row is being treated like a bounded service call even though workflow scope and control-plane ownership change the decision
* a supplier row is settling a product comparison before supplier dependence is the real question
* a law, framework, or standard is sitting beside runtime options as if both answer the same buying or architecture question
* an architecture pattern and a product row belong together only because one local proposal bundled them

## Step 4: Use The Minimum Required Fields

Every comparison-heavy page should make these fields visible unless the page has a very strong reason not to.

| Field | Why it is required |
| --- | --- |
| Entity type | Prevents tools, vendors, standards, and patterns from collapsing into one list |
| Primary purpose | Makes the job of the thing explicit |
| Why this entity is in scope | Forces the table to justify why this row improves the decision instead of riding on name recognition |
| Deployment or control posture | Shows whether the organization operates it, rents it, or inherits it indirectly |
| Openness posture | Separates open source, open weights, mixed, and proprietary positions |
| Main lock-in or dependence note | Forces the comparison to name where dependence actually sits |
| Primary source | Keeps the row traceable |

## Step 5: Add Extended Fields Only When They Change The Decision

Do not widen the table mechanically. Widen either coverage or fields only when the added breadth helps the reader answer the same decision question more honestly.

### Widen Coverage Only When It Adds A Real Decision Lane

Add another row or comparison lane only if:

* it introduces a materially different control posture, sourcing posture, workflow scope, or operating burden that the current rows do not already represent
* the chapter would otherwise hide a real option or canonical public anchor the reader is likely to compare
* the added row prevents a false either-or framing between visible options on the same surface
* the new row can still meet the same minimum row-depth and sourcing standard as the rest of the table

### Prune Or Split When Breadth Starts Weakening The Table

Prune the row or split the table when:

* multiple rows now carry nearly the same trade-off shape and one representative row can make the point more clearly
* a familiar name is being kept mainly for coverage optics instead of decision value
* the added row forces thinner sourcing, vaguer row text, or more caveats than the rest of the table
* the added breadth turns a decision table into a market map, supplier list, or architecture grab bag
* the same comparison would become more honest as two smaller like-with-like tables

Add extended fields only when they explain a difference that is already real in the row set. If a field would be mostly identical, mostly empty, or only decorative, keep it in prose or omit it.

| Field | Use when |
| --- | --- |
| Stack layer | The same category appears in multiple layers and that layer difference changes control or buying posture |
| Data boundary implications | Data placement, residency, secrecy, retention, or permissioning changes the choice materially |
| Portability implications | Exit posture or migration burden differs enough to shape the decision |
| Observability implications | Traceability, telemetry export, or incident evidence differs meaningfully across options |
| Security implications | Threat surface, isolation, or control design differs meaningfully across options |
| Governance implications | Approval, audit, assurance, or management-system evidence differs across options |
| Operational complexity | The burden of running the option is a major trade-off |
| Fit by organization type | The same option fits startups, SMEs, public sector, and regulated enterprises differently |
| Strengths | A concise summary of where the option is strongest after the major trade-offs are already visible |
| Weaknesses | A concise summary of where the option is weakest after the major trade-offs are already visible |

If adding a field would force you to widen the row set just to populate the column, the field is probably not doing useful work on this surface.

## Step 6: Make Each Row Deep Enough To Matter

A row should do more than name the category.

| Weak row shape | Stronger row shape |
| --- | --- |
| product name plus one vague fit phrase | purpose, why the row is in scope, control posture, dependence note, and one or two decision-shaping trade-offs |
| “open” or “managed” with no consequence | the openness or managed posture plus why it changes portability, control, or operating burden |
| source link only | source link plus a row description clear enough that the reader can use the source intelligently |
| marketing-style strength summary | chapter-specific strength and weakness phrased in atlas language |

If a row cannot explain why it belongs in the table and what decision it changes, the problem is usually row selection, not missing columns.

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

* Can you state the table's first question in one sentence before the table, and does every row still answer that same question?
* Does each row represent a distinct decision lane rather than a familiar name or a weaker duplicate?
* Would removing the weakest row make the page more honest or more readable? If yes, prune it.
* Has the table widened only where extra rows or fields change control posture, operating burden, dependence, privacy, governance, or sourcing?
* Are any rows too thin to meet the minimum fields, row-depth, and sourcing standard? If yes, prune or split before publishing.
* Would splitting the table by entity class make the comparison more truthful than keeping one mixed view?
* If the same point could be made more clearly in prose or bullets, should this table stay at all?
* If a ranking, recommendation, or compressed editorial judgment is visible, does the page need `Evidence Notes`, and are they present?

## Minimum Table Example

| Option | Entity type | Primary purpose | Why this row is in scope | Deployment or control posture | Openness posture | Main lock-in note | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Example A | Open-source framework | Retrieval orchestration | Represents the self-managed control-oriented lane | Self-hosted | Open source | Local ops burden and framework coupling | Official docs |
| Example B | Managed platform | End-to-end app delivery | Represents the integrated workflow and control-plane lane | Vendor-managed | Proprietary | Data-plane and workflow dependence | Official docs |

Back to [2.2 Applying The Taxonomy](02-02-00-applying-the-taxonomy.md).
