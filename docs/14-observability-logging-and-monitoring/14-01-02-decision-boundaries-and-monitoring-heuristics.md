# 14.1.2 Decision Boundaries And Monitoring Heuristics

_Page Type: Decision Guide | Maturity: Draft_

Use this page when the signal families are already clear and the remaining question is how much observability the service actually needs by default. The goal is to match instrumentation depth to the incident, privacy, and portability burden so teams do not ship blind services with only uptime graphs or create uncontrolled stores of prompts, traces, and customer data in the name of "better visibility."

## Decision Lanes

| Lane | Use it when the main question is... | Default monitoring posture |
| --- | --- | --- |
| Health-baseline lane | whether a bounded service needs enough visibility to detect outages, latency regressions, rate-limit trouble, and obvious failures | capture request IDs, release version, route or model identifier, latency, error codes, and basic cost or capacity signals before adding richer traces |
| Reconstruction lane | whether support, QA, or incident review must explain why one request failed, drifted, or took the wrong branch | link request, retrieval, policy, tool, and user-outcome events under one trace so a reviewer can reconstruct the path without manual stitching |
| Sensitive-support lane | whether the service handles internal, customer, or regulated content that makes raw payload capture risky | keep structured and masked telemetry always on, put rich content behind break-glass controls, and define redaction, retention, and deletion behavior before launch |
| Multi-step autonomy lane | whether the system routes across models, uses tools, waits on approvals, or executes agentic steps that can fail outside the model call | trace plan creation, tool invocation, approval events, retries, rollback markers, and final state under shared identifiers rather than logging only the model exchange |
| Portability-critical lane | whether observability depends on a managed platform, gateway, or vendor-specific analysis path that could become a procurement, sovereignty, or outage issue | use stable schemas, export tests, and documented vendor-only logic so incident reconstruction survives platform changes or regional restrictions |

## Practical Heuristics

- Choose the lightest lane that still answers the hardest review question. If leadership needs only uptime and capacity signals, the health-baseline lane may be enough; if support must explain a bad answer or blocked action, move immediately to reconstruction or beyond.
- Instrument the whole decision path, not just the model call. Retrieval, route selection, policy checks, tool use, approval gates, and human overrides usually explain incidents faster than token logs alone.
- Separate routine support visibility from exceptional forensic access. Most operating work should succeed with masked traces and structured fields; raw prompts, retrieved documents, or tool payloads should require explicit access controls and auditability.
- Make release evidence and runtime evidence meet in the same identifiers. Prompt version, model route, policy version, feature flag, and release ID should map directly into traces so rollouts and incidents do not rely on manual correlation.
- Treat exportability as an observability requirement, not a later procurement convenience. A polished vendor console is not enough if the underlying evidence cannot be extracted, retained, and reviewed elsewhere.
- Escalate the lane as soon as the service gains more authority, richer data classes, or deeper platform dependence. Additional tools, longer-lived memory, broader retrieval, or automated actions raise the monitoring burden even if the user interface stays the same.

## Escalate When

- the team can show dashboards but cannot reconstruct a single user-visible failure across retrieval, policy, tool, and handoff steps
- support or incident review still depends on unrestricted access to raw prompts, documents, or tool payloads because structured telemetry is too weak
- a managed platform or gateway becomes the only place where traces, policy outcomes, or export events can be understood
- new tools, approvals, memory, or background jobs are being added, but the trace schema still assumes one request and one model response
- telemetry may contain sensitive or regulated content while redaction, retention, deletion, or storage-region rules remain vague
- release reviewers cannot connect a production incident to the exact prompt, policy, route, or model version that was active at the time

## Monitoring Anti-Patterns

- calling latency, error rate, and token spend "observability" when nobody can explain why a specific answer, action, or policy outcome occurred
- tracing only the model interaction while retrieval, gateway, approval, and tool decisions disappear into generic application logs
- logging raw prompts, documents, or tool outputs by default because schema design looked slower than payload dumping
- assuming a managed observability product has solved portability, retention, and sovereignty review automatically
- treating masked telemetry as optional and broad break-glass access as the normal support path
- expanding system authority or autonomy without widening the trace model, alert catalog, and incident packet that must accompany it

## Chapter Handoffs

- [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md) when the unresolved issue is retention, redaction, regional storage, deletion, or sensitive-data handling rather than monitoring depth alone.
- [9. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md) when routing, identity, tenant policy, or centralized control points are shaping what should be observed and exported.
- [10. Agentic Systems And Orchestration](../10-agentic-systems-and-orchestration/10-00-00-agentic-systems-and-orchestration.md) when the real decision is workflow shape, background execution, or tool choreography rather than instrumentation policy.
- [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md) when the dominant gap is release proof, regression evidence, or test coverage rather than runtime reconstruction.
- [15. Security And Abuse Resistance](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md) when the missing signal is abuse containment, attack investigation, or trust-boundary review.
- [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) when escalation ownership, on-call authority, manual intervention, or approval review is still undefined.
- [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when vendor dependence, exit posture, or managed-platform lock-in matters as much as the technical telemetry design.

## Practical Reading Rule

Pick the lowest observability lane that still supports reconstruction, privacy control, and exportability for the service that actually exists, not the safer system described in demos. If the chosen lane cannot explain failures across the full request path, protect sensitive data during support, and survive platform dependence, the monitoring design is already underspecified.

Back to [14.1 Observability Foundations](14-01-00-observability-foundations.md).
