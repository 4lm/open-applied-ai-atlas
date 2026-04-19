# 20.3.1 Standards And Bodies

_Page Type: Comparison Page | Maturity: Draft_

This page compares the main legal, standards, practice, and coordination anchors used across the atlas. Read it as a standards-system crosswalk: first identify the artifact family, then choose the smallest credible starting set for the problem at hand.

## Laws And Regulations

| Anchor | Entity type | Primary purpose | Standards-system use | Openness posture | Main misuse or dependence note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | Regulation | Risk-based AI obligations for providers, deployers, importers, distributors, and other actors | Legal applicability, prohibited-practice screening, and high-risk governance starting point | Public law | Not a management system or implementation checklist by itself | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) |
| [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Regulation | Personal-data rights, accountability, transfers, and processing rules | Privacy and data-rights anchor when AI systems use personal data | Public law | Strong privacy coverage does not automatically settle supplier, provenance, or portability posture | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj) |
| [EU Data Act](https://eur-lex.europa.eu/eli/reg/2023/2854/oj) | Regulation | Access, use, portability, and sharing rules in connected data ecosystems | Access-right, switching, and ecosystem-control anchor | Public law | Often cited as a privacy instrument when the real issue is portability and dependence | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2023/2854/oj) |
| [Data Governance Act](https://eur-lex.europa.eu/eli/reg/2022/868/oj) | Regulation | Data intermediation and protected-data reuse framework | Trusted data-sharing and governance anchor where reuse or intermediation matters | Public law | Useful for specific sharing models, not as a general AI governance substitute | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2022/868/oj) |

## Governance Standards And Frameworks

| Anchor | Entity type | Primary purpose | Standards-system use | Openness posture | Main misuse or dependence note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [ISO/IEC 42001](https://www.iso.org/standard/42001) | Standard | AI management-system requirements | Organization-wide governance, accountability, and continual-improvement structure | Paywalled standard with public summary | Conformance language does not remove the need for local controls, owners, and evidence | [ISO](https://www.iso.org/standard/42001) |
| [ISO/IEC 23894](https://www.iso.org/standard/77304.html) | Standard | AI risk-management guidance | Structured risk identification, assessment, and treatment | Paywalled standard with public summary | Risk language alone does not produce release evidence or operating controls | [ISO](https://www.iso.org/standard/77304.html) |
| [ISO/IEC 42005](https://www.iso.org/standard/42005) | Standard | AI system impact assessment guidance | Stakeholder, societal, and rights-impact review input to governance and oversight | Paywalled standard with public summary | Helpful for impact framing, but not the whole oversight operating model | [ISO](https://www.iso.org/standard/42005) |
| [ISO/IEC 38507](https://www.iso.org/standard/56641.html) | Standard | Governance implications of AI use by organizations | Board and executive oversight framing | Paywalled standard with public summary | Useful for leadership framing, not as a substitute for control design | [ISO](https://www.iso.org/standard/56641.html) |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | Framework | Voluntary AI risk-management framework | Common governance vocabulary and implementation framing | Public framework | Often cited too abstractly unless paired with local review artifacts and control decisions | [NIST](https://www.nist.gov/itl/ai-risk-management-framework) |
| [NIST AI RMF Playbook](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook) | Implementation playbook | Suggested actions for AI RMF outcomes | Turning AI RMF outcomes into repeatable governance activities | Public implementation guidance | Helpful for operationalization, but still not organization-specific approval logic | [NIST](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook) |
| [OECD AI Principles](https://oecd.ai/ai-principles/) | Intergovernmental recommendation | Trustworthy-AI policy framing and interoperability context | High-level policy and cross-jurisdiction alignment anchor | Public policy guidance | Too high-level to function as direct operating guidance on its own | [OECD.AI](https://oecd.ai/ai-principles/) |

## Technical Specifications And Practice Guidance

| Anchor | Entity type | Primary purpose | Standards-system use | Openness posture | Main misuse or dependence note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf) | Framework | Secure development and release discipline | Connects AI-enabled services to broader secure-development expectations | Public framework | Not AI-specific enough to carry the whole governance model alone | [NIST](https://csrc.nist.gov/projects/ssdf) |
| [NIST Privacy Framework](https://www.nist.gov/privacy-framework) | Framework | Privacy risk-management and privacy-engineering structure | Privacy-program and data-governance crosswalk for AI systems using personal data | Public framework | Helpful for structure, but not a substitute for applicable legal analysis | [NIST](https://www.nist.gov/privacy-framework) |
| [C2PA](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) | Open technical specification | Content provenance and authenticity metadata | Provenance anchor where content origin, transformation history, or authenticity matter | Open specification | Provenance metadata does not by itself guarantee truthfulness, safety, or privacy compliance | [C2PA](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) |
| [SPDX AI](https://spdx.dev/learn/areas-of-interest/ai/) | Open specification initiative | AI system bill-of-materials style metadata for models, data, prompts, and agents | Component-inventory and supply-chain visibility anchor | Open community specification effort | Inventory visibility helps review, but it does not enforce portability or control discipline by itself | [SPDX](https://spdx.dev/learn/areas-of-interest/ai/) |
| [OWASP GenAI Security Project](https://genai.owasp.org/) | Community practice guidance | Security and safety guidance for generative and agentic AI systems | Practical review patterns, threat surfaces, and control questions for AI application security | Open community guidance | Useful for security operating detail, but not a legal or management-system anchor | [OWASP](https://genai.owasp.org/) |
| [MITRE ATLAS](https://atlas.mitre.org/) | Public knowledge base | Adversarial tactics, techniques, and mitigations for AI-enabled systems | Threat-model and adversary-behavior anchor for security review | Public knowledge base | Valuable for threat reasoning, but not a complete secure-development program | [MITRE ATLAS](https://atlas.mitre.org/) |

## Bodies, Committees, And Coordination Programs

| Anchor | Entity type | Primary purpose | Standards-system use | Openness posture | Main misuse or dependence note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [ISO/IEC JTC 1/SC 42](https://www.iso.org/committee/6794475.html) | Standards committee | AI standards development within ISO/IEC | Tracks the committee behind many AI governance and lifecycle standards | Public committee information | Useful for landscape awareness, not direct conformance on its own | [ISO](https://www.iso.org/committee/6794475.html) |
| [CEN-CENELEC AI work](https://www.cencenelec.eu/areas-of-work/cen-cenelec-topics/artificial-intelligence/) | European standards program | European AI standards and harmonization activity | EU-facing standards tracking and implementation planning | Public program information | Relevant for harmonization context, not itself a legal obligation or control set | [CEN-CENELEC](https://www.cencenelec.eu/areas-of-work/cen-cenelec-topics/artificial-intelligence/) |
| [ETSI AI](https://www.etsi.org/technologies/artificial-intelligence) | Standards body program | ICT and telecom AI standardization work | Technical standards tracking where telecom, ICT, or AI security specifications matter | Public program information | Program visibility does not mean a team has adopted the right technical controls | [ETSI](https://www.etsi.org/technologies/artificial-intelligence) |
| [NIST AI Standards](https://www.nist.gov/artificial-intelligence/ai-standards) | Public coordination program | U.S. and international AI standards landscape coordination | Landscape tracking beyond any single framework or standards family | Public program information | Best used as a tracking anchor, not as an operating framework | [NIST](https://www.nist.gov/artificial-intelligence/ai-standards) |
| [AI Pact](https://digital-strategy.ec.europa.eu/en/policies/ai-pact) | Voluntary implementation program | Early preparation for AI Act-related measures | Governance-program acceleration before or alongside legal applicability milestones | Public voluntary program | Participation is not equivalent to legal compliance or mature control implementation | [European Commission](https://digital-strategy.ec.europa.eu/en/policies/ai-pact) |
| [MLCommons Benchmarks](https://mlcommons.org/benchmarks/) | Benchmark consortium | Open benchmark suites for AI performance, quality, and safety work | Benchmark and measurement landscape anchor where reproducible evaluation signals matter | Open consortium | Benchmarks help comparison and measurement, but they do not by themselves create governance coverage | [MLCommons](https://mlcommons.org/benchmarks/) |

## Starting Sets By Need

| Need | Starting set | Why | Pull in chapter |
| --- | --- | --- | --- |
| EU-facing governance posture | EU AI Act + GDPR + ISO/IEC 42001 | combines obligations, privacy duties, and management-system structure | `04`, `06`, `16` |
| Practical AI risk program | ISO/IEC 23894 or NIST AI RMF + ISO/IEC 42001 | pairs risk method with durable governance ownership | `04`, `13` |
| Executive or board oversight design | ISO/IEC 38507 + ISO/IEC 42001 + ISO/IEC 42005 | separates leadership oversight from management-system and impact-review work | `16` |
| Security and abuse-resistance review | OWASP GenAI + MITRE ATLAS + NIST SSDF | combines threat knowledge with secure-development and AI-specific review patterns | `14`, `15` |
| Portability, provenance, and supplier visibility | EU Data Act + SPDX AI + C2PA | connects access and switching concerns to inventory and provenance evidence | `06`, `18`, `21` |
| EU standards monitoring and implementation context | CEN-CENELEC AI work + ETSI AI + AI Pact | supports harmonization tracking and early implementation planning | `04`, `21` |

## Reading Rule

- Use laws and regulations to identify obligations.
- Use standards and frameworks to structure governance and implementation work.
- Use bodies, committees, and programs to track movement in the landscape, not to replace local control design.

## Evidence Notes

- The named anchors above are linked to official legal texts or official standards-body, organization, or project pages.
- The `Primary purpose` and `Openness posture` columns are source-backed summaries.
- The `Standards-system use`, `Main misuse or dependence note`, and `Starting set` rows are atlas synthesis. They describe how these anchors complement one another in organizational implementation work; they are not legal advice, certification rules, or direct quotations from any single source.

Back to [20.3 Reference Points](20-03-00-reference-points.md).
