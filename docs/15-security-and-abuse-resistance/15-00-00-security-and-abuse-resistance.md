# 15. Security And Abuse Resistance

_Page Type: Chapter Index | Maturity: Draft_

This chapter treats security and abuse resistance as a control-boundary problem across prompts, retrieval, tool use, identity, secrets, model dependencies, and provider egress. Use it to decide which crossings need isolation, which actions need mediation or approval, and which failures should block release before teams mistake "guardrails" for a complete security posture.

The hard part is not only hostile input. It is deciding how much authority the system has, what evidence must exist to reconstruct misuse, how containment works when a provider or integration misbehaves, and where privacy, sovereignty, portability, and lock-in change the acceptable control shape.

## Chapter Index

- 15.1 [Security Foundations](15-01-00-security-foundations.md)
- 15.1.1 [Threat Surfaces, Trust Boundaries, And Core Distinctions](15-01-01-threat-surfaces-trust-boundaries-and-core-distinctions.md)
- 15.1.2 [Decision Boundaries And Hardening Heuristics](15-01-02-decision-boundaries-and-hardening-heuristics.md)
- 15.2 [Operating Security And Abuse Resistance](15-02-00-operating-security-and-abuse-resistance.md)
- 15.2.1 [Worked Security Scenarios](15-02-01-worked-security-scenarios.md)
- 15.2.2 [Patterns And Anti-Patterns](15-02-02-patterns-and-anti-patterns.md)
- 15.3 [Reference Points](15-03-00-reference-points.md)
- 15.3.1 [Tools And Platforms](15-03-01-tools-and-platforms.md)
- 15.3.2 [Standards And Bodies](15-03-02-standards-and-bodies.md)
- 15.3.3 [Controls And Artifacts](15-03-03-controls-and-artifacts.md)

## How To Read This Chapter

- Start with [15.1 Security Foundations](15-01-00-security-foundations.md) when the team still needs stable boundaries between threat surfaces, trust boundaries, privilege levels, and reviewable abuse evidence.
- Move to [15.2 Operating Security And Abuse Resistance](15-02-00-operating-security-and-abuse-resistance.md) when the architecture is already framed and the work shifts to delivery review, containment readiness, scenario testing, and recurring operating patterns.
- Use [15.3 Reference Points](15-03-00-reference-points.md) only after the control problem is clear enough that tools, standards, and artifact templates will sharpen the decision instead of replacing it.

## What This Chapter Helps Decide

- which user, model, retrieval, tool, gateway, and provider crossings need isolation, mediation, approval, or stronger evidence before rollout
- what should count as release-blocking security proof for action-capable systems, external integrations, retrieved content, and high-impact workflows
- how abuse testing, provenance, secrets handling, runtime evidence, and containment drills should fit into one review packet instead of living in disconnected teams
- when the dominant question has shifted to data handling, telemetry design, human escalation, or sourcing posture rather than security alone

## Reading Boundaries

- Revisit [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md) when the binding issue is residency, cross-border transfer, retention, or data-handling limits rather than attack containment.
- Revisit [9. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md) when identity, routing, policy enforcement, and provider mediation are the real control plane.
- Revisit [10. Agentic Systems And Orchestration](../10-agentic-systems-and-orchestration/10-00-00-agentic-systems-and-orchestration.md) when autonomy, tool choreography, and approval design are creating the main abuse surface.
- Revisit [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md) when incident reconstruction, signal coverage, or evidentiary logging is the unresolved problem.
- Revisit [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) when the missing control is named escalation ownership, intervention rights, or approval authority.
- Revisit [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when managed-provider dependence, self-hosting posture, export limits, or exit planning are driving the acceptable security shape.

## Adjacent Chapters

- Previous: [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md)
- Next: [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md)
- Repository guidance: [Contributing](../../CONTRIBUTING.md), [Editorial Rules](../../EDITORIAL_RULES.md)
