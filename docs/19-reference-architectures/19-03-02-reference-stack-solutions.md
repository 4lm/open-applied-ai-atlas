# 19.3.2 Reference Stack Solutions

_Page Type: Comparison Page | Maturity: Draft_

This file groups reusable architecture shapes so readers can move from individual layers to coherent compositions. It separates summary pattern comparison from component anchors so the reference architectures are easier to compare tool by tool.

## How To Use This File

- These shapes are reusable starting points, not drop-in blueprints.
- A stronger openness tier does not automatically mean lower operating burden.
- Use the chapter front door to understand when a pattern fits before comparing solutions.

## Representative Solution Shapes

| Pattern | Typical stack | Openness-policy tier | Strongest fit | Main trade-off |
| --- | --- | --- | --- | --- |
| SaaS-first assistant | Managed model API, thin gateway, basic monitoring | Controlled Exception | Low- to moderate-risk internal assistance | Fastest start, weakest runtime autonomy |
| Managed suite architecture | Enterprise workflow suite plus embedded AI capabilities | Controlled Exception | Service, CRM, or productivity estates standardizing on one suite | Strongest application-level lock-in and data gravity |
| Enterprise gateway stack | Gateway, retrieval, evaluation, observability | Acceptable | Multi-team portfolios needing common control points | Added platform dependence and design overhead |
| Open infrastructure stack | Self-hosted models, open gateway, open retrieval, exportable telemetry | Preferred | Exit-sensitive organizations with platform maturity | More operational burden |
| Sovereign private platform | Portable serving, controlled data boundary, strong auditability | Strategic Open | High-sovereignty or regulated environments | Highest support and lifecycle burden |
| Agentic workflow platform | Gateway, workflow runtime, tool policy, step tracing | Acceptable | Delegated action with explicit guardrails | Highest QA and security burden |
| Public-facing content architecture | Content generation or verification pipeline with provenance enforcement | Acceptable | Synthetic-content publishing, newsroom, and media-trust use cases | Provenance work adds operational complexity |
| Edge-capable local platform | Smaller models, local inference, and exportable telemetry | Preferred | Edge, air-gapped, or workstation-heavy operations | Lower raw capability than cloud-first frontier stacks |
| Hybrid predictive plus generative stack | Predictive ML pipeline plus retrieval-backed language interface | Acceptable | Forecasting, scoring, and explanation workloads | More stack complexity across method families |

## Representative Component Anchors

| Pattern | Layer | Anchor | Why it fits this architecture | Primary source |
| --- | --- | --- | --- | --- |
| SaaS-first assistant | Model access | [OpenAI Models](https://platform.openai.com/docs/models) | Common managed model anchor for SaaS-first architectures | [Docs](https://platform.openai.com/docs/models) |
| SaaS-first assistant | Model access | [Anthropic Claude](https://docs.anthropic.com/) | Similar managed anchor for assistant-heavy internal architectures | [Docs](https://docs.anthropic.com/) |
| SaaS-first assistant | Monitoring | [OpenTelemetry](https://opentelemetry.io/) | Even thin architectures benefit from exportable telemetry | [OTel](https://opentelemetry.io/) |
| Managed suite architecture | Application layer | [ServiceNow Now Assist](https://www.servicenow.com/products/now-assist.html) | Strong fit where service workflows dominate the architecture | [ServiceNow](https://www.servicenow.com/products/now-assist.html) |
| Managed suite architecture | Application layer | [Salesforce Einstein](https://www.salesforce.com/products/einstein-ai-solutions/) | Strong fit where CRM gravity dominates the architecture | [Salesforce](https://www.salesforce.com/products/einstein-ai-solutions/) |
| Managed suite architecture | Application layer | [Microsoft 365 Copilot](https://www.microsoft.com/en-us/microsoft-365/copilot) | Strong fit where workplace productivity architecture is already Microsoft-centered | [Microsoft](https://www.microsoft.com/en-us/microsoft-365/copilot) |
| Enterprise gateway stack | Gateway | [LiteLLM](https://docs.litellm.ai/) | Common open control-plane anchor | [Docs](https://docs.litellm.ai/) |
| Enterprise gateway stack | Retrieval | [Qdrant](https://qdrant.tech/) | Portable retrieval layer for internal enterprise knowledge systems | [Docs](https://qdrant.tech/documentation/) |
| Enterprise gateway stack | Evaluation | [Inspect AI](https://inspect.aisi.org.uk/) | Strong fit when shared scenario-based evaluation should be a platform capability, not a team-by-team add-on | [Inspect](https://inspect.aisi.org.uk/) |
| Enterprise gateway stack | Evaluation | [promptfoo](https://www.promptfoo.dev/) | Portable regression evidence for multi-team stacks | [Docs](https://www.promptfoo.dev/docs/intro) |
| Enterprise gateway stack | Observability | [SigNoz](https://signoz.io/docs/) | Strong fit when the platform wants self-hostable observability beside exportable telemetry | [Docs](https://signoz.io/docs/) |
| Enterprise gateway stack | Observability | [Langfuse](https://langfuse.com/) | AI-specific trace visibility across shared platform components | [Langfuse](https://langfuse.com/) |
| Open infrastructure stack | Serving runtime | [vLLM](https://docs.vllm.ai/) | Common self-hosted serving backbone | [Docs](https://docs.vllm.ai/) |
| Open infrastructure stack | Serving runtime | [MLServer](https://docs.seldon.ai/mlserver) | Useful when open infrastructure should serve both predictive and generative workloads through one layer | [Docs](https://docs.seldon.ai/mlserver) |
| Open infrastructure stack | Gateway | [Envoy AI Gateway](https://aigateway.envoyproxy.io/) | Useful open gateway path for self-hosted control planes | [Docs](https://aigateway.envoyproxy.io/) |
| Open infrastructure stack | Retrieval | [pgvector](https://github.com/pgvector/pgvector) | Keeps knowledge storage portable and simple in many architectures | [Repo](https://github.com/pgvector/pgvector) |
| Open infrastructure stack | Telemetry | [OpenTelemetry](https://opentelemetry.io/) | Exportable evidence is central to build-heavy architectures | [OTel](https://opentelemetry.io/) |
| Sovereign private platform | Serving platform | [Seldon Core 2](https://docs.seldon.ai/seldon-core-v2/) | Useful for standardized self-hosted deployment at scale across multiple runtimes | [Docs](https://docs.seldon.ai/seldon-core-v2/) |
| Sovereign private platform | Serving runtime | [KServe](https://kserve.github.io/kserve/) | Useful for standardized self-hosted deployment at scale | [KServe](https://kserve.github.io/kserve/) |
| Sovereign private platform | Retrieval | [Milvus](https://milvus.io/) | Local retrieval layer for high-control deployments | [Docs](https://milvus.io/docs) |
| Sovereign private platform | Policy | [Open Policy Agent](https://www.openpolicyagent.org/) | Makes policy a first-class architectural layer | [OPA](https://www.openpolicyagent.org/) |
| Sovereign private platform | Observability | [OpenTelemetry](https://opentelemetry.io/) | Exportable telemetry is required for auditability and exit posture | [OTel](https://opentelemetry.io/) |
| Agentic workflow platform | Orchestration | [LangGraph](https://langchain-ai.github.io/langgraph/) | Common stateful runtime for tool-using agent systems | [Docs](https://langchain-ai.github.io/langgraph/) |
| Agentic workflow platform | Durable execution | [Temporal](https://temporal.io/) | Strong fit when resumability and retries matter | [Docs](https://docs.temporal.io/) |
| Agentic workflow platform | Security | [Presidio](https://microsoft.github.io/presidio/) | Useful redaction layer in tool- and data-heavy agent systems | [Docs](https://microsoft.github.io/presidio/) |
| Agentic workflow platform | Observability | [Arize Phoenix](https://phoenix.arize.com/) | Useful trace and eval layer for agent workflows | [Phoenix](https://phoenix.arize.com/) |
| Public-facing content architecture | Provenance | [C2PA](https://c2pa.org/) | Core content-authenticity anchor | [C2PA](https://c2pa.org/) |
| Public-facing content architecture | Signing | [Sigstore](https://www.sigstore.dev/) | Useful signing layer for surrounding artifacts and workflows | [Sigstore](https://www.sigstore.dev/) |
| Public-facing content architecture | Telemetry | [OpenTelemetry](https://opentelemetry.io/) | Exportable incident evidence remains important in public systems | [OTel](https://opentelemetry.io/) |
| Edge-capable local platform | Local runtime | [Ollama](https://ollama.com/) | Practical local serving anchor for workstation-heavy patterns | [Docs](https://docs.ollama.com/) |
| Edge-capable local platform | Local runtime | [OpenVINO Model Server](https://docs.openvino.ai/2025/openvino-workflow/model-server/ovms_what_is_openvino_model_server.html) | Strong fit for governed local and edge inference in CPU-heavy enterprise estates | [Docs](https://docs.openvino.ai/2025/openvino-workflow/model-server/ovms_what_is_openvino_model_server.html) |
| Edge-capable local platform | Telemetry | [OpenTelemetry](https://opentelemetry.io/) | Keeps local architectures exportable when they synchronize upstream | [OTel](https://opentelemetry.io/) |
| Hybrid predictive plus generative stack | Lifecycle | [MLflow](https://mlflow.org/) | Connects classical ML lifecycle work with language interfaces | [MLflow](https://mlflow.org/) |
| Hybrid predictive plus generative stack | Platform | [Dataiku](https://www.dataiku.com/product/machine-learning/) | Strong fit where one governed platform should span predictive, optimization, and generative delivery | [Dataiku](https://www.dataiku.com/product/machine-learning/) |
| Hybrid predictive plus generative stack | Managed platform | [Databricks Mosaic AI](https://www.databricks.com/product/mosaic-ai) | Natural anchor when a lakehouse architecture already exists | [Databricks](https://www.databricks.com/product/mosaic-ai) |
| Hybrid predictive plus generative stack | Evaluation | [Inspect AI](https://inspect.aisi.org.uk/) | Strong fit where evaluation has to cover realistic task scenarios across method families | [Inspect](https://inspect.aisi.org.uk/) |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [19.3 Reference Points](19-03-00-reference-points.md).
