# 7.2.1 Worked Model Selection Scenarios

_Page Type: Worked Example | Maturity: Review-Ready_

Use these scenarios to test whether the team has a true model-selection problem, a retrieval or workflow problem wearing a model label, a hard control constraint, or a release-discipline problem. Each scenario is framed around the dominant question, the recommended posture, and the evidence outputs that should exist before rollout widens.

## Internal Knowledge Assistant Under Source Churn

| Field | Decision |
| --- | --- |
| Context | An internal assistant answers policy, support, and operating questions from documents that change weekly and must remain attributable to current sources |
| Dominant question | Does the team need the broadest available model, or does it need a stable language model posture that works well with retrieval, citation, and prompt discipline? |
| Recommended posture | Start with a frontier-managed or stability-first shortlist only after the retrieval baseline is credible, then compare models on instruction following, citation behavior, version stability, and fallback posture rather than leaderboard reputation alone |
| Why | Freshness and provenance sit mostly in retrieval and workflow design, so model choice should optimize for dependable reasoning and release discipline instead of pretending a larger model solves stale or weak source handling |
| Evidence and control outputs | shortlist rationale, retrieval-backed eval pack, citation review, model-version pinning note, fallback provider or family option, approved re-review trigger for major version shifts |
| Watch for | Escalating to a newer model because retrieval is weak, treating one provider brand as the default answer to every assistant task, or widening use without a version-change response plan |
| Adjacent chapters | `05`, `11`, `13`, `18` |

## Document Extraction Workflow With Schema Pressure

| Field | Decision |
| --- | --- |
| Context | An operations team extracts invoice, claims, or contract fields from messy scans and mixed document layouts, with downstream systems expecting fixed schemas and measurable error rates |
| Dominant question | Should the team standardize on a general chat model, or does the task justify a specialist extraction, vision, or hybrid pipeline posture instead? |
| Recommended posture | Use the specialist-fit lane first: compare task-specific extraction or multimodal candidates against a structured hybrid baseline, and keep any general model only if it clearly beats narrower options on schema fidelity and operating burden |
| Why | Extraction quality depends on document structure, OCR behavior, output constraints, and repeatable error handling more than on broad conversational reach, so a general model is often the wrong default |
| Evidence and control outputs | field-level accuracy pack, representative document set, schema-validation report, ambiguity-routing rule, human-review threshold, fallback path for unreadable or out-of-scope documents |
| Watch for | Forcing the workflow through a chat-shaped interface because procurement is simpler, mixing OCR failure with reasoning failure, or skipping specialist baselines before approving a larger model |
| Adjacent chapters | `05`, `12`, `13`, `19` |

## Sovereignty-Constrained Deployment Filter

| Field | Decision |
| --- | --- |
| Context | A public-sector or regulated program needs model capability for internal work, but runtime placement, support-access boundaries, and exportability are hard constraints rather than negotiation points |
| Dominant question | Which candidates remain viable once deployment freedom, acceptable licenses, model provenance, and self-hosting feasibility are treated as mandatory requirements? |
| Recommended posture | Use the open-weight control lane: shortlist only models with acceptable license terms, packaging maturity, and operating evidence for the target estate, then prove the organization can host, patch, monitor, and retire them under its own control model |
| Why | Sovereignty is not satisfied by regional marketing language or abstract openness claims; the shortlist must survive real runtime ownership, evidence export, and incident-response constraints |
| Evidence and control outputs | license and usage-rights note, provenance record, runtime compatibility check, hosting-operability packet, exportability review, incident and rollback ownership map |
| Watch for | Calling a model choice sovereign because it is region-pinned but still provider-administered, assuming open weights remove supplier dependence by themselves, or approving a shortlist before hosting capacity exists |
| Adjacent chapters | `06`, `08`, `15`, `18` |

## Model Refresh Under Portfolio Stability Pressure

| Field | Decision |
| --- | --- |
| Context | A production assistant or workflow already works acceptably, but a new model release promises better scores, larger context windows, or lower unit cost and teams want to refresh quickly |
| Dominant question | Is the new model materially better for the real workload, or is the organization about to trade portfolio stability for benchmark novelty and hidden retesting cost? |
| Recommended posture | Use the stability-first lane unless the new release clears a side-by-side regression pack, preserves fallback behavior, and comes with a documented rollback path and reapproval trigger |
| Why | Model swaps change outputs, moderation behavior, latency, prompting sensitivity, and downstream automation risk, so refresh should be governed like a release decision rather than a silent upgrade |
| Evidence and control outputs | side-by-side evaluation packet, downstream workflow regression check, deprecation or release-change note, rollback plan, exception approval if evaluation gaps remain, date for the next review window |
| Watch for | Treating a model swap as harmless infrastructure maintenance, accepting provider auto-upgrades without controlled comparison, or widening rollout before downstream owners sign off on changed behavior |
| Adjacent chapters | `08`, `13`, `14`, `16` |

## Reading Rule

If more than one scenario appears to fit, choose the posture that respects the hardest workload and control constraint first, then force the team to prove why a broader, newer, or more fashionable model is still justified. Model choice is not settled when a shortlist looks impressive; it is settled when the operating evidence, fallback plan, and adjacent chapter handoffs are strong enough to survive review.

Back to [7.2 Applying The Model Landscape](07-02-00-applying-the-model-landscape.md).
