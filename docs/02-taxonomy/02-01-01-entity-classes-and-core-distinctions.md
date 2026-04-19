# 2.1.1 Entity Classes And Core Distinctions

_Page Type: Concept Explainer | Maturity: Draft_

Use this page when a proposal, tool list, or policy note sounds plausible but the comparison feels unstable. The taxonomy layer is doing its job only if it separates the kind of thing being discussed before the atlas compares it.

## Core Entity Classes

| Entity class | The question it answers | Compare with | Do not compare directly with | Usual handoff |
| --- | --- | --- | --- | --- |
| Organizational use case or AI system | What business or operating job is being done, and with what autonomy or consequence? | Other systems or use cases with similar task shape, human oversight, and failure cost | Individual models, tools, or standards treated as if they were the whole solution | Chapters `03`, `05`, `16` |
| Model or model family | What predictive, generative, ranking, or classification capability is being used? | Peer models with similar modality, lifecycle, and serving assumptions | Full applications, suppliers, or legal anchors | Chapters `07`, `08`, `13` |
| Tool, framework, or project | What building block or control surface is being adopted? | Peer tools at the same stack layer and with similar operating burden | Vendors, management-system standards, or whole architectures | Chapters `03`, `09`, `11`, `14`, `15` |
| Managed platform or service | What combined capability is the organization renting rather than operating directly? | Other managed services with comparable scope and control posture | Open-source projects in isolation or one model row stripped from its operating context | Chapters `08`, `09`, `17`, `18` |
| Vendor or organization | Who controls the roadmap, contracts, support path, and concentration risk? | Other suppliers, stewarding bodies, or ecosystem actors | Products, APIs, or standards without the supplier layer being named separately | Chapters `17`, `18` |
| Standard, framework, or regulation | What obligations, governance vocabulary, or public reference anchor applies? | Other anchors in the same family first: law with law, standard with standard, framework with framework | Products, managed services, or architecture options | Chapters `04`, `06`, `20` |
| Architecture or pattern | How should layers, controls, and responsibilities fit together? | Other architecture shapes or pattern choices | Single vendors or tools presented as if they settle the whole design | Chapters `03`, `10`, `19` |
| Control or evidence artifact | What record, test, checklist, or approval artifact proves the system is governed and reviewable? | Peer control artifacts serving the same review job | Standards text, vendor policy pages, or demos used as if they were operating evidence | Chapters `04`, `13`, `15`, `16` |

## Distinctions That Change Real Decisions

- A model is not the same thing as the managed service exposing it. Model quality questions belong beside hosting, gateway, sourcing, and evidence questions rather than replacing them.
- A tool or framework is not the same thing as the supplier behind it. Product fit and supplier dependence must be reviewable separately.
- A standard or regulation is not a product candidate. It sets obligations, vocabulary, or structure; it does not replace implementation design.
- An architecture pattern is not a vendor ranking. It explains how layers should fit together before the team starts narrowing named options.
- A control artifact is not proof because it exists in theory. It matters only when it is tied to owners, thresholds, and a repeatable review lane.

## Reviewer Checks

- Has the proposal named the entity class before comparing options?
- Does each comparison row answer the same question, or are mixed classes hiding in one table?
- Are the cross-cutting dimensions from [2.1.2 Cross-Cutting Dimensions And Heuristics](02-01-02-cross-cutting-dimensions-and-heuristics.md) being applied to the right class instead of to everything equally?
- If a local term differs from atlas language, is it normalized back through the [2.1.3 Terminology Ledger](02-01-03-terminology-ledger.md)?
- If a comparison is still valid after the entity class is named, is the page using the reusable fields from [2.2.3 Comparison Schema](02-02-03-comparison-schema.md)?

## Reading Rule

If the entity class is still ambiguous, do not move on to vendor, standards, or tooling comparison yet. The taxonomy pass is supposed to remove category confusion before later chapters narrow the decision.

Back to [2.1 Classification Foundations](02-01-00-classification-foundations.md).
