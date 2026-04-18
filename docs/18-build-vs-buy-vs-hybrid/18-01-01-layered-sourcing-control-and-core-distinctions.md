# 18.1.1 Layered Sourcing, Control, And Core Distinctions

_Page Type: Concept Explainer | Maturity: Review-Ready_

Use this page to separate sourcing questions by layer before arguing about named vendors or hosting products. Build-vs-buy only becomes useful when the team can say which part of the stack is being sourced, where real control sits, and which dependence will be hardest to unwind later.

## Layered Sourcing Matrix

| Layer | Typical sourcing bias | Build or own it when... | Buy or outsource it when... | Hidden dependence risk | Adjacent chapter |
| --- | --- | --- | --- | --- | --- |
| Model access | Buy or hybrid | model behavior, weights, or runtime control are strategic or regulated | speed, breadth, and supplier support matter more than model ownership | provider APIs, policy changes, and model retirement become the real constraint | [07. Model Ecosystem](../07-model-ecosystem/07-00-00-model-ecosystem.md) |
| Hosting and inference runtime | Hybrid | latency, locality, cost control, or hardware policy justify direct runtime ownership | the organization is not ready to own GPUs, upgrades, and serving reliability | hosted inference can lock the team into one cloud, one acceleration path, or one support channel | [08. Model Hosting And Inference](../08-model-hosting-and-inference/08-00-00-model-hosting-and-inference.md) |
| Gateway and control plane | Build or hybrid | routing, policy, budgets, approvals, or multi-provider abstraction must stay internal | one managed estate already provides proportionate controls | the gateway can become the real lock-in layer even when models look portable | [09. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md) |
| Retrieval and data layer | Hybrid | permissions, freshness, provenance, and exit posture depend on internal control | the content is low-risk and governance demands are modest | a managed retrieval layer can absorb the sensitive data, permission, and audit burden | [11. Knowledge Retrieval And Memory](../11-knowledge-retrieval-and-memory/11-00-00-knowledge-retrieval-and-memory.md) |
| Workflow and application logic | Build | the process itself creates differentiation, risk controls, or domain leverage | the workflow is commodity and tightly tied to a purchased suite | buying the app can quietly transfer business logic ownership to the vendor | [10. Agentic Systems And Orchestration](../10-agentic-systems-and-orchestration/10-00-00-agentic-systems-and-orchestration.md) |
| Telemetry and evidence layer | Build or compose around portable tools | auditability, cross-provider comparison, and incident reconstruction must stay exportable | vendor-native visibility is sufficient for a low-consequence workload | teams think they have portability until traces, evals, and review evidence are trapped in one estate | [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md) |
| Service operations and support model | Hybrid | the service is becoming a real internal platform with support, SLAs, and review obligations | the workload is narrow enough that managed support is proportionate | integrators or SaaS operators can become the irreplaceable operating memory of the system | [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) |

## Core Distinctions

| Distinction | Why it matters |
| --- | --- |
| Vendor contract vs. real control | Buying one supplier does not mean the organization controls data paths, policies, telemetry, or migration timing. |
| Hosting choice vs. sourcing choice | Self-hosting one layer does not mean the rest of the system is built; managed hosting can still sit inside an otherwise portable design. |
| Commodity layer vs. differentiating layer | A team should only own the burden of a layer when it can name the strategic, regulatory, or operating reason. |
| Exit posture vs. present convenience | Migration difficulty is determined by data, workflow, and evidence dependence, not only by the initial contract term. |
| Bought capability vs. bought operating model | Managed services often bundle support, incident response, upgrade cadence, and control logic along with the technical feature. |

## What Reviewers Should Check

- Which layer is actually being proposed for ownership, and which layers are merely assumed to come along with it?
- Where would the organization feel lock-in first: runtime, data plane, workflow, or operating evidence?
- Is the proposal buying speed in one layer while accidentally outsourcing the control plane somewhere else?
- If the supplier changed terms or the integrator exited, which layer would break first?

## Reading Rule

Use this page to name the layer and dependence shape first. Then move to [18.1.2 Decision Boundaries And Sourcing Heuristics](18-01-02-decision-boundaries-and-sourcing-heuristics.md) and [18.1.3 Build Buy And Hosting Decision Tree](18-01-03-build-buy-and-hosting-decision-tree.md) to narrow the actual sourcing choice.

Back to [18.1 Sourcing Foundations](18-01-00-sourcing-foundations.md).
