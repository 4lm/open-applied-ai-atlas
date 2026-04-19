# 19.1.1 Architecture Shapes, Constraints, And Core Distinctions

_Page Type: Concept Explainer | Maturity: Draft_

Use this page to separate the major architecture families before choosing named products. A good reference architecture narrows the design space. It does not pretend that one canonical stack fits every organization.

## Architecture Families

| Pattern family | Strongest fit | Non-negotiable controls | Main trade-off |
| --- | --- | --- | --- |
| SaaS-first assistant | low- to moderate-risk internal assistance with minimal platform capacity | approved provider lane, basic telemetry, fallback workflow | fastest start, weakest runtime autonomy |
| Managed suite architecture | organizations standardizing on a workflow or productivity estate | application-level governance, identity alignment, exit review | strongest application-level lock-in |
| Enterprise gateway stack | multi-team portfolios needing common control points across providers | shared auth, routing, budget control, eval and trace standards | added platform dependence and design overhead |
| Open infrastructure stack | exit-sensitive organizations willing to operate core runtime components | self-hosted serving, retrieval, telemetry, and upgrade ownership | higher operational burden |
| Sovereign private platform | high-control or regulated environments where locality and operator control dominate | local runtime, policy enforcement, provenance, strong auditability | highest staffing and lifecycle burden |
| Agentic workflow platform | delegated task execution with bounded tool use and approvals | workflow runtime, tool policy, human escalation, step tracing | highest QA and security burden |
| Public-facing content architecture | synthetic-media publishing, provenance, and authenticity use cases | provenance, signing, abuse controls, incident evidence | more operational complexity for authenticity and review |
| Edge-capable local platform | disconnected, workstation-heavy, or edge operations | local inference, update discipline, exportable telemetry | lower raw capability than cloud-first frontier stacks |
| Hybrid predictive plus generative stack | organizations combining forecasting, scoring, optimization, and language interfaces | ML lifecycle control, retrieval and workflow integration, cross-method evaluation | more stack complexity across method families |

## Core Distinctions

| Distinction | Why it matters |
| --- | --- |
| Reusable shape vs. turnkey blueprint | The pattern should guide design choices without hiding local constraints |
| Stack map vs. reference architecture | Chapter `03` says where responsibilities sit; chapter `19` says how those layers are commonly composed |
| Control intensity vs. operating burden | Stronger autonomy, sovereignty, or workflow capability usually increases support and evidence cost |
| Architecture family vs. vendor estate | Many vendors can fit one architecture family, and one vendor estate can imply several distinct families |

## What Reviewers Should Check

- Is the proposed pattern actually matched to the dominant constraint: speed, control, sovereignty, workflow automation, or hybrid-method support?
- Which layer would become the operational bottleneck if the pattern succeeds and scales?
- Does the chosen pattern preserve optionality where the organization says optionality matters most?

Back to [19.1 Architecture Foundations](19-01-00-architecture-foundations.md).
