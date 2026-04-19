# 5.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use this page during rollout review, portfolio renewal, and platform-standardization debates to recognize healthy operating shapes before assistance, prediction, extraction, and automation work get flattened into one "AI program" with one owner and one control story.

## Reusable Use-Case Portfolio Patterns

| Pattern | What good looks like | Fit signal | Review warning |
| --- | --- | --- | --- |
| Typed portfolio lanes before platform standardization | The organization classifies work into assistive, decision-support, sensitive-information, action-taking, and shared-control infrastructure lanes before it standardizes tools, funding, or approvals | several teams want one common AI roadmap, but their systems differ materially in consequence, data class, or action surface | people can name the preferred suite or model, but cannot say which lane the work belongs to or why one lane should inherit another lane's controls |
| Small first release with explicit fallback and expansion boundary | Each use-case family starts with a narrow production shape, named fallback process, and a clear statement of what is intentionally out of scope until new proof exists | delivery pressure is high and the portfolio needs early value without accidental autonomy growth | the first release is described as a pilot, but nobody can show what stays manual, what happens when the system fails, or what evidence would justify a broader pattern |
| Shared-control infrastructure treated as a product, not plumbing | Gateways, evaluation surfaces, routing layers, retrieval corpora, and approval paths are given owners, service expectations, and portability notes because many later use cases will depend on them | internal enablement systems are becoming prerequisites for multiple visible use cases | leadership treats these surfaces as secondary engineering detail even though later rollout quality and governance depend on them |
| Consequence-scaled oversight and review packet | Approval rights, exception handling, and release evidence scale with the strongest consequence in the use-case family instead of with the most convenient interface label | the portfolio mixes chat assistance, extraction, recommendation, or workflow execution, and some outputs can affect rights, money, safety, or regulated outcomes | the team is reusing one review ritual for every system because they all "use AI" |
| Domain-owned knowledge and document boundaries | Retrieval-backed assistants and document-intelligence workflows keep source ownership, permission scope, update cadence, and deletion obligations visible at the domain level before they join a shared platform story | the portfolio depends on changing policies, operational content, or regulated records rather than static prompt behavior alone | rollout conversations focus on model quality while nobody owns source freshness, revocation, or exception handling for the underlying content |
| Re-review trigger register across the portfolio | Every lane keeps explicit triggers for reopening governance, privacy, retrieval, evaluation, observability, oversight, or sourcing review before the portfolio drifts into a new operating model | one successful deployment is already being used as justification for reuse in new domains or higher-consequence tasks | teams can describe the current use case, but cannot say what change would force them to revisit earlier chapter decisions |

## Use-Case Portfolio Anti-Patterns

| Anti-pattern | Why it fails | Early signal | Review action |
| --- | --- | --- | --- |
| One-chatbot portfolio flattening | A single assistant narrative hides the real differences between retrieval, predictive scoring, document extraction, and action-taking workflows, so the portfolio inherits the wrong architecture and approval model | roadmap language keeps collapsing everything into "copilot" or "agent" even when the work patterns differ | reopen [5.1 Use-Case Foundations](05-01-00-use-case-foundations.md) and force lane selection before more standardization work |
| Assistive-to-automation drift | A drafting or search system quietly accumulates tool execution, workflow control, or policy-significant recommendations without reopening consequence and oversight review | the team still describes the system as assistive, but new features now trigger external actions, route cases, or shape consequential decisions | send the design back through [10. Agentic Systems And Orchestration](../10-agentic-systems-and-orchestration/10-00-00-agentic-systems-and-orchestration.md), [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md), and [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) |
| Shared platform with hidden centralization | A common suite, gateway, or workflow layer becomes the real product and policy owner, but accountability, portability, and substitute operating paths remain vague | teams say the platform will "handle governance" or "solve integration" without naming domain owners and exit posture | reopen [09. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md), [17. Vendors Organizations And Market Structure](../17-vendors-organizations-and-market-structure/17-00-00-vendors-organizations-and-market-structure.md), and [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) before rollout expands |
| Retrieval or document workflow without source ownership | Good demos mask weak source stewardship, permission control, or deletion handling, so answer quality and auditability degrade as the portfolio scales | the team can show relevant outputs, but cannot name source owners, freshness rules, or revocation behavior | route the work back through [06. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md) and [11. Knowledge Retrieval And Memory](../11-knowledge-retrieval-and-memory/11-00-00-knowledge-retrieval-and-memory.md) before wider adoption |
| Predictive or recommendation work hidden behind a fluent interface | Conversation design makes the system feel like assistance even though the real power comes from scoring, ranking, or optimization that needs stronger evidence and review | stakeholders mainly discuss prompt quality or UX while the system is quietly influencing prices, triage, entitlement, routing, or prioritization | reopen [03. Enterprise AI Stack Map](../03-enterprise-ai-stack-map/03-00-00-enterprise-ai-stack-map.md) and [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md) to restate the dominant system family and proof burden |
| Pilot success treated as enterprise proof | A good bounded launch becomes an argument for platform-wide rollout even though staffing, exception handling, privacy posture, and supplier dependence have not been retested in the new context | the next proposal starts with "we already proved this works elsewhere" instead of showing the new domain packet | require a new evidence packet with chapter handoffs into `04`, `06`, `14`, `16`, or `18` before scale-out approval |

## Review Prompts

- Which portfolio pattern is doing the real safety and delivery work here: typed lanes, narrow-first release, shared-control infrastructure ownership, consequence-scaled oversight, domain-owned knowledge boundaries, or explicit re-review triggers?
- What has to remain local to the use-case family instead of being standardized too early: source ownership, evaluation set, reviewer packet, workflow boundary, or supplier choice?
- Which anti-pattern is most likely under current pressure: one-chatbot flattening, autonomy drift, hidden centralization, source-owner gaps, predictive work disguised as chat, or pilot-to-platform overreach?
- Which adjacent chapter must re-enter before approval: `04`, `06`, `09`, `10`, `11`, `13`, `14`, `16`, `17`, or `18`?

## Re-Review Triggers

- a nominally assistive or retrieval-backed service gains tool execution, case routing, or other external side effects
- a domain-specific success is reused for another business unit, jurisdiction, or data class without a fresh owner and evidence packet
- a shared gateway, retrieval corpus, workflow engine, or vendor suite becomes mandatory infrastructure for multiple lanes
- forecast, ranking, recommendation, or optimization outputs start driving policy, pricing, staffing, entitlement, or escalation decisions
- exception volume, reviewer load, content freshness, or portability dependence changes enough that the original fallback and control model no longer fit

## Practical Reading Rule

Use these patterns after the task family and initial solution pattern are clear but before the organization calls the rollout model settled. If the team cannot show bounded portfolio lanes, a narrow first release, owned control surfaces, consequence-matched review, and explicit triggers for reopening the decision, the use-case portfolio is still too weak to standardize.

Back to [5.2 Applying Use-Case Portfolios](05-02-00-applying-use-case-portfolios.md).
