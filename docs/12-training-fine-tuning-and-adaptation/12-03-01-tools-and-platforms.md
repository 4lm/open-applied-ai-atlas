# 12.3.1 Tools And Platforms

This subsection holds the chapter's named comparison material. Read it as a reference layer, not as a substitute for the chapter's conceptual and implementation sections.

This file compares the tools used to adapt systems after model selection: prompt and program optimization, fine-tuning stacks, training ops, and managed platform services. It keeps the chapter's core bias visible: escalate to heavier adaptation only when prompting, retrieval, and evaluation discipline are no longer enough.

## How To Use This File

- Read the tables as comparison surfaces, not as a ranking list.
- Separate prompt or program optimization from parameter updates and from full training operations.
- Re-check `07`, `08`, `11`, `13`, and `18` before treating fine-tuning as the default answer.

## Prompt, Program, And Fine-Tuning Tooling

These tools matter when teams are deciding whether to stay in prompt or retrieval space or escalate to actual weight adaptation.

| Resource | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best fit | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [DSPy](https://dspy.ai/) | Open-source framework | Programmatic prompt and pipeline optimization | Preferred | Open source | Self-hosted library | Adaptation work that should remain in prompt or program space before training escalation | Optimization value still depends on strong eval loops | [DSPy](https://dspy.ai/) |
| [OpenAI fine-tuning guide](https://platform.openai.com/docs/guides/fine-tuning) | Vendor service and docs | Managed fine-tuning | Controlled Exception | Proprietary service | Vendor-hosted | API-first adaptation workflows with limited platform staffing | Fine-tuning remains inside vendor runtime, policy, and lifecycle boundaries | [Docs](https://platform.openai.com/docs/guides/fine-tuning) |
| [Hugging Face PEFT](https://huggingface.co/docs/peft/index) | Open-source library | Parameter-efficient fine-tuning | Preferred | Fully open source | Self-hosted | Open-weight adaptation with lower compute budgets | Still requires surrounding training, evaluation, and deployment discipline | [Docs](https://huggingface.co/docs/peft/index) |
| [TRL](https://huggingface.co/docs/trl/index) | Open-source library | RLHF and preference-optimization workflows | Preferred | Fully open source | Self-hosted | Post-training and preference-based adaptation on open models | Higher methodological and data-governance burden than simple SFT | [Docs](https://huggingface.co/docs/trl/index) |
| [Axolotl](https://docs.axolotl.ai/) | Open-source framework | Open-weight fine-tuning orchestration | Preferred | Open source | Self-hosted | Practical LoRA and SFT workflows on self-managed infrastructure | Best fit assumes teams already own the hosting and eval story | [Docs](https://docs.axolotl.ai/) |
| [Unsloth](https://docs.unsloth.ai/) | Open-source framework | Efficiency-focused fine-tuning stack | Preferred | Open source | Self-hosted | Faster fine-tuning with lower hardware budgets | Efficiency gains do not replace data, eval, or governance quality | [Docs](https://docs.unsloth.ai/) |
| [torchtune](https://pytorch.org/torchtune/main/) | Open-source library | PyTorch-native post-training and fine-tuning | Preferred | Open source | Self-hosted | Teams wanting closer control over PyTorch-based adaptation | Lower abstraction means more engineering burden than turnkey stacks | [Docs](https://pytorch.org/torchtune/main/) |
| [LlamaFactory](https://llamafactory.readthedocs.io/en/latest/) | Open-source framework | Unified LLM fine-tuning workflow | Preferred | Open source | Self-hosted | Teams comparing multiple post-training recipes in one framework | Needs careful method and license review per model family | [Docs](https://llamafactory.readthedocs.io/en/latest/) |

## Training Ops, Experimentation, And Lifecycle Platforms

These platforms matter when adaptation work becomes a repeatable operating function rather than a one-off experiment.

| Resource | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best fit | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [MLflow](https://mlflow.org/) | Open-source project | Experiment tracking and model lifecycle | Preferred | Fully open source | Self-hosted or managed ecosystem | Adaptation experiments and governance | Needs surrounding platform and release discipline | [MLflow](https://mlflow.org/) |
| [Weights & Biases](https://wandb.ai/site) | Experiment platform | Experiment tracking and analysis | Acceptable | Open source / commercial ecosystem | Self-hosted or managed | Training-heavy teams needing rich experiment visibility | Feature depth can pull teams toward a broader managed estate | [W&B](https://wandb.ai/site) |
| [Kubeflow](https://www.kubeflow.org/) | Open-source platform | ML pipelines and training ops | Preferred | Fully open source | Self-hosted | Platformized training workflows on Kubernetes | Requires cluster maturity and MLOps ownership | [Kubeflow](https://www.kubeflow.org/) |
| [Ray Train](https://docs.ray.io/en/latest/train/train.html) | Open-source framework | Distributed training orchestration | Preferred | Open source | Self-hosted | Scale-out training and adaptation on self-managed clusters | Stronger fit for engineering-led teams than UI-first experimentation flows | [Docs](https://docs.ray.io/en/latest/train/train.html) |
| [Dataiku](https://www.dataiku.com/product/machine-learning/) | Enterprise AI platform | Governed model development, deployment, and monitoring | Acceptable | Proprietary platform with open-tool integration | Self-managed or managed | Broad enterprise ML programs spanning analysts, data scientists, and governed deployment | Platform breadth can become a strategic workflow dependency | [Dataiku](https://www.dataiku.com/product/machine-learning/) |
| [H2O AI Cloud](https://docs.h2o.ai/haic-documentation/overview/what-is-h2o-ai-cloud) | Enterprise AI platform | End-to-end AI and MLOps platform | Acceptable | Mixed | Customer-managed or managed | Teams that want packaged ML, document, and LLM workflows with deployment flexibility | Stronger fit assumes willingness to adopt a larger platform surface | [Docs](https://docs.h2o.ai/haic-documentation/overview/what-is-h2o-ai-cloud) |
| [SAS Viya](https://support.sas.com/en/software/sas-viya.html) | Enterprise analytics and AI platform | Governed predictive analytics, ML, and operational decisioning | Controlled Exception | Proprietary platform | Self-managed, SAS-managed, or SaaS depending on offering | Regulated, analytics-heavy, or decisioning-heavy organizations | Strongest where broader SAS operating and governance posture is already material | [SAS](https://support.sas.com/en/software/sas-viya.html) |
| [Amazon SageMaker AI](https://aws.amazon.com/sagemaker/ai/) | Managed platform | Managed training and adaptation operations | Controlled Exception | Proprietary platform | AWS-managed | AWS estates needing unified training and deployment workflows | Strong cloud-estate coupling | [AWS](https://aws.amazon.com/sagemaker/ai/) |
| [Vertex AI tuning and training](https://cloud.google.com/vertex-ai/docs) | Managed platform | Managed training, tuning, and lifecycle operations | Controlled Exception | Proprietary platform | GCP-managed | GCP-centered adaptation and MLOps workflows | Strong cloud-estate coupling | [Docs](https://cloud.google.com/vertex-ai/docs) |
| [Azure AI Foundry fine-tuning](https://learn.microsoft.com/azure/ai-foundry/) | Managed platform capability | Managed fine-tuning and adaptation workflows | Controlled Exception | Proprietary platform | Azure-managed | Microsoft-centered adaptation workflows | Strong platform and cloud coupling | [Docs](https://learn.microsoft.com/azure/ai-foundry/) |
| [Databricks Mosaic AI](https://www.databricks.com/product/mosaic-ai) | Managed platform | Data-plus-model adaptation workflows | Acceptable | Proprietary / mixed ecosystem | Managed | Teams aligning adaptation work tightly to data lakehouse estates | Data estate, workflow, and model tooling dependence can compound | [Databricks](https://www.databricks.com/product/mosaic-ai) |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [12.3 Reference Points](12-03-00-reference-points.md).
