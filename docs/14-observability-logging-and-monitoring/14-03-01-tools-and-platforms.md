# 14.3.1 Tools And Platforms

This subsection holds the chapter's named comparison material. Read it as a reference layer, not as a substitute for the chapter's conceptual and implementation sections.

This file compares the main telemetry and monitoring layers relevant to AI systems. It covers open telemetry foundations, general observability backplanes, and AI-specific tracing platforms because a useful observability stack usually combines at least two of those categories.

## How To Use This File

- Read the tables as comparison surfaces, not as universal rankings.
- Separate open telemetry standards from visualization platforms and from AI-specific trace products.
- Re-check `06`, `09`, `13`, and `15` before assuming more logging is automatically better logging.

## Open And Portable Telemetry Foundations

These foundations matter when the organization wants exportable evidence rather than a telemetry dead end.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [OpenTelemetry](https://opentelemetry.io/) | Standard / project | Telemetry standard and instrumentation model | Preferred | Open source | Self-managed standard | Trace and metric foundations | Needs implementation discipline and downstream tooling | [OTel](https://opentelemetry.io/) |
| [OpenLIT](https://docs.openlit.io/) | Open-source platform | OpenTelemetry-native AI observability layer | Preferred | Open source | Self-hosted | Teams wanting OSS tracing, evaluations, and dashboards with OTel alignment | Still requires deliberate retention, redaction, and operations design | [Docs](https://docs.openlit.io/) |
| [Grafana](https://grafana.com/) | Open-source project / platform | Metrics and dashboard layer | Preferred | Open source / open core ecosystem | Self-hosted or managed | Unified infrastructure and AI runtime dashboards | AI-specific traces usually need companion tooling or custom schemas | [Grafana](https://grafana.com/) |
| [Elastic Observability](https://www.elastic.co/observability) | Observability platform | Logs, traces, and metrics analysis | Acceptable | Open core / commercial ecosystem | Self-hosted or managed | Unified observability for teams already invested in Elastic | AI-native semantics usually need extra schema and instrumentation work | [Elastic](https://www.elastic.co/observability) |
| [OpenObserve](https://openobserve.ai/) | Observability platform | Logs, metrics, and trace storage | Preferred | Open source / commercial ecosystem | Self-hosted or managed | Organizations wanting a more open backplane for broad telemetry storage | AI-specific analysis still needs additional semantic modeling | [OpenObserve](https://openobserve.ai/) |
| [SigNoz](https://signoz.io/docs/) | Open-source observability platform | OpenTelemetry-native observability backplane | Preferred | Open source | Self-hosted or managed | Teams wanting a more complete OSS traces, metrics, and logs stack with AI telemetry potential | Still needs application-level schemas and retention design for AI-specific use | [Docs](https://signoz.io/docs/) |

## AI-Specific Observability And Trace Platforms

These tools matter when teams need prompt, tool-call, context, and cost visibility rather than only infrastructure traces.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Langfuse](https://langfuse.com/) | Product / project | LLM observability | Acceptable | Open source / commercial ecosystem | Self-hosted or managed | Prompt, trace, and evaluation telemetry | Managed use improves convenience but adds dependence | [Langfuse](https://langfuse.com/) |
| [Helicone](https://www.helicone.ai/) | Product / project | LLM observability gateway | Acceptable | Open source / commercial ecosystem | Self-hosted or managed | Cost and request observability | Gateway placement changes control-plane posture | [Docs](https://docs.helicone.ai/) |
| [Arize Phoenix](https://phoenix.arize.com/) | Open-source project | AI observability and evaluation | Preferred | Open source | Self-hosted | Trace, embedding, and eval visibility | Requires internal deployment and instrumentation work | [Phoenix](https://phoenix.arize.com/) |
| [Weights & Biases Weave](https://wandb.ai/site/weave/) | Product / project | LLM trace and eval observability | Acceptable | Open source / commercial ecosystem | Self-hosted or managed | Experiment-heavy and agent-heavy teams | Feature depth can pull teams toward broader W&B estate | [W&B](https://wandb.ai/site/weave/) |
| [LangSmith](https://docs.smith.langchain.com/) | Managed platform | Trace-linked debugging and evaluation | Controlled Exception | Proprietary service | Managed | Teams already using LangChain and needing fast trace inspection | Strong ecosystem coupling and managed control-plane dependence | [Docs](https://docs.smith.langchain.com/) |
| [Galileo Observe](https://docs.galileo.ai/galileo) | Observability and eval platform | Production AI monitoring linked to evaluation signals | Controlled Exception | Proprietary platform | SaaS, VPC, or on-prem options | Teams linking live failures to eval and guardrail workflows | Broader platform dependence grows as more lifecycle stages move into Galileo | [Docs](https://docs.galileo.ai/galileo) |

## Managed Enterprise Observability Platforms

These platforms matter when AI telemetry must fit into a wider enterprise incident and monitoring stack.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Honeycomb](https://www.honeycomb.io/) | Product | High-cardinality observability | Controlled Exception | Proprietary service | Managed | Investigation-heavy teams needing strong trace exploration | Managed observability platform dependence | [Honeycomb](https://www.honeycomb.io/) |
| [Datadog LLM Observability](https://www.datadoghq.com/product/llm-observability/) | Managed platform capability | Managed LLM telemetry and cost visibility | Controlled Exception | Proprietary service | Managed | Teams already running Datadog as the central observability plane | Adds more dependence to the managed observability control plane | [Datadog](https://www.datadoghq.com/product/llm-observability/) |
| [New Relic AI Monitoring](https://newrelic.com/platform/ai-monitoring) | Managed platform capability | AI monitoring integrated with general application observability | Controlled Exception | Proprietary service | Managed | Existing New Relic estates extending observability to AI systems | Managed platform dependence remains strong | [New Relic](https://newrelic.com/platform/ai-monitoring) |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [14.3 Reference Points](14-03-00-reference-points.md).
