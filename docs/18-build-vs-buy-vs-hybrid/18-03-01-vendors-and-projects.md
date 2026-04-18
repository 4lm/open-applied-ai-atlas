# 18.3.1 Vendors And Projects

This subsection holds the chapter's named comparison material. Read it as a reference layer, not as a substitute for the chapter's conceptual and implementation sections.

This file compares the vendors and projects that tend to pull decisions toward buy, build, or hybrid sourcing. The same tool can appear in multiple sections because sourcing posture depends on how it is adopted, not only on what the product is.

## How To Use This File

- Separate sourcing posture from marketing category.
- The question is not whether a product is good; it is where control, operating burden, and exit difficulty sit after adoption.
- Use this file together with `07`, `08`, `09`, `17`, and the reference stack shapes in this chapter.

## Buy-Leaning Managed Platforms

These entries matter when speed, vendor support, and low initial operating burden dominate the decision.

| Resource | Entity type | Sourcing posture | Why it matters | Main dependence note | Primary source |
| --- | --- | --- | --- | --- | --- |
| [OpenAI Models](https://platform.openai.com/docs/models) | Managed platform | Buy API-first frontier model access | Fastest route to managed frontier capability | Runtime, policy, and roadmap dependence on vendor APIs | [Docs](https://platform.openai.com/docs/models) |
| [Anthropic Claude](https://docs.anthropic.com/) | Managed platform | Buy enterprise conversational and agentic model access | Similar buy-first path with strong managed safety and enterprise positioning | Managed endpoint and vendor lifecycle dependence | [Docs](https://docs.anthropic.com/) |
| [AWS Bedrock](https://docs.aws.amazon.com/bedrock/) | Managed service | Buy managed foundation-model access | Managed model marketplace plus cloud-estate integration | Layered dependence on AWS contracts and services | [Docs](https://docs.aws.amazon.com/bedrock/) |
| [Google Vertex AI](https://cloud.google.com/vertex-ai/docs) | Managed service | Buy cloud-native model hosting and ML platform services | Managed model and MLOps surfaces in GCP | Strong cloud-estate coupling | [Docs](https://cloud.google.com/vertex-ai/docs) |
| [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/) | Managed service | Buy Microsoft-centered AI runtime and platform services | Managed hosting and model platform for Microsoft estates | Strong cloud and platform coupling | [Docs](https://learn.microsoft.com/azure/ai-foundry/) |
| [IBM watsonx.ai](https://www.ibm.com/products/watsonx-ai) | Managed platform | Buy governed enterprise AI and model services | Strong fit where model access, governance, and runtime controls are procured together | Managed platform dependence remains central even with more portable posture than API-only vendors | [IBM](https://www.ibm.com/products/watsonx-ai) |
| [Cohere](https://docs.cohere.com/) | Managed platform | Buy enterprise language and retrieval APIs | Focused managed access for enterprise NLP and retrieval patterns | API-first dependence remains central | [Docs](https://docs.cohere.com/) |
| [Groq](https://console.groq.com/docs/overview) | Managed platform | Buy low-latency managed inference | Useful when latency and throughput matter more than building optimization layers internally | Performance advantages can become a new routing and hardware dependence | [Docs](https://console.groq.com/docs/overview) |
| [Together AI](https://docs.together.ai/) | Managed platform | Buy open-model access without operating self-hosted infrastructure immediately | Useful transitional option for open-weight consumers | Still a managed-provider dependence layer | [Docs](https://docs.together.ai/) |
| [Fireworks AI](https://docs.fireworks.ai/) | Managed platform | Buy high-throughput managed inference | Reduces performance engineering burden for open-model inference | Platform-specific routing and cost dependence | [Docs](https://docs.fireworks.ai/) |
| [Baseten](https://docs.baseten.co/overview) | Managed platform | Buy application and model serving together | Useful when teams want a single managed deployment surface | Platform becomes part of the runtime architecture, not just a model provider | [Docs](https://docs.baseten.co/overview) |

## Build-Leaning Open Infrastructure Projects

These entries matter when portability, operating control, or sovereign deployment are strategic requirements rather than preferences.

| Resource | Entity type | Sourcing posture | Why it matters | Main dependence note | Primary source |
| --- | --- | --- | --- | --- | --- |
| [vLLM](https://docs.vllm.ai/) | Open-source project | Build or self-host inference | Common portable serving backbone for open-weight deployments | Requires direct platform and GPU ownership | [Docs](https://docs.vllm.ai/) |
| [Hugging Face Text Generation Inference](https://huggingface.co/docs/text-generation-inference/index) | Open-source project | Build self-managed text-generation serving | Alternative portable serving backbone with broad ecosystem support | Requires surrounding deployment, telemetry, and support disciplines | [Docs](https://huggingface.co/docs/text-generation-inference/index) |
| [KServe](https://kserve.github.io/kserve/) | Open-source platform | Build Kubernetes-native inference | Good fit for platform teams standardizing predictive and generative serving on Kubernetes | Requires cluster maturity and platform engineering depth | [KServe](https://kserve.github.io/kserve/) |
| [MLServer](https://docs.seldon.ai/mlserver) | Open-source project | Build portable predictive and generative serving | Useful where one serving layer should span classical ML and newer language-model workloads | Needs surrounding deployment and model-governance discipline | [Docs](https://docs.seldon.ai/mlserver) |
| [Seldon Core 2](https://docs.seldon.ai/seldon-core-v2/) | Open-source platform | Build governed self-hosted inference at organizational scale | Strong fit when platform teams need a shared control plane over mixed model-serving backends | Kubernetes and platform operating burden remain significant | [Docs](https://docs.seldon.ai/seldon-core-v2/) |
| [LiteLLM](https://docs.litellm.ai/) | Open-source project | Build a portable gateway and provider-abstraction layer | Useful when routing and provider abstraction should stay under internal control | Gateway quality depends on internal policy and operations maturity | [Docs](https://docs.litellm.ai/) |
| [Qdrant](https://qdrant.tech/) | Vector database | Build portable retrieval infrastructure | Portable retrieval substrate with self-hosted path | Retrieval architecture still needs permissions, freshness, and evaluation design | [Docs](https://qdrant.tech/documentation/) |
| [pgvector](https://github.com/pgvector/pgvector) | Open-source extension | Keep retrieval inside existing PostgreSQL estates | Practical default for simpler, more portable retrieval adoption | Feature depth differs from dedicated vector stores | [Repo](https://github.com/pgvector/pgvector) |
| [OpenTelemetry](https://opentelemetry.io/) | Open specification / project | Build exportable telemetry instead of vendor-specific instrumentation | Core building block for portable evidence and incident reconstruction | Still needs disciplined implementation and downstream tooling | [OTel](https://opentelemetry.io/) |
| [MLflow](https://mlflow.org/) | Open-source project | Build experiment and lifecycle governance around open tooling | Useful for open lifecycle control across model and adaptation work | Operating burden is lower than full custom tooling, but not zero | [MLflow](https://mlflow.org/) |
| [Open Policy Agent](https://www.openpolicyagent.org/) | Open-source project | Build shared policy enforcement under internal control | Central for portable policy-as-code across AI and non-AI systems | Integration burden sits with the organization | [OPA](https://www.openpolicyagent.org/) |

## Hybrid And Composition-Friendly Resources

These entries matter when organizations want to buy speed at some layers while preserving stronger exit or control posture elsewhere.

| Resource | Entity type | Sourcing posture | Why it matters | Main dependence note | Primary source |
| --- | --- | --- | --- | --- | --- |
| [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers/index) | Managed platform | Compose or buy model access through unified APIs | Useful as a hybrid discovery and access layer over multiple providers | Still a managed mediation layer between app and runtime | [Docs](https://huggingface.co/docs/inference-providers/index) |
| [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/) | Managed gateway capability | Add a shared control plane over mixed provider choices | Can improve governance in a hybrid estate without full self-hosting | Creates a new managed control dependency | [Docs](https://developers.cloudflare.com/ai-gateway/) |
| [Langfuse](https://langfuse.com/) | Open-source / managed platform | Keep observability exportable in mixed estates | Lets teams preserve stronger telemetry portability across managed and self-hosted layers | Managed deployment improves convenience but adds dependence | [Langfuse](https://langfuse.com/) |
| [NVIDIA NIM](https://build.nvidia.com/) | Mixed deployment ecosystem | Blend customer-managed deployment with vendor-specific optimization | Useful middle ground between raw self-hosting and fully managed inference | Hardware and optimization dependence can still become structural | [NVIDIA](https://build.nvidia.com/) |
| [Dataiku](https://www.dataiku.com/product/machine-learning/) | Enterprise AI and ML platform | Add governed predictive and generative workflows to mixed estates | Useful when existing teams need one governed surface across classical ML, optimization, and generative interfaces | Workflow and governance gravity can become a durable platform dependency | [Dataiku](https://www.dataiku.com/product/machine-learning/) |
| [SAS Viya](https://www.sas.com/en_us/software/viya.html) | Enterprise analytics and AI platform | Blend existing governed analytics estates with newer AI interfaces | Useful in analytics-heavy organizations that already operate strong SAS-centered controls | Existing estate fit is an advantage, but also raises exit costs | [SAS](https://www.sas.com/en_us/software/viya.html) |
| [Databricks Mosaic AI](https://www.databricks.com/product/mosaic-ai) | Managed platform | Hybrid data-estate plus model platform sourcing | Useful where existing lakehouse control matters as much as model choice | Data estate, workflow, and model tooling dependence can compound | [Databricks](https://www.databricks.com/product/mosaic-ai) |
| [CNCF Landscape](https://landscape.cncf.io/) | Ecosystem map | Scan adjacent open-source building blocks before defaulting to proprietary stack layers | Useful discovery surface for hybrid and build-heavy platform design | Landscape breadth requires filtering and architectural discipline | [CNCF](https://landscape.cncf.io/) |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [18.3 Reference Points](18-03-00-reference-points.md).
