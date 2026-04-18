# 19.3.1 Tooling By Layer

_Page Type: Comparison Page | Maturity: Review-Ready_

This file maps named tooling to the architecture positions that most often decide whether a reference architecture stays portable, governable, and supportable. It is intentionally architecture-oriented rather than exhaustive.

## How To Use This File

- Layer placement matters because tool sprawl often hides architectural confusion.
- The same tool can play different roles depending on deployment posture.
- Use this file with the chapter's architecture patterns rather than as a stand-alone catalog.

## Governance And Architecture Policy Anchors

| Layer | Anchor | Best-fit architecture pattern | Why it matters | Primary source |
| --- | --- | --- | --- | --- |
| Governance and architecture policy | [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | All serious production patterns | Architecture selection is not defensible without regulatory and evidence anchors | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) |
| Governance and architecture policy | [ISO/IEC 42001](https://www.iso.org/standard/42001) | All serious production patterns | Useful management-system anchor for operating architectures at organizational scale | [ISO](https://www.iso.org/standard/42001) |
| Governance and architecture policy | [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | All serious production patterns | Public risk framing that can travel across architectures | [NIST](https://www.nist.gov/itl/ai-risk-management-framework) |
| Governance and architecture policy | [COBIT](https://www.isaca.org/resources/cobit) | Large enterprise and regulated patterns | Useful where architecture governance is tied to broader enterprise control models | [ISACA](https://www.isaca.org/resources/cobit) |

## Core Runtime And Control-Plane Anchors

| Layer | Anchor | Best-fit architecture pattern | Why it matters | Primary source |
| --- | --- | --- | --- | --- |
| Managed model access | [OpenAI Models](https://platform.openai.com/docs/models) | SaaS-first, gateway-centric | Fastest path to managed capability when control needs are moderate | [Docs](https://platform.openai.com/docs/models) |
| Managed model access | [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/) | SaaS-first, cloud-estate native | Common managed runtime anchor in AWS-centered architectures | [Docs](https://docs.aws.amazon.com/bedrock/) |
| Managed model access | [IBM watsonx.ai](https://www.ibm.com/products/watsonx-ai) | Managed suite, hybrid predictive plus generative | Useful when model access, governance, and enterprise runtime controls need to travel together | [IBM](https://www.ibm.com/products/watsonx-ai) |
| Self-hosted serving | [vLLM](https://docs.vllm.ai/) | Open infrastructure, sovereign private | Determines whether private or sovereign architectures are viable | [Docs](https://docs.vllm.ai/) |
| Self-hosted serving | [KServe](https://kserve.github.io/kserve/) | Open infrastructure, sovereign private | Important for Kubernetes-standardized architectures | [KServe](https://kserve.github.io/kserve/) |
| Self-hosted serving | [MLServer](https://docs.seldon.ai/mlserver) | Open infrastructure, hybrid predictive plus generative | Useful when one serving layer should span classical ML and LLM workloads | [Docs](https://docs.seldon.ai/mlserver) |
| Self-hosted serving | [Seldon Core 2](https://docs.seldon.ai/seldon-core-v2/) | Sovereign private, open infrastructure | Useful where platform teams need a standardized self-hosted serving control plane | [Docs](https://docs.seldon.ai/seldon-core-v2/) |
| Self-hosted serving | [Ollama](https://ollama.com/) | Edge-capable local platform | Useful for local and workstation-heavy reference designs | [Docs](https://docs.ollama.com/) |
| Gateway / control plane | [LiteLLM](https://docs.litellm.ai/) | Gateway-centric, hybrid, agentic workflow | Common open control-plane anchor for routing and abstraction | [Docs](https://docs.litellm.ai/) |
| Gateway / control plane | [Envoy AI Gateway](https://aigateway.envoyproxy.io/) | Open infrastructure, gateway-centric | Useful where self-hosted gateway patterns are preferred | [Docs](https://aigateway.envoyproxy.io/) |
| Gateway / control plane | [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/) | Gateway-centric, edge-aware | Useful when managed shared routing is acceptable | [Docs](https://developers.cloudflare.com/ai-gateway/) |
| Retrieval / memory | [Qdrant](https://qdrant.tech/) | Controlled enterprise, sovereign private | Portable retrieval substrate with clear self-hosted path | [Docs](https://qdrant.tech/documentation/) |
| Retrieval / memory | [pgvector](https://github.com/pgvector/pgvector) | Open infrastructure, simpler enterprise stacks | Keeps retrieval inside existing Postgres estates | [Repo](https://github.com/pgvector/pgvector) |
| Retrieval / memory | [Zep](https://help.getzep.com/overview) | Agentic workflow, controlled enterprise | Useful where architectures need explicit long-lived memory rather than only document retrieval | [Docs](https://help.getzep.com/overview) |
| Retrieval / memory | [Neo4j](https://neo4j.com/) | Knowledge-graph-heavy reference designs | Shapes architectures that need relationship-aware knowledge layers | [Neo4j](https://neo4j.com/) |

## Workflow, Evidence, And Security Anchors

| Layer | Anchor | Best-fit architecture pattern | Why it matters | Primary source |
| --- | --- | --- | --- | --- |
| Orchestration | [LangGraph](https://langchain-ai.github.io/langgraph/) | Agentic workflow, controlled enterprise | Governs stateful tool use and multi-step execution | [Docs](https://langchain-ai.github.io/langgraph/) |
| Orchestration | [Temporal](https://temporal.io/) | Agentic workflow, hybrid stack | Governs durable execution, retries, and resumability | [Docs](https://docs.temporal.io/) |
| Orchestration | [Camunda](https://camunda.com/) | Human-governed enterprise architectures | Useful when approvals and BPM are first-class architectural constraints | [Docs](https://docs.camunda.io/) |
| QA and observability | [OpenTelemetry](https://opentelemetry.io/) | All serious production patterns | Provides exportable traces and metrics across architectures | [OTel](https://opentelemetry.io/) |
| QA and observability | [Inspect AI](https://inspect.aisi.org.uk/) | Gateway-centric, agentic workflow, hybrid predictive plus generative | Makes scenario-based evaluation explicit in architecture instead of leaving it to ad hoc testing | [Inspect](https://inspect.aisi.org.uk/) |
| QA and observability | [SigNoz](https://signoz.io/docs/) | Open infrastructure, sovereign private, enterprise gateway | Useful when reference architectures need self-hostable observability on top of exportable telemetry | [Docs](https://signoz.io/docs/) |
| QA and observability | [Langfuse](https://langfuse.com/) | Gateway-centric, agentic workflow | Provides AI-specific trace visibility and evaluation signals | [Langfuse](https://langfuse.com/) |
| QA and observability | [promptfoo](https://www.promptfoo.dev/) | All architectures that need release gates | Provides portable regression evidence in CI-style workflows | [Docs](https://www.promptfoo.dev/docs/intro) |
| Security and provenance | [Open Policy Agent](https://www.openpolicyagent.org/) | Gateway-centric, sovereign private, public-facing systems | Makes policy enforcement explicit in architecture, not only in prose | [OPA](https://www.openpolicyagent.org/) |
| Security and provenance | [Google Cloud Model Armor](https://docs.cloud.google.com/model-armor/overview) | SaaS-first, managed suite, gateway-centric | Makes managed prompt and response filtering explicit where runtime protection is required | [Docs](https://docs.cloud.google.com/model-armor/overview) |
| Security and provenance | [Presidio](https://microsoft.github.io/presidio/) | Data-sensitive enterprise architectures | Makes redaction and PII handling explicit in the data path | [Docs](https://microsoft.github.io/presidio/) |
| Security and provenance | [ModelScan](https://modelscan.readthedocs.io/) | Open infrastructure, sovereign private | Makes model artifact scanning explicit in the supply-chain path for self-hosted architectures | [Docs](https://modelscan.readthedocs.io/) |
| Security and provenance | [Sigstore](https://www.sigstore.dev/) | Sovereign private, public-facing media, regulated stacks | Makes artifact integrity and signing explicit | [Sigstore](https://www.sigstore.dev/) |
| Security and provenance | [C2PA](https://c2pa.org/) | Public-facing content architectures | Makes provenance explicit for synthetic media and signed content chains | [C2PA](https://c2pa.org/) |

## Pattern Selection Notes

| Pattern | Tooling bias |
| --- | --- |
| SaaS-first assistant | Managed model access plus lightweight telemetry |
| Gateway-centric enterprise platform | Shared gateway, retrieval, evaluation, observability, and policy become core |
| Open infrastructure stack | Self-hosted serving, portable data stores, and exportable telemetry dominate |
| Sovereign private platform | Preference for self-managed serving, strong policy control, provenance, and auditable evidence chains |
| Public-facing content system | Provenance, content authenticity, abuse controls, and incident evidence become first-class design concerns |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [19.3 Reference Points](19-03-00-reference-points.md).
