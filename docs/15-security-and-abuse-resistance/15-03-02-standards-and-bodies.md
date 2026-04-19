# 15.3.2 Standards And Bodies

_Page Type: Comparison Page | Maturity: Review-Ready_

This page compares the external security anchors that matter most once the threat boundary is already clear. Read it as a control-planning crosswalk: first decide whether the team needs threat vocabulary, secure-delivery discipline, runtime-evidence structure, or supply-chain assurance, then choose the smallest credible starting set instead of treating every named framework as one interchangeable "AI security" checklist.

## Security Practice And Governance Anchors

| Anchor | Entity type | Primary purpose | Security-review use | Openness posture | Main misuse or dependence note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [OWASP GenAI Security Project](https://genai.owasp.org/) | Community practice guidance | Security guidance and control vocabulary for generative and agentic AI systems | Application-security review, control design, and abuse-case planning | Open community guidance | Useful for review structure and threat vocabulary, but not an enforcement mechanism or management system by itself | [OWASP](https://genai.owasp.org/) |
| [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) | Community guidance | Common failure patterns and attack classes for LLM-enabled applications | Fast triage for recurring prompt, retrieval, plugin, and data-exposure failure modes | Open community guidance | A memorable list is not a complete threat model, secure design review, or release gate | [OWASP](https://genai.owasp.org/llm-top-10/) |
| [MITRE ATLAS](https://atlas.mitre.org/) | Public knowledge base | Adversarial tactics, techniques, and mitigations for AI-enabled systems | Threat modeling, red teaming, and control mapping against attacker behavior | Public knowledge base | Valuable for adversary reasoning, but it does not replace local approval logic, secure delivery, or runtime evidence design | [MITRE ATLAS](https://atlas.mitre.org/) |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | Framework | Trustworthiness and risk-management structure for AI systems | Common risk vocabulary and governance framing for security reviews that must align with broader AI assurance work | Public framework | Often cited too abstractly unless paired with chapter-specific controls, owners, and release evidence | [NIST](https://www.nist.gov/itl/ai-risk-management-framework) |
| [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf) | Framework | Secure software development and release discipline | Connects AI-enabled services to broader secure build, change, and release expectations | Public framework | Strong for secure delivery, but not specific enough to act as the whole AI security model on its own | [NIST](https://csrc.nist.gov/projects/ssdf) |

## Telemetry, Provenance, And Supply-Chain Anchors

| Anchor | Entity type | Primary purpose | Security-review use | Openness posture | Main misuse or dependence note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [OpenTelemetry Specifications](https://opentelemetry.io/docs/specs/) | Open specification | Standardized telemetry semantics and data model | Runtime-evidence portability, trace design, and export-boundary planning for investigations | Open specification | Standardized telemetry helps reconstruction, but it can still widen the data boundary or miss AI-specific events if adopted mechanically | [OpenTelemetry](https://opentelemetry.io/docs/specs/) |
| [C2PA](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) | Open technical specification | Content provenance and authenticity metadata | Provenance evidence for generated or transformed media where authenticity, tamper review, or disclosure matters | Open specification | Provenance metadata helps authenticity review, but it does not guarantee truthfulness, safety, or authorization discipline | [C2PA](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) |
| [SPDX AI](https://spdx.dev/learn/areas-of-interest/ai/) | Open specification initiative | AI system bill-of-materials style metadata for models, data, prompts, and agents | Component-inventory and dependency visibility for model, prompt, and agent supply chains | Open community specification effort | Inventory visibility supports review, but it does not by itself enforce version control, signing, or rollback discipline | [SPDX](https://spdx.dev/learn/areas-of-interest/ai/) |
| [OpenSSF model signing v1.0](https://openssf.org/blog/2025/04/04/launch-of-model-signing-v1-0-openssf-ai-ml-working-group-secures-the-machine-learning-supply-chain/) | Open community project | Model signing and machine-learning artifact integrity guidance | Model artifact provenance and verification where teams need to prove what was trained, promoted, or deployed | Open community effort | Still emerging, so adoption depth and tooling coverage vary across organizations and deployment pipelines | [OpenSSF](https://openssf.org/blog/2025/04/04/launch-of-model-signing-v1-0-openssf-ai-ml-working-group-secures-the-machine-learning-supply-chain/) |

## Bodies, Programs, And Benchmark Anchors

| Anchor | Entity type | Primary purpose | Security-review use | Openness posture | Main misuse or dependence note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [ETSI AI](https://www.etsi.org/technologies/artificial-intelligence) | Standards body program | ICT and telecom AI standardization work | Standards tracking where regulated, telecom, or infrastructure-heavy deployments need formal security context | Public program information | Program visibility helps planning, but it is not equivalent to having adopted the right controls or evidence pack | [ETSI](https://www.etsi.org/technologies/artificial-intelligence) |
| [ETSI EN 304 223 announcement](https://www.etsi.org/newsroom/press-releases/2627-etsi-secures-artificial-intelligence-baseline-cybersecurity-standard) | Official standards release | Baseline cybersecurity requirements framing for AI models and systems | EU-facing security baseline tracking and procurement discussions about formal AI cybersecurity expectations | Public standards release | A standards announcement is useful orientation, but local teams still need the concrete control mappings and operating artifacts behind it | [ETSI](https://www.etsi.org/newsroom/press-releases/2627-etsi-secures-artificial-intelligence-baseline-cybersecurity-standard) |
| [NIST AI Standards](https://www.nist.gov/artificial-intelligence/ai-standards) | Public coordination program | U.S. and international AI standards landscape coordination | Landscape tracking beyond any single framework when security teams need to monitor external movement | Public program information | Best used as a tracking surface, not as an operating framework or release gate by itself | [NIST](https://www.nist.gov/artificial-intelligence/ai-standards) |
| [MLCommons Benchmarks](https://mlcommons.org/benchmarks/) | Benchmark consortium | Reproducible benchmark suites and measurement governance | Benchmark awareness where security or abuse-resistance claims depend on reproducible measurement and shared test conventions | Open consortium | Benchmarks help comparison and repeatability, but they do not create threat containment, secure delivery, or runtime evidence on their own | [MLCommons](https://mlcommons.org/benchmarks/) |

## Starting Sets By Security Need

| Need | Starting set | Why | Pull in chapter |
| --- | --- | --- | --- |
| Threat modeling and abuse-case design | OWASP GenAI Security Project + OWASP Top 10 for LLM Applications + MITRE ATLAS | combines fast failure-mode triage with richer attacker-behavior mapping | `13`, `15` |
| Secure release and change control | NIST Secure Software Development Framework + NIST AI RMF | pairs secure delivery discipline with broader AI risk and control vocabulary | `13`, `16` |
| Runtime evidence and incident reconstruction | OpenTelemetry Specifications + MITRE ATLAS | links telemetry structure to the abuse patterns security teams need to reconstruct and contain | `14`, `15` |
| Artifact provenance and supply-chain assurance | SPDX AI + OpenSSF model signing v1.0 + C2PA | separates component inventory, signing, and content provenance so supply-chain review is not reduced to one control family | `14`, `18`, `21` |
| EU-facing baseline security tracking | ETSI AI + ETSI EN 304 223 announcement + NIST AI Standards | gives teams a compact way to follow named standards movement without pretending standards tracking is the same thing as implementation | `20`, `21` |

## Reading Rule

- Use practice guidance and knowledge bases to understand failure shapes and attacker behavior.
- Use frameworks to structure ownership, secure delivery, and review logic.
- Use specifications to make telemetry, provenance, and supply-chain evidence exportable.
- Use bodies, releases, and benchmark programs to track the external landscape, not to replace system-specific threat analysis.

## Evidence Notes

- The named anchors above link to official organization, standards-body, specification, or project pages.
- The `Primary purpose` and `Openness posture` columns are source-backed summaries of what each anchor is for.
- The `Security-review use`, `Main misuse or dependence note`, and `Starting set` rows are atlas synthesis. They describe how these anchors complement one another in organizational security review; they are not legal advice, certification rules, or direct quotations from any single source.

Back to [15.3 Reference Points](15-03-00-reference-points.md).
