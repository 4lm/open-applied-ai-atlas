# 2.1.2 Cross-Cutting Dimensions And Heuristics

_Page Type: Decision Guide | Maturity: Review-Ready_

Use this page to decide which cross-cutting dimensions belong in the analysis before a local preference turns into a misleading comparison. The taxonomy layer is not a scoring system. It is a triage step that decides what kind of thing is being reviewed, which dimensions matter, and which chapter owns the next decision.

## Step 1: Identify The Entity Class First

* Ask "what kind of thing is this?" before asking "which option is best?"
* If the answer is a system or use case, compare system shapes, oversight needs, and operating consequences.
* If the answer is a model, tool, managed platform, managed service or API, vendor, standard, or architecture, keep that class separate even when one procurement package combines them.
* If the proposal mixes classes in one paragraph, split it before assigning scores, risks, or rankings.

## Step 2: Apply The Right Dimensions

The same dimensions recur across the atlas, but they should not be weighted equally for every class.

Read the columns literally. `Always-visible` means the page should usually name those dimensions even in a short comparison. `Add when the decision needs it` means bring them in only when they change the decision materially. `Usually secondary or misleading if overused` marks dimensions that often look sophisticated while pulling the review off the real question.

| Entity class | Always-visible dimensions | Add when the decision needs it | Usually secondary or misleading if overused |
| --- | --- | --- | --- |
| Organizational use case or AI system | consequence model, compliance exposure, privacy boundary, sovereignty exposure, lock-in and exit posture | openness posture, portability implications, observability implications, security implications, governance implications | raw benchmark comparison detached from workflow, ownership, or failure consequences |
| Model or model family | primary purpose, openness posture, portability implications, lifecycle fit, lock-in and exit posture | privacy implications, sovereignty exposure, operational complexity, fit by organization type | treating supplier brand or one hosting choice as if it settles the whole model decision |
| Tool, framework, or project | primary purpose, stack layer, openness posture, portability implications, operational complexity | security implications, observability implications, governance implications, data boundary implications | using legal or management-system language as the primary comparison field |
| Managed platform | control posture, workflow coupling, data boundary implications, observability implications, lock-in and exit posture | sovereignty exposure, privacy implications, governance implications, support-path dependence | treating one embedded tool or model brand as if it settles the whole platform decision |
| Managed service or API | control posture, support-path dependence, data boundary implications, portability implications, lock-in and exit posture | sovereignty exposure, privacy implications, observability implications, governance implications | assuming convenience or speed makes control loss and exit burden irrelevant |
| Vendor or organization | concentration, stewardship, roadmap control, support posture, exit posture | sovereignty exposure, contract dependence, ecosystem leverage, evidence responsiveness | using feature checklists alone to compare suppliers |
| Standard, framework, or regulation | compliance exposure, governance implications, evidence implications | portability, sourcing, security, or privacy only after the legal or governance role is clear | scoring it like a product, service, or runtime option |
| Architecture or pattern | sovereignty exposure, portability implications, privacy boundary, control posture, lock-in and exit posture | security implications, observability implications, governance implications, operational complexity | treating one benchmark, product row, or supplier name as enough to choose the pattern |
| Control or evidence artifact | owner clarity, reviewability, repeatability, evidence usefulness, threshold logic | audit trail depth, operational burden, governance implications | treating a blank template, checklist, or policy statement as if it were operating proof |

## Step 3: Ask The Dependence And Control Questions Early

Many weak comparisons happen because the page notices dependence too late.

Check these questions early:

* Does the hard dependence sit mainly in the supplier contract, the workflow coupling, the data gravity, the control plane, the model adaptation path, or the operator skills required to run the stack?
* If the option is managed, which controls stay visible, exportable, or independently testable, and which controls are inherited on trust?
* Does “open” actually improve exit posture here, or does the real lock-in sit in policy logic, telemetry paths, plugins, data movement, or local expertise?
* Are portability, privacy, sovereignty, and control posture pointing in the same direction here, or does one improve while another gets weaker?
* Which dimensions are first-order for this class, and which ones are only familiar because they mattered in a different class?

## Step 4: Hand Off To The Dominant Chapter

Once the class and dimensions are clear, move the work to the chapter that owns the real decision. Do not keep adding dimensions once one chapter clearly owns the next meaningful step.

| When the dominant question becomes... | Move to... | Why |
| --- | --- | --- |
| system boundaries, layer ownership, or control-point placement | [3. Enterprise AI Stack Map](../03-enterprise-ai-stack-map/03-00-00-enterprise-ai-stack-map.md) | Chapter `03` maps where the thing actually sits in the stack |
| model capability, modality, or lifecycle fit | [7. Model Ecosystem](../07-model-ecosystem/07-00-00-model-ecosystem.md) | Chapter `07` owns model families, capability lanes, and model-specific trade-offs |
| hosting boundary, tenancy, or managed-versus-self-hosted runtime posture | [8. Model Hosting And Inference](../08-model-hosting-and-inference/08-00-00-model-hosting-and-inference.md) | Chapter `08` separates runtime control posture from model choice |
| gateway routing, access control, or control-plane policy enforcement | [9. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md) | Chapter `09` owns shared gateway and policy-layer decisions |
| approval lanes, policy ownership, or evidence design | [4. Governance Risk Compliance](../04-governance-risk-compliance/04-00-00-governance-risk-compliance.md) | Chapter `04` separates governance structure from local terminology |
| use-case fit, task shape, or oversight consequences | [5. Use Cases And Application Landscapes](../05-use-cases-and-application-landscapes/05-00-00-use-cases-and-application-landscapes.md) | Chapter `05` owns use-case distinctions and their downstream implications |
| residency, retention, support access, or jurisdictional exposure | [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md) | Chapter `06` owns boundary and handling questions |
| evaluation thresholds, release gates, or failure measurement | [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md) | Chapter `13` turns system concerns into test, release, and review evidence |
| telemetry export, incident evidence, or operator visibility | [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md) | Chapter `14` owns runtime visibility and operating evidence |
| hardening, abuse resistance, or least-privilege control design | [15. Security And Abuse Resistance](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md) | Chapter `15` owns threat surface and control-hardening work |
| supplier concentration, market leverage, or ecosystem stewardship | [17. Vendors Organizations And Market Structure](../17-vendors-organizations-and-market-structure/17-00-00-vendors-organizations-and-market-structure.md) | Chapter `17` compares actors rather than products |
| build versus buy versus hybrid control posture | [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) | Chapter `18` turns dependence and exit posture into sourcing decisions |
| legal text, standards, frameworks, or public bodies need to be combined correctly | [20. Standards Frameworks And Bodies Of Knowledge](../20-standards-frameworks-and-bodies-of-knowledge/20-00-00-standards-frameworks-and-bodies-of-knowledge.md) | Chapter `20` distinguishes obligations, frameworks, and bodies of knowledge |
| the issue is implementation detail inside retrieval, memory, training, fine-tuning, or adaptation work | the relevant implementation chapters `11` and `12` | The taxonomy pass should stop once the comparison becomes layer-specific rather than taxonomy-level |

## Shortcut Errors To Stop Early

* Do not use openness language as a proxy for sovereignty, compliance, or exit posture.
* Do not treat lock-in as only an API concern when it may also sit in data gravity, workflow coupling, control planes, support paths, or supplier expertise.
* Do not let a managed platform row inherit the same dimension logic as a narrower managed service or API row. Their control surfaces and exit burdens are often different.
* Do not assume the taxonomy only matters for LLM tools. Forecasting, recommender, optimization, vision, speech, and hybrid systems still need the same class-first discipline.
* Do not jump to named vendors when the real uncertainty is still about entity class or chapter ownership.
* Do not widen a comparison table before checking whether the wrong dimensions are making the table unstable.

## Reading Rule

The taxonomy pass is complete when the team can name the class, apply the right dimensions, and hand the issue to the correct chapter without mixing product, supplier, and standards logic together.

Back to [2.1 Classification Foundations](02-01-00-classification-foundations.md).
