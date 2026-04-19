# 5.1.1 Task Classes, Autonomy, And Core Distinctions

_Page Type: Concept Explainer | Maturity: Draft_

Use this page to classify the work pattern before the discussion collapses into "assistant", "agent", or one preferred product suite. Use-case review becomes weak when drafting help, predictive decision support, extraction workflows, optimization engines, action-taking automation, and internal control surfaces are all treated as the same thing with different interfaces.

## Use-Case Posture Map

| Use-case posture | Where the real value is created | Where the real human judgment sits | What fails when it is misclassified |
| --- | --- | --- | --- |
| Worker assistance | helping a person draft, summarize, search, explain, or transform material faster without changing the formal decision owner | the person still decides what to accept, publish, send, or implement | teams import heavy autonomy rhetoric while still neglecting answer quality, provenance, access control, or downstream work quality |
| Knowledge-grounded assistance | combining retrieval, permissions, and response generation so people can act on changing internal knowledge | reviewers decide whether the answer is sufficiently grounded and whether the source set is complete for the task | retrieval is treated like generic chat, so source authority, deletion duties, and permission boundaries are handled too late |
| Predictive decision support | producing scores, forecasts, classifications, or anomaly signals that influence a human decision or policy path | a human or policy forum interprets the score, sets thresholds, and owns the resulting action | probability or ranking output is mistaken for a final decision, so weak thresholds or poor interpretation become operational policy |
| Extraction and document workflows | turning documents, forms, images, or speech into structured data, case signals, or exception queues | people decide how low-confidence cases, edge cases, and legally material exceptions are handled | organizations treat extraction confidence as truth and skip exception routing, audit trails, or source re-checks |
| Recommendation and optimization | shaping which option, route, inventory choice, price, schedule, or action sequence gets surfaced first | humans or control rules decide which objectives, fairness limits, and override rights govern the optimization | optimization logic quietly hardens one objective or bias into the default operating policy |
| Perception and inspection | using vision, audio, or sensor signals to detect conditions, defects, identities, or events | reviewers choose thresholds, fallback checks, and the consequence model for false positives and false negatives | threshold tuning is treated as a technical detail even though it changes safety, service, or compliance outcomes materially |
| Action-taking automation | triggering tools, workflows, record updates, or external actions with limited human intervention | approval design, rollback authority, and exception ownership define where people stay in control | teams describe the system as an assistant or copilot while it is already changing records, initiating workflows, or affecting outside systems |
| Shared AI control surface | governing evaluation, routing, gateway policy, review packets, or orchestration rules that shape many other use cases at once | platform owners and assurance leads decide which controls are mandatory, monitored, and exportable | internal infrastructure is treated as neutral plumbing, so repeated portfolio risk accumulates behind convenience tooling |

## Core Distinctions

| Distinction | Why it changes the operating decision |
| --- | --- |
| Task class vs. interface style | A chat box, form, dashboard, or background service can wrap many different work patterns; interface familiarity is not enough to classify the real system. |
| Assistance vs. decision influence | A system can leave the final click to a human and still be high consequence if its score, ranking, or recommendation strongly shapes the human choice. |
| Decision influence vs. action authority | Advising a person, proposing a workflow step, and directly executing a tool call are different operating postures even when the same model is underneath. |
| Confidence signal vs. acceptable evidence | Extraction confidence, forecast probability, or route score does not by itself show whether the evidence is good enough for the business consequence at stake. |
| Local feature vs. shared control surface | An evaluation layer, gateway, retrieval fabric, or review queue may look like supporting infrastructure, but it often becomes the real policy boundary across many use cases. |
| Data sensitivity vs. autonomy | A low-autonomy assistant can still be high pressure if it touches regulated or strategically sensitive information, and a higher-autonomy internal tool may still be bounded if the environment is narrow and reversible. |
| Model novelty vs. method fit | The newest generative interface may be the wrong answer when the real job is forecasting, optimization, extraction, or threshold-based inspection. |

## What These Distinctions Change In Practice

- Start by naming the dominant work pattern in plain language: drafting help, grounded search, forecasting, extraction, optimization, perception, action-taking automation, or shared control infrastructure.
- Separate consequence from autonomy. A recommendation engine, risk score, or document-classification workflow can be low-autonomy in interface terms but still deserve heavier evaluation, governance, and oversight than a simple drafting assistant.
- Treat infrastructure-facing systems as first-class use cases. Gateways, evaluation layers, routing services, and review queues influence many downstream deployments and should not be scoped as invisible internal plumbing.
- Keep non-LLM families visible. Forecasting, anomaly detection, recommenders, optimization, speech, vision, and document-intelligence systems belong in the same portfolio conversation because they change approval, evidence, and sourcing obligations differently.
- Expect chapter handoffs. Use-case classification is only the first boundary: retrieval-heavy cases move into [11](../11-knowledge-retrieval-and-memory/11-00-00-knowledge-retrieval-and-memory.md), action-taking work into [10](../10-agentic-systems-and-orchestration/10-00-00-agentic-systems-and-orchestration.md), predictive and quality-heavy cases into [13](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md), and consequence-heavy controls into [16](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md).

## Reviewer Checks

- What is the real work being done: drafting, retrieval-backed explanation, scoring, extraction, optimization, perception, action execution, or control-plane mediation?
- Where does the first materially consequential judgment happen: when the user reads the output, when a threshold is crossed, when a case is routed, or when a tool call executes?
- Which evidence is actually needed: source grounding, precision and recall, backtesting, threshold calibration, approval traceability, or control-surface observability?
- Is the proposal hiding a higher-consequence posture behind low-consequence language such as "assistant", "copilot", "internal only", or "workflow helper"?
- If the favored product disappeared, would the organization still understand the use-case class clearly enough to choose a different pattern without redesigning the whole operating model?

## Practical Reading Rule

Classify the task class and consequence posture first, then use [5.1.2 Portfolio Boundaries And Prioritization Heuristics](05-01-02-portfolio-boundaries-and-prioritization-heuristics.md) to choose the review lane and [5.1.3 Solution Pattern Selection Guide](05-01-03-solution-pattern-selection-guide.md) to choose the starting architecture pattern. If the team still cannot explain the dominant task class, consequence trigger, needed evidence, and real human control point in one sentence, the use case is not ready for portfolio prioritization or vendor shortlisting.

Back to [5.1 Use-Case Foundations](05-01-00-use-case-foundations.md).
