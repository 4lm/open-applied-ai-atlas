# 2.1.1 Entity Classes And Core Distinctions

_Page Type: Concept Explainer | Maturity: Review-Ready_

Use this page when a proposal, tool list, or policy note sounds plausible but the comparison still feels unstable. The taxonomy layer is doing its job only if it separates the kind of thing being discussed before the atlas compares it.

## Core Rule

Ask "what kind of thing is this?" before asking "which option is best?"

If the entity class is wrong, the rest of the comparison will usually be wrong too. Teams often think they are comparing products when they are really comparing suppliers, comparing laws when they are really choosing control patterns, or comparing models when the real decision is about a managed service and its dependence posture. For table builders, the safest first move is to mark the entity class in a draft working column before adding strengths, weaknesses, or rankings.

## Core Entity Classes

| Entity class | The question it answers | Compare with | Do not compare directly with | What usually changes if you classify it correctly | Next owner once class is clear |
| --- | --- | --- | --- | --- | --- |
| Organizational use case or AI system | What business or operating job is being done, and with what autonomy or consequence? | Other systems or use cases with similar task shape, human oversight, and failure cost | Individual models, tools, or standards treated as if they were the whole solution | use-case fit, workflow design, ownership, and oversight | Chapters `03`, `05`, `16` |
| Model or model family | What predictive, generative, ranking, or classification capability is being used? | Peer models with similar modality, lifecycle, and serving assumptions | Full applications, suppliers, or legal anchors | capability trade-offs, lifecycle fit, portability, and evaluation design | Chapters `07`, `08`, `13` |
| Tool, framework, or project | What building block or control surface is being adopted? | Peer tools at the same stack layer and with similar operating burden | Vendors, managed platforms, management-system standards, or whole architectures | integration burden, operational complexity, and control implementation | Chapters `03`, `09`, `11`, `14`, `15` |
| Managed platform | What integrated environment or control plane is being adopted and partly delegated? | Other platforms with similar stack coverage, workflow scope, and operating posture | Single tools, isolated model rows, or supplier names used as if they settled the platform question | workflow coupling, control-plane ownership, observability export, and exit posture | Chapters `03`, `08`, `09`, `18` |
| Managed service or API | What bounded capability is the organization calling instead of operating directly? | Other services with comparable capability scope, data posture, and evidence surface | Open-source projects in isolation, one model row stripped from its operating context, or a platform-level sourcing decision | supplier dependence, data boundary choices, support-path evidence, and exit posture | Chapters `08`, `09`, `17`, `18` |
| Vendor or organization | Who controls the roadmap, contracts, support path, and concentration risk? | Other suppliers, stewarding bodies, or ecosystem actors | Products, APIs, or standards without the supplier layer being named separately | market leverage, support dependence, and sourcing posture | Chapters `17`, `18` |
| Standard, framework, or regulation | What obligations, governance vocabulary, or public reference anchor applies? | Other anchors in the same family first: law with law, standard with standard, framework with framework | Products, managed services, or architecture options | compliance interpretation, evidence design, and review structure | Chapters `04`, `06`, `20` |
| Architecture or pattern | How should layers, controls, and responsibilities fit together? | Other architecture shapes or pattern choices | Single vendors or tools presented as if they settle the whole design | layer ownership, control placement, and sourcing options | Chapters `03`, `10`, `19` |
| Control or evidence artifact | What record, test, checklist, or approval artifact proves the system is governed and reviewable? | Peer control artifacts serving the same review job | Standards text, vendor policy pages, or demos used as if they were operating evidence | reviewability, auditability, and operating discipline | Chapters `04`, `13`, `15`, `16` |

The last column is a routing rule, not a suggestion. Once the class is stable, move to the owning chapter instead of stretching this page into a supplier comparison, standards crosswalk, or implementation guide.

## Common Collapse Errors

| Mistake | What gets collapsed | Why it is misleading | Better move |
| --- | --- | --- | --- |
| “Which model should we use?” when the real proposal is a hosted API service | model class and managed service | it hides supplier, data-boundary, and exit questions | separate the model from the managed service and compare both at the right level |
| “Which vendor is best?” when the real difference is between products at different layers | supplier and tool or platform | it turns stack design into brand preference | compare products first, then compare suppliers if supplier dependence still matters |
| treating a managed platform as if it were just one tool choice | platform and tool class | it hides workflow coupling, control-plane dependence, and replacement scope | compare the platform against peer platforms first, then compare embedded tools only where local replacement is real |
| putting laws, standards, and products in one table | public anchors and implementation choices | obligations start to look like vendor options | split the reference anchors from the implementation surface |
| using one architecture diagram as if it were one product decision | architecture and component selection | it hides the control points and ownership choices inside the pattern | compare architecture patterns first, then compare the tools that can implement them |
| using a checklist or runbook as if it were evidence by itself | control idea and operating proof | a control artifact matters only if it is owned, used, and reviewable | connect the artifact to owners, thresholds, and review lanes |

## Fast Setup For Entity Tables

* Put the entity class in the first working column before adding fit notes, strengths, or rankings.
* If one candidate bundles a supplier, platform, model, and control promise, split it into separate rows unless the bundle itself is the thing being compared.
* If two rows stop answering the same question, separate them before adding more fields.
* Once the rows are truly like with like, use the minimum fields and row-depth rules from [2.2.3 Comparison Schema](02-02-03-comparison-schema.md).

## Distinctions That Change Real Decisions

* A model is not the same thing as the managed service exposing it. Model quality questions belong beside hosting, gateway, sourcing, and evidence questions rather than replacing them.
* A tool or framework is not the same thing as the supplier behind it. Product fit and supplier dependence should stay reviewable as separate questions.
* A managed platform is not the same thing as a managed API or service. Platform questions usually pull in control-plane coverage, workflow coupling, and replacement scope; service questions are often narrower.
* A standard or regulation is not a product candidate. It sets obligations, vocabulary, or structure; it does not replace implementation design.
* An architecture pattern is not a vendor ranking. It explains how layers should fit together before the team narrows named options.
* A control artifact is not proof because it exists in theory. It matters only when it is tied to owners, thresholds, and a repeatable review lane.

## After You Name The Class

* System or use-case questions belong next in Chapters `03`, `05`, or `16`.
* Model, tool, platform, and service questions belong next in the runtime and stack chapters `07` through `15`, depending on layer.
* Vendor and supplier questions belong next in Chapters `17` and `18`.
* Standards, frameworks, and regulatory-anchor questions belong next in Chapters `04`, `06`, and `20`.
* Architecture and pattern questions belong next in Chapters `03`, `10`, and `19`.
* Control and evidence artifact questions belong next in Chapters `04`, `13`, `15`, and `16`.

## Reviewer Checks

* Has the proposal named one primary entity class before comparing options?
* Can every row be labeled with the same entity class in the first working column, or are mixed classes hiding in one table?
* If a managed platform and a tool both appear, does the page explain whether the decision is really about stack layer, sourcing bundle, or control-plane ownership?
* If a vendor, tool, and standard all appear in the same page, does the page explain why they are there and what each class is doing?
* Before scoring or ranking rows, has the page removed or split rows that answer different questions?
* Are the cross-cutting dimensions from [2.1.2 Cross-Cutting Dimensions And Heuristics](02-01-02-cross-cutting-dimensions-and-heuristics.md) being applied to the right class instead of to everything equally?
* If a local term differs from atlas language, is it normalized back through the [2.1.3 Terminology Ledger](02-01-03-terminology-ledger.md)?
* Once the class is stable, is the page either handing off to the owning chapter or using the reusable rules from [2.2.3 Comparison Schema](02-02-03-comparison-schema.md)?

## Reading Rule

If the entity class is still ambiguous, do not move on to vendor, standards, or tooling comparison yet. The taxonomy pass is supposed to remove category confusion before later chapters narrow the decision. Once the class is clear, hand the issue to the owning chapter instead of trying to settle sourcing, standards, and implementation detail here.

Back to [2.1 Classification Foundations](02-01-00-classification-foundations.md).
