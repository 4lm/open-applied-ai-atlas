# 8.3.2 Reference Stack Solutions

This subsection holds the chapter's named comparison material. Read it as a reference layer, not as a substitute for the chapter's conceptual and implementation sections.

This file turns hosting patterns into reusable solution shapes. The summary table compares the patterns, and the component table breaks bundled tool lists into one anchor per row so readers can compare realistic runtime compositions more directly.

## How To Use This File

- These shapes are reusable starting points, not drop-in blueprints.
- A stronger openness tier does not automatically mean lower operating burden.
- Treat the runtime, optimization layer, and surrounding control plane as separate sourcing decisions.

## Hosting Solution Shapes

| Solution shape | Typical composition | Openness-policy tier | Strongest fit | Main trade-off |
| --- | --- | --- | --- | --- |
| API-first inference | Vendor API plus basic app integration | Controlled Exception | Fast experimentation and low-ops adoption | Highest provider dependence |
| Dedicated managed endpoints | Managed endpoint plus customer-controlled app layer | Acceptable | Moderate sovereignty needs with limited platform staffing | Control improves, but managed dependence remains |
| Cloud-estate native inference | Cloud-managed runtime plus cloud IAM, logging, and networking | Controlled Exception | Organizations standardizing heavily on one cloud | Strong convenience, high cloud lock-in |
| Managed open-model inference | Managed platform around open-weight ecosystems | Acceptable | Teams wanting faster open-model adoption without self-hosting immediately | Better portability story than closed APIs, but still provider-coupled |
| Self-hosted open-weight serving | Open-weight models plus self-managed runtime and telemetry | Preferred | Private workloads and exit-sensitive programs | Higher ops burden and model-ops complexity |
| GPU-optimized enterprise serving | Self-hosted serving with hardware-specific optimization | Acceptable | Large-volume inference on well-understood hardware | Best performance often means stronger hardware dependence |
| Edge or local inference | Smaller or optimized models running close to the workload | Preferred | Offline, workstation, or device-adjacent deployments | Capability ceiling may be lower than centralized GPU-serving patterns |
| Sovereign private inference | Self-hosted stack with offline-capable operations and exportable telemetry | Strategic Open | High-control or regulated environments | Highest operating and support burden |

## Representative Component Anchors

The table below splits comparable references into separate rows so each anchor can be evaluated on its own merits.

| Pattern | Layer | Anchor | Why it belongs in the pattern | Primary source |
| --- | --- | --- | --- | --- |
| API-first inference | Model access | [OpenAI Models](https://platform.openai.com/docs/models) | Fastest managed model access for teams prioritizing speed over hosting control | [Docs](https://platform.openai.com/docs/models) |
| API-first inference | Model access | [Anthropic Claude](https://docs.anthropic.com/) | Similar API-first posture for conversational and agentic workloads | [Docs](https://docs.anthropic.com/) |
| API-first inference | Basic telemetry | [OpenTelemetry](https://opentelemetry.io/) | Even the thinnest managed pattern still benefits from exportable app telemetry | [OTel](https://opentelemetry.io/) |
| Dedicated managed endpoints | Endpoint runtime | [Hugging Face Inference Endpoints](https://huggingface.co/docs/inference-endpoints/index) | Dedicated managed endpoints with more model choice than closed API-only stacks | [Docs](https://huggingface.co/docs/inference-endpoints/index) |
| Dedicated managed endpoints | Endpoint runtime | [Baseten](https://docs.baseten.co/overview) | Managed deployment surface for model APIs and surrounding app logic | [Docs](https://docs.baseten.co/overview) |
| Dedicated managed endpoints | Observability | [Langfuse](https://langfuse.com/) | Exportable request and trace visibility around managed endpoints | [Langfuse](https://langfuse.com/) |
| Cloud-estate native inference | Cloud runtime | [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/) | Managed model access aligned to AWS estates | [Docs](https://docs.aws.amazon.com/bedrock/) |
| Cloud-estate native inference | Cloud runtime | [Google Vertex AI](https://cloud.google.com/vertex-ai/docs) | Managed model hosting and deployment inside GCP | [Docs](https://cloud.google.com/vertex-ai/docs) |
| Cloud-estate native inference | Cloud runtime | [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/) | Managed hosting and model platform for Microsoft-centered estates | [Docs](https://learn.microsoft.com/azure/ai-foundry/) |
| Managed open-model inference | Managed provider | [Together AI](https://docs.together.ai/) | Faster open-model adoption without immediate self-hosting | [Docs](https://docs.together.ai/) |
| Managed open-model inference | Managed provider | [Fireworks AI](https://docs.fireworks.ai/) | Performance-oriented managed inference for mixed open-model portfolios | [Docs](https://docs.fireworks.ai/) |
| Managed open-model inference | Managed provider | [Groq](https://console.groq.com/docs/overview) | Distinctive fit where latency-sensitive inference matters more than full infrastructure control | [Groq](https://console.groq.com/docs/overview) |
| Self-hosted open-weight serving | Serving runtime | [vLLM](https://docs.vllm.ai/) | Common high-throughput open serving backbone | [Docs](https://docs.vllm.ai/) |
| Self-hosted open-weight serving | Serving runtime | [Hugging Face TGI](https://huggingface.co/docs/text-generation-inference/index) | Common open serving backbone for self-managed text generation | [Docs](https://huggingface.co/docs/text-generation-inference/index) |
| Self-hosted open-weight serving | Serving platform | [KServe](https://kserve.github.io/kserve/) | Kubernetes-oriented serving for platformized open inference | [KServe](https://kserve.github.io/kserve/) |
| Self-hosted open-weight serving | Serving platform | [MLServer](https://docs.seldon.ai/mlserver) | Useful for mixed predictive and generative serving behind a common API surface | [Docs](https://docs.seldon.ai/mlserver) |
| Self-hosted open-weight serving | Telemetry | [OpenTelemetry](https://opentelemetry.io/) | Exportable traces are central to portable self-hosted operations | [OTel](https://opentelemetry.io/) |
| GPU-optimized enterprise serving | Optimization layer | [TensorRT-LLM](https://docs.nvidia.com/tensorrt-llm/index.html) | Hardware-optimized serving for NVIDIA-heavy estates | [Docs](https://docs.nvidia.com/tensorrt-llm/index.html) |
| GPU-optimized enterprise serving | Serving platform | [NVIDIA Triton Inference Server](https://developer.nvidia.com/triton-inference-server) | Multi-framework serving for large GPU estates | [NVIDIA](https://developer.nvidia.com/triton-inference-server) |
| GPU-optimized enterprise serving | Packaged deployment | [NVIDIA NIM](https://build.nvidia.com/) | Packaged deployment path for NVIDIA-standardized operations | [NVIDIA](https://build.nvidia.com/) |
| Edge or local inference | Local runtime | [Ollama](https://ollama.com/) | Practical local serving for developer and workstation use | [Docs](https://docs.ollama.com/) |
| Edge or local inference | Local runtime | [llama.cpp](https://github.com/ggml-org/llama.cpp) | CPU-friendly and lightweight local inference | [Repo](https://github.com/ggml-org/llama.cpp) |
| Edge or local inference | Cross-hardware runtime | [ONNX Runtime GenAI](https://onnxruntime.ai/docs/genai/) | Edge and device-adjacent inference with broader hardware support | [Docs](https://onnxruntime.ai/docs/genai/) |
| Edge or local inference | Serving platform | [OpenVINO Model Server](https://docs.openvino.ai/2025/openvino-workflow/model-server/ovms_what_is_openvino_model_server.html) | Useful when CPU-heavy, Intel-oriented, or edge-serving patterns matter | [OpenVINO](https://docs.openvino.ai/2025/openvino-workflow/model-server/ovms_what_is_openvino_model_server.html) |
| Sovereign private inference | Serving runtime | [vLLM](https://docs.vllm.ai/) | Portable self-hosted serving backbone for high-control environments | [Docs](https://docs.vllm.ai/) |
| Sovereign private inference | Serving runtime | [Hugging Face TGI](https://huggingface.co/docs/text-generation-inference/index) | Portable alternative serving backbone for self-hosted deployments | [Docs](https://huggingface.co/docs/text-generation-inference/index) |
| Sovereign private inference | Control plane | [Seldon Core 2](https://docs.seldon.ai/seldon-core-v2/) | Useful where self-hosted serving needs a stronger Kubernetes-native operating layer | [Docs](https://docs.seldon.ai/seldon-core-v2/) |
| Sovereign private inference | Policy and auditability | [Open Policy Agent](https://www.openpolicyagent.org/) | Policy-as-code around access and runtime control | [OPA](https://www.openpolicyagent.org/) |
| Sovereign private inference | Telemetry | [OpenTelemetry](https://opentelemetry.io/) | Exportable telemetry is critical to evidence and exit posture | [OTel](https://opentelemetry.io/) |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [8.3 Reference Points](08-03-00-reference-points.md).
