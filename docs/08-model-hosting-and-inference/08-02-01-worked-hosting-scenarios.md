# 8.2.1 Worked Hosting Scenarios

_Page Type: Worked Example | Maturity: Draft_

These scenarios turn runtime posture into concrete operating review. Each one shows the hosting shape, evidence packet, and re-review trigger that should already exist before rollout widens or a team claims that its runtime is stable, private, or sovereign.

## Public API Experimentation

| Field | Decision |
| --- | --- |
| System | Early-stage internal assistant or prototype workflow with low-consequence usage and no hard residency or offline constraint |
| Dominant operating failure | Fast experimentation silently becomes the production default even though fallback behavior, provider support access, and exportable telemetry were never designed |
| Hosting shape | Shared-managed inference stays acceptable while the team keeps the runtime boundary explicit, limits sensitive data classes, and records the provider, model version, latency expectation, and fallback path per release |
| Required evidence | Allowed-use boundary, provider-region note, example trace or request log, disablement plan, and checkpoint for revisiting hosting before broader rollout |
| Release question | If the provider API degrades, changes terms, or exposes weaker support and logging boundaries than expected, can the team pause or migrate without discovering its operating assumptions too late? |
| Re-review trigger | Reopen chapters `06`, `09`, `14`, and `18` when sensitive data classes expand, the service becomes business-critical, or the team starts relying on vendor-only observability or gateway features |

## Dedicated Managed Service Rollout

| Field | Decision |
| --- | --- |
| System | Customer-facing or internal production workload that needs better isolation, predictable throughput, or private networking without taking on full serving operations |
| Dominant operating failure | The team treats dedicated tenancy or private networking as proof of full control even though upgrades, support channels, and telemetry still depend on the provider estate |
| Hosting shape | Dedicated managed deployment is acceptable only when support access, runtime versioning, scaling limits, and evidence export are contractually and operationally visible rather than implied |
| Required evidence | Support-access matrix, version change notice path, failover test, throughput budget, telemetry export sample, and rollback packet for provider or model changes |
| Release question | Can the team explain exactly which runtime decisions it owns versus which ones still belong to the provider before it promises regulated, high-availability, or private-service behavior? |
| Re-review trigger | Reopen chapters `09`, `14`, `15`, and `18` when provider-managed admin paths widen, new regulated workloads land on the estate, or gateway policy and observability become dependent on the managed platform |

## Open-Weight Self-Hosting

| Field | Decision |
| --- | --- |
| System | Privacy-sensitive or cost-shaped workload that justifies operating an open-weight model directly on organizational infrastructure |
| Dominant operating failure | Self-hosting is approved as a control win without proving capacity ownership, patch discipline, GPU dependence, or incident reconstruction under real load |
| Hosting shape | The runtime is owned end to end: serving stack, hardware planning, secrets handling, patch cadence, model packaging, and rollback are all assigned to named operators with clear release gates |
| Required evidence | Capacity model, on-call ownership, image and model provenance record, runtime hardening checklist, rollback drill, and exportable telemetry for latency, failures, and support actions |
| Release question | Does the organization truly want the operational burden that comes with private runtime control, or is it using self-hosting language to avoid a separate sourcing and risk discussion? |
| Re-review trigger | Reopen chapters `07`, `12`, `14`, `15`, and `18` when the model family changes, quantization or tuning becomes necessary, new accelerator dependence appears, or the runtime estate expands across regions or business units |

## Air-Gapped Deployment Review

| Field | Decision |
| --- | --- |
| System | Sensitive environment that requires tightly bounded connectivity, local processing, or disconnected operations for legal, security, or operational reasons |
| Dominant operating failure | Teams approve "air-gapped" as a slogan even though update channels, model refresh cadence, telemetry transfer, or support workflows still assume external connectivity |
| Hosting shape | Offline or heavily bounded runtime is accepted only after the team proves how models arrive, how patches are validated, how incidents are reconstructed, and how degraded functionality is handled when external services disappear |
| Required evidence | Media-transfer procedure, offline update workflow, local telemetry and retention policy, support escalation path, degraded-mode runbook, and completed restore test in the disconnected environment |
| Release question | If the estate is isolated during both normal operations and an incident, can the team still update safely, reconstruct failures, and govern privileged access without hidden external dependencies? |
| Re-review trigger | Reopen chapters `06`, `14`, `15`, `19`, and `20` when new data classes, new remote administration channels, or standards obligations change what the offline posture must prove |

## Cross-Scenario Review Signals

- strong hosting review makes runtime ownership explicit: who operates upgrades, who can access support channels, what evidence is exportable, and how rollback works under pressure
- the real boundary is operational, not geographic: region pinning, dedicated tenancy, or self-hosting claims are weak if telemetry, admin access, or hardware dependence remain unexamined
- the most important trigger for re-review is scope expansion: broader data sensitivity, new model packaging, heavier traffic, stricter latency promises, or deeper platform dependence should reopen adjacent chapter decisions instead of being treated as runtime tuning

Back to [8.2 Operating Hosting And Inference](08-02-00-operating-hosting-and-inference.md).
