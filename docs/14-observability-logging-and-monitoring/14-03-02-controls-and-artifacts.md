# 14.3.2 Controls And Artifacts

_Page Type: Operational Artifact | Maturity: Review-Ready_

Use this page when a team needs to prove that observability is operationally usable, not just technically present. A dashboard is not enough if incident responders cannot reconstruct what happened, reviewers cannot see what data was retained, or governance teams cannot tell which telemetry left the platform boundary.

## Minimum Observability Control Pack

| Control or artifact | What it should make explicit | Typical owner | Review trigger |
| --- | --- | --- | --- |
| Telemetry schema and field dictionary | Required event fields, field meanings, identifiers, and optional extensions | Platform or observability owner | New service, major feature, or schema change |
| Sensitive-data redaction rules | Which prompt, retrieval, tool, and user fields are masked, hashed, dropped, or stored separately | Privacy or security owner | New data source, provider, or logging sink |
| Retention and storage-boundary record | Retention periods, storage regions, export paths, and deletion workflow | Platform, privacy, or compliance owner | New region, vendor, or policy update |
| Alert catalog and escalation matrix | Severity thresholds, on-call targets, business-hour vs out-of-hours flow, and blocking conditions | Operations or service owner | New failure mode, SLO, or release tier |
| Release-to-trace mapping | Which release identifier, prompt version, model version, policy version, and retrieval version can be tied to a trace | Engineering or release owner | Every production release |
| Incident reconstruction packet | Trace links, timeline, impacted cohorts, decision log, and mitigation record | Incident commander or service owner | Sev incident, rollback, or audit replay |
| Export and portability register | Which telemetry can be exported in open formats and which analysis steps depend on a vendor-specific platform | Platform or architecture owner | Procurement review or tooling change |

## Signal Coverage Checklist

The control pack should make the following signal families reviewable before launch:

| Signal family | Minimum visible fields | Why it matters |
| --- | --- | --- |
| Request and user context | Tenant or segment, workflow, channel, feature flag, and request ID | Separates product issues from broad platform failures |
| Model and runtime behavior | Model ID, provider, latency, token or compute use, retries, and timeout outcome | Distinguishes provider, routing, and local runtime regressions |
| Retrieval and tool activity | Index or source used, cache status, tool invoked, permission path, and failure code | Makes agent and retrieval errors diagnosable instead of appearing as generic model failure |
| Safety and policy events | Guardrail decisions, moderation outcomes, blocked actions, and approval requirements | Shows whether protections triggered, failed, or were bypassed |
| User-visible outcome | Final status, fallback path, human handoff, and complaint or correction signal | Connects technical traces to real service impact |
| Cost and capacity | Unit cost, queue depth, rate-limit state, and degraded-mode activation | Prevents "healthy" traces from hiding unsustainable runtime posture |

## Minimal Review Packet

- telemetry schema with named owner and last revision date
- retention, redaction, and access-control decisions for each sink that stores rich traces or logs
- alert catalog covering customer-visible failure, silent degradation, and policy-trigger events
- evidence that release identifiers map to traces and dashboards without manual reconstruction
- one completed incident-reconstruction example or dry run using realistic trace data
- export note showing which telemetry remains portable if the team leaves the current vendor stack

## Failure Signs

- Logs exist, but the team cannot answer which identifiers link a user incident to a model, retrieval, or policy change.
- Prompt and trace capture are enabled without a clear rule for masking sensitive content or honoring deletion requests.
- Alerting only watches latency or uptime and misses retrieval failure, guardrail failure, or silently wrong outcomes.
- A managed observability product is doing critical interpretation work that cannot be exported or reproduced elsewhere.
- Incident review depends on screenshots from dashboards rather than stable trace links, release IDs, and preserved timelines.

## Approval Prompt

If the team cannot show which artifact would let a reviewer reconstruct a failed decision, verify retention boundaries, and prove whether the failure came from the model, retrieval layer, toolchain, or policy path, the observability design is not yet ready.

Back to [14.3 Reference Points](14-03-00-reference-points.md).
