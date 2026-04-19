# 14.1.1 Signals, Traces, And Core Distinctions

_Page Type: Concept Explainer | Maturity: Review-Ready_

Use this page to separate the signal families that make AI observability useful: event logs, end-to-end traces, metrics, alerts, and richer investigation artifacts. Teams often say they have "logging" when what they really have is an incomplete mixture of payload dumps, dashboard counters, and vendor-specific traces that cannot answer the review question in front of them.

## Runtime-Evidence Map

| Signal family | Main question it answers | Best fit | Common misuse |
| --- | --- | --- | --- |
| Event logs | What discrete thing happened at a given step? | request admission, tool invocation, policy decision, handoff, retry, failure code, export event | stuffing full prompts, documents, or tool payloads into generic logs because no structured schema exists |
| End-to-end traces | How did one request or job move across components and decisions? | multi-step assistants, agent workflows, routed model calls, retrieval-plus-tool chains, rollback investigation | tracing only the model call and leaving retrieval, gateway, approval, or tool steps invisible |
| Metrics and aggregates | Is the service getting healthier or worse over time? | latency, error rate, cost, queue depth, retry rate, alert thresholds, cohort-level drift signals | expecting metrics alone to explain a single incident or user complaint |
| Alerts and escalation signals | Which conditions require immediate human attention? | security events, silent failure spikes, degraded-mode activation, missing approvals, broken dependencies | alerting on volume and uptime only while user-visible quality or control failures stay silent |
| Investigation artifacts | What evidence must survive incident, audit, support, or supplier review? | incident timelines, release-to-trace links, redaction records, export samples, reconstruction packets | treating screenshots or ad hoc notebook work as durable evidence |

## Core Distinctions

| Distinction | Why it changes the design |
| --- | --- |
| Event capture vs. causal reconstruction | A list of events can prove that something happened, but only traces or linked identifiers show how one decision led to the next across runtime layers. |
| Structured telemetry vs. raw payload capture | Structured fields usually support routine support and operations better than universal raw-content capture, which raises privacy, retention, and access burdens fast. |
| Service health signals vs. decision-quality signals | Low latency and high uptime do not prove that citations, tool choices, policy checks, or human handoffs are behaving correctly. |
| Model-call visibility vs. full workflow visibility | AI incidents often come from routing, retrieval, tools, approvals, or surrounding services rather than from the model call alone. |
| Always-on observability vs. break-glass forensics | Rich content and replay data may be justified for exceptional investigations, but they should not become the default access pattern for daily support. |
| Operational debugging vs. governance evidence | Telemetry that helps engineers debug may still be unusable for audit, release review, deletion handling, or supplier-exit planning if retention, export, and ownership are unclear. |
| Portable evidence spine vs. vendor-only convenience | A polished observability UI is not enough if identifiers, schemas, and exports cannot survive procurement pressure, sovereignty review, or platform change. |

## What These Distinctions Change In Practice

- Design shared identifiers first so request, retrieval, tool, policy, approval, and user-outcome events can be tied together without manual guesswork.
- Keep raw prompt, document, and tool-payload capture proportionate; most daily support and monitoring should work from masked fields, structured traces, and explicit redaction rules.
- Treat retrieval steps, gateway policy decisions, and human overrides as first-class observability events instead of burying them beside generic application logging.
- Require release identifiers, prompt versions, model routes, and policy versions to map into traces so rollout and incident review use the same runtime evidence spine.
- Separate alerting thresholds from investigative depth: metrics should tell the team that something is wrong, while traces and artifacts should explain why.
- Test exportability and retention boundaries early when the team relies on a managed platform, because observability lock-in usually appears after the schema and workflow are already embedded.

## Reviewer Checks

- Can the team show which signal family is supposed to answer each review question: health, reconstruction, support, audit, or supplier portability?
- Which important decisions remain invisible because only model calls are traced while retrieval, tool, gateway, or approval steps are not?
- Does routine support depend on unrestricted access to raw prompts or documents because structured telemetry is too weak?
- Which telemetry must persist as evidence, and who owns retention, redaction, deletion, and export for it?
- If the current observability vendor disappeared tomorrow, which identifiers, traces, and artifacts would still let the team reconstruct a serious incident?

## Practical Reading Rule

Classify the signal family and evidence burden before arguing about dashboards or tools. Then move to [14.1.2 Decision Boundaries And Monitoring Heuristics](14-01-02-decision-boundaries-and-monitoring-heuristics.md) to choose the default instrumentation lane. If the team still cannot say what must be always visible, what belongs behind break-glass controls, and what must remain exportable across tooling changes, the observability design is not ready yet.

Back to [14.1 Observability Foundations](14-01-00-observability-foundations.md).
