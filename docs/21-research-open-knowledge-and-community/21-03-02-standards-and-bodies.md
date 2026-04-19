# 21.3.2 Standards And Bodies

_Page Type: Comparison Page | Maturity: Draft_

This page compares the public standards, benchmark bodies, provenance initiatives, and coordination programs that matter once the source class and adoption posture are already clear. Read it as an open-knowledge crosswalk: first decide whether the team needs benchmark literacy, public implementation guidance, provenance and artifact transparency, or standards-tracking context, then choose the smallest credible starting set instead of treating every named body as the same kind of authority.

## Benchmark And Measurement Anchors

| Anchor | Entity type | Primary purpose | Open-knowledge use | Openness posture | Main misuse or dependence note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [MLCommons Benchmarks](https://mlcommons.org/benchmarks/) | Benchmark consortium | Open benchmark suites and measurement governance for AI performance, efficiency, safety, and systems work | Benchmark-literacy anchor when external scores, benchmark suites, or public evaluations start influencing model or stack shortlists | Open consortium | Benchmarks support comparison and shared measurement, but they do not prove local task fit, release readiness, or governance sufficiency on their own | [MLCommons](https://mlcommons.org/benchmarks/) |
| [NIST ITL AI Program](https://www.nist.gov/artificial-intelligence/nist-information-technology-laboratory-itl-ai-program) | Public measurement and standards program | Measurement science, evaluation methods, and trustworthy-AI standards work | Public measurement context when teams need to understand how benchmarks, evaluation methods, and standards activity are evolving together | Public program information | Useful for landscape awareness and measurement framing, not as a turnkey evaluation plan or implementation checklist | [NIST](https://www.nist.gov/artificial-intelligence/nist-information-technology-laboratory-itl-ai-program) |

## Public Guidance And Practice Anchors

| Anchor | Entity type | Primary purpose | Open-knowledge use | Openness posture | Main misuse or dependence note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [NIST AI RMF Playbook](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook) | Public implementation guide | Suggested actions for AI RMF outcomes and organizational implementation work | Public implementation bridge when teams need to turn research, benchmark, or community signals into concrete review prompts and operating tasks | Public implementation guidance | Helpful for operationalization, but still not a substitute for local approval logic, test design, or operating evidence | [NIST](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook) |
| [OECD AI Principles](https://oecd.ai/ai-principles/) | Intergovernmental recommendation | Trustworthy-AI policy framing and high-level interoperability language | Shared vocabulary for reading public research, guidance, and policy claims without collapsing them into one local standard | Public policy guidance | Useful for framing and comparability, not for direct implementation sequencing, benchmark interpretation, or control ownership by itself | [OECD.AI](https://oecd.ai/ai-principles/) |
| [OWASP GenAI Security Project](https://genai.owasp.org/) | Community practice guidance | Security and safety guidance for generative and agentic AI systems | Public review aid when open projects, model demos, or community tooling need threat-aware reading before pilot adoption | Open community guidance | Strong for failure-mode triage, but not a complete security program, release gate, or supplier review on its own | [OWASP](https://genai.owasp.org/) |
| [MITRE ATLAS](https://atlas.mitre.org/) | Public knowledge base | Adversarial tactics, techniques, and mitigations for AI-enabled systems | Threat-model anchor when public examples or reference implementations need to be read through abuse and misuse paths before reuse | Public knowledge base | Valuable for adversary reasoning, but it does not by itself decide acceptable risk, release readiness, or operating controls | [MITRE ATLAS](https://atlas.mitre.org/) |

## Provenance, Reproducibility, And Supply-Chain Specifications

| Anchor | Entity type | Primary purpose | Open-knowledge use | Openness posture | Main misuse or dependence note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [C2PA](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) | Open technical specification | Content provenance and authenticity metadata | Provenance anchor where public demos, media outputs, or dataset artifacts need portable authenticity and transformation evidence | Open specification | Provenance metadata improves traceability, but it does not prove truthfulness, authorization, or broader governance compliance | [C2PA](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) |
| [SPDX AI](https://spdx.dev/learn/areas-of-interest/ai/) | Open specification initiative | AI system bill-of-materials style metadata for models, data, prompts, and agents | Artifact-inventory anchor when organizations want reusable metadata for community models, datasets, prompts, or agent components | Open community specification effort | Inventory visibility supports review, but it does not enforce portability, integrity, or version-control discipline on its own | [SPDX](https://spdx.dev/learn/areas-of-interest/ai/) |
| [OpenSSF model signing v1.0](https://openssf.org/blog/2025/04/04/launch-of-model-signing-v1-0-openssf-ai-ml-working-group-secures-the-machine-learning-supply-chain/) | Open community project | Model signing and machine-learning artifact integrity guidance | Integrity anchor where teams need to verify what public model or dataset artifact was promoted, mirrored, or deployed | Open community effort | Still emerging, so adoption depth, tooling coverage, and ecosystem convergence vary across organizations and supply chains | [OpenSSF](https://openssf.org/blog/2025/04/04/launch-of-model-signing-v1-0-openssf-ai-ml-working-group-secures-the-machine-learning-supply-chain/) |

## Bodies, Committees, And Coordination Programs

| Anchor | Entity type | Primary purpose | Open-knowledge use | Openness posture | Main misuse or dependence note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [ISO/IEC JTC 1/SC 42](https://www.iso.org/committee/6794475.html) | Standards committee | AI standards development within ISO/IEC | Committee-tracking anchor when public references cite ISO/IEC AI work and teams need to understand where those standards families are coming from | Public committee information | Useful for landscape awareness, not direct conformance, implementation guidance, or source-quality proof on its own | [ISO](https://www.iso.org/committee/6794475.html) |
| [NIST AI Standards](https://www.nist.gov/artificial-intelligence/ai-standards) | Public coordination program | U.S. and international AI standards landscape coordination | Standards-tracking surface when teams need to follow movement across named frameworks instead of anchoring to one familiar document | Public program information | Best used as a monitoring surface, not as an operating framework, evaluation plan, or chapter-specific decision rule | [NIST](https://www.nist.gov/artificial-intelligence/ai-standards) |
| [CEN-CENELEC AI work](https://www.cencenelec.eu/areas-of-work/cen-cenelec-topics/artificial-intelligence/) | European standards program | European AI standards and harmonization activity | EU standards-tracking context when public guidance starts to harden into harmonized standards expectations | Public program information | Relevant for harmonization planning, but not itself a legal obligation, benchmark suite, or local control set | [CEN-CENELEC](https://www.cencenelec.eu/areas-of-work/cen-cenelec-topics/artificial-intelligence/) |
| [ETSI AI](https://www.etsi.org/technologies/artificial-intelligence) | Standards body program | ICT and telecom AI standardization work | Technical standards-tracking context where infrastructure-heavy, telecom, or operational AI programs need to monitor external specification work | Public program information | Program visibility helps planning, but it is not equivalent to having chosen or implemented the right controls | [ETSI](https://www.etsi.org/technologies/artificial-intelligence) |
| [OECD.AI](https://oecd.ai/about-oecd-ai) | Intergovernmental observatory | Shared policy, terminology, and governance resource hub | Observatory anchor when teams need a stable public map of policy, terminology, and governance developments alongside research and standards signals | Public policy resource | Useful for comparability and policy context, not for direct architecture, release, or supplier decisions | [OECD.AI](https://oecd.ai/about-oecd-ai) |

## Starting Sets By Open-Knowledge Need

| Need | Starting set | Why | Pull in chapter |
| --- | --- | --- | --- |
| Benchmark literacy before shortlist refresh | MLCommons Benchmarks + NIST ITL AI Program | combines open benchmark suites with public measurement context before external scores harden into local selection policy | `07`, `13` |
| Public governance and implementation framing | OECD AI Principles + NIST AI RMF Playbook + OECD.AI | links high-level policy language to reusable public implementation guidance and observatory tracking | `04`, `20`, `21` |
| Security review of community artifacts and demos | OWASP GenAI Security Project + MITRE ATLAS | turns public examples into concrete threat, misuse, and control questions before pilot adoption | `15`, `21` |
| Provenance and artifact transparency | SPDX AI + C2PA + OpenSSF model signing v1.0 | separates inventory, content provenance, and artifact integrity so public artifact review is not reduced to one metadata layer | `14`, `18`, `21` |
| Standards-landscape tracking | ISO/IEC JTC 1/SC 42 + NIST AI Standards + CEN-CENELEC AI work + ETSI AI | gives teams a compact way to follow external standards movement without confusing monitoring with implementation | `20`, `21` |

## Reading Rule

- Use benchmark and measurement anchors to understand what an external score, benchmark suite, or public evaluation actually does and does not tell you.
- Use public guidance and practice anchors to translate outside signals into bounded local review questions rather than direct adoption.
- Use provenance and supply-chain specifications to make public artifacts more inspectable and portable.
- Use committees, programs, and observatories to track movement in the landscape, not to replace chapter-specific design, security, sourcing, or standards-selection work.

## Evidence Notes

- The named anchors above link to official organization, standards-body, specification, or project pages.
- The `Primary purpose` and `Openness posture` columns are source-backed summaries of what each anchor is for.
- The `Open-knowledge use`, `Main misuse or dependence note`, and `Starting set` rows are atlas synthesis. They describe how these anchors complement one another in research-to-practice review; they are not legal advice, certification rules, or direct quotations from any single source.

Back to [21.3 Reference Points](21-03-00-reference-points.md).
