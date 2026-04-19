# 15.1 Security Foundations

_Page Type: Chapter Index | Maturity: Review-Ready_

This section establishes the boundary model teams need before they argue about scanners, red-team tools, or provider security features. Use it to separate threat surfaces, trust boundaries, privilege lanes, and containment expectations so the later operating and reference pages stay tied to actual abuse paths instead of generic "AI security" language.

## Section Map

- 15.1.1 [Threat Surfaces, Trust Boundaries, And Core Distinctions](15-01-01-threat-surfaces-trust-boundaries-and-core-distinctions.md)
- 15.1.2 [Decision Boundaries And Hardening Heuristics](15-01-02-decision-boundaries-and-hardening-heuristics.md)

## What This Section Helps Decide

- which crossings between user input, model calls, retrieval, tools, secrets, external services, and human approvals need separate controls rather than one shared guardrail story
- whether the dominant security burden is prompt abuse, privilege escalation, data exfiltration, dependency compromise, unsafe action execution, or missing incident evidence
- what minimum proof should exist before rollout, including abuse tests, trust-boundary ownership, containment plans, and reconstruction paths
- when the binding question has shifted into gateway policy, observability design, oversight ownership, privacy constraints, or sourcing dependence rather than security foundations alone

## Reading Boundaries

- Start with [15.1.1 Threat Surfaces, Trust Boundaries, And Core Distinctions](15-01-01-threat-surfaces-trust-boundaries-and-core-distinctions.md) when the team still needs a stable way to separate model abuse, tool abuse, dependency risk, identity weakness, and containment obligations.
- Continue to [15.1.2 Decision Boundaries And Hardening Heuristics](15-01-02-decision-boundaries-and-hardening-heuristics.md) when the issue is choosing a default hardening lane, naming escalation triggers, and deciding which failures should block release.
- Move to [15.2 Operating Security And Abuse Resistance](15-02-00-operating-security-and-abuse-resistance.md) when the control frame is clear and the work becomes scenario coverage, recurring review, drills, and operational ownership.
- Revisit [9. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md), [10. Agentic Systems And Orchestration](../10-agentic-systems-and-orchestration/10-00-00-agentic-systems-and-orchestration.md), [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md), [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md), or [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when the real blocker is policy enforcement, autonomy design, runtime evidence, named intervention rights, or provider dependence rather than boundary framing.

Back to [15. Security And Abuse Resistance](15-00-00-security-and-abuse-resistance.md).
