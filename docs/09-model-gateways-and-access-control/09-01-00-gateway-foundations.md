# 9.1 Gateway Foundations

_Page Type: Chapter Index | Maturity: Draft_

This section establishes the control-plane distinctions teams need before they centralize model traffic behind a shared gateway. Use it to separate provider routing, caller identity, policy enforcement, approval boundaries, and audit evidence so gateway adoption does not collapse into a vague "platform standardization" project.

## Section Map

- 9.1.1 [Routing, Identity, And Policy Distinctions](09-01-01-routing-identity-and-policy-distinctions.md)
- 9.1.2 [Decision Boundaries And Adoption Heuristics](09-01-02-decision-boundaries-and-adoption-heuristics.md)

## What This Section Helps Decide

- whether the real problem is unmanaged provider sprawl, missing identity attribution, inconsistent policy enforcement, or a broader sourcing and operating issue
- when a gateway adds useful shared control versus when it only inserts another dependency, latency hop, and export problem
- which responsibilities belong in gateway policy, application logic, runtime hosting, or human approval lanes instead of being blended together
- what minimum reviewability should exist before a gateway becomes the default path for teams, including route ownership, policy versioning, quota logic, and audit evidence

## Reading Boundaries

- Start with [9.1.1 Routing, Identity, And Policy Distinctions](09-01-01-routing-identity-and-policy-distinctions.md) when the team still needs stable language for provider abstraction, tenant identity, policy scope, quota ownership, and the difference between mediation and actual control.
- Continue to [9.1.2 Decision Boundaries And Adoption Heuristics](09-01-02-decision-boundaries-and-adoption-heuristics.md) when the issue is deciding whether gateway adoption is proportionate, what should trigger escalation, and which exceptions should stay outside the shared path.
- Move to [9.2 Operating Gateways And Controls](09-02-00-operating-gateways-and-controls.md) when the foundations are clear and the work shifts to rollout patterns, exception handling, scenario review, and recurring failure modes.
- Revisit [8. Model Hosting And Inference](../08-model-hosting-and-inference/08-00-00-model-hosting-and-inference.md), [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md), [15. Security And Abuse Resistance](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md), or [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when the dominant blocker is runtime placement, telemetry evidence, trust-boundary hardening, or managed-gateway dependence rather than gateway foundations alone.

Back to [9. Model Gateways And Access Control](09-00-00-model-gateways-and-access-control.md).
