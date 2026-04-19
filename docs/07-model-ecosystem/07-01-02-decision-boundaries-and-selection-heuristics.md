# 7.1.2 Decision Boundaries And Selection Heuristics

_Page Type: Decision Guide | Maturity: Review-Ready_

Use this page when the team understands the model postures well enough and the remaining question is which shortlist lane fits by default. The goal is to stop model choice from collapsing into benchmark chasing, supplier loyalty, or self-hosting theater before the workload, control needs, and lifecycle burden are actually clear.

## Decision Lanes

| Lane | Use it when the main question is... | Default shortlist posture |
| --- | --- | --- |
| Frontier-managed lane | whether a broad language or multimodal capability is needed quickly and the main constraint is delivery speed rather than runtime control | shortlist managed general-purpose models, pin evaluation and fallback expectations, and reject claims that assume deployment freedom the provider does not offer |
| Open-weight control lane | whether weight access, self-hosting freedom, residency posture, or adaptation flexibility is already a hard requirement | shortlist models with acceptable licenses, packaging maturity, and evaluation evidence, then prove the organization can actually operate the chosen weights in its target runtime |
| Specialist-fit lane | whether the workload is extraction, ranking, speech, vision, document parsing, or another bounded task where a narrower model may outperform a general chat default | start from task-specific or modality-specific models, keep a separate evaluation pack for that task, and justify any move to a larger general model explicitly |
| Multimodal workflow lane | whether the product genuinely depends on mixed text, image, audio, video, or document-native interaction rather than treating multimodality as a prestige feature | shortlist models by end-to-end workflow support, artifact formats, and modality-specific evidence, and keep fallback paths for unsupported or weak modalities explicit |
| Classical-or-hybrid lane | whether prediction, retrieval, rules, ranking, optimization, or workflow logic carries most of the value and the model is only one component | keep classical ML or hybrid designs in scope, assign each component the work it fits, and force reviewers to explain why a general model belongs at all |
| Stability-first lane | whether regulated change control, long validation cycles, or downstream integration burden matters more than newest-model reach | prefer suppliers or model families with clearer versioning, deprecation behavior, and regression discipline, even when they trail the latest benchmark headlines |

## Practical Heuristics

- Start from workload shape before model prestige. If the task is extraction, forecasting, ranking, or fixed-schema generation, the strongest public general model may not be the best default.
- Treat openness as an operating requirement, not a cultural signal. Ask whether the need is weight access, self-hosting freedom, exportable artifacts, auditability, or only reduced supplier concentration.
- Separate model choice from hosting ambition. A self-hostable model does not justify self-hosting by itself, and a managed model does not settle sourcing, privacy, or portability questions on its own.
- Keep lifecycle burden in the shortlist. Silent version shifts, unclear retirement terms, or volatile output behavior can be more expensive than a slightly weaker but more stable model family.
- Force adaptation alternatives onto the table before escalating model size. Retrieval, prompt structure, workflow decomposition, and fine-tuning often fix the real problem more cheaply than swapping to a bigger base model.
- Make multimodality earn its place. If only one step of the workflow needs images, speech, or document parsing, a mixed portfolio may be safer than standardizing on one multimodal supplier.
- Use model portability as a full-system review, not a weight-only claim. Prompts, adapters, evaluation baselines, safety tuning, and operator knowledge can be the real lock-in even when a nominal substitute model exists.

## Escalate When

- the shortlist is dominated by vendor reputation or leaderboard position, but the team still cannot name the workload class in concrete terms
- self-hostable or open-weight options are being treated as automatically lower lock-in even though runtime, packaging, or adaptation ownership is still undefined
- the proposal needs stable outputs, approval cycles, or regulated review, but no one has described version pinning, regression cadence, or deprecation response
- multimodal standardization is being proposed even though the product only has one narrow non-text step that could be served separately
- a larger or newer model is being proposed to fix hallucination, freshness, or tool-use errors that more likely belong in retrieval, workflow, or evaluation design
- the team describes the system as "the model" even though retrieval, rules, classifiers, or other non-LLM components are doing most of the consequential work

## Model-Selection Anti-Patterns

- standardizing on one frontier provider because early prototypes looked strong before checking bounded task fit, lifecycle burden, or exit posture
- calling a model choice "open" when only the weights are accessible but serving, packaging, safety, or support dependencies remain opaque or fragile
- forcing perception, extraction, or prediction tasks through a chat-oriented interface because it simplifies procurement language
- selecting a multimodal platform for branding or consolidation while modality-specific evidence, cost shape, and fallback behavior remain weak
- replacing a working classical ML or hybrid design with a general model for novelty rather than measurable decision benefit
- widening production use before the team can explain how model changes will be detected, evaluated, approved, and rolled back

## Chapter Handoffs

- [5. Use Cases And Application Landscapes](../05-use-cases-and-application-landscapes/05-00-00-use-cases-and-application-landscapes.md) when the unresolved issue is still task framing, autonomy level, or which solution pattern the organization actually needs.
- [8. Model Hosting And Inference](../08-model-hosting-and-inference/08-00-00-model-hosting-and-inference.md) when runtime placement, hardware dependence, support access, or sovereignty posture is what now distinguishes the shortlist.
- [11. Knowledge Retrieval And Memory](../11-knowledge-retrieval-and-memory/11-00-00-knowledge-retrieval-and-memory.md) when freshness, provenance, permissions, or memory design seem to matter more than the base model family.
- [12. Training Fine-Tuning And Adaptation](../12-training-fine-tuning-and-adaptation/12-00-00-training-fine-tuning-and-adaptation.md) when the real question is whether prompt work, retrieval, fine-tuning, or retraining should change behavior before the base model changes.
- [13. Evaluation Testing And QA](../13-evaluation-testing-and-qa/13-00-00-evaluation-testing-and-qa.md) when the shortlist cannot be defended without clearer regression evidence, task-specific benchmarks, or release gates.
- [18. Build Vs Buy Vs Hybrid](../18-build-vs-buy-vs-hybrid/18-00-00-build-vs-buy-vs-hybrid.md) when supplier concentration, managed-service dependence, or long-term exit posture matters as much as raw model capability.

## Practical Reading Rule

Choose the lightest shortlist lane that still matches the hardest workload and control requirement, then tighten it as soon as openness needs, lifecycle burden, or modality complexity rise. If the team cannot explain why this model family fits the work better than retrieval, workflow redesign, a specialist model, or a hybrid system, the selection decision is still too weak.

Back to [7.1 Model Ecosystem Foundations](07-01-00-model-ecosystem-foundations.md).
