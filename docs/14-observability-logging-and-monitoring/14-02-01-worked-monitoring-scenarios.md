# 14.2.1 Worked Monitoring Scenarios

_Page Type: Worked Example | Maturity: Draft_

These scenarios show what usable runtime evidence looks like in practice. Each one names the monitoring shape, required artifacts, and re-review trigger that should already exist before rollout expands or an incident is treated as understood.

## Internal Assistant With Sensitive Knowledge Access

| Field | Decision |
| --- | --- |
| System | Internal retrieval-backed assistant used for policy, support, or knowledge lookup |
| Dominant operating failure | Teams capture too little detail to explain wrong answers or too much raw content to govern safely |
| Observability shape | Request identifiers link user cohort, route, retrieval source IDs, citation set, redaction class, handoff outcome, and reviewer override without making unrestricted raw prompt access the default |
| Required evidence | Field dictionary, redaction rules, example trace, citation-failure investigation packet, retention record, and support escalation path |
| Release question | Can reviewers reconstruct why an answer was wrong, incomplete, or over-permissive without turning observability into a second uncontrolled knowledge store? |
| Re-review trigger | Reopen chapters `06`, `11`, and `15` when new source classes, broader trace capture, or memory-linked context are proposed |

## Multi-Step Agent Incident Reconstruction

| Field | Decision |
| --- | --- |
| System | Agentic workflow that plans, calls tools, retries, and waits on approvals across multiple steps |
| Dominant operating failure | Only the final output is visible, so investigators cannot tell whether the failure came from planning, tool selection, approval handling, policy enforcement, or an external dependency |
| Observability shape | The system emits a span tree that records plan creation, tool invocation, approval events, retries, policy blocks, rollback markers, and final user-visible state under one incident timeline |
| Required evidence | Correlated trace example, denied-action log, approval audit trail, rollback drill, and named on-call ownership for tool and policy failures |
| Release question | Can an incident commander isolate the failing step and prove whether the issue belongs to the model, toolchain, approval path, or surrounding service? |
| Re-review trigger | Reopen chapters `10`, `15`, and `16` when the workflow gains broader tool scope, background autonomy, or lower-friction approvals |

## Replay-Safe Support Investigation

| Field | Decision |
| --- | --- |
| System | Production support workflow for failed assistant or agent runs that may include customer, employee, or regulated data |
| Dominant operating failure | Incident review depends on broad access to raw prompts, retrieved documents, or tool payloads because the structured traces are too thin to support support operations |
| Observability shape | Rich raw payloads are isolated behind break-glass controls, while routine investigation uses masked traces, deterministic request identifiers, event summaries, and recorded handoff decisions |
| Required evidence | Access matrix, break-glass log, redaction test output, deletion workflow, and one completed support drill using masked telemetry only |
| Release question | Can first-line support explain what happened and route the case correctly without unrestricted access to sensitive content? |
| Re-review trigger | Reopen chapters `06`, `15`, and `16` when retention periods, storage regions, access roles, or support ownership change materially |

## Managed Observability Export Review

| Field | Decision |
| --- | --- |
| System | Application and gateway stack instrumented through a managed tracing or monitoring platform |
| Dominant operating failure | The team becomes dependent on a vendor UI or proprietary schema for incident reconstruction, so portability disappears just when procurement, sovereignty, or outage pressure rises |
| Observability shape | Application events, gateway decisions, and provider calls can be exported with stable identifiers into open or documented formats without losing the fields needed for investigation |
| Required evidence | Sample export, field-loss register, periodic extraction test, architecture note describing vendor-only logic, and procurement review of lock-in implications |
| Release question | Would incident reconstruction still work if the managed platform were unavailable, too expensive, or no longer acceptable for sovereignty reasons? |
| Re-review trigger | Reopen chapters `09`, `15`, and `18` when route logic changes, telemetry leaves an approved region, or analysis becomes dependent on non-exportable vendor features |

## Cross-Scenario Review Signals

- strong observability links release identifiers, policy outcomes, retrieval behavior, tool activity, and human intervention into one reconstructable operating story
- rich telemetry is tiered rather than universally exposed; investigation quality should improve without normalizing unrestricted content access
- the most important re-review trigger is scope expansion: new tools, broader retrieval, persistent memory, or deeper vendor dependence should reopen adjacent chapter decisions instead of being treated as logging-only changes

Back to [14.2 Operating Observability](14-02-00-operating-observability.md).
