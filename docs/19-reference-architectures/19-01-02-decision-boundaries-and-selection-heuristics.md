# 19.1.2 Decision Boundaries And Selection Heuristics

_Page Type: Decision Guide | Maturity: Draft_

Use this page to narrow the architecture family before comparing detailed reference stacks or named suppliers.

## Decision Lanes

| Lane | Use it when the main question is... |
| --- | --- |
| Speed-first | how to ship quickly with proportionate controls and low platform overhead |
| Shared-control | how to support many teams with one gateway, telemetry, and review model |
| Sovereignty-first | how to maximize operator control, locality, and exit posture |
| Workflow-automation | how to support tool use, approvals, and durable multi-step execution |
| Mixed-method | how to combine predictive ML, retrieval, and language interfaces coherently |

## Practical Heuristics

- Do not jump from use case to tooling without naming the architecture family first.
- If more than one team will depend on the system, re-evaluate whether a thin SaaS-first pattern is about to become an accidental platform.
- Treat sovereignty and exit posture as architecture-level questions, not as procurement clauses layered onto the same managed pattern.
- Default to workflow-first control when the system can take actions, call tools, or trigger downstream processes.
- Choose hybrid predictive-plus-generative patterns when forecasting, scoring, ranking, or optimization remain core to the business outcome.

## Escalate When

- the team cannot explain why a lighter or heavier pattern was rejected
- a managed pattern is being stretched to meet strong locality, auditability, or workflow-control demands
- the same architecture is being proposed for low-risk assistance and high-consequence action-taking work
- the main dispute is really about supplier dependence, data boundary, or governance ownership rather than pattern shape

## Architecture Anti-Patterns

- letting a temporary SaaS-first assistant become the portfolio default without review
- centralizing on a shared gateway or platform without naming service ownership and support burden
- treating self-hosting as a virtue when the organization lacks the operating capacity to sustain it
- forcing one architecture family onto mixed predictive, generative, and workflow-heavy workloads

## Chapter Handoffs

- [3. Enterprise AI Stack Map](../03-enterprise-ai-stack-map/03-00-00-enterprise-ai-stack-map.md)
- [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md)
- [10. Agentic Systems And Orchestration](../10-agentic-systems-and-orchestration/10-00-00-agentic-systems-and-orchestration.md)
- [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md)

Back to [19.1 Architecture Foundations](19-01-00-architecture-foundations.md).
