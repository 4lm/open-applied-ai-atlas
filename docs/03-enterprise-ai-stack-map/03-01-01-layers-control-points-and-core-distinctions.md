# 3.1.1 Layers, Control Points, And Core Distinctions

_Page Type: Concept Explainer | Maturity: Review-Ready_

Use this page to map organizational AI systems by responsibility layer before comparing architectures or products. The goal is not to prove that every system uses every layer. The goal is to stop teams from hiding control obligations inside a single favorite component.

## Layer Map

| Layer | Main question | Typical control points | Go deeper in chapter |
| --- | --- | --- | --- |
| Governance and policy | Who owns approval, exceptions, and re-review? | policy, review lane, exception register, evidence standards | `04`, `16`, `20` |
| Data boundary and privacy | What data is allowed, where does it flow, and who can operate it? | classification, minimization, retention, support access, key management | `06` |
| Model ecosystem | Which model family or supplier posture is viable? | model class, openness posture, licensing, provider dependence | `07`, `18` |
| Hosting and inference | Where does execution run and who operates the runtime? | region, tenancy, serving runtime, scaling, rollback path | `08`, `19` |
| Gateway and policy enforcement | How are routing, identity, quotas, and budget controls shared? | provider abstraction, auth, spend guardrails, audit logs | `09` |
| Orchestration and workflow | How is step sequencing controlled? | workflow boundaries, tool approvals, retries, handoffs | `10`, `16` |
| Retrieval and memory | What knowledge state is retrieved, stored, or updated? | permissions, provenance, refresh policy, memory retention | `11` |
| Training and adaptation | How is the model or prompt surface changed over time? | fine-tuning path, eval threshold, artifact lineage, rollback | `12`, `13` |
| Evaluation and release evidence | How is the system tested before and after release? | test pack, scenario evals, release gate, drift review | `13`, `14` |
| Observability and security | How are failures, misuse, and incidents seen and handled? | traces, alerts, abuse controls, redaction, incident workflow | `14`, `15` |
| Application and operating context | Which business workflow is actually being changed? | user role, approval point, system of record, fallback route | `05`, `16`, `18` |

## Core Distinctions

| Distinction | Why it matters |
| --- | --- |
| Stack layer vs. product choice | The stack map asks where a responsibility sits; vendor selection comes later |
| Control plane vs. execution plane | Identity, policy, approval, and audit often live outside the runtime that generates outputs |
| Cross-cutting concern vs. local feature | Privacy, sovereignty, portability, compliance, and lock-in must travel across multiple layers |
| Stack map vs. reference architecture | The stack map names the layers; chapter `19` turns them into reusable architecture shapes |
| Application consequence vs. technical complexity | A system can be technically small and still demand heavy governance or assurance |

## What Reviewers Should Check

- Which layer currently carries the strongest hidden risk: data boundary, gateway, workflow, or evidence?
- Which controls are genuinely shared across teams versus copied into each application separately?
- Which layer would have to change if the supplier, hosting posture, or regulatory consequence changed?
- Has the team mapped where openness and portability matter most, rather than treating them as abstract preferences?

Back to [3.1 Stack Foundations](03-01-00-stack-foundations.md).
