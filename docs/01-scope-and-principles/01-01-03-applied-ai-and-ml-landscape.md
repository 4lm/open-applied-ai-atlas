# 1.1.3 Applied AI And ML Landscape

_Page Type: Concept Explainer | Maturity: Draft_

Use this page when a discussion about "AI" is drifting toward chat systems, copilots, or one model family as if they represent the whole organizational landscape. The atlas is intentionally broader: organizations adopt predictive systems, retrieval-backed services, document workflows, recommenders, optimization engines, perception systems, and hybrid control surfaces that share some infrastructure concerns but do not create the same proof burden, review sequence, or operating risk.

This page is not the detailed classification layer. Its job is to keep the broad landscape visible long enough for the team to choose the right next chapter instead of importing LLM-first assumptions into every later decision.

## Landscape Map

| System family | What organizations are usually trying to achieve | What tends to matter first | Common narrowing mistake |
| --- | --- | --- | --- |
| Assistive and generative interaction systems | help people draft, summarize, explain, translate, or explore options faster | source grounding, workflow consequence, human acceptance criteria, and whether the interaction is still only advisory | treating a fluent interface as if it settles governance, evidence, or sourcing questions by itself |
| Knowledge-grounded and document systems | answer from changing internal knowledge, search across records, extract structured information, or route document-heavy work | source ownership, permission boundaries, freshness, deletion duties, and exception handling for low-confidence cases | calling retrieval or extraction "just chat" and missing information-governance and audit consequences |
| Predictive decision-support systems | forecast demand, classify cases, score risk, detect anomalies, or rank alternatives for human use | data quality, threshold setting, evaluation design, interpretation burden, and who owns the final consequential decision | focusing on interface polish while the real system influence comes from scores, rankings, or thresholds |
| Recommendation and optimization systems | choose routes, schedules, allocations, prices, or next-best actions under operational constraints | objective design, fairness and override rules, simulation or backtesting quality, and feedback-loop effects on the business process | describing optimization output as neutral recommendation even when it quietly hardens policy |
| Perception and signal-processing systems | detect events, conditions, defects, identities, or spoken content from images, audio, or sensor streams | error tolerance, calibration, fallback checks, environment drift, and the consequence model for false positives and false negatives | treating threshold tuning as a minor technical detail when it actually changes safety, service, or compliance outcomes |
| Hybrid systems and shared AI control surfaces | combine multiple AI methods or provide common routing, evaluation, retrieval, approval, or monitoring capability for many use cases | stack boundaries, control ownership, portability posture, and whether one internal pattern is about to become a portfolio-wide dependency | assuming a shared platform is neutral plumbing rather than a real architecture and governance choice |

## Distinctions That Keep Scope Honest

| Distinction | Why it matters before later chapter work starts |
| --- | --- |
| System family vs. method family | "Generative AI", "classical ML", "deep learning", and "hybrid" describe technical methods; they do not by themselves explain the business job, failure mode, or review burden of the system being discussed. |
| Interface style vs. operating consequence | A chat box can front a low-consequence drafting helper, a retrieval system, a risk-ranking workflow, or an action-taking agent. Interface familiarity is not enough to classify the real system. |
| Local feature vs. shared dependency | A gateway, retrieval corpus, evaluation layer, or approval queue may start as support infrastructure but can quickly become a portfolio-wide control point with lock-in and operating consequences of its own. |
| Fluent output vs. decision quality | A persuasive response does not prove grounded knowledge, calibrated prediction, safe automation, or policy-quality optimization. The proof burden depends on the consequence, not the wording style. |
| Automation ambition vs. evidence burden | A system can be low autonomy yet still require strong evidence if it shapes entitlements, investigations, or high-pressure workflows; another system can be more automated but bounded enough to stay reversible and well controlled. |
| Novelty vs. method fit | The newest generative approach is not automatically the best answer when the real job is forecasting, retrieval, extraction, optimization, anomaly detection, or perception. |

## What This Changes In Practice

- Keep non-LLM families in frame from the start. If the real work is forecasting, recommendation, extraction, vision, speech, or optimization, name that plainly before teams standardize on assistant language.
- Ask where the first consequential judgment happens. The critical point may be a human accepting a draft, a threshold crossing, a case-routing decision, or a tool call, and each posture sends the reader to different chapters next.
- Expect different evidence shapes. Retrieval-heavy work needs source and permission discipline; predictive and optimization work needs evaluation and threshold logic; perception work needs calibration and fallback checks; action-taking systems need stronger oversight, rollback, and traceability.
- Reopen chapter `1` when portfolio language starts flattening unlike systems into one "AI program". Shared labels are useful only if they do not hide different control, privacy, or sourcing consequences.
- Use this page only until the team can name the dominant system family, the main failure mode it must avoid, and the next chapter that should own the deeper decision.

## Chapter Handoffs

| If the unresolved question is mainly about... | Move to... |
| --- | --- |
| classifying the task pattern, autonomy shape, or portfolio lane | [5. Use Cases And Application Landscapes](../05-use-cases-and-application-landscapes/05-00-00-use-cases-and-application-landscapes.md) |
| separating system, model, tool, vendor, standard, and architecture classes | [2. Taxonomy](../02-taxonomy/02-00-00-taxonomy.md) |
| mapping the control points and layer boundaries of the solution | [3. Enterprise AI Stack Map](../03-enterprise-ai-stack-map/03-00-00-enterprise-ai-stack-map.md) |
| choosing model families, hosting posture, or adaptation depth | chapters [7](../07-model-ecosystem/07-00-00-model-ecosystem.md), [8](../08-model-hosting-and-inference/08-00-00-model-hosting-and-inference.md), and [12](../12-training-fine-tuning-and-adaptation/12-00-00-training-fine-tuning-and-adaptation.md) |
| grounding answers in internal knowledge, search, or persistent memory | [11. Knowledge Retrieval And Memory](../11-knowledge-retrieval-and-memory/11-00-00-knowledge-retrieval-and-memory.md) |
| bounded autonomy, tool execution, or workflow orchestration | [10. Agentic Systems And Orchestration](../10-agentic-systems-and-orchestration/10-00-00-agentic-systems-and-orchestration.md) |
| evaluation burden, release proof, human oversight, or high-consequence controls | [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md) and [16. Human Oversight And Operating Model](../16-human-oversight-and-operating-model/16-00-00-human-oversight-and-operating-model.md) |

## Reviewer Checks

- What is the dominant system family here: assistance, knowledge grounding, prediction, recommendation, optimization, perception, or a hybrid control surface?
- Is the team naming the real source of value and risk, or is it using generic "AI", "copilot", or "agent" language that hides the consequence boundary?
- Which method family is being proposed, and does it actually fit the organizational job better than simpler statistical, retrieval, rules-based, or hybrid alternatives?
- What kind of evidence will matter most first: grounding quality, calibration, backtesting, exception handling, threshold review, traceability, or portability of the operating pattern?
- If the favored vendor or model disappeared, would the team still understand the system family clearly enough to redesign the solution without re-learning the problem from scratch?

## Reading Rule

Stay on this page only long enough to prevent scope collapse. Once the team can state the dominant system family, the main consequence boundary, and the next decision owner in one sentence, move into taxonomy, use-case classification, stack design, evaluation, oversight, or sourcing work rather than repeating generic landscape language.

Back to [1.1 Mission And Scope](01-01-00-mission-and-scope.md).
