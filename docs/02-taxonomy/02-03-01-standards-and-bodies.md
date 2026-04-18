# 2.3.1 Standards And Bodies

This subsection holds the chapter's named comparison material. Read it as a reference layer, not as a substitute for the chapter's conceptual and implementation sections.

This file keeps formal standards, public bodies, benchmark consortia, and provenance or supply-chain initiatives in one place so the atlas can classify them before comparing anything else.

## How To Use This File

- Start with entity class before using any name as a comparison anchor.
- Standards, bodies, and public frameworks are reference points, not software products.
- A standard becomes useful only when a chapter translates it into a control, design, sourcing, or operating choice.

## Bodies, Consortia, And Stewardship Anchors

| Resource | Entity type | Classification role | Why it matters to the atlas | Primary source |
| --- | --- | --- | --- |
| [ISO/IEC JTC 1/SC 42](https://www.iso.org/committee/6794475.html) | Standards committee | Core AI international standardization body | Anchor for terminology, governance, lifecycle, data-quality, and risk standards reused across chapters | Official ISO committee page |
| [CEN-CENELEC JTC 21](https://www.cencenelec.eu/areas-of-work/cen-cenelec-topics/artificial-intelligence/) | European standards committee | European AI standards and AI Act support | Matters when readers need European harmonization and conformity-oriented references | Official CEN-CENELEC page |
| [ETSI AI](https://www.etsi.org/technologies/artificial-intelligence) | Standards body program | ICT and telecom-centered AI standardization | Useful where network, telecom, and operational-security contexts shape the AI system boundary | Official ETSI page |
| [NIST AI Standards](https://www.nist.gov/artificial-intelligence/ai-standards) | Public standards coordination program | U.S. standards landscape and participation anchor | Strong crosswalk point between public guidance, measurement, and global standards participation | Official NIST page |
| [OECD.AI](https://oecd.ai/about-oecd-ai) | Intergovernmental observatory | Policy and principle stewardship | Useful when a chapter needs policy vocabulary rather than product or implementation vocabulary | Official OECD.AI page |
| [MLCommons Benchmarks](https://mlcommons.org/benchmarks/) | Benchmark consortium | Open benchmark and measurement stewardship | Keeps performance, safety, and procurement benchmarking separate from vendor marketing claims | Official MLCommons page |
| [OWASP GenAI Security Project](https://genai.owasp.org/) | Community project | AI application security vocabulary | Shared public taxonomy for prompt, retrieval, tool-use, and application risks | Official OWASP project |
| [MITRE ATLAS](https://atlas.mitre.org/) | Threat knowledge base | Adversarial AI tactics and techniques | Helps classify threats and controls without confusing them with products | Official MITRE site |
| [C2PA](https://spec.c2pa.org/specifications/specifications/2.3/index.html) | Technical specification community | Content provenance and authenticity standardization | Important for synthetic-media provenance, content credentials, and evidence chains | Official C2PA spec site |
| [SPDX AI](https://spdx.dev/learn/areas-of-interest/ai/) | Open specification initiative | AI bill-of-materials and supply-chain metadata | Useful for classifying prompts, models, datasets, and agents as governed artifacts | Official SPDX page |

## Standards And Framework Families

| Resource | Entity type | Classification role | Why it matters to the atlas | Primary source |
| --- | --- | --- | --- | --- |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | Framework | Trustworthiness and risk vocabulary | One of the main public vocabularies reused across governance, evaluation, and oversight sections | Official NIST page |
| [ISO/IEC 22989](https://www.iso.org/standard/74296.html) | Standard | Core AI concepts and terminology | Canonical terminology reference that helps keep the atlas taxonomy stable | Official ISO page |
| [ISO/IEC 23053](https://www.iso.org/standard/74438.html) | Standard | ML-based AI system framework | Helps distinguish AI-system structure from runtime, vendor, or use-case descriptions | Official ISO page |
| [ISO/IEC 42001](https://www.iso.org/standard/42001) | Standard | AI management-system vocabulary | Keeps management-system language distinct from risk, legal, or product language | Official ISO page |
| [ISO/IEC 23894](https://www.iso.org/standard/77304.html) | Standard | AI risk-management vocabulary | Reused when classifying harms, controls, and assessment approaches | Official ISO page |
| [ISO/IEC 42005](https://www.iso.org/standard/42005) | Standard | AI impact-assessment vocabulary | Useful where the atlas needs societal, human, and stakeholder impact framing | Official ISO page |
| [ISO/IEC 5338](https://www.iso.org/standard/81118.html) | Standard | AI system lifecycle processes | Keeps lifecycle descriptions structured instead of ad hoc | Official ISO page |
| [ISO/IEC 5259-1](https://www.iso.org/standard/81088.html) | Standard | AI and ML data-quality overview | Strong anchor for data-quality classification across analytics and ML chapters | Official ISO page |
| [ISO/IEC 5259-3](https://www.iso.org/standard/81092.html) | Standard | Data-quality management requirements | Useful when the atlas needs auditable data-quality management rather than general data-governance language | Official ISO page |
| [OECD AI Principles](https://oecd.ai/ai-principles/) | Intergovernmental principle set | Human-centric policy vocabulary | Good policy-level classification anchor when no binding law applies yet | Official OECD.AI page |

## Combination Heuristics

| If the chapter needs to classify... | Better starting point |
| --- | --- |
| Legal or quasi-legal obligations | Laws and regulations first, then standards and playbooks |
| Risk, trustworthiness, or governance posture | NIST AI RMF, ISO/IEC 42001, ISO/IEC 23894, OECD AI Principles |
| System structure or lifecycle language | ISO/IEC 22989, ISO/IEC 23053, ISO/IEC 5338 |
| Data-quality and evidence-quality language | ISO/IEC 5259 family and MLCommons benchmarks |
| Threats, provenance, or supply-chain transparency | MITRE ATLAS, OWASP GenAI, C2PA, SPDX AI |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [2.3 Reference Points](02-03-00-reference-points.md).
