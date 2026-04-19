# 7.3.1 Tools And Platforms

_Page Type: Comparison Page | Maturity: Draft_

This file compares the product surfaces through which organizations discover, select, and access model families. It is intentionally broader than a short vendor API list because the model ecosystem now includes managed catalogs, open-weight programs, hub platforms, and cloud-native model gardens.

## How To Use This File

- Read the tables as comparison surfaces, not as universal rankings.
- Separate model availability from model governance: a broad catalog does not automatically provide strong portability or evidence quality.
- Check `08`, `09`, `12`, `17`, and `18` before treating model choice as a stand-alone decision.

## Managed Model Platforms And Catalogs

These products matter when the organization wants model access as a managed service and accepts a stronger control-plane dependency.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [OpenAI Models](https://platform.openai.com/docs/models) | Vendor platform | API-first model catalog | Controlled Exception | Proprietary | Vendor-hosted | Broad commercial assistant, multimodal, and agentic use | Strong runtime and policy dependence on vendor APIs | [Docs](https://platform.openai.com/docs/models) |
| [Anthropic Claude](https://docs.anthropic.com/) | Vendor platform | API-first model catalog | Controlled Exception | Proprietary | Vendor-hosted | Enterprise conversational and agentic use | High dependence on managed endpoints and vendor change cadence | [Docs](https://docs.anthropic.com/) |
| [Gemini API](https://ai.google.dev/gemini-api/docs/models) | Vendor platform | API-first model catalog | Controlled Exception | Proprietary | Vendor-hosted | Google ecosystem and multimodal use | Best fit often improves inside Google stack assumptions | [Docs](https://ai.google.dev/gemini-api/docs/models) |
| [Cohere](https://docs.cohere.com/) | Vendor platform | Language and retrieval-oriented model platform | Controlled Exception | Proprietary | Vendor-hosted | Enterprise text, embeddings, reranking, and retrieval use | API-first posture and provider dependence remain material | [Docs](https://docs.cohere.com/) |
| [Mistral AI](https://docs.mistral.ai/) | Vendor platform | Mixed API and open-weight ecosystem | Acceptable | Mixed | API plus self-hostable options for some models | Teams balancing managed access with more open posture | Mixed posture still requires model-by-model scrutiny | [Docs](https://docs.mistral.ai/) |
| [IBM watsonx.ai](https://www.ibm.com/products/watsonx-ai) | Managed platform | Enterprise AI studio and model access layer | Acceptable | Mixed | Managed, hybrid, or customer-controlled depending on deployment | Organizations that need governed AI and ML development across classical ML and generative systems | Broader platform scope can become a strategic workflow dependency | [IBM](https://www.ibm.com/products/watsonx-ai) |
| [Amazon Bedrock Model Catalog](https://docs.aws.amazon.com/bedrock/) | Managed platform capability | Cloud-native model marketplace | Controlled Exception | Proprietary service | AWS-managed | Multi-model access inside AWS estates | Model choice remains filtered through AWS contracts, interfaces, and surrounding services | [Docs](https://docs.aws.amazon.com/bedrock/) |
| [Vertex AI Model Garden](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-garden/self-deployed-models) | Managed platform capability | Cloud-native model catalog and deployment surface | Acceptable | Mixed | GCP-managed with self-deployed options | Organizations that want both managed and self-deployed model paths in GCP | Broader Google Cloud estate coupling remains material | [Docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-garden/self-deployed-models) |
| [Azure AI Foundry Model Catalog](https://learn.microsoft.com/azure/ai-foundry/) | Managed platform capability | Cloud-native model catalog and deployment surface | Controlled Exception | Mixed | Azure-managed | Microsoft-centered organizations needing catalog plus deployment workflows | Strong cloud-estate and control-plane coupling | [Docs](https://learn.microsoft.com/azure/ai-foundry/) |

## Open-Weight And Open-Model Programs

These programs matter when portability, local deployment, inspection, or sovereign operation are strategic concerns.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Meta Llama](https://www.llama.com/) | Model family ecosystem | Open-weight model family | Acceptable | Open weights | Self-hostable with third-party serving | Self-hosted assistants, experimentation, and sovereign builds | Not fully open source or open pipeline; license and support posture vary | [Meta](https://www.llama.com/) |
| [IBM Granite](https://www.ibm.com/granite) | Model family ecosystem | Enterprise-focused open model family | Preferred | Open source / open-weight mix | Self-hostable and managed options | Enterprise builds needing more portable model posture | Broader ecosystem support is smaller than top API vendors | [IBM](https://www.ibm.com/granite) |
| [AI2 OLMo](https://allenai.org/olmo) | Open model program | Open model family and research artifacts | Preferred | Open weights with research transparency | Self-hosted and research-oriented | Organizations wanting more inspectable model-development artifacts | Enterprise support ecosystem is smaller than mainstream platform vendors | [AI2](https://allenai.org/olmo) |
| [Microsoft Phi](https://azure.microsoft.com/en-us/products/phi) | Model family ecosystem | Small model family for local and managed use | Acceptable | Open source / open-weight mix | Self-hosted and managed options | Smaller-footprint deployments and edge-oriented reasoning workloads | Still benefits from Microsoft ecosystem tooling and hosting assumptions | [Microsoft](https://azure.microsoft.com/en-us/products/phi) |
| [Google Gemma](https://ai.google.dev/gemma) | Model family ecosystem | Open model family for developer and local deployment use | Acceptable | Open-weight ecosystem | Self-hosted and managed options | Local, edge, and single-accelerator deployments with Google model lineage | Requires model-by-model license and deployment review like other open-weight families | [Google](https://ai.google.dev/gemma) |
| [Qwen](https://qwenlm.github.io/about/) | Model family ecosystem | Open-weight and mixed-access model family | Acceptable | Mixed leaning open | Self-hosted and managed options | Multilingual and coding-oriented deployments that need broader model variety | Openness and access posture vary materially by model line and commercial endpoint | [Qwen](https://qwenlm.github.io/about/) |

## Model Hubs, Libraries, And Discovery Layers

These platforms matter because model choice is often mediated through a distribution and discovery layer before it reaches hosting or application teams.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Hugging Face Model Hub](https://huggingface.co/models) | Platform ecosystem | Model discovery and distribution | Preferred | Mixed ecosystem with strong open support | Platform, not runtime itself | Broad open and mixed ecosystem exploration | Quality, support, and licenses vary by publisher | [Hub](https://huggingface.co/models) |
| [TensorFlow Hub](https://www.tensorflow.org/hub) | Public model hub | Reusable model discovery for TensorFlow ecosystems | Preferred | Open repository and library | Platform, not runtime itself | Vision, speech, NLP, and on-device model reuse beyond LLM-heavy workflows | Strongest fit is inside TensorFlow-oriented stacks rather than general multi-framework estates | [TensorFlow](https://www.tensorflow.org/hub) |
| [Kaggle Models](https://www.kaggle.com/models) | Public model platform | Public model sharing and discovery | Acceptable | Mixed ecosystem | Hosted discovery platform | Public experimentation and accessible model discovery | Platform is a discovery surface, not a control plane for production governance | [Kaggle](https://www.kaggle.com/models) |
| [Ollama Library](https://ollama.com/library) | Local model ecosystem | Packaging and local runtime access | Preferred | Mixed model ecosystem on open runtime | Local and self-hosted | Prototyping, local testing, and small private deployments | Enterprise controls and fleet management need extra tooling | [Library](https://ollama.com/library) |
| [GitHub Models](https://github.com/marketplace/models) | Managed developer platform capability | Developer-facing model access and evaluation surface | Controlled Exception | Proprietary platform around mixed model access | Managed | Developer experimentation close to software delivery workflows | Strong coupling to GitHub's managed control plane and developer workflow assumptions | [GitHub](https://github.com/marketplace/models) |

## Selection Notes

| If the primary need is... | Default bias |
| --- | --- |
| Fast managed access with minimal platform work | Managed model platforms |
| Exit-sensitive or sovereign deployment options | Open-weight model programs |
| Broad discovery before procurement or hosting decisions | Model hubs and public catalogs |
| Smaller local or edge deployment footprints | Phi, Gemma, Llama, Qwen, and Ollama-friendly ecosystems |
| Enterprise retrieval and search workloads | Cohere, Granite, watsonx.ai, and open embedding or reranking ecosystems deserve extra attention |
| Broader applied AI and ML beyond frontier chat | Hugging Face Hub, TensorFlow Hub, IBM Granite, and cloud model gardens deserve extra attention |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [7.3 Reference Points](07-03-00-reference-points.md).
