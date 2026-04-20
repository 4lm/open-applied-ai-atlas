# 2.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Review-Ready_

Use this file during review after the team has named the entity class. The point is to catch recurring taxonomy mistakes quickly enough that later chapter work is still fixable.

## Patterns To Reuse

| Pattern | Good shape in practice | What it protects |
| --- | --- | --- |
| Classify before comparing | The page names whether it is comparing systems, models, tools, vendors, standards, or architectures before any ranking language appears | Prevents mixed-category tables and false equivalence |
| Separate product choice from standards choice | A runtime decision is compared against peer products, while laws and frameworks are used as reference anchors and control inputs | Keeps governance language from replacing design work |
| Separate openness from sovereignty | The review names source availability, deployment control, support dependence, telemetry exposure, and jurisdictional exposure independently | Prevents "open" from hiding control risk |
| Pick entities because they change the decision | The table includes representative, chapter-relevant entities rather than easy or familiar names | Prevents shallow, brand-led, or arbitrary comparison surfaces |
| Deepen rows before widening columns | The page makes each row explain a real trade-off before adding decorative fields | Prevents table polish from hiding thin comparison logic |
| Normalize vendor language back to atlas terms | Marketing categories are translated into the shared terms in [2.1.3 Terminology Ledger](02-01-03-terminology-ledger.md) before they enter the atlas | Keeps chapter language stable across suppliers |
| Keep non-LLM applicability visible | Retrieval, forecasting, recommender, optimization, and classical-ML examples remain legible alongside chat or agentic examples | Preserves the repository's broad applied-AI scope |

## Anti-Patterns To Stop

| Anti-pattern | Why it distorts the review | Corrective move |
| --- | --- | --- |
| Mixing vendors with standards in one table | It makes obligations, supplier dependence, and product fit look interchangeable | Split the table by entity class and move standards work to chapter `20` |
| Using "open" as a proxy for portability or compliance | Source availability does not tell you who operates the system, where the data sits, or how easy exit really is | Re-score with sovereignty, privacy, and exit posture visible separately |
| Treating frameworks as proof of implementation | A cited framework can look complete even when no controls, owners, or evidence exist | Ask which internal artifact, test, or review lane the framework changes |
| Letting local terminology drift from chapter `02` | Teams silently redefine terms and later chapters stop comparing like with like | Normalize back to the terminology ledger before publishing or reviewing |
| Comparing a model row to a service row without naming the difference | Capability, supplier, hosting, and control trade-offs get flattened into one misleading score | Split model, managed-service, and vendor comparisons into separate surfaces |
| Keeping weak rows for symmetry or name recognition | The table gets longer without helping the reader choose or review better | Prune the rows and keep only entities that improve the decision |
| Adding columns instead of fixing selection or depth | The table looks richer while staying shallow | Rebuild the comparison logic, entity set, and row content before widening the surface |

## Fast Review Prompts

- What entity class is each row actually describing?
- Which rows are here because they improve the decision, and which rows are here only because the names are familiar?
- Which cross-cutting dimensions are first-order for that class, and which are being added out of habit?
- If a standard or framework is named, what concrete control, evidence, or review lane does it change?
- If a vendor claim uses words like "open," "private," or "sovereign," which atlas dimensions still need to be checked separately?
- Would this page still make sense for a non-LLM system such as forecasting, ranking, optimization, or vision?

## Reading Rule

Use the patterns here to stress-test draft comparison or policy material before it becomes chapter-local doctrine. If the anti-patterns still describe the page accurately, the review is not finished.

Back to [2.2 Applying The Taxonomy](02-02-00-applying-the-taxonomy.md).
