# 3.3.1 Tooling By Layer

_Page Type: Comparison Page | Maturity: Review-Ready_

This file maps named tools, platforms, and standards anchors to the enterprise AI stack. It replaces the older bundled-list pattern with one-row-per-anchor comparisons so readers can compare the actual control points more directly.

## How To Use This File

- Layer placement matters because tool sprawl often hides architectural confusion.
- The same tool can play different roles depending on deployment posture.
- Use this file with the stack map rather than as a stand-alone catalog.

## Governance, Boundary, And Policy Layers

These anchors matter because the stack is not defensible if control, evidence, and boundary decisions are left implicit.

| Layer | Anchor | Entity type | Openness-policy tier | Why it belongs at this layer | Primary source |
| --- | --- | --- | --- | --- | --- |
| Governance / GRC | [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | Regulation | Not applicable | Shapes obligations, risk classes, and evidence expectations for many deployments | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) |
| Governance / GRC | [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Regulation | Not applicable | Defines privacy, processing, and data subject obligations that often shape system design | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj) |
| Governance / GRC | [ISO/IEC 42001](https://www.iso.org/standard/42001) | Management-system standard | Not applicable | Provides an AIMS-style operating anchor for AI governance | [ISO](https://www.iso.org/standard/42001) |
| Governance / GRC | [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | Framework | Not applicable | Useful public framing for risk functions, controls, and evidence | [NIST](https://www.nist.gov/itl/ai-risk-management-framework) |
| Data boundary / privacy | [Microsoft Purview](https://www.microsoft.com/en-us/security/business/microsoft-purview) | Data governance platform | Controlled Exception | Common control point for classification, retention, and data policy in Microsoft estates | [Purview](https://www.microsoft.com/en-us/security/business/microsoft-purview) |
| Data boundary / privacy | [BigID](https://bigid.com/) | Data governance platform | Controlled Exception | Common control point for discovery and policy over sensitive enterprise data | [BigID](https://bigid.com/) |
| Data boundary / privacy | [Immuta](https://www.immuta.com/) | Data access-control platform | Acceptable | Useful where fine-grained data access and policy enforcement matter | [Immuta](https://www.immuta.com/) |
| Data boundary / privacy | [Collibra](https://www.collibra.com/) | Data governance platform | Controlled Exception | Strong fit where cataloging, stewardship, and governance process already exist | [Collibra](https://www.collibra.com/) |

## Model, Runtime, And Control Layers

These anchors matter because they determine where capability comes from, who operates it, and how much of the control plane remains portable.

| Layer | Anchor | Entity type | Openness-policy tier | Why it belongs at this layer | Primary source |
| --- | --- | --- | --- | --- | --- |
| Model ecosystem | [OpenAI Models](https://platform.openai.com/docs/models) | Managed model platform | Controlled Exception | Representative API-first model catalog for buy-heavy stacks | [Docs](https://platform.openai.com/docs/models) |
| Model ecosystem | [IBM watsonx.ai](https://www.ibm.com/products/watsonx-ai) | Managed model and AI platform | Acceptable | Representative governed enterprise model platform with stronger portability posture than API-only stacks | [IBM](https://www.ibm.com/products/watsonx-ai) |
| Model ecosystem | [Mistral AI](https://docs.mistral.ai/) | Mixed model platform | Acceptable | Representative mixed API and open-weight posture | [Docs](https://docs.mistral.ai/) |
| Model ecosystem | [Hugging Face Model Hub](https://huggingface.co/models) | Model hub | Preferred | Representative discovery and distribution layer for open and mixed ecosystems | [Hub](https://huggingface.co/models) |
| Model ecosystem | [TensorFlow Hub](https://www.tensorflow.org/hub) | Model hub | Preferred | Representative reusable model layer for broader applied ML beyond LLM-centric catalogs | [TensorFlow](https://www.tensorflow.org/hub) |
| Hosting / inference | [vLLM](https://docs.vllm.ai/) | Open-source serving runtime | Preferred | Representative high-throughput self-hosted serving backbone | [Docs](https://docs.vllm.ai/) |
| Hosting / inference | [Hugging Face TGI](https://huggingface.co/docs/text-generation-inference/index) | Open-source serving runtime | Preferred | Representative portable open serving runtime | [Docs](https://huggingface.co/docs/text-generation-inference/index) |
| Hosting / inference | [MLServer](https://docs.seldon.ai/mlserver) | Open-source serving runtime | Preferred | Representative mixed predictive and generative model-serving layer for portable platform teams | [Docs](https://docs.seldon.ai/mlserver) |
| Hosting / inference | [Seldon Core 2](https://docs.seldon.ai/seldon-core-v2/) | Open-source serving platform | Preferred | Representative Kubernetes-native control plane for governed self-hosted inference | [Docs](https://docs.seldon.ai/seldon-core-v2/) |
| Hosting / inference | [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/) | Managed inference platform | Controlled Exception | Representative cloud-managed runtime choice | [Docs](https://docs.aws.amazon.com/bedrock/) |
| Hosting / inference | [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/) | Managed edge inference platform | Controlled Exception | Representative edge-hosted inference path | [Docs](https://developers.cloudflare.com/workers-ai/) |
| Gateway / policy | [LiteLLM](https://docs.litellm.ai/) | Gateway project | Preferred | Representative open gateway and provider-abstraction layer | [Docs](https://docs.litellm.ai/) |
| Gateway / policy | [Envoy AI Gateway](https://aigateway.envoyproxy.io/) | Gateway project | Preferred | Representative self-hosted AI-aware proxy path | [Docs](https://aigateway.envoyproxy.io/) |
| Gateway / policy | [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/) | Managed gateway capability | Controlled Exception | Representative managed AI routing and usage-control layer | [Docs](https://developers.cloudflare.com/ai-gateway/) |
| Gateway / policy | [Open Policy Agent](https://www.openpolicyagent.org/) | Policy engine | Preferred | Representative policy-as-code layer beside the gateway path | [OPA](https://www.openpolicyagent.org/) |

## Orchestration, Knowledge, And Assurance Layers

These anchors matter because they govern how systems act, what they know, and how evidence is created after deployment.

| Layer | Anchor | Entity type | Openness-policy tier | Why it belongs at this layer | Primary source |
| --- | --- | --- | --- | --- | --- |
| Orchestration / workflow | [LangGraph](https://langchain-ai.github.io/langgraph/) | Agent workflow framework | Acceptable | Representative graph-style orchestration for stateful agent flows | [Docs](https://langchain-ai.github.io/langgraph/) |
| Orchestration / workflow | [Temporal](https://temporal.io/) | Durable execution platform | Acceptable | Representative workflow-first alternative to agent-heavy designs | [Docs](https://docs.temporal.io/) |
| Orchestration / workflow | [Camunda](https://camunda.com/) | BPM platform | Acceptable | Representative process-governed orchestration with human approvals | [Docs](https://docs.camunda.io/) |
| Retrieval / memory | [LlamaIndex](https://www.llamaindex.ai/) | Retrieval framework | Acceptable | Representative document-centric retrieval composition layer | [Docs](https://docs.llamaindex.ai/) |
| Retrieval / memory | [Zep](https://help.getzep.com/overview) | Memory and context platform | Acceptable | Representative long-lived memory layer for assistant and agent systems that need explicit context management | [Docs](https://help.getzep.com/overview) |
| Retrieval / memory | [Qdrant](https://qdrant.tech/) | Vector database | Preferred | Representative portable vector store | [Docs](https://qdrant.tech/documentation/) |
| Retrieval / memory | [Neo4j](https://neo4j.com/) | Graph platform | Acceptable | Representative graph-oriented knowledge layer | [Neo4j](https://neo4j.com/) |
| Training / adaptation | [MLflow](https://mlflow.org/) | Lifecycle platform | Preferred | Representative open lifecycle and experiment layer | [MLflow](https://mlflow.org/) |
| Training / adaptation | [Dataiku](https://www.dataiku.com/product/machine-learning/) | Enterprise AI and ML platform | Acceptable | Representative governed platform for combining predictive, optimization, and generative workflows | [Dataiku](https://www.dataiku.com/product/machine-learning/) |
| Training / adaptation | [Hugging Face PEFT](https://huggingface.co/docs/peft/index) | Fine-tuning library | Preferred | Representative lightweight weight-adaptation layer | [Docs](https://huggingface.co/docs/peft/index) |
| Evaluation / QA | [promptfoo](https://www.promptfoo.dev/) | Evaluation project | Preferred | Representative CI-style regression layer | [Docs](https://www.promptfoo.dev/docs/intro) |
| Evaluation / QA | [Inspect AI](https://inspect.aisi.org.uk/) | Evaluation framework | Preferred | Representative scenario-based evaluation layer for high-stakes model and agent testing | [Inspect](https://inspect.aisi.org.uk/) |
| Evaluation / QA | [Ragas](https://docs.ragas.io/) | Evaluation project | Preferred | Representative retrieval-specific evaluation layer | [Docs](https://docs.ragas.io/) |
| Observability / monitoring | [OpenTelemetry](https://opentelemetry.io/) | Open standard / project | Preferred | Representative exportable telemetry foundation | [OTel](https://opentelemetry.io/) |
| Observability / monitoring | [SigNoz](https://signoz.io/docs/) | Observability platform | Preferred | Representative self-hostable observability surface on top of exportable telemetry | [Docs](https://signoz.io/docs/) |
| Observability / monitoring | [Langfuse](https://langfuse.com/) | Observability platform | Acceptable | Representative AI-specific tracing and evaluation telemetry layer | [Langfuse](https://langfuse.com/) |
| Security / abuse resistance | [Presidio](https://microsoft.github.io/presidio/) | Security project | Preferred | Representative redaction and PII-protection layer | [Docs](https://microsoft.github.io/presidio/) |
| Security / abuse resistance | [Google Cloud Model Armor](https://docs.cloud.google.com/model-armor/overview) | Managed protection service | Controlled Exception | Representative prompt and response filtering layer when managed runtime protection is required | [Docs](https://docs.cloud.google.com/model-armor/overview) |
| Security / abuse resistance | [Sigstore](https://www.sigstore.dev/) | Supply-chain security project | Preferred | Representative artifact-signing and integrity layer | [Sigstore](https://www.sigstore.dev/) |
| Provenance / supply chain | [C2PA](https://c2pa.org/) | Provenance standard | Acceptable | Representative content and artifact provenance anchor | [C2PA](https://c2pa.org/) |
| Application / integration | [ServiceNow Now Assist](https://www.servicenow.com/products/now-assist.html) | Product suite | Controlled Exception | Representative enterprise application layer where AI meets workflows | [ServiceNow](https://www.servicenow.com/products/now-assist.html) |

## Layer Selection Notes

| Layer | Common mistake | Better default |
| --- | --- | --- |
| Model ecosystem | Picking a model before defining data and review constraints | Start with `05`, `06`, and `04` |
| Hosting / inference | Treating managed and self-hosted as purely cost decisions | Include sovereignty, observability, and support burden |
| Gateway / policy | Assuming a gateway is only for provider swapping | Use it for shared identity, budget, and audit control |
| Orchestration | Reaching for agents when a workflow will do | Default to bounded workflows first |
| Retrieval / memory | Treating a vector store as the whole retrieval architecture | Design provenance, permissions, and refresh policy beside the store |
| Observability | Logging prompts without retention or access design | Structure traces and redact deliberately |
| Provenance / supply chain | Leaving authenticity and artifact metadata until after deployment | Treat provenance and bill-of-materials work as design-time concerns |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [3.3 Stack Reference Points](03-03-00-stack-reference-points.md).
