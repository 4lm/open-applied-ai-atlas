# 2.1.2 Cross-Cutting Dimensions And Heuristics

_Page Type: Decision Guide | Maturity: Draft_

Use this page to decide which cross-cutting dimensions belong in the analysis before a local preference turns into a misleading comparison. The taxonomy layer is not a scoring system; it is a triage step that decides what kind of thing is being reviewed, which dimensions matter, and which chapter owns the next decision.

## Step 1: Identify The Entity Class First

- Ask "what kind of thing is this?" before asking "which option is best?"
- If the answer is a system or use case, compare system shapes and operating consequences.
- If the answer is a model, tool, service, vendor, standard, or architecture, keep that class separate even when one procurement package combines them.
- If the proposal mixes classes in one paragraph, split it before assigning scores, risks, or rankings.

## Step 2: Apply The Right Dimensions

The same dimensions recur across the atlas, but they should not be weighted equally for every class.

| Entity class | Always-visible dimensions | Add when the decision needs it | Usually secondary or misleading if overused |
| --- | --- | --- | --- |
| Organizational use case or AI system | Compliance exposure, privacy, sovereignty, lock-in and exit posture | Openness, portability, observability, security, governance implications | Raw benchmark comparison detached from workflow consequences |
| Model or model family | Openness posture, portability, lock-in and exit posture | Privacy, sovereignty, operational complexity, fit by organization type | Treating supplier brand as the whole decision |
| Tool, framework, or project | Openness posture, portability, operational complexity | Security, observability, governance implications, data boundary implications | Using legal or management-system language as the primary comparison field |
| Managed platform or service | Sovereignty, privacy, portability, lock-in and exit posture | Openness posture, observability, governance implications, support-path dependence | Assuming speed-to-value makes control posture irrelevant |
| Vendor or organization | Concentration, stewardship, roadmap control, exit posture | Sovereignty, contract dependence, support model, ecosystem leverage | Using feature checklists alone to compare suppliers |
| Standard, framework, or regulation | Compliance exposure, governance implications, evidence implications | Portability, sourcing, or security only after the legal or governance role is clear | Scoring it like a product or runtime option |
| Architecture or pattern | Sovereignty, portability, privacy, lock-in and exit posture | Security, observability, governance implications, operational complexity | Treating one benchmark or one vendor row as enough to choose the pattern |

## Step 3: Hand Off To The Dominant Chapter

Once the class and dimensions are clear, move the work to the chapter that owns the real decision.

| When the dominant question becomes... | Move to... | Why |
| --- | --- | --- |
| system boundaries, layer ownership, or control-point placement | [3. Enterprise AI Stack Map](../03-enterprise-ai-stack-map/03-00-00-enterprise-ai-stack-map.md) | Chapter `03` maps where the thing actually sits in the stack |
| approval lanes, policy ownership, or evidence design | [4. Governance Risk Compliance](../04-governance-risk-compliance/04-00-00-governance-risk-compliance.md) | Chapter `04` separates governance structure from local terminology |
| residency, retention, support access, or jurisdictional exposure | [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md) | Chapter `06` owns boundary and handling questions |
| supplier concentration, market leverage, or ecosystem stewardship | [17. Vendors Organizations And Market Structure](../17-vendors-organizations-and-market-structure/17-00-00-vendors-organizations-and-market-structure.md) | Chapter `17` compares actors rather than products |
| build versus buy versus hybrid control posture | [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) | Chapter `18` turns dependence and exit posture into sourcing decisions |
| legal text, standards, frameworks, or public bodies need to be combined correctly | [20. Standards Frameworks And Bodies Of Knowledge](../20-standards-frameworks-and-bodies-of-knowledge/20-00-00-standards-frameworks-and-bodies-of-knowledge.md) | Chapter `20` distinguishes obligations, frameworks, and bodies of knowledge |
| the issue is implementation detail inside model, retrieval, evaluation, observability, or security work | The relevant runtime and assurance chapters `07` through `15` | The taxonomy pass should stop once the comparison becomes layer-specific |

## Shortcut Errors To Stop Early

- Do not use openness language as a proxy for sovereignty, compliance, or exit posture.
- Do not treat lock-in as only an API concern when it may also sit in data gravity, workflow coupling, control planes, or supplier expertise.
- Do not assume the taxonomy only matters for LLM tools. Forecasting, recommender, optimization, vision, speech, and hybrid systems still need the same class-first discipline.
- Do not jump to named vendors when the real uncertainty is still about entity class or chapter ownership.

## Reading Rule

The taxonomy pass is complete when the team can name the class, apply the right dimensions, and hand the issue to the correct chapter without mixing product, supplier, and standards logic together.

Back to [2.1 Classification Foundations](02-01-00-classification-foundations.md).
