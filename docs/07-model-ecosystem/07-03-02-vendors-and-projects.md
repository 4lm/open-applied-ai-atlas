# 7.3.2 Vendors And Projects

This subsection holds the chapter's named comparison material. Read it as a reference layer, not as a substitute for the chapter's conceptual and implementation sections.

This file separates organizations and stewardship models from the tools and catalogs they influence. That distinction matters because concentration, governance posture, and ecosystem stewardship shape long-term model strategy as much as benchmark results do.

## How To Use This File

- Separate the organization from the products it influences.
- Concentration and stewardship posture often matter as much as model features.
- Use this file together with sourcing, hosting, and market-structure chapters, not in isolation.

## Frontier And Managed-Platform Actors

These actors matter most when the organization is buying API access, managed safety posture, and vendor roadmaps rather than operating models directly.

| Organization / project | Entity type | Stack role | Stewardship or business model | Openness posture | Dependence / concentration note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [OpenAI](https://openai.com/) | Vendor | Frontier model and platform provider | Commercial platform provider | Proprietary | High-capability concentration and strong API dependence | [OpenAI](https://openai.com/) |
| [Anthropic](https://www.anthropic.com/) | Vendor | Frontier model provider | Commercial platform provider | Proprietary | Similar concentration pattern for enterprise assistant use | [Anthropic](https://www.anthropic.com/) |
| [Google DeepMind](https://deepmind.google/) | Vendor / research organization | Frontier model and research actor | Commercial research and platform actor | Proprietary | Deep integration advantages for Google-centered estates | [Google DeepMind](https://deepmind.google/) |
| [Microsoft Azure AI](https://azure.microsoft.com/products/ai-services/) | Vendor platform | Managed AI access and hosting ecosystem | Commercial cloud platform | Proprietary | Can create control-plane and cloud-estate concentration | [Microsoft](https://azure.microsoft.com/products/ai-services/) |
| [Amazon Bedrock](https://aws.amazon.com/bedrock/) | Vendor platform | Managed model marketplace and runtime | Commercial cloud platform | Proprietary | Layered dependence on AWS contracts, runtime, and surrounding services | [AWS](https://aws.amazon.com/bedrock/) |
| [Cohere](https://cohere.com/) | Vendor | Enterprise language and retrieval models | Commercial platform provider | Proprietary | Strong fit for enterprise NLP and retrieval workloads, but still API dependent | [Cohere](https://cohere.com/) |
| [Mistral AI](https://mistral.ai/) | Vendor | Frontier and open-weight model provider | Commercial vendor | Mixed | More optionality than API-only vendors, but still model-specific and roadmap-sensitive | [Mistral](https://mistral.ai/) |
| [IBM watsonx.ai](https://www.ibm.com/products/watsonx-ai) | Vendor platform | Governed AI studio, model access, and deployment layer | Commercial enterprise platform | Mixed | Broader enterprise control story than pure API vendors, but still a consequential platform dependency | [IBM](https://www.ibm.com/products/watsonx-ai) |

## Open-Weight Programs And Ecosystem Stewards

These actors matter when the organization cares about deployment freedom, inspectability, and a wider option set beyond closed managed APIs.

| Organization / project | Entity type | Stack role | Stewardship or business model | Openness posture | Dependence / concentration note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [Meta AI / Llama](https://www.llama.com/) | Ecosystem actor | Open-weight model family | Research-led ecosystem strategy | Open weights | Strong deployment freedom, weaker full-pipeline openness | [Meta](https://www.llama.com/) |
| [IBM Granite](https://www.ibm.com/granite) | Vendor / ecosystem actor | Enterprise-oriented open model family | Commercial vendor with open model strategy | Mixed leaning open | Stronger portability posture than typical proprietary model vendors, with smaller ecosystem concentration | [IBM](https://www.ibm.com/granite) |
| [AI2 OLMo](https://allenai.org/olmo) | Research program | Open model and artifact program | Nonprofit research organization | Open and research-oriented | Strong transparency posture, lighter commercial support ecosystem | [AI2](https://allenai.org/olmo) |
| [Microsoft Phi](https://azure.microsoft.com/en-us/products/phi) | Vendor / model program | Small open model family | Commercial vendor with open model distribution | Mixed leaning open | Smaller models improve deployment flexibility but still benefit from Microsoft ecosystem gravity | [Microsoft](https://azure.microsoft.com/en-us/products/phi) |
| [Google Gemma](https://ai.google.dev/gemma) | Model program | Open model family | Commercial vendor with open model strategy | Open-weight ecosystem | Useful counterweight to cloud-only model consumption, but not full-pipeline openness | [Google](https://ai.google.dev/gemma) |
| [Qwen Team](https://qwenlm.github.io/about/) | Model program | Open-weight and mixed-access model family | Commercial research and product program | Mixed leaning open | Provides more deployment choice than pure API vendors, but openness still varies by model line | [Qwen](https://qwenlm.github.io/about/) |
| [Hugging Face](https://huggingface.co/) | Platform / ecosystem actor | Model, dataset, and tooling hub | Platform plus ecosystem steward | Mixed with strong open ecosystem support | Broadest discovery layer, but support and maturity vary by asset | [Hugging Face](https://huggingface.co/) |
| [TensorFlow Hub](https://www.tensorflow.org/hub) | Public model repository | Reusable model distribution for TensorFlow ecosystems | Open community repository | Open | Important counterweight to LLM-only discovery surfaces, but narrower than general multi-framework hubs | [TensorFlow](https://www.tensorflow.org/hub) |

## Foundations, Benchmarks, And Public-Interest Counterweights

These organizations matter because they provide ecosystem governance, measurement, or open stewardship that partly offsets pure vendor narrative control.

| Organization / project | Entity type | Stack role | Stewardship or business model | Openness posture | Dependence / concentration note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [LF AI & Data](https://lfaidata.foundation/) | Foundation | Open-source AI and data project stewardship | Nonprofit foundation | Open ecosystem | Lower direct concentration risk, but project maturity varies | [LF AI & Data](https://lfaidata.foundation/) |
| [PyTorch Foundation](https://pytorch.org/foundation/) | Foundation | Neutral stewardship for major open AI infrastructure projects | Foundation under the Linux Foundation | Open ecosystem | Important ecosystem counterweight around PyTorch, vLLM, DeepSpeed, and Ray rather than a single vendor-controlled stack | [PyTorch Foundation](https://pytorch.org/foundation/) |
| [MLCommons](https://mlcommons.org/benchmarks/) | Benchmark consortium | Benchmark and measurement governance | Consortium | Open benchmark ecosystem | Important counterweight to purely vendor-authored performance claims | [MLCommons](https://mlcommons.org/benchmarks/) |
| [Stanford CRFM](https://crfm.stanford.edu/) | Research center | Public model analysis and benchmark framing | Academic center | Open research | Influences evaluation framing more than deployment, but strongly shapes ecosystem narrative | [CRFM](https://crfm.stanford.edu/) |
| [EleutherAI](https://www.eleuther.ai/) | Research collective | Open model and evaluation community stewardship | Research collective / nonprofit ecosystem | Open research | Lower commercial concentration, but lighter enterprise support posture | [EleutherAI](https://www.eleuther.ai/) |
| [C2PA](https://c2pa.org/) | Specification community | Provenance and authenticity standards relevant to model outputs and assets | Multi-stakeholder technical community | Open specification | Important for public-facing content systems and content-trust ecosystems | [C2PA](https://c2pa.org/) |
| [OpenSSF AI/ML Working Group](https://openssf.org/blog/2025/04/04/launch-of-model-signing-v1-0-openssf-ai-ml-working-group-secures-the-machine-learning-supply-chain/) | Community initiative | AI model supply-chain security stewardship | Open security foundation working group | Open community effort | Important for long-term model signing and software-style supply-chain assurance | [OpenSSF](https://openssf.org/blog/2025/04/04/launch-of-model-signing-v1-0-openssf-ai-ml-working-group-secures-the-machine-learning-supply-chain/) |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [7.3 Reference Points](07-03-00-reference-points.md).
