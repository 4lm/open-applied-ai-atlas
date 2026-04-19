# 3.1.2 Boundaries, Dependencies, And Reading Heuristics

_Page Type: Decision Guide | Maturity: Draft_

Use this page to decide whether the issue in front of you is really a stack-mapping problem, or whether another chapter now owns the decision.

## Decision Lanes

| Lane | Use it when the main question is... |
| --- | --- |
| Layer-location | where a capability belongs and which layer must own the decision |
| Control-placement | where policy, approval, logging, redaction, or monitoring should sit |
| Dependency-reading | whether a supplier, gateway, workflow, or data choice creates hidden coupling |
| Handoff-to-architecture | whether the team is now choosing a reusable architecture family rather than locating a responsibility |

## Practical Heuristics

- Map the full path before comparing vendors: governance, data boundary, model access, runtime, workflow, evaluation, and operating controls.
- Treat shared gateways, telemetry, and identity systems as architecture-shaping layers, not as implementation detail.
- Do not let a model-quality discussion replace questions about data access, approval ownership, or release evidence.
- Revisit the stack map whenever the deployment posture changes from managed to self-hosted, from single-team to shared platform, or from advisory to action-taking.
- Use chapter `19` only after the layer map is stable enough that reusable architecture families can be compared meaningfully.

## Escalate When

- the team cannot say which layer owns policy, budget, telemetry, or rollback
- a single product is being asked to solve governance, hosting, retrieval, and workflow concerns all at once
- the main disagreement is no longer about layer placement but about sourcing, sovereignty, or architecture family
- two apparently different options still rely on the same hidden cloud, gateway, or support dependency

## Common Failure Modes

- picking a model before deciding which data and review constraints dominate
- treating the gateway as optional even though multiple teams, suppliers, or budgets must be coordinated
- assuming self-hosting settles privacy or sovereignty questions without reviewing support access and evidence burden
- confusing a reference architecture with the stack map that explains why the architecture exists

## Chapter Handoffs

- [4. Governance Risk Compliance](../04-governance-risk-compliance/04-00-00-governance-risk-compliance.md)
- [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md)
- [10. Agentic Systems And Orchestration](../10-agentic-systems-and-orchestration/10-00-00-agentic-systems-and-orchestration.md)
- [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md)
- [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md)
- [19. Reference Architectures](../19-reference-architectures/19-00-00-reference-architectures.md)

Back to [3.1 Stack Foundations](03-01-00-stack-foundations.md).
