# 2.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Review-Ready_

Use this file during review after the team has named the entity class and started shaping the first comparison surface. The point is to catch recurring taxonomy mistakes quickly enough that later chapter work is still fixable.

## Patterns To Reuse

| Pattern | Good shape in practice | What it protects |
| --- | --- | --- |
| Classify before comparing | The page names the primary entity class and the first comparison surface before any ranking language appears | Prevents mixed-category tables and false equivalence |
| Choose the first comparison surface on purpose | The first table compares peers answering the same question, while supplier, standards, and architecture questions are split out until they become the real decision | Prevents the wrong first surface from shaping every later trade-off |
| Separate managed services or APIs from managed platforms | A bounded capability call is compared with peer services, while integrated workflow or control-plane offerings are compared with peer platforms | Prevents service speed from hiding platform coupling and control loss |
| Separate product choice from standards choice | A runtime decision is compared against peer products, while laws and frameworks are used as reference anchors and control inputs | Keeps governance language from replacing design work |
| Separate openness from sovereignty | The review names source availability, deployment control, support dependence, telemetry exposure, and jurisdictional exposure independently | Prevents "open" from hiding control risk |
| Pick entities because they change the decision | The first surface includes representative, chapter-relevant entities rather than easy or familiar names | Prevents shallow, brand-led, or arbitrary comparison surfaces |
| Deepen rows before widening columns | The page makes each row explain a real trade-off before adding decorative fields | Prevents table polish from hiding thin comparison logic |
| Normalize vendor language back to atlas terms | Marketing categories are translated into the shared terms in [2.1.3 Terminology Ledger](02-01-03-terminology-ledger.md) before they enter the atlas | Keeps chapter language stable across suppliers |
| Keep non-LLM applicability visible | Retrieval, forecasting, recommender, optimization, and classical-ML examples remain legible alongside chat or agentic examples | Preserves the repository's broad applied-AI scope |

## Anti-Patterns To Stop

| Anti-pattern | Why it distorts the review | Corrective move |
| --- | --- | --- |
| Starting with the wrong first table | If the first surface mixes supplier, standards, architecture, and product rows, every later judgment gets pulled off the real decision | Name the first question explicitly and keep the first table narrow until that question is stable |
| Mixing vendors with standards in one table | It makes obligations, supplier dependence, and product fit look interchangeable | Split the table by entity class and move standards work to chapter `20` |
| Treating a managed platform row as if it were just another service row | Workflow scope, control-plane ownership, and exit burden disappear behind a convenience comparison | Split platform and service surfaces unless the page explains clearly why both belong in the same view |
| Using "open" as a proxy for portability or compliance | Source availability does not tell you who operates the system, where the data sits, or how easy exit really is | Re-score with sovereignty, privacy, and exit posture visible separately |
| Treating frameworks as proof of implementation | A cited framework can look complete even when no controls, owners, or evidence exist | Ask which internal artifact, test, or review lane the framework changes |
| Comparing a model row to a service row without naming the difference | Capability, supplier, hosting, and control trade-offs get flattened into one misleading score | Split model, managed-service or API, platform, and vendor comparisons into separate surfaces |
| Reusing dimensions out of habit | Familiar dimensions from another class make the table look rigorous while hiding the real control, dependence, or boundary questions | Re-check which dimensions are first-order for this class before widening the surface |
| Keeping weak rows for symmetry or name recognition | The table gets longer without helping the reader choose or review better | Prune the rows and keep only entities that improve the decision |
| Adding columns instead of fixing selection or depth | The table looks richer while staying shallow | Rebuild the comparison logic, entity set, and row content before widening the surface |

## Fast Review Prompts

- What is the first comparison surface here: systems, models, tools, managed services or APIs, managed platforms, suppliers, standards, or architectures?
- Does every current row answer that same first question, or are supplier, standards, and architecture rows sneaking into a product comparison too early?
- If both a managed service or API and a managed platform appear, has the page explained whether the decision is about bounded capability access or integrated workflow and control-plane scope?
- Which rows are here because they change the decision, and which rows are here only because the names are familiar?
- Which cross-cutting dimensions are first-order for this class, and which ones are being dragged in from another class out of habit?
- Would splitting supplier posture, standards anchors, or architecture patterns into a second surface make the first table more honest and more readable?
- If a standard or framework is named, what concrete control, evidence, or review lane does it change?
- If a vendor claim uses words like "open," "private," or "sovereign," which atlas dimensions still need to be checked separately?
- Would this page still make sense for a non-LLM system such as forecasting, ranking, optimization, or vision?

## Reading Rule

Use the patterns here to stress-test draft comparison or policy material after [2.2.1 Worked Classification Scenarios](02-02-01-worked-classification-scenarios.md) has stabilized the first surface. If the anti-patterns still describe the page accurately, the review is not finished.

Back to [2.2 Applying The Taxonomy](02-02-00-applying-the-taxonomy.md).
