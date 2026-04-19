# 7.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use this page during shortlist review, rollout planning, and model-refresh approval to recognize healthy model-portfolio shapes before one strong demo, one provider relationship, or one benchmark headline hardens into default policy.

## Reusable Model Operating Patterns

| Pattern | What good looks like | Fit signal | Review warning |
| --- | --- | --- | --- |
| Task-fit lane before portfolio standardization | Each workload is classified first as assistant, extraction, multimodal, predictive, or hybrid work, and the approved model lane follows that task shape instead of one supplier becoming the automatic answer | multiple teams want to reuse an early model success across very different tasks | the organization talks about "our standard model" before it can explain which workloads still need specialist or classical-ML treatment |
| Shortlist plus adaptation review packet | Model choice is approved together with retrieval, prompt, workflow, and fine-tuning alternatives so reviewers can see whether the model is really the constraint | quality issues could plausibly be fixed by retrieval, workflow structure, or bounded adaptation instead of a bigger base model | a weaker system design is being compensated for by demanding a larger or newer model |
| Portfolio ledger with named lifecycle ownership | Every approved model family has an owner, version policy, fallback option, evaluation packet, deprecation trigger, and adjacent hosting or sourcing handoff so the portfolio stays reviewable over time | more than one business process now depends on the same model family or provider relationship | teams can name the model and provider, but not who owns regressions, retirement, or substitution planning |
| Stability-gated refresh discipline | Model upgrades only proceed after side-by-side evaluation, downstream workflow checks, and a documented rollback path prove the new release is materially better for the real workload | provider releases are arriving quickly and teams want to refresh because context window, price, or benchmark claims improved | a model swap is being described as routine maintenance even though prompts, moderation, or workflow behavior will change |
| Bounded multimodal expansion | Text, image, audio, or document-native capabilities are added only where the workflow truly needs them, with explicit fallback handling for unsupported modalities and clear proof that one multimodal stack is better than a mixed portfolio | teams want one model surface for convenience, but only part of the workload depends on non-text inputs | multimodality is being adopted as a prestige feature instead of a workflow requirement |
| Open-weight control lane with runtime proof | Open-weight models stay in scope when deployment control, exportability, or adaptation freedom matter, but they are only approved after the organization shows credible hosting, packaging, monitoring, and incident ownership | sovereignty, exit posture, or self-hosting freedom is being treated as a hard requirement | reviewers hear "open" or "self-hostable" more often than evidence about runtime operations, patching, or fallback |

## Model Portfolio Anti-Patterns

| Anti-pattern | Why it fails | Early signal | Review action |
| --- | --- | --- | --- |
| One-provider default portfolio | Early wins turn into concentration risk, weak task fit, and hidden supplier dependence when every new problem is routed to the same model family | roadmap conversations start from a provider name instead of the workload class and control requirement | reopen chapter `05`, chapter `12`, and chapter `18` before allowing more standardization |
| Bigger-model escalation for system-design gaps | Retrieval, decomposition, prompt structure, or specialist tooling problems get mislabeled as model weakness, driving cost and risk without fixing the real issue | teams ask for a more powerful model before showing retrieval quality, tool-use design, or adaptation baselines | require a model-versus-adaptation review packet and pull chapter `11` or chapter `12` back in |
| Open-weight theater without operating ownership | Weight access is treated as sufficient proof of sovereignty or low lock-in even though runtime hardening, packaging, telemetry, and restore work are still unowned | architecture notes emphasize licenses and artifacts, but not who patches serving software or runs rollback drills | block approval until chapter `08`, chapter `15`, and chapter `18` handoffs are explicit |
| Benchmark-led refresh with no regression gate | Portfolio churn increases because public score gains outrun the organization's ability to test, approve, and reverse changed behavior | release discussions emphasize leaderboard movement or lower token cost while downstream owners are absent | require chapter `13` evidence and a named rollback owner before the swap proceeds |
| Multimodal consolidation before modality evidence | One general model becomes the answer to image, speech, and document workflows even when narrower tools or mixed portfolios are safer and easier to govern | procurement or platform teams want consolidation before modality-specific failure modes are understood | reopen task-fit review with chapter `05` and evaluation review with chapter `13` |

## Review Prompts

- Which pattern best matches the current decision: task-fit lane selection, model-versus-adaptation review, lifecycle ownership, stability-gated refresh, bounded multimodal expansion, or open-weight control with runtime proof?
- What evidence shows the chosen model family is better for this workload than retrieval changes, workflow redesign, a specialist model, or a classical-ML or hybrid alternative?
- Which anti-pattern is most likely after rollout pressure arrives: one-provider defaulting, bigger-model escalation, open-weight theater, benchmark-led refresh, or premature multimodal consolidation?
- Which adjacent chapter must re-enter before approval: `05`, `08`, `11`, `12`, `13`, `15`, or `18`?

## Re-Review Triggers

- a new workload class, modality, or regulated use case appears that was not represented in the original shortlist
- the provider changes model versioning, deprecation timing, pricing, or usage terms enough that fallback and sourcing assumptions no longer hold
- retrieval, prompt, or fine-tuning work materially changes the boundary between "model issue" and "system design issue"
- self-hosting, sovereign deployment, or exportability claims become harder requirements than they were at the original approval point
- downstream evaluation, moderation, or workflow owners can no longer explain how a model refresh would be tested, approved, and rolled back

## Practical Reading Rule

Use these patterns after a plausible shortlist exists but before the organization treats model choice as settled. If the team cannot show task fit, named lifecycle ownership, adaptation alternatives, bounded modality scope, and a believable refresh or exit path, the model operating posture is not ready.

Back to [7.2 Applying The Model Landscape](07-02-00-applying-the-model-landscape.md).
