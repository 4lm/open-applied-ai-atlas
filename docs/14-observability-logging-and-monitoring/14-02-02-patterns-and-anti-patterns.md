# 14.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use this page during rollout review, incident readiness checks, and observability redesign work to recognize healthy monitoring operating shapes before teams mistake dashboard presence for reconstructable runtime evidence.

## Reusable Observability Patterns

| Pattern | What good looks like | Fit signal | Review warning |
| --- | --- | --- | --- |
| Trace-first reconstruction tied to release identity | Every meaningful run can be reconstructed through stable request, workflow, release, model, policy, and retrieval identifiers without relying on ad hoc screenshots or memory | incidents or regressions must be traced across model, gateway, retrieval, tool, and approval layers | responders can see dashboard spikes, but cannot connect a failed user outcome to the exact release, route, or decision path |
| Tiered telemetry with governed raw-access paths | Routine monitoring uses masked or summarized events, while raw prompts, documents, or tool payloads sit behind explicit break-glass rules, logging, and retention controls | support, privacy, and security teams all need usable telemetry, but unrestricted payload access would create a second uncontrolled data store | the team claims observability requires full content capture for everyone because the structured traces are too thin |
| Alerting anchored to user-visible and control-visible failure | Alerts cover silent wrong answers, retrieval failure, policy bypass, tool misuse, approval stalls, and degraded fallbacks instead of only latency or uptime | the system can fail in ways that remain "up" from infrastructure’s point of view | the alert catalog is detailed for infrastructure events, but says little about user harm, blocked decisions, or control failure |
| Exportable evidence path with vendor-boundary awareness | The service can export the fields needed for investigation, audit replay, and migration into open or documented formats, with known gaps and owner review for any vendor-only logic | the team relies on a managed telemetry product, gateway analytics layer, or proprietary trace UI | observability works only inside one vendor console and nobody can show which fields, joins, or timelines survive export |
| Re-review hooks from live signals into adjacent control chapters | Monitoring outputs explicitly name which incidents or changes reopen evaluation, security, oversight, privacy, or sourcing review | rollout scope, action authority, retrieval depth, or platform dependence will change over time | incidents are closed locally as "ops noise" even when they reveal release-proof, abuse, or governance gaps |

## Observability Anti-Patterns

| Anti-pattern | Why it fails | Early signal | Review action |
| --- | --- | --- | --- |
| Log-everything as a substitute for telemetry design | indiscriminate capture increases privacy, cost, and retention burden while still failing to preserve the right identifiers or summaries for reconstruction | rich payload logging is on by default, but investigators still cannot explain route, retrieval, or policy behavior cleanly | redesign the schema around reconstructable events and reopen chapters `06` and `15` before rollout expands |
| Dashboard theater with weak evidence lineage | attractive charts do not help if they cannot explain the user-visible event, release change, or control failure behind the spike | reviews lead with screenshots, aggregate trends, or vanity metrics instead of traceable incidents | require one end-to-end reconstruction packet and verify release-to-trace mapping before approval |
| Raw-content dependence for routine support | support workflows become unsafe and hard to scale when first-line investigation requires broad access to prompts, documents, or tool payloads | support asks for wider access because masked traces and event summaries are not sufficient to route cases | block rollout broadening until masked telemetry and break-glass boundaries support routine investigation |
| Orphaned alerts with no decision owner | alert volume rises, but incidents still stall because nobody owns the business interpretation, user communication, or control follow-through | on-call coverage exists for infrastructure, yet retrieval, policy, or tool failures bounce between teams | assign named owners, escalation paths, and chapter handoffs for each alert family before launch |
| Vendor-locked reconstruction | the observability design quietly depends on proprietary joins, schemas, or retention defaults that cannot survive procurement, sovereignty, or outage pressure | export tests are absent and incident review depends on one UI rather than portable artifacts | document the dependence, add extraction drills, and reopen chapters `09` and `18` if the portability cost is unacceptable |

## Review Prompts

- Which observability pattern best matches the dominant operating risk: release-linked reconstruction, tiered telemetry, control-aware alerting, exportable evidence, or live-signal re-review?
- Which identifier or artifact would let a reviewer prove whether a failure came from the model, route, retrieval source, toolchain, policy path, or human handoff?
- Where is raw-content access controlled, and can routine support still work without granting broad visibility into prompts, retrieved material, or payloads?
- Which adjacent chapter must re-enter before rollout widens: `06`, `09`, `10`, `13`, `15`, `16`, or `18`?

## Re-Review Triggers

- a model, prompt, route, retrieval source, tool binding, or approval path changes without confirming the same identifiers still connect live incidents to the new system shape
- new telemetry sinks, regions, vendors, or export paths are added, especially if they change retention, access boundaries, or portability posture
- support or incident response starts requesting broader raw-content access because structured traces no longer answer routine operational questions
- alerting shows recurring silent failures, blocked decisions, or policy events that the release packet in chapter `13` never tested
- investigation quality depends on proprietary dashboards or missing joins that have not been exercised through export or migration drills

## Practical Reading Rule

Use these patterns after the instrumentation lane is chosen but before the operating model is treated as safe. If the team cannot reconstruct a failed run, explain who can see which evidence, show which alerts drive action, and prove the telemetry remains governable under vendor or scope change, the observability design is not finished.

Back to [14.2 Operating Observability](14-02-00-operating-observability.md).
