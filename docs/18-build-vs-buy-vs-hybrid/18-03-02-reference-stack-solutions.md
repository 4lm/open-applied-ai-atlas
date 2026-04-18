# 18.3.2 Reference Stack Solutions

_Page Type: Comparison Page | Maturity: Review-Ready_

This file translates sourcing postures into reusable stack shapes. The summary table compares the patterns, and the component table breaks the common anchor choices into one row per entry so trade-offs are easier to compare.

## How To Use This File

- These shapes are reusable starting points, not drop-in blueprints.
- A stronger openness tier does not automatically mean lower operating burden.
- Use the chapter front door to understand when a pattern fits before comparing solutions.

## Sourcing Shapes

| Shape | Typical composition | Openness-policy tier | Strongest fit | Main trade-off |
| --- | --- | --- | --- | --- |
| Buy-first assistant | Managed model access plus lightweight integration and telemetry | Controlled Exception | Fast internal copilots and low-ops experimentation | Fastest start, weakest exit posture |
| Buy-first enterprise platform | Managed model runtime plus managed evaluation and observability | Controlled Exception | Teams standardized on one cloud or SaaS ecosystem | Control and evidence often remain inside the vendor estate |
| Gateway-centric hybrid stack | Managed models plus internal or semi-portable gateway, policy, and telemetry | Acceptable | Multi-team portfolios that need common controls quickly | Adds platform work without removing managed-model dependence |
| Retrieval-heavy hybrid stack | Managed or open model access plus internal retrieval and permissions layer | Acceptable | Knowledge assistants over sensitive internal content | Better data control, but retrieval governance becomes central |
| Open infrastructure stack | Self-hosted serving plus open-source gateway, retrieval, and telemetry | Preferred | Exit-sensitive organizations with platform maturity | Higher operating burden and on-call ownership |
| Mixed open-model managed stack | Managed open-model provider plus exportable gateway and evaluation layer | Acceptable | Teams needing speed now with a later self-hosting option | Easier migration story than closed APIs, but still provider-coupled |
| Sovereign private stack | Self-hosted serving, portable data stores, strong policy controls, exportable telemetry | Strategic Open | Highly regulated or sovereignty-sensitive environments | Highest support burden and deepest internal capability requirements |
| Hybrid predictive-plus-generative stack | Existing ML platform plus LLM gateway, retrieval, and evaluation layers | Acceptable | Organizations with established ML estates adding language interfaces | More architectural complexity across method families |

## Representative Component Anchors

| Shape | Layer | Anchor | Why it belongs in the shape | Primary source |
| --- | --- | --- | --- | --- |
| Buy-first assistant | Model access | [OpenAI Models](https://platform.openai.com/docs/models) | Common buy-first anchor for managed frontier capability | [Docs](https://platform.openai.com/docs/models) |
| Buy-first assistant | Model access | [Anthropic Claude](https://docs.anthropic.com/) | Similar buy-first anchor for managed conversational and agentic systems | [Docs](https://docs.anthropic.com/) |
| Buy-first assistant | Basic telemetry | [OpenTelemetry](https://opentelemetry.io/) | Even thin buy-first stacks benefit from exportable app telemetry | [OTel](https://opentelemetry.io/) |
| Buy-first enterprise platform | Managed runtime | [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/) | Common cloud-estate buy-first runtime | [Docs](https://docs.aws.amazon.com/bedrock/) |
| Buy-first enterprise platform | Managed runtime | [Google Vertex AI](https://cloud.google.com/vertex-ai/docs) | Common GCP-native managed platform choice | [Docs](https://cloud.google.com/vertex-ai/docs) |
| Buy-first enterprise platform | Managed runtime | [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/) | Common Microsoft-native managed platform choice | [Docs](https://learn.microsoft.com/azure/ai-foundry/) |
| Buy-first enterprise platform | Managed runtime | [IBM watsonx.ai](https://www.ibm.com/products/watsonx-ai) | Strong fit where model access and governance are procured together | [IBM](https://www.ibm.com/products/watsonx-ai) |
| Gateway-centric hybrid stack | Gateway | [LiteLLM](https://docs.litellm.ai/) | Keeps some provider abstraction and routing under internal control | [Docs](https://docs.litellm.ai/) |
| Gateway-centric hybrid stack | Gateway | [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/) | Adds centralized governance over mixed providers with less platform effort | [Docs](https://developers.cloudflare.com/ai-gateway/) |
| Gateway-centric hybrid stack | Observability | [Langfuse](https://langfuse.com/) | Supports more portable tracing and evaluation signals across mixed runtimes | [Langfuse](https://langfuse.com/) |
| Retrieval-heavy hybrid stack | Retrieval store | [Qdrant](https://qdrant.tech/) | Portable retrieval substrate for sensitive internal content | [Docs](https://qdrant.tech/documentation/) |
| Retrieval-heavy hybrid stack | Retrieval store | [pgvector](https://github.com/pgvector/pgvector) | Lower-friction retrieval path for Postgres-heavy estates | [Repo](https://github.com/pgvector/pgvector) |
| Retrieval-heavy hybrid stack | Managed model access | [Mistral AI](https://docs.mistral.ai/) | Mixed posture can work well in hybrid sourcing designs | [Docs](https://docs.mistral.ai/) |
| Open infrastructure stack | Serving runtime | [vLLM](https://docs.vllm.ai/) | Common self-hosted serving backbone | [Docs](https://docs.vllm.ai/) |
| Open infrastructure stack | Serving runtime | [Hugging Face TGI](https://huggingface.co/docs/text-generation-inference/index) | Alternative open serving backbone | [Docs](https://huggingface.co/docs/text-generation-inference/index) |
| Open infrastructure stack | Serving runtime | [MLServer](https://docs.seldon.ai/mlserver) | Useful when one open serving layer should cover predictive and generative workloads | [Docs](https://docs.seldon.ai/mlserver) |
| Open infrastructure stack | Telemetry | [OpenTelemetry](https://opentelemetry.io/) | Exportable evidence is central to build-heavy stacks | [OTel](https://opentelemetry.io/) |
| Mixed open-model managed stack | Managed provider | [Groq](https://console.groq.com/docs/overview) | Useful where open-model access is paired with very low-latency managed inference | [Docs](https://console.groq.com/docs/overview) |
| Mixed open-model managed stack | Managed provider | [Together AI](https://docs.together.ai/) | Faster path to open-model consumption without immediate self-hosting | [Docs](https://docs.together.ai/) |
| Mixed open-model managed stack | Evaluation | [promptfoo](https://www.promptfoo.dev/) | Keeps evaluation more portable than provider-native-only tooling | [Docs](https://www.promptfoo.dev/docs/intro) |
| Sovereign private stack | Serving platform | [Seldon Core 2](https://docs.seldon.ai/seldon-core-v2/) | Useful for standardized self-hosted deployment at organizational scale across multiple serving backends | [Docs](https://docs.seldon.ai/seldon-core-v2/) |
| Sovereign private stack | Serving runtime | [KServe](https://kserve.github.io/kserve/) | Useful for Kubernetes-native self-hosted deployment patterns | [KServe](https://kserve.github.io/kserve/) |
| Sovereign private stack | Policy | [Open Policy Agent](https://www.openpolicyagent.org/) | Policy-as-code is central when control posture is strategic | [OPA](https://www.openpolicyagent.org/) |
| Sovereign private stack | Telemetry | [OpenTelemetry](https://opentelemetry.io/) | Exportable telemetry is critical to evidence and exit posture | [OTel](https://opentelemetry.io/) |
| Hybrid predictive-plus-generative stack | Lifecycle | [MLflow](https://mlflow.org/) | Connects classical ML lifecycle work with newer language interfaces | [MLflow](https://mlflow.org/) |
| Hybrid predictive-plus-generative stack | Platform | [Dataiku](https://www.dataiku.com/product/machine-learning/) | Strong fit when one governed platform should span predictive, optimization, and language-interface work | [Dataiku](https://www.dataiku.com/product/machine-learning/) |
| Hybrid predictive-plus-generative stack | Platform | [Databricks Mosaic AI](https://www.databricks.com/product/mosaic-ai) | Natural anchor when a lakehouse estate already exists | [Databricks](https://www.databricks.com/product/mosaic-ai) |
| Hybrid predictive-plus-generative stack | Evaluation | [Inspect AI](https://inspect.aisi.org.uk/) | Useful portable evaluation layer when scenario-based testing matters across method families | [Inspect](https://inspect.aisi.org.uk/) |

## Evidence Notes

- The component anchors are linked to official documentation or project pages in the `Primary source` column.
- The shapes and trade-offs are atlas synthesis. They are intended as reusable sourcing patterns, not certified reference architectures or one-size-fits-all blueprints.
- A stronger openness posture does not eliminate operating burden; that trade-off is explicitly preserved in the summary table.

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [18.3 Reference Points](18-03-00-reference-points.md).
