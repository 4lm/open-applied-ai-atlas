# 8.1.2 Decision Boundaries And Deployment Heuristics

_Page Type: Decision Guide | Maturity: Draft_

Use this page when the runtime posture is clear enough and the remaining question is which deployment lane fits by default. The goal is to match hosting control, evidence, and operating burden to the actual workload so teams do not self-host for prestige, mistake dedicated managed endpoints for true sovereignty, or push regulated and latency-sensitive services onto runtime estates that cannot be defended later.

## Decision Lanes

| Lane | Use it when the main question is... | Default deployment posture |
| --- | --- | --- |
| Shared-managed lane | whether a bounded workload needs fast access to a capable model with minimal platform work and limited runtime specificity | use the provider API, keep release and telemetry identifiers stable, and block production claims that assume deeper control than the provider actually offers |
| Dedicated-managed lane | whether production rollout needs stronger isolation, predictable scale, or network controls without taking on full serving operations | require explicit support-access limits, exported evidence, versioning visibility, and fallback behavior before calling the posture "enterprise-ready" |
| Cloud-estate lane | whether the organization wants hosting embedded in an existing cloud IAM, networking, and platform estate more than it wants rapid exit flexibility | treat surrounding cloud services as part of the dependency, document cloud-specific control assumptions, and prove how logging, keys, and network boundaries will work in practice |
| Self-hosted control lane | whether privacy, model choice, cost shape, or exit posture justifies owning serving software, GPU capacity, patching, and runtime evidence directly | narrow the scope to workloads that genuinely need this control, name the operating owner, and require capacity, rollback, and security plans before rollout widens |
| Edge-or-local lane | whether low latency, intermittent connectivity, site-local processing, or data minimization requires inference close to a device or workplace boundary | keep model size, fleet update mechanics, offline failure handling, and local evidence capture explicit before treating device placement as automatically safer |
| Sovereign-runtime lane | whether legal, contractual, or organizational control requirements demand a tightly bounded support path, jurisdiction, and exportable incident evidence | verify who can administer the runtime, who can update it, and how audit and incident records leave the estate before sovereignty language is accepted |

## Practical Heuristics

- Choose the lightest lane that still satisfies the hardest control requirement. If the real issue is fast experimentation, a shared-managed path is usually better than premature self-hosting; if the issue is support access, evidence export, or jurisdictional control, managed convenience may already be too weak.
- Separate isolation from ownership. Dedicated endpoints, private networking, or single-tenant claims can improve posture, but they do not by themselves transfer upgrade timing, incident reconstruction, or patch responsibility to the customer.
- Make support access a first-class hosting criterion. The hosting lane is underspecified until the team can explain who can inspect prompts, weights, logs, and runtime state during support or incident response.
- Treat hardware dependence as a sourcing decision, not a mere performance detail. Quantization choices, accelerator families, optimized kernels, and inference servers can become the real lock-in even when the model itself looks portable.
- Escalate quickly once the runtime carries regulated data, offline commitments, or user-visible latency promises. Those constraints usually change queueing, fallback, telemetry, and staffing requirements more than teams expect.
- Require an exit sketch before the lane is accepted: model packaging, deployment automation, observability schema, secrets handling, and rollback behavior should all survive a provider, cloud, or hardware change.
- Do not let hosting absorb unresolved model-fit problems. If the workload still depends on the wrong model class, missing retrieval, or unproven adaptation, changing runtime posture first usually creates expensive noise rather than a real fix.

## Escalate When

- the team describes the lane with vague labels such as "private," "sovereign," or "enterprise" but cannot name who owns upgrades, support access, logs, and rollback
- latency, throughput, or cost targets depend on a specific GPU family, driver stack, or optimized runtime that has not been reviewed as a sourcing dependency
- provider support, remote administration, or opaque telemetry would still be necessary even though the proposal is being presented as a control-first or residency-first posture
- self-hosting is justified mainly by distrust of one vendor, yet staffing, on-call ownership, security hardening, and capacity management remain undefined
- edge or local deployment is proposed without a credible plan for model updates, fleet drift, abuse handling, and offline audit evidence
- the chosen runtime lane cannot explain how incidents, deletions, policy reviews, or emergency disablement would work during a provider outage, migration, or procurement dispute

## Deployment Anti-Patterns

- calling a managed endpoint "self-hosted enough" because it sits in a preferred region or VPC while critical runtime control still belongs to the provider
- moving to self-hosting to escape lock-in while rebuilding the same lock-in around one GPU vendor, one optimization stack, or one internal platform team
- treating cloud-estate alignment as neutral architecture even though IAM, observability, secrets, and network controls now depend on one cloud's service model
- choosing edge deployment for privacy theater while local storage, update discipline, and forensic visibility remain weaker than the centralized alternative
- using sovereignty language for estates that still rely on remote support channels, vendor-mediated upgrades, or non-exportable operational evidence
- widening production rollout before the team has proven capacity assumptions, fallback behavior, and operator ownership for the selected lane

## Chapter Handoffs

- [6. Data Sovereignty And Privacy](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md) when residency, deletion, support-access, or lawful-access posture is driving the hosting decision more than runtime mechanics.
- [7. Model Ecosystem](../07-model-ecosystem/07-00-00-model-ecosystem.md) when the unresolved problem is model-family fit, openness requirement, lifecycle burden, or whether the workload needs a different model posture before it needs a different runtime.
- [9. Model Gateways And Access Control](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md) when identity propagation, route policy, quota ownership, or shared control planes are shaping the acceptable hosting lane.
- [12. Training Fine-Tuning And Adaptation](../12-training-fine-tuning-and-adaptation/12-00-00-training-fine-tuning-and-adaptation.md) when quantization, tuning, packaging, or adaptation strategy is what actually forces the runtime change.
- [14. Observability Logging And Monitoring](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md) when exportable telemetry, trace reconstruction, or support visibility is the weak link in the proposed lane.
- [15. Security And Abuse Resistance](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md) when trust boundaries, privileged runtime access, secret handling, or incident containment dominate the review.
- [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when managed-platform dependence, internal platform investment, or exit posture matters as much as the technical runtime design.

## Practical Reading Rule

Pick the lowest deployment lane that still satisfies control, evidence, and performance needs for the service that actually exists, then tighten immediately when data sensitivity, authority, or hardware dependence increases. If the chosen lane cannot explain who operates the runtime, what evidence is exportable, how support access is bounded, and how the system exits its current estate, the hosting decision is still too weak.

Back to [8.1 Hosting Foundations](08-01-00-hosting-foundations.md).
