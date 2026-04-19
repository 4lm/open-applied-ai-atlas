# 5.1.2 Portfolio Boundaries And Prioritization Heuristics

_Page Type: Decision Guide | Maturity: Review-Ready_

Use this page when the chapter has already clarified the work pattern and the remaining question is where the organization should invest, review, or slow down first. The goal is to stop teams from treating every AI proposal as one portfolio and to make consequence, dependence, and operating burden visible before product fashion starts choosing the roadmap.

## Prioritization Lanes

| Lane | Use it when the main question is... | Default prioritization posture |
| --- | --- | --- |
| Assistive enablement lane | whether low-autonomy drafting, search, summarization, or coding support can deliver real worker lift without reshaping policy or approvals | start with the smallest assistive pattern, prove bounded user value, and resist memory, agents, or enterprise-wide platform standardization until the recurring workflow is clear |
| Decision-support lane | whether prediction, ranking, forecasting, optimization, or recommendations will influence consequential human choices even if the system does not act directly | prioritize evaluation quality, interpretation burden, and governance review before interface polish, because a fluent wrapper does not reduce the need for model and decision evidence |
| Sensitive-information lane | whether retrieval, document intelligence, speech, or knowledge surfaces depend on regulated data, permission boundaries, deletion duties, or residency constraints | resolve ownership, data classes, retention, and processor posture before wider rollout, because the wrong boundary choice can invalidate later architecture convenience |
| Action-taking automation lane | whether the system will execute tools, trigger workflows, route cases, or affect external systems with limited human intervention | treat approval design, rollback, exception handling, and observability as day-one scope and keep autonomy narrower than the most optimistic demo suggests |
| Shared-control infrastructure lane | whether an internal gateway, evaluation surface, routing layer, or portfolio platform will quietly shape many later use cases at once | prioritize these surfaces earlier than their novelty suggests, because weak internal controls create repeated portfolio risk even when individual use cases look low consequence |

## Practical Heuristics

- Start with consequence and repeatability together. A one-off executive demo does not deserve the same priority as a recurring workflow that will touch thousands of decisions, employees, customers, or records.
- Separate worker assistance from decision delegation. A system that helps a person draft or search belongs in a different investment and review lane than a system that ranks applicants, routes claims, adjusts prices, or triggers actions.
- Keep predictive and generative families distinct in the portfolio. Forecasting, anomaly detection, recommenders, document extraction, assistants, and agentic workflows do not share the same proof burden just because they all use modern AI techniques.
- Prioritize control surfaces when they are portfolio multipliers. Evaluation, observability, gateway, permission, and review infrastructure can deserve earlier investment than a visible assistant because they determine whether later use cases remain governable.
- Escalate sooner when portability, sovereignty, or supplier dependence matter materially. If a use case depends on a managed control plane, cross-border processing, or one vendor's workflow gravity, treat that dependence as part of prioritization rather than as a sourcing footnote.
- Prefer narrow pattern wins before chapter-wide standardization. A retrieval-backed assistant for one knowledge domain, a document workflow for one intake stream, or a forecasting service for one planning loop is usually a better first move than a generic "AI platform" program.
- Revisit portfolio priority when the system changes the review burden of another system. If a gateway, evaluation suite, or document pipeline becomes necessary to keep other AI services safe, it is no longer secondary infrastructure.

## Escalate When

- the same initiative is describing chat assistance, retrieval, workflow automation, forecasting, and agentic execution as one use case with one owner and one approval path
- leadership pressure is favoring highly visible demos while internal control surfaces, evaluation assets, or data-boundary work remain unfunded
- a low-autonomy assistive proposal is quietly accumulating tool execution, long-lived memory, or policy-significant recommendation power
- teams want one portfolio standard despite materially different consequence profiles across customer-facing, employee-facing, back-office, and infrastructure-facing systems
- the expected value depends mainly on a managed suite, bundled workflow engine, or provider-specific knowledge graph, but exit, portability, and substitute operating paths are still vague
- nobody can name the highest-consequence failure, the fallback process, or the accountable owner for the proposed use case family

## Portfolio Anti-Patterns

- one-chatbot strategy: using a single assistant narrative to flatten document intelligence, predictive analytics, workflow automation, and action-taking systems into the same roadmap
- autonomy inflation: starting with assistance language and then widening into execution, approvals, or system actions without reopening the portfolio priority call
- demo-led prioritization: funding the most impressive interface rather than the use case with the clearest repeatable value and governable operating model
- governance-by-category-label: calling something "internal only", "copilot", or "AI platform" instead of naming the real data class, consequence, and action surface
- infrastructure blindness: underinvesting in evaluation, gateway, observability, or review systems because they are less visible than end-user experiences
- open-by-default reasoning: assuming an open model, framework, or project is automatically the right first bet even when staffing, security, hosting, or exit posture are still weak

## Chapter Handoffs

- [04. Governance Risk Compliance](../04-governance-risk-compliance/04-00-00-governance-risk-compliance.md) when portfolio sequencing depends mainly on policy ownership, regulated decisions, or control approval forums.
- [06. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md) when sensitive information classes, retention, residency, or processor posture are the real prioritization constraint.
- [10. Agentic Systems And Orchestration](../10-agentic-systems-and-orchestration/10-00-00-agentic-systems-and-orchestration.md) when the debate has shifted from use-case family to tool execution, bounded autonomy, and orchestration design.
- [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md) when the priority call depends on proving forecast quality, recommendation quality, extraction quality, or user-lift claims rather than on chapter-level categorization alone.
- [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) when a use case needs explicit approval lanes, intervention rights, or reviewer capacity design before expansion.
- [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when portfolio order is being driven more by supplier dependence, suite gravity, or operating burden than by the work pattern itself.

## Practical Reading Rule

Choose the lane that matches the hardest consequence, dependence, and operating burden in the proposed family, then fund the smallest version that can prove value without hiding the next control problem. If the portfolio story still starts with a vendor, a model, or an "AI platform" slogan instead of a bounded work pattern and a named failure consequence, the prioritization logic is still too weak.

Back to [5.1 Use-Case Foundations](05-01-00-use-case-foundations.md).
