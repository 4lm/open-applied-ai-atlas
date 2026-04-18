# 8.3.1 Tools And Platforms

This subsection holds the chapter's named comparison material. Read it as a reference layer, not as a substitute for the chapter's conceptual and implementation sections.

This file compares the main runtime choices for serving models. It covers self-hosted runtimes, Kubernetes-oriented serving layers, local and edge stacks, and managed inference services because hosting posture is where portability, sovereignty, performance, and support burden become concrete.

## How To Use This File

- Read the tables as comparison surfaces, not as universal rankings.
- Treat serving software, optimization layers, and managed inference platforms as different control choices even when they can expose similar APIs.
- Re-check `07`, `09`, `14`, `15`, and `18` before choosing a runtime purely on latency or price.

## Open And Self-Hosted Serving Runtimes

These projects matter when the organization wants direct runtime control, private deployments, or a clearer exit path from vendor-hosted inference.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [vLLM](https://docs.vllm.ai/) | Open-source project | High-throughput serving | Preferred | Fully open source | Self-hosted | Private and high-throughput open-weight inference | Requires platform engineering, GPU operations, and surrounding controls | [Docs](https://docs.vllm.ai/) |
| [Hugging Face Text Generation Inference](https://huggingface.co/docs/text-generation-inference/index) | Open-source project | LLM serving runtime | Preferred | Fully open source | Self-hosted | Self-managed text-generation serving | Needs surrounding observability, deployment discipline, and lifecycle ownership | [Docs](https://huggingface.co/docs/text-generation-inference/index) |
| [SGLang](https://docs.sglang.ai/) | Open-source project | Structured generation and serving runtime | Preferred | Open source | Self-hosted | High-performance and structured serving for advanced open-model stacks | Requires hands-on tuning and platform expertise | [Docs](https://docs.sglang.ai/) |
| [TensorRT-LLM](https://docs.nvidia.com/tensorrt-llm/index.html) | Open-source project / optimization stack | GPU-optimized serving | Acceptable | Open source with NVIDIA alignment | Self-hosted on NVIDIA-heavy stacks | Performance-sensitive serving on NVIDIA estates | Hardware and optimization dependence can become structural | [Docs](https://docs.nvidia.com/tensorrt-llm/index.html) |
| [NVIDIA Triton Inference Server](https://developer.nvidia.com/triton-inference-server) | Serving platform | Multi-framework inference serving | Acceptable | Open source / NVIDIA-led ecosystem | Self-hosted | Unified serving for predictive and generative workloads | Best fit usually strengthens NVIDIA ecosystem dependence | [NVIDIA](https://developer.nvidia.com/triton-inference-server) |
| [NVIDIA NIM](https://build.nvidia.com/) | Packaged deployment ecosystem | Vendor-packaged inference runtime access | Acceptable | Mixed | Customer-managed or managed depending on deployment | Faster deployment on NVIDIA-standardized estates | Optimized convenience usually increases hardware and platform dependence | [NVIDIA](https://build.nvidia.com/) |
| [KServe](https://kserve.github.io/kserve/) | Open-source platform | Kubernetes-native predictive and generative serving | Preferred | Open source | Self-hosted on Kubernetes | Organizations standardizing model serving on Kubernetes | Requires cluster maturity and platform engineering depth | [KServe](https://kserve.github.io/kserve/) |
| [MLServer](https://docs.seldon.ai/mlserver) | Open-source inference server | Multi-model serving for classical ML and transformer workloads | Preferred | Open source | Self-hosted | Mixed predictive and generative serving using the V2 data plane | Stronger fit for teams comfortable composing their own serving architecture | [Docs](https://docs.seldon.ai/mlserver) |
| [Seldon Core 2](https://docs.seldon.ai/seldon-core-v2/) | Open-source platform | Kubernetes-native inference control plane | Preferred | Open source | Self-hosted on Kubernetes | Platformized inference across models, pipelines, and experiments | Requires meaningful cluster and platform ownership | [Docs](https://docs.seldon.ai/seldon-core-v2/) |
| [Ray Serve](https://docs.ray.io/en/latest/serve/) | Open-source framework | Programmable serving layer | Preferred | Open source | Self-hosted | Python-heavy application and model serving with custom scaling logic | Stronger fit for engineering-owned systems than general platform governance | [Docs](https://docs.ray.io/en/latest/serve/) |
| [BentoML](https://docs.bentoml.com/en/latest/) | Open-source platform | Application-oriented inference serving | Acceptable | Open source / commercial ecosystem | Self-hosted or managed companion platform | Teams packaging model APIs with surrounding service logic | Broader platform and deployment choices still need deliberate design | [Docs](https://docs.bentoml.com/en/latest/) |
| [OpenVINO Model Server](https://docs.openvino.ai/2025/openvino-workflow/model-server/ovms_what_is_openvino_model_server.html) | Serving platform | CPU, edge, and Intel-oriented model serving | Acceptable | Open source / Intel-led ecosystem | Self-hosted | Edge, CPU-heavy, and heterogeneous enterprise inference | Strongest fit assumes Intel-friendly hardware strategy | [OpenVINO](https://docs.openvino.ai/2025/openvino-workflow/model-server/ovms_what_is_openvino_model_server.html) |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | Open-source project | Local and lightweight inference runtime | Preferred | Fully open source | Local or self-hosted | CPU-friendly and edge-oriented open-weight inference | Best for lightweight and specialized deployments, not a full enterprise platform | [Repo](https://github.com/ggml-org/llama.cpp) |
| [ONNX Runtime GenAI](https://onnxruntime.ai/docs/genai/) | Open-source runtime | Optimized local and edge inference | Preferred | Open source | Local, edge, or self-hosted | Cross-hardware inference and local deployment | Serving maturity depends on surrounding stack choices | [Docs](https://onnxruntime.ai/docs/genai/) |
| [Ollama](https://ollama.com/) | Open-source runtime | Local and small-scale serving | Preferred | Open source runtime | Local or self-hosted | Developer workstations, demos, and smaller internal deployments | Not a full enterprise control plane by itself | [Docs](https://docs.ollama.com/) |

## Managed Inference And Serving Platforms

These platforms matter when the organization wants rapid access, managed operations, or cloud-estate alignment more than direct runtime control.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Hugging Face Inference Endpoints](https://huggingface.co/docs/inference-endpoints/index) | Managed service | Dedicated managed inference | Acceptable | Proprietary service | Dedicated managed | Managed production endpoints with some model flexibility | Managed control plane still centralizes dependence | [Docs](https://huggingface.co/docs/inference-endpoints/index) |
| [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/) | Managed service | Model access and managed inference | Controlled Exception | Proprietary service | AWS-managed | AWS-centric managed AI runtime | Depends on AWS contracts, routing, and surrounding services | [Docs](https://docs.aws.amazon.com/bedrock/) |
| [Google Vertex AI](https://cloud.google.com/vertex-ai/docs) | Managed service | Hosted model and ML platform | Controlled Exception | Proprietary service | GCP-managed | GCP-centric AI hosting and MLOps | Strong cloud-estate coupling | [Docs](https://cloud.google.com/vertex-ai/docs) |
| [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/) | Managed service | Hosted AI platform | Controlled Exception | Proprietary service | Azure-managed | Microsoft-centric AI hosting | Strong cloud and platform coupling | [Docs](https://learn.microsoft.com/azure/ai-foundry/) |
| [Groq](https://console.groq.com/docs/overview) | Managed inference platform | Low-latency model inference | Acceptable | Proprietary platform around mixed and open models | Managed | Ultra-low-latency inference and agent-adjacent response pipelines | Performance strengths do not remove provider dependence | [Groq](https://console.groq.com/docs/overview) |
| [Together AI](https://docs.together.ai/) | Managed platform | Open-model inference service | Acceptable | Proprietary platform with open-model access | Managed | Faster open-model adoption without self-hosting immediately | Still a managed-provider dependence layer | [Docs](https://docs.together.ai/) |
| [Fireworks AI](https://docs.fireworks.ai/) | Managed platform | Performance-oriented inference service | Acceptable | Proprietary platform | Managed | High-throughput managed inference with model variety | Platform-specific routing and cost dependence | [Docs](https://docs.fireworks.ai/) |
| [Baseten](https://docs.baseten.co/overview) | Managed platform | Managed model and application serving | Acceptable | Proprietary platform | Managed | Teams that want application and inference delivery in one managed surface | Another strategic platform layer between workloads and portable infrastructure | [Docs](https://docs.baseten.co/overview) |
| [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/) | Managed edge platform | Edge inference and AI API access | Controlled Exception | Proprietary service around open-model access | Managed edge | Low-latency edge and web-adjacent inference use cases | Strong dependence on Cloudflare edge and developer platform | [Docs](https://developers.cloudflare.com/workers-ai/) |

## Selection Notes

| If the primary need is... | Default bias |
| --- | --- |
| Private serving with stronger portability | Open self-hosted runtimes such as vLLM, TGI, KServe, or Ray Serve |
| Local and edge deployment | Ollama, llama.cpp, or ONNX Runtime GenAI |
| GPU-estate optimization at scale | TensorRT-LLM, Triton, or NVIDIA NIM on known hardware |
| Fast managed access with limited platform staffing | Managed inference services |
| Kubernetes-standardized model operations | KServe, MLServer, or Seldon Core 2 plus open telemetry and policy layers |
| Broader predictive and generative serving together | Triton, MLServer, Seldon Core 2, or OpenVINO deserve extra attention |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [8.3 Reference Points](08-03-00-reference-points.md).
