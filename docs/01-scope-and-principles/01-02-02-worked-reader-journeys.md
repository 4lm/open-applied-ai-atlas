# 1.2.2 Worked Reader Journeys

_Page Type: Worked Example | Maturity: Review-Ready_

These scenarios show how mixed teams should translate chapter `1` into a bounded reading pass. The goal is not to give every reader a long custom tour. The goal is to start from the immediate blocker, choose the shortest credible chapter path, and name the convergence gate that must be cleared before downstream architecture, procurement, or rollout choices harden.

## Public-Sector Service Owner Preparing A Citizen Assistant

| Field | Decision |
| --- | --- |
| Context | A digital-service owner wants to move a citizen-facing assistant from discovery into a bounded pilot without losing track of public-service obligations |
| Immediate blocker | The team needs to decide whether it is still exploring a low-consequence information service or drifting into advice, triage, eligibility, or case-handling territory |
| Shortest credible path | `1 -> 5 -> 4 -> 6 -> 13 -> 15 -> 16 -> 20` |
| Why this path first | The use-case class, governance burden, data handling posture, and release evidence matter more than model novelty or vendor convenience at this stage |
| Convergence gate | Before any supplier shortlist or public pilot promise, the service owner, privacy lead, security lead, and assurance owner agree on user group, task boundary, data classes, human fallback, and the evidence required for launch |
| This pass should leave behind | a named use-case class, affected-service boundary, control owner list, initial evidence packet, and explicit statement of which decisions still need specialist approval |
| Re-review trigger | Reopen chapters `1`, `4`, `6`, `13`, and `16` when the assistant gains workflow execution, starts affecting rights or service access, or moves from FAQ-style support into recommendation or decision support |

## Enterprise Platform Team Standardizing Shared AI Infrastructure

| Field | Decision |
| --- | --- |
| Context | A platform group is being pushed to standardize model access, hosting, and gateway controls across several internal teams that currently use different providers and ad hoc tooling |
| Immediate blocker | The group needs a shared control-plane view before it commits to one hosting posture, one gateway, or one reference architecture |
| Shortest credible path | `1 -> 2 -> 3 -> 7 -> 8 -> 9 -> 14 -> 18 -> 19` |
| Why this path first | The core problem is stack shape, control reuse, and portability posture, not which provider currently has the strongest benchmark or easiest demo |
| Convergence gate | Before platform standardization begins, architecture, operations, security, and procurement agree on supported system families, control surfaces to centralize, observability burden, and the acceptable exit posture for managed dependencies |
| This pass should leave behind | a stable system classification, shared-versus-local control map, shortlist of runtime postures, minimum telemetry requirements, and a sourcing note that explains where lock-in is acceptable or not |
| Re-review trigger | Reopen chapters `1`, `3`, `8`, `9`, `14`, and `18` when a local pilot becomes a shared service, when sovereign-hosting demands appear, or when supplier concentration starts constraining future architecture moves |

## Nonprofit Analytics Lead Choosing Between Forecasting And Document Automation

| Field | Decision |
| --- | --- |
| Context | A small nonprofit analytics team is deciding whether to invest first in a forecasting workflow, a document-intelligence pipeline, or a light internal assistant |
| Immediate blocker | The team needs to separate task families and operating burden before it buys a broad platform it cannot staff or govern |
| Shortest credible path | `1 -> 5 -> 2 -> 12 -> 13 -> 18` |
| Why this path first | The highest-value question is whether the organization needs prediction, extraction, retrieval, or generative assistance, and whether it can support the resulting evaluation and maintenance burden |
| Convergence gate | Before procurement or implementation starts, program ownership, delivery staff, and budget holders agree on the dominant task family, data readiness, evaluation method, and which operating burden the organization can realistically absorb |
| This pass should leave behind | one primary use-case lane, a realistic evidence plan, an explicit note on retrieval versus adaptation needs, and a sourcing posture that matches staffing and support capacity |
| Re-review trigger | Reopen chapters `1`, `5`, `12`, `13`, and `18` when the initial workflow expands into multi-step automation, sensitive-record handling, or shared organizational infrastructure instead of a narrow team tool |

## Privacy And Compliance Reviewer Challenging A Procurement Narrative

| Field | Decision |
| --- | --- |
| Context | A privacy or compliance reviewer is asked to assess a supplier proposal that describes an AI product as turnkey, compliant, and low-risk |
| Immediate blocker | The reviewer needs to test whether the procurement narrative matches the actual system boundary, control allocation, and evidence available to the organization |
| Shortest credible path | `1 -> 4 -> 6 -> 17 -> 18 -> 20 -> 13/15` |
| Why this path first | Supplier claims are not enough; the review must separate policy obligations, data boundaries, market dependence, standards claims, and release proof before contract language hardens the architecture |
| Convergence gate | Before sign-off, procurement, legal or privacy, security, and the accountable business owner agree on processing boundaries, control ownership, portability expectations, audit rights, and which assurance artifacts must be delivered |
| This pass should leave behind | a boundary and ownership summary, list of supplier claims that still need proof, standards and policy anchors that actually apply, and the escalation path if promised controls are unavailable or non-exportable |
| Re-review trigger | Reopen chapters `1`, `4`, `6`, `13`, `15`, `17`, and `18` when contract scope changes, support access expands, data residency claims weaken, or the supplier starts mediating more of the stack than originally planned |

## Cross-Journey Review Signals

- The shortest credible reading path is only useful if it ends with a named convergence gate and a concrete output such as a boundary map, sourcing note, evidence packet, or ownership decision.
- A journey is probably wrong if the team is comparing vendors before it agrees on task class, workflow consequence, data boundary, or who will own the resulting controls.
- Reopen chapter `1` whenever the system crosses into a new consequence class, a broader user group, a different operating model, or a stronger supplier dependence than the journey assumed at the start.

Back to [1.2 Using The Atlas](01-02-00-using-the-atlas.md).
