# 6.3.1 Standards And Bodies

_Page Type: Comparison Page | Maturity: Review-Ready_

This page gathers the main legal, standards, and specification anchors that matter for privacy, sovereignty, portability, and data-boundary control. The point is not to imply that one anchor answers everything; it is to show which source helps with which boundary question.

## Laws And Regulatory Anchors

| Anchor | Entity type | Primary purpose | Boundary use | Openness posture | Main misuse or dependence note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Regulation | Personal-data rights, accountability, transfers, and processing rules | Privacy review, rights handling, retention, and deletion design | Public law | Strong privacy coverage does not automatically settle sovereignty or portability posture | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj) |
| [EU Data Act](https://eur-lex.europa.eu/eli/reg/2023/2854/oj) | Regulation | Access, sharing, and portability expectations in connected data ecosystems | Access-right, switching, and ecosystem-control review | Public law | Often misread as a privacy instrument when the harder question is portability and control | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2023/2854/oj) |
| [Data Governance Act](https://eur-lex.europa.eu/eli/reg/2022/868/oj) | Regulation | European data governance and intermediation framework | Trusted sharing, intermediation, and protected-data reuse review | Public law | Relevant for specific sharing structures, not for every privacy or hosting decision | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2022/868/oj) |
| [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | Regulation | Risk-based AI obligations with privacy and rights implications | Boundary review where data handling and high-risk governance intersect | Public law | Important in context, but not a replacement for privacy-law analysis | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) |

## Privacy, Data-Quality, And Boundary Standards

| Anchor | Entity type | Primary purpose | Boundary use | Openness posture | Main misuse or dependence note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [NIST Privacy Framework](https://www.nist.gov/privacy-framework) | Framework | Privacy risk-management and engineering structure | Privacy-program design and privacy engineering crosswalks | Public framework | Helpful for structure, but not a substitute for applicable legal analysis | [NIST](https://www.nist.gov/privacy-framework) |
| [ISO/IEC 27701](https://www.iso.org/standard/27701) | Standard | Privacy information management system requirements and guidance | Privacy accountability and PII management structure | Paywalled standard with public summary | Strong management-system support, but still needs system-specific data-flow review | [ISO](https://www.iso.org/standard/27701) |
| [ISO/IEC 5259-1](https://www.iso.org/standard/81088.html) | Standard | Overview and terminology for AI and ML data quality | Shared vocabulary and framing for data-quality review | Paywalled standard with public summary | Foundational, but not enough on its own for operating controls | [ISO](https://www.iso.org/standard/81088.html) |
| [ISO/IEC 5259-3](https://www.iso.org/standard/81092.html) | Standard | Data-quality management requirements and guidance | Building auditable data-quality management around analytics and ML | Paywalled standard with public summary | Data quality is necessary, but it does not answer access-control or sovereignty questions by itself | [ISO](https://www.iso.org/standard/81092.html) |
| [ISO/IEC 5259-5](https://www.iso.org/standard/84150.html) | Standard | Data-quality governance framework | Governance-level oversight of data quality across the lifecycle | Paywalled standard with public summary | Strong for governance framing, but not a direct deletion or export mechanism | [ISO](https://www.iso.org/standard/84150.html) |
| [ISO/IEC 42005](https://www.iso.org/standard/42005) | Standard | AI system impact assessment | Human and societal impact review where privacy or rights issues are material | Paywalled standard with public summary | Impact assessment helps scope risk, but still needs concrete boundary controls | [ISO](https://www.iso.org/standard/42005) |
| [SPDX AI](https://spdx.dev/learn/areas-of-interest/ai/) | Open specification initiative | AI system bill-of-materials style metadata for models, data, prompts, and agents | Supply-chain and component visibility for AI systems | Open community specification effort | Metadata visibility helps review, but it does not enforce access or retention controls | [SPDX](https://spdx.dev/learn/areas-of-interest/ai/) |
| [C2PA](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) | Open technical specification | Content provenance and authenticity metadata | Provenance evidence where content integrity and attribution matter | Open specification | Valuable for provenance, not a full privacy or data-governance framework | [C2PA](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) |
| [OpenTelemetry Specifications](https://opentelemetry.io/docs/specs/) | Open specification | Standardized telemetry data model and semantics | Inspecting telemetry shape, exportability, and observability-related privacy posture | Open specification | Exportable telemetry is useful, but it can still widen the data boundary materially | [OpenTelemetry](https://opentelemetry.io/docs/specs/) |

## Bodies And Programs

| Anchor | Entity type | Primary purpose | Boundary use | Openness posture | Main misuse or dependence note | Primary source |
| --- | --- | --- | --- | --- | --- | --- |
| [ISO/IEC JTC 1/SC 42](https://www.iso.org/committee/6794475.html) | Standards committee | AI standards development | Tracking the source committee behind many AI data-quality and governance standards | Public committee information | Useful for landscape visibility, not for direct operating guidance | [ISO](https://www.iso.org/committee/6794475.html) |
| [CEN-CENELEC AI work](https://www.cencenelec.eu/areas-of-work/cen-cenelec-topics/artificial-intelligence/) | European standards program | European AI standards and harmonization activity | EU-facing tracking where sovereignty-sensitive deployments need standards context | Public program information | Helpful context for harmonization, but not itself a compliance shortcut | [CEN-CENELEC](https://www.cencenelec.eu/areas-of-work/cen-cenelec-topics/artificial-intelligence/) |
| [OECD AI Principles](https://oecd.ai/en/ai-principles) | Intergovernmental principles | High-level policy framing for trustworthy AI | Cross-jurisdiction policy context for privacy, transparency, and accountability | Public principles | Too general to settle architecture or operating-boundary choices by itself | [OECD.AI](https://oecd.ai/en/ai-principles) |

## Reading Rule

- Use GDPR when the dominant question is personal-data rights and lawful handling.
- Use the Data Act and related governance instruments when access, switching, and ecosystem control are central.
- Use standards and specifications to structure management, quality, provenance, and telemetry review after the legal question is clear.

## Evidence Notes

- The rows above are anchored in official legal texts or official standards, specification, and organization pages.
- The `Boundary use` and `Main misuse or dependence note` columns are atlas synthesis. They describe how these anchors help in practice when reviewing AI system data boundaries.
- This page distinguishes privacy, sovereignty, portability, and provenance concerns, but those categories still interact in real systems. That interaction is an implementation judgment, not a direct quotation from any single source.

Back to [6.3 Reference Points](06-03-00-reference-points.md).
