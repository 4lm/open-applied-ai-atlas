# 8.1.1 Runtime Postures, Constraints, And Core Distinctions

_Page Type: Concept Explainer | Maturity: Review-Ready_

Use this page to separate runtime postures before hosting gets reduced to "API versus self-hosted." Hosting review becomes sloppy when shared provider APIs, dedicated managed endpoints, cloud-estate runtimes, self-hosted serving, edge inference, and sovereign private estates are treated as interchangeable just because they all answer the same model call.

## Runtime-Posture Map

| Runtime posture | Where real control sits | Strongest fit | What fails when it is misclassified |
| --- | --- | --- | --- |
| Shared provider API | provider owns the serving estate, upgrade cadence, and most runtime evidence | early experimentation, low-volume assistants, and workloads where speed matters more than hosting control | teams assume portability or sovereignty because the application code is theirs while the runtime, incident evidence, and deprecation timing remain provider-defined |
| Dedicated managed endpoint | provider still runs the serving layer, but the customer gets stronger isolation and deployment specificity | production rollout that needs more predictable scaling, model choice, or network controls without full platform ownership | "dedicated" gets mistaken for self-operated, so teams under-budget for export limits, support access, or provider-side change windows |
| Cloud-estate native hosting | runtime is deeply tied to one cloud's IAM, networking, logging, and service contracts | organizations already standardized on one cloud where estate integration matters more than exit flexibility | cloud alignment is confused with neutrality, and the real lock-in shifts from model access to surrounding platform services |
| Self-hosted open-weight serving | the organization owns serving software, deployment automation, capacity planning, and most runtime evidence | privacy-sensitive, exit-sensitive, or performance-tuned workloads with genuine platform capability | teams celebrate model portability while ignoring on-call burden, GPU operations, runtime patching, and rollback responsibility |
| Edge or local inference | runtime is pushed close to the user, device, or workstation boundary | offline, low-latency, site-local, or data-minimizing deployments | local placement is treated as universally safer even when model quality, patch distribution, or fleet governance becomes the real bottleneck |
| Sovereign private runtime | organization or sovereign operator controls network, support paths, and exportable evidence under tighter jurisdictional rules | regulated, defense-adjacent, or high-control environments where external dependence is tightly bounded | private placement gets mistaken for full sovereignty even when remote support, proprietary accelerators, or vendor-managed updates remain decisive |

## Core Distinctions

| Distinction | Why it changes the hosting decision |
| --- | --- |
| Tenancy isolation vs. operational control | A dedicated tenant or VPC boundary can improve isolation without giving the customer meaningful control over serving code, upgrades, or incident evidence. |
| Hosting location vs. support-access boundary | A workload can run in a preferred region while privileged provider staff, opaque support tooling, or outbound telemetry still shape the real risk posture. |
| Model portability vs. runtime portability | Open weights help, but migration still hurts if prompts, quantization formats, accelerators, gateways, and observability assumptions are tied to one runtime estate. |
| Performance optimization vs. hardware dependence | The fastest serving path often relies on specific GPU families, drivers, kernels, or packaged runtimes that become hard to unwind later. |
| Elastic convenience vs. predictable capacity | Managed elasticity reduces early operations work, but high-consequence workloads still need explicit capacity assumptions, fallback lanes, and queueing behavior. |
| Private deployment vs. sovereign evidence | Private hosting claims are weak if logs, admin access, incident response, or model updates still depend on external operators and non-exportable tooling. |
| Self-hosted runtime vs. self-owned operating model | Running the containers yourself is not the same as owning patch cadence, security hardening, telemetry, support rotations, and lifecycle revalidation. |

## What These Distinctions Change In Practice

- Start with the least-complex runtime lane that satisfies the real control requirement. Many teams do not need self-hosting; many others do not realize that region pinning or "private" managed hosting still leaves critical review questions unanswered.
- Make support-access, telemetry export, and incident reconstruction part of the hosting choice up front. A runtime posture is weak if only the provider can explain failures, prove deletions, or reconstruct a serious outage.
- Separate model choice from runtime choice. A good model family does not make a managed platform acceptable, and a self-hosted runtime does not fix poor model-method fit from [7. Model Ecosystem](../07-model-ecosystem/07-00-00-model-ecosystem.md).
- Review hardware assumptions early when latency or cost claims depend on one accelerator family, one kernel stack, or one packaged optimization layer. Performance wins often become sourcing commitments.
- Treat gateways, observability, security, and sourcing as adjacent constraints rather than afterthoughts. Hosting decisions are rarely stable if [9](../09-model-gateways-and-access-control/09-00-00-model-gateways-and-access-control.md), [14](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md), [15](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md), or [18](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) would force a different control posture.
- Ask for a real exit sketch before rollout expands: model packaging, configuration, telemetry schemas, support procedures, and capacity assumptions should survive a provider, hardware, or region change.

## Reviewer Checks

- Which runtime decisions can the organization actually make itself: model packaging, autoscaling, patch timing, region choice, logging schema, support access, or rollback?
- If the current provider or platform disappeared tomorrow, which parts of the serving stack would move cleanly and which would need redesign?
- What evidence would prove the claimed posture during an audit or incident: exported traces, access records, model-version history, capacity tests, deletion proofs, or support logs?
- Where does the proposal rely on a hardware or optimization path that may become the real source of cost, delay, or lock-in?
- Which responsibilities are still unowned: GPU fleet operations, queueing and fallback, model refresh, runtime patching, security hardening, or operator support?

## Practical Reading Rule

Classify the runtime posture first, then use [8.1.2 Decision Boundaries And Deployment Heuristics](08-01-02-decision-boundaries-and-deployment-heuristics.md) to choose the default deployment lane. If the team still cannot say who owns runtime changes, what support access exists, which evidence is exportable, and where hardware dependence lives, the hosting design is not ready for rollout review yet.

Back to [8.1 Hosting Foundations](08-01-00-hosting-foundations.md).
