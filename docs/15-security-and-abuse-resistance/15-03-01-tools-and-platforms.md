# 15.3.1 Tools And Platforms

_Page Type: Comparison Page | Maturity: Draft_

This file compares practical security and abuse-resistance tooling for AI systems. It spans runtime guardrails, policy enforcement, redaction, red teaming, and supply-chain integrity because no single control family covers prompt attacks, data leakage, unsafe tool use, and artifact tampering together.

## How To Use This File

- Read the tables as comparison surfaces, not as universal rankings.
- Treat guardrails, policy engines, red-team tools, and supply-chain controls as complementary layers rather than substitutes.
- Re-check `09`, `13`, and `14` before assuming a security control can operate effectively without routing, evidence, and trace visibility.

## Guardrails, Validation, And Runtime Protection

These tools matter when the system needs to detect or block unsafe prompts, outputs, tool use, or data leakage at runtime.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [NVIDIA NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | Open-source project | Guardrail and policy tooling | Acceptable | Open source | Self-hosted with platform dependence considerations | Runtime guardrails and policy workflows | Integration and coverage still need broader security architecture | [Repo](https://github.com/NVIDIA/NeMo-Guardrails) |
| [Guardrails AI](https://www.guardrailsai.com/docs) | Framework | Validation and guardrail framework | Acceptable | Open source / commercial ecosystem | Self-hosted or managed layers | Output validation and structured control workflows | Needs explicit architecture fit and policy design | [Docs](https://www.guardrailsai.com/docs) |
| [Open Policy Agent](https://www.openpolicyagent.org/) | Open-source project | Policy-as-code enforcement | Preferred | Open source | Self-hosted | Shared authorization and policy enforcement around AI systems | Not AI-native; requires explicit integration | [OPA](https://www.openpolicyagent.org/) |
| [Kyverno](https://kyverno.io/) | Open-source project | Kubernetes policy enforcement | Preferred | Open source | Self-hosted | Cluster policy enforcement for AI workloads on Kubernetes | Best fit is infrastructure policy, not application-layer reasoning control | [Kyverno](https://kyverno.io/) |
| [Presidio](https://microsoft.github.io/presidio/) | Open-source project | PII detection and anonymization | Preferred | Open source | Self-hosted | Prompt, log, and document redaction workflows | Needs surrounding governance and context-specific policy tuning | [Docs](https://microsoft.github.io/presidio/) |
| [Google Cloud Model Armor](https://docs.cloud.google.com/model-armor/overview) | Managed security service | Prompt, response, and document screening for AI systems | Controlled Exception | Proprietary service | Managed | Organizations wanting a managed AI firewall layer with cloud or model-agnostic coverage | Strong managed control-plane dependence remains material | [Docs](https://docs.cloud.google.com/model-armor/overview) |
| [Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview) | Managed safety service | Harm detection, prompt attack screening, and content controls | Controlled Exception | Proprietary service | Managed, with preview container options for some features | Organizations needing managed moderation and prompt-shield controls with stronger enterprise integration | Service dependence remains material even where containers are available for parts of the stack | [Docs](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview) |
| [Lakera](https://www.lakera.ai/) | Security platform | Managed prompt attack and misuse protection | Controlled Exception | Proprietary platform | Managed | Organizations needing managed runtime protection for GenAI apps | Managed control-plane dependence and opaque detection logic remain material | [Lakera](https://www.lakera.ai/) |
| [Robust Intelligence AI Firewall](https://www.robustintelligence.com/platform/ai-firewall) | Security platform | Runtime protection and guardrails | Controlled Exception | Proprietary platform | Managed or enterprise deployment | Real-time protection against unsafe model behavior and attacks | Proprietary detection stack increases vendor dependence | [Robust Intelligence](https://www.robustintelligence.com/platform/ai-firewall) |
| [HiddenLayer AI Runtime Security](https://www.hiddenlayer.com/platform/ai-runtime-security) | Security platform | Runtime defense for prompts, agents, and tool abuse | Controlled Exception | Proprietary platform | Managed or enterprise deployment | Enterprises needing AI-specific runtime security and investigation | Product breadth increases platform dependence | [HiddenLayer](https://www.hiddenlayer.com/platform/ai-runtime-security) |

## Security Testing, Red Teaming, And Threat Modeling

These tools and frameworks matter when teams need evidence that controls actually hold under adversarial inputs and unsafe workflows.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [promptfoo Red Team](https://www.promptfoo.dev/docs/red-team/) | Open-source capability | Automated adversarial testing | Preferred | Open source | Self-hosted or CI-integrated | Security regression tests for prompts, agents, and policies | Strongest when paired with explicit release gates and remediation workflows | [Docs](https://www.promptfoo.dev/docs/red-team/) |
| [PyRIT](https://azure.github.io/PyRIT/) | Open-source framework | Generative AI red teaming and risk identification | Preferred | Open source | Self-hosted | Structured adversarial testing and risk discovery for generative AI systems | Requires security and prompt-engineering discipline to use well | [PyRIT](https://azure.github.io/PyRIT/) |
| [garak](https://docs.garak.ai/garak) | Open-source project | LLM vulnerability scanning | Preferred | Open source | Self-hosted | Broad failure probing for jailbreaks, leakage, and other LLM-specific risks | Probe breadth does not remove the need for application-specific security tests | [garak](https://docs.garak.ai/garak) |
| [OWASP GenAI Security Project](https://genai.owasp.org/) | Community project | Threat model and control guidance | Preferred | Open community effort | Public guidance | Shared threat vocabulary and control mapping | Guidance is not an enforcement mechanism by itself | [OWASP](https://genai.owasp.org/) |
| [MITRE ATLAS](https://atlas.mitre.org/) | Knowledge base | Adversarial threat model for AI systems | Preferred | Open public framework | Public knowledge base | Threat modeling, purple teaming, and control design | Framework value depends on actual security operations using it | [MITRE](https://atlas.mitre.org/) |
| [Semgrep](https://semgrep.dev/) | Security tooling ecosystem | Secure development and code scanning | Acceptable | Open core / commercial ecosystem | Self-hosted or managed | Securing AI-adjacent application code and pipelines | More software-security oriented than runtime-AI specific | [Semgrep](https://semgrep.dev/) |

## Supply-Chain Integrity, Provenance, And Artifact Assurance

These controls matter when the organization needs to know what models, dependencies, and signed artifacts it is actually running.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Sigstore](https://www.sigstore.dev/) | Open-source project | Signing and verification for software artifacts | Preferred | Open source | Public or self-managed supporting infrastructure | Supply-chain integrity for AI application components and deployment artifacts | Covers artifact integrity, not AI-specific behavior or safety | [Sigstore](https://www.sigstore.dev/) |
| [ModelScan](https://github.com/protectai/modelscan) | Open-source project | Model artifact scanning | Preferred | Open source | Self-hosted | Scanning serialized models for unsafe code before training, tuning, or deployment | Narrower than full supply-chain assurance and still format-dependent | [Repo](https://github.com/protectai/modelscan) |
| [SPDX AI](https://spdx.dev/learn/areas-of-interest/ai/) | Open specification initiative | AI bill-of-materials metadata | Preferred | Open specification | Exportable metadata standard | Recording model, prompt, agent, and data dependencies for review and audit | Needs tooling adoption to become operationally useful | [SPDX AI](https://spdx.dev/learn/areas-of-interest/ai/) |
| [C2PA](https://c2pa.org/) | Technical specification community | Content authenticity and provenance | Acceptable | Open specification community | Exportable provenance standard | Synthetic-media provenance and signed content chains | Helps authenticity and evidence, not general application security | [C2PA](https://c2pa.org/) |
| [OpenSSF Model Signing](https://openssf.org/blog/2025/04/04/launch-of-model-signing-v1-0-openssf-ai-ml-working-group-secures-the-machine-learning-supply-chain/) | Open community project | Model signing and verification | Preferred | Open community effort | Self-hosted or integrated into supply-chain tooling | Model artifact assurance and machine-learning supply-chain hardening | Still emerging, so adoption and tooling depth vary | [OpenSSF](https://openssf.org/blog/2025/04/04/launch-of-model-signing-v1-0-openssf-ai-ml-working-group-secures-the-machine-learning-supply-chain/) |
| [HiddenLayer AI Supply Chain Security](https://www.hiddenlayer.com/platform/ai-supply-chain-security) | Security platform | Managed scanning and integrity protection for models | Controlled Exception | Proprietary platform | Managed or enterprise deployment | Enterprises that need stronger commercial support around model supply-chain scanning | Proprietary scanning stack adds another vendor dependency | [HiddenLayer](https://www.hiddenlayer.com/platform/ai-supply-chain-security) |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [15.3 Reference Points](15-03-00-reference-points.md).
