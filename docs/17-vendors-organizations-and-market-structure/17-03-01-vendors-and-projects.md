# 17.3.1 Vendors And Projects

This subsection holds the chapter's named comparison material. Read it as a reference layer, not as a substitute for the chapter's conceptual and implementation sections.

This file compares the organizations that concentrate power, shape standards, or broaden optionality across the applied AI stack. The goal is not to list every brand in the market, but to make visible where capability concentration, hardware dependence, platform gravity, and open-ecosystem counterweights actually sit.

## How To Use This File

- Separate the organization from the products it influences.
- Concentration and stewardship posture often matter as much as product features.
- Use this file together with sourcing, hosting, and ecosystem chapters, not in isolation.

## Frontier Model And Platform Concentration Points

These actors matter when organizations are buying managed capability and inheriting roadmaps, policy shifts, and commercial leverage from a small number of providers.

| Organization / project | Entity type | Stack role | Stewardship or business model | Openness posture | Dependence / concentration note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [OpenAI](https://openai.com/) | Vendor | Frontier model and platform provider | Commercial platform provider | Proprietary | High-capability concentration and strong API dependence | [OpenAI](https://openai.com/) |
| [Anthropic](https://www.anthropic.com/) | Vendor | Frontier model provider | Commercial platform provider | Proprietary | Similar concentration pattern for enterprise assistant use | [Anthropic](https://www.anthropic.com/) |
| [Google DeepMind](https://deepmind.google/) | Vendor / research organization | Frontier model and research actor | Commercial research and platform actor | Proprietary | Strong pull into Google cloud and ecosystem choices | [Google DeepMind](https://deepmind.google/) |
| [Microsoft Azure AI](https://azure.microsoft.com/products/ai-services/) | Vendor platform | Cloud-hosted model and AI platform layer | Commercial cloud platform | Proprietary | Platform plus contract concentration for Microsoft estates | [Microsoft](https://azure.microsoft.com/products/ai-services/) |
| [Amazon Bedrock](https://aws.amazon.com/bedrock/) | Vendor platform | Managed model marketplace and runtime | Commercial cloud platform | Proprietary | Cloud-estate dependence can become structural | [AWS](https://aws.amazon.com/bedrock/) |
| [Databricks Mosaic AI](https://www.databricks.com/product/mosaic-ai) | Vendor platform | Data-plus-model platform actor | Commercial platform provider | Proprietary / mixed ecosystem | Data estate, model tooling, and workflow dependence can compound | [Databricks](https://www.databricks.com/product/mosaic-ai) |
| [Cohere](https://cohere.com/) | Vendor | Enterprise language-model actor | Commercial platform provider | Proprietary | Enterprise focus does not remove provider concentration risk | [Cohere](https://cohere.com/) |
| [Mistral AI](https://mistral.ai/) | Vendor | Frontier and open-weight model provider | Commercial vendor | Mixed | Offers more optionality than API-only vendors, but still centralizes some model dependence | [Mistral](https://mistral.ai/) |
| [IBM watsonx.ai](https://www.ibm.com/products/watsonx-ai) | Vendor platform | Enterprise model, governance, and runtime platform | Commercial platform provider | Mixed | Stronger governance posture than API-only providers, but still concentrates platform control | [IBM](https://www.ibm.com/products/watsonx-ai) |

## Infrastructure And Hardware Control Points

These actors matter because they shape who can actually deploy, optimize, and economically scale AI systems.

| Organization / project | Entity type | Stack role | Stewardship or business model | Openness posture | Dependence / concentration note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [NVIDIA](https://www.nvidia.com/en-us/ai-data-science/) | Infrastructure and ecosystem actor | Hardware, model-serving, and optimization control point | Commercial infrastructure vendor | Mixed | Hardware dependence can reinforce runtime and tooling lock-in | [NVIDIA](https://www.nvidia.com/en-us/ai-data-science/) |
| [AMD](https://www.amd.com/en/solutions/ai.html) | Infrastructure vendor | Alternative accelerator and inference hardware actor | Commercial infrastructure vendor | Mixed | Important counterweight to single-vendor GPU concentration, but ecosystem depth still differs | [AMD](https://www.amd.com/en/solutions/ai.html) |
| [Intel](https://www.intel.com/content/www/us/en/artificial-intelligence/overview.html) | Infrastructure vendor | CPU, accelerator, and edge AI control point | Commercial infrastructure vendor | Mixed | Significant for edge, enterprise CPU estates, and some inferencing paths | [Intel](https://www.intel.com/content/www/us/en/artificial-intelligence/overview.html) |
| [Groq](https://console.groq.com/docs/overview) | Infrastructure and inference actor | Low-latency inference platform and accelerator control point | Commercial infrastructure vendor | Proprietary platform around mixed model access | Performance differentiation can become a distinct dependence layer even when model choices look portable | [Docs](https://console.groq.com/docs/overview) |
| [Cloudflare](https://www.cloudflare.com/developer-platform/products/workers-ai/) | Network and edge platform actor | Edge inference, routing, and gateway control point | Commercial platform provider | Proprietary platform around open-model access | Edge distribution can become a new concentration layer when adopted broadly | [Cloudflare](https://www.cloudflare.com/developer-platform/products/workers-ai/) |
| [Hugging Face](https://huggingface.co/) | Platform / ecosystem actor | Model, dataset, and tooling hub | Platform plus ecosystem steward | Mixed with strong open support | Broadest ecosystem hub, but maturity varies by artifact and publisher | [Hugging Face](https://huggingface.co/) |

## Open-Weight Programs, Foundations, And Public Counterweights

These actors matter because they broaden deployment options or create shared measurement and governance surfaces that are not controlled by one vendor alone.

| Organization / project | Entity type | Stack role | Stewardship or business model | Openness posture | Dependence / concentration note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [Meta AI / Llama](https://www.llama.com/) | Research and ecosystem actor | Open-weight model family | Research-led ecosystem strategy | Open weights | Strong deployment freedom without full-pipeline openness | [Meta](https://www.llama.com/) |
| [AI2 OLMo](https://allenai.org/olmo) | Research program | Open model artifacts and methods | Nonprofit research organization | Open and research-oriented | Lower concentration risk, but lighter enterprise support ecosystem | [AI2](https://allenai.org/olmo) |
| [Qwen Team](https://qwenlm.github.io/about/) | Model program | Open-weight and mixed-access model family | Commercial research and product program | Mixed leaning open | Broader model access than API-only stacks, but openness still varies by model line | [Qwen](https://qwenlm.github.io/about/) |
| [LF AI & Data](https://lfaidata.foundation/) | Foundation | Open ecosystem stewardship | Nonprofit foundation | Open ecosystem | Low concentration risk directly, but project maturity varies by community | [LF AI & Data](https://lfaidata.foundation/) |
| [PyTorch Foundation](https://pytorch.org/foundation/) | Foundation | Open framework and ecosystem stewardship | Nonprofit foundation | Open ecosystem | Critical counterweight to proprietary framework concentration, though deployed stacks still vary widely | [PyTorch](https://pytorch.org/foundation/) |
| [MLCommons](https://mlcommons.org/benchmarks/) | Benchmark consortium | Benchmark and measurement governance | Consortium | Open benchmark ecosystem | Critical counterweight to vendor-authored benchmark narratives | [MLCommons](https://mlcommons.org/benchmarks/) |
| [OpenSSF AI/ML Working Group](https://openssf.org/blog/2025/04/04/launch-of-model-signing-v1-0-openssf-ai-ml-working-group-secures-the-machine-learning-supply-chain/) | Community initiative | Model supply-chain security stewardship | Open security foundation working group | Open community effort | Important for shared assurance layers beyond any one vendor | [OpenSSF](https://openssf.org/blog/2025/04/04/launch-of-model-signing-v1-0-openssf-ai-ml-working-group-secures-the-machine-learning-supply-chain/) |
| [C2PA](https://c2pa.org/) | Specification community | Provenance and authenticity standards | Multi-stakeholder technical community | Open specification | Important for public-facing content systems and content-trust ecosystems | [C2PA](https://c2pa.org/) |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [17.3 Reference Points](17-03-00-reference-points.md).
