# 1.2.1 Role-Based Reading Paths

_Page Type: Concept Explainer | Maturity: Draft_

Use this page when the atlas fits the problem but different readers still need different chapter entry points before they reconverge on the same system description. The goal is not to give every role a private tour. The goal is to choose the shortest credible path for each reader lane, then force alignment before architecture, vendor, or rollout decisions start drifting apart.

## Reading Path Map

| Reader lane | Start here when the live question is mostly about | Recommended chapter path | Rejoin before the team moves on | The pass should leave behind |
| --- | --- | --- | --- | --- |
| Product, project, and business readers | whether the use case is worth doing, who is affected, and how much workflow change the organization is really accepting | `1 -> 5 -> 18 -> 16 -> 4` | vendor comparison, implementation commitment, or rollout promises | a named use-case family, expected user and workflow change, basic sourcing posture, and a clear statement of which decisions need specialist review |
| Architecture and platform readers | where the system sits in the stack, which controls should be shared, and how reversible the design must stay | `1 -> 2 -> 3 -> 7/8/9 -> 19` | supplier selection, production architecture lock-in, or platform standardization | a stable system classification, boundary map, shortlist of runtime shapes, and known control surfaces that other teams must approve |
| ML, data, and delivery readers | what kind of evidence, data work, retrieval state, or adaptation burden the system will create | `1 -> 5 -> 11/12 -> 13 -> 14` | deployment promises, staffing assumptions, or claims about measurable benefit | a concrete task pattern, evidence plan, adaptation or retrieval stance, and the operating burden that later chapters must absorb |
| Privacy, security, assurance, and GRC readers | what obligations or release gates appear once the system touches sensitive data, high-stakes outcomes, or regulated processes | `1 -> 4 -> 6 -> 13 -> 15 -> 20` | procurement sign-off, launch approval, or external assurance claims | named control triggers, required evidence artifacts, boundary constraints, and the standards or policy anchors that actually matter |
| Operations, sourcing, procurement, and leadership readers | what the organization is willing to own, which suppliers or stack layers create dependence, and what exit posture is acceptable | `1 -> 17 -> 18 -> 19 -> 16` | contract negotiation, internal platform commitments, or support-model promises | a sourcing posture, ownership boundary, escalation route for shared services, and explicit lock-in or portability concerns |

## Convergence Gates

| Gate | Readers who must reconverge | What they need to agree before leaving chapter `1` behind |
| --- | --- | --- |
| Before taxonomy and use-case classification hardens | product, architecture, and ML/data | the dominant task family, affected workflow, user group, and whether the system is assistive, decision-support, action-taking, predictive, retrieval-heavy, or hybrid |
| Before stack, hosting, or gateway choices narrow | architecture, ML/data, privacy/security, and operations | data boundary, runtime control burden, evaluation expectations, and whether the design is a one-off feature or a reusable organizational service |
| Before vendor or sourcing choices narrow | product, architecture, sourcing, privacy/security, and leadership | acceptable supplier dependence, portability expectations, sovereignty constraints, support model, and what the team is willing to operate itself |
| Before rollout or public commitment | product, assurance, operations, and leadership | release evidence, exception handling, human-oversight model, incident path, and who owns re-review when scope expands later |

## How To Choose The Right Path

- Start with the reader lane that owns the immediate blocker, not the most senior title in the room. If the disagreement is about architecture reversibility, begin with the architecture path even if leadership is sponsoring the work.
- Keep the path short until the next real decision appears. A small internal assistant does not need the same chapter sweep as a regulated external service, but both still need an explicit convergence gate before downstream decisions fork.
- Reopen chapter `1` whenever the system crosses a boundary it did not originally have, such as moving from prototype to shared platform, from internal use to public service, or from one team to procurement-led rollout.
- Treat skipped chapters as explicit risk, not as invisible simplification. If a team bypasses privacy, security, evaluation, or sourcing lanes, note the assumption and the trigger that would force those readers back in.
- Use the path to expose disagreement early. If product wants speed, platform wants shared controls, and procurement wants a managed supplier, the conflict is telling you which later chapters must be read together before any shortlist is credible.

## Signs The Path Is Wrong

| Signal | What it usually means | Better next move |
| --- | --- | --- |
| The team keeps debating vendor names before it agrees on task class, workflow consequence, or control burden | the reading path jumped into market options before the system was classified | go back to chapters [2](../02-taxonomy/02-00-00-taxonomy.md), [5](../05-use-cases-and-application-landscapes/05-00-00-use-cases-and-application-landscapes.md), and [3](../03-enterprise-ai-stack-map/03-00-00-enterprise-ai-stack-map.md) |
| Security or privacy concerns appear late and invalidate earlier design work | the path treated governance lanes as downstream paperwork instead of design inputs | pull in chapters [4](../04-governance-risk-compliance/04-00-00-governance-risk-compliance.md), [6](../06-data-sovereignty-and-privacy/06-00-00-data-sovereignty-and-privacy.md), and [15](../15-security-and-abuse-resistance/15-00-00-security-and-abuse-resistance.md) before narrowing the shortlist |
| The team claims the system is lightweight, but nobody can name who owns monitoring, exceptions, or refresh decisions | the path skipped operations and oversight because build effort looked small | bring in chapters [14](../14-observability-logging-and-monitoring/14-00-00-observability-logging-and-monitoring.md) and [16](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) |
| Different groups are using the same project name for materially different systems | reader lanes never reconverged on one shared system description | return to [1.1.2 Audience, Roles, And Reader Modes](01-01-02-audience-roles-and-reader-modes.md) and restate the system family, workflow, and owner set before moving on |

## Reviewer Checks

- Which reader lane owns the immediate blocker, and which lanes only need to rejoin at the next convergence gate?
- What concrete output should this reading pass produce: classification, boundary map, evidence plan, sourcing posture, or rollout gate?
- Which later chapters are being skipped for now, and what trigger would make that skip unsafe?
- Has the team explicitly named when it will reconverge before stack, vendor, or release decisions harden?

Use this page until the team can name the current reader lane, the next convergence gate, and the artifact the reading pass must produce. Then move to [1.2.2 Worked Reader Journeys](01-02-02-worked-reader-journeys.md) for scenario-led examples or jump directly into the downstream chapters that now own the decision.

Back to [1.2 Using The Atlas](01-02-00-using-the-atlas.md).
