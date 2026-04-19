# 15.1.2 Decision Boundaries And Hardening Heuristics

_Page Type: Decision Guide | Maturity: Draft_

Use this page when the threat surface is clear enough that the team needs a default hardening lane, not another generic promise to "add guardrails." The goal is to match the control posture to the authority boundary so that harmless-looking assistants are not secured like transaction systems and action-capable agents are not released with only prompt filtering and hope.

## Decision Lanes

| Lane | Use it when the main question is... | Default hardening posture |
| --- | --- | --- |
| Content-only lane | whether the system can only generate or summarize content with no tool execution or durable state | isolate untrusted input, narrow logging exposure, test prompt abuse, and keep outputs non-authoritative by default |
| Retrieval-boundary lane | whether external or internal documents can reshape answers, policy interpretation, or citations | treat retrieved content as untrusted evidence, keep instruction hierarchy explicit, and prove provenance plus citation review before rollout expands |
| Action-capable lane | whether the model or workflow can trigger tickets, messages, records, transactions, or configuration changes | deny by default, gate actions with explicit preconditions and approvals, and require rollback plus disablement before release |
| Memory-bearing lane | whether interaction data, user state, or workflow context persists across sessions or actors | minimize stored fields, type memory writes, set retention and deletion rules, and review access scope before persistence broadens |
| Shared-control lane | whether the service depends on gateways, provider controls, external plugins, or managed security features that shape trust boundaries | export evidence, document residual vendor-only controls, and verify incident reconstruction still works if the provider path changes |

## Practical Heuristics

- Match controls to authority, not to interface style. A chat UI that can create tickets or modify records belongs in the action-capable lane even if it "looks like" a simple assistant.
- Treat retrieval and memory as separate security problems. Retrieved text is untrusted input; persistent memory is durable state with retention, deletion, and privilege consequences.
- Require two stories for every release: how abuse is prevented and how abuse is contained after prevention fails.
- Escalate fast when the system crosses from read-only to write-capable behavior. The approval model, rollback path, and audit record must tighten before autonomy expands.
- Do not rely on provider safety features as the only boundary. Local policy, identity, logging, and emergency disablement remain the organization's responsibility.
- Favor reversible controls first. Narrower tools, smaller memory scope, tighter routes, and explicit human approval usually create more security value than larger prompt rule sets alone.
- Treat exportability as part of hardening when a gateway, model host, or managed security layer mediates the path. Incident review fails if only the vendor can explain what happened.

## Escalate When

- the team cannot say whether the system is content-only, retrieval-influenced, action-capable, memory-bearing, or dependent on vendor-only controls
- a proposed tool or workflow change would create irreversible or high-authority side effects without tested rollback
- stored memory, logs, or provider telemetry may hold sensitive data but retention, deletion, or regional handling is still vague
- broad service credentials, shared API keys, or implicit impersonation remain in place because prompt controls are expected to compensate
- a provider or plugin becomes a trust-critical control point but the team cannot export evidence, reproduce policy outcomes, or disable the dependency quickly
- abuse testing focuses on prompt wording while weak authorization, route policy, dependency provenance, or approval logic remains untested

## Hardening Anti-Patterns

- treating "prompt injection defense" as the whole security plan when the real risk is tool authority or durable state
- approving broad agent permissions because the model appears well-behaved in demos
- logging everything for investigations and accidentally creating a larger privacy or secret-exposure problem
- storing memory for convenience first and defining deletion, correction, and role boundaries later
- trusting managed-provider attestations without checking whether local teams can still reconstruct incidents and prove control ownership
- running security review only once, then expanding tools, routes, or memory scope as if those were harmless configuration tweaks

## Chapter Handoffs

- [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md) when the dominant question is retention, cross-border handling, deletion, or sensitive-data minimization rather than abuse containment alone.
- [9. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md) when routing policy, identity, tenant isolation, or centralized controls are doing more security work than the application itself.
- [10. Agentic Systems And Orchestration](../10-agentic-systems-and-orchestration/10-00-00-agentic-systems-and-orchestration.md) when the unresolved issue is autonomy shape, tool choreography, or background execution rather than hardening logic alone.
- [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md) when the missing control is reconstructable runtime evidence, telemetry boundaries, or incident-review visibility.
- [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) when the real gap is approval rights, intervention authority, escalation ownership, or operator review cadence.
- [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when managed control planes, provider dependence, or exit posture matter as much as the technical hardening design.

## Practical Reading Rule

Choose the lightest lane that still matches the highest authority boundary, then tighten the evidence pack as soon as the system gains actions, persistence, or vendor-dependent control points. If the chosen lane no longer explains how the service is prevented, contained, and reconstructed, the hardening model is already behind the architecture.

Back to [15.1 Security Foundations](15-01-00-security-foundations.md).
