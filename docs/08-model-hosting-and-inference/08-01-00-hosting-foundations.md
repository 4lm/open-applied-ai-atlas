# 8.1 Hosting Foundations

_Page Type: Chapter Index | Maturity: Review-Ready_

This section establishes the runtime-posture distinctions teams need before they turn hosting into a vendor default or an infrastructure vanity project. Use it to separate provider-managed APIs, dedicated managed deployments, self-hosted runtimes, edge placements, and sovereignty-constrained environments so later comparisons stay anchored to control, evidence, and operating burden instead of to pricing anecdotes alone.

## Section Map

- 8.1.1 [Runtime Postures, Constraints, And Core Distinctions](08-01-01-runtime-postures-constraints-and-core-distinctions.md)
- 8.1.2 [Decision Boundaries And Deployment Heuristics](08-01-02-decision-boundaries-and-deployment-heuristics.md)

## What This Section Helps Decide

- whether the workload can stay on a provider-managed inference path or needs a more isolated, dedicated, or self-operated runtime
- when latency, throughput, GPU dependence, residency, or offline-operability constraints materially change the acceptable hosting lane
- which responsibilities belong to the application team, platform team, managed provider, or hardware estate instead of being hidden inside a generic "deployment" label
- what minimum reviewability should exist before the organization commits to a runtime posture, including telemetry access, support-access limits, rollback paths, and exit constraints

## Reading Boundaries

- Start with [8.1.1 Runtime Postures, Constraints, And Core Distinctions](08-01-01-runtime-postures-constraints-and-core-distinctions.md) when the team still needs stable language for shared APIs, dedicated endpoints, self-hosted serving, edge runtimes, and the difference between nominal hosting location and real operational control.
- Continue to [8.1.2 Decision Boundaries And Deployment Heuristics](08-01-02-decision-boundaries-and-deployment-heuristics.md) when the issue is choosing the least-complex viable hosting lane, naming escalation triggers, and spotting when a runtime move is really driven by policy, support, or sourcing pressure.
- Move to [8.2 Operating Hosting And Inference](08-02-00-operating-hosting-and-inference.md) when the foundations are clear and the work shifts to rollout shape, failure handling, ongoing support load, and recurring runtime review.
- Revisit [7. Model Ecosystem](../07-model-ecosystem/07-00-00-model-ecosystem.md), [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md), [9. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md), or [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when the real blocker is model-family fit, transfer restrictions, shared policy enforcement, or platform dependence rather than hosting foundations alone.

Back to [8. Model Hosting And Inference](08-00-00-model-hosting-and-inference.md).
