# 13.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Review-Ready_

Use this page during release planning, regression review, and post-change re-approval to recognize healthy evaluation operating shapes before polished demos or narrow metrics substitute for real evidence.

## Reusable Evaluation Patterns

| Pattern | What good looks like | Fit signal | Review warning |
| --- | --- | --- | --- |
| Release packet anchored to the real system shape | The team names the dominant system boundary first, then assembles evidence that matches it: retrieval checks for source-backed assistants, routing comparisons for gateway changes, tool misuse tests for action-capable agents, or drift review for predictive services | reviewers can state in one sentence what must be proven before release | the packet is organized around favorite tools or benchmark types rather than the actual release question |
| Baseline plus bounded-change regression lane | Every proposed change is tested against a stable prior baseline, with explicit attention to what changed and what should remain invariant | model, prompt, routing, policy, retrieval, or tool changes are frequent and often look "small" | the team treats hidden infrastructure or prompt edits as too minor to reopen evaluation |
| Scenario-led evidence mix with failure-mode coverage | Success cases, edge cases, abuse cases, and rollback checks are all represented in the operating pack instead of only happy-path samples | the system affects policy, customer communication, approvals, or automated actions | evaluation examples look persuasive in demos, but there is no evidence for refusal behavior, error recovery, or harmful drift |
| Calibrated human review with explicit decision rights | Human reviewers work from rubrics, disagreement thresholds, and escalation rules rather than free-form opinion | quality depends partly on judgment, contextual nuance, or domain interpretation | reviewer sign-off exists, but nobody can explain what counts as disagreement, failure, or release blocking |
| Re-evaluation tied to rollout, monitoring, and rollback | The evaluation plan already names which live signals, incidents, or operating changes reopen review and what rollback artifact is used if the release fails | the system will expand by geography, audience, action scope, or data sensitivity after launch | the team treats evaluation as a one-time prelaunch event with no defined monitoring handoff |

## Evaluation Anti-Patterns

| Anti-pattern | Why it fails | Early signal | Review action |
| --- | --- | --- | --- |
| Benchmark or demo substitution | Offline scores or polished walkthroughs can hide system regressions, permission leaks, or unsafe operating behavior | decks lead with benchmark deltas, but no system-level pack exists | require a release packet tied to the real workflow and dominant failure modes |
| Change blindness around prompts, routing, or retrieval | Teams miss regressions when they treat non-code changes as invisible or reversible without proof | prompts, gateway policies, index changes, or retrieval settings changed, but evaluation scope stayed static | reopen evaluation and require a bounded-change comparison against the prior live baseline |
| Human review as taste rather than control | Reviewer confidence does not scale if rubrics, escalation triggers, and disagreement handling are missing | sign-off depends on a few trusted people "looking at samples" | add scoring rules, disagreement thresholds, and named blocking conditions before approval |
| Release gates with no rollback evidence | A system is not ready if rollback depends on memory, notebooks, or ad hoc console history | the team can describe launch criteria, but not how it will revert safely | require the rollback target, owner, and release artifact before rollout widens |
| Evaluation isolated from monitoring and abuse review | Pre-release QA cannot stay credible if live incidents, abuse patterns, or telemetry gaps never feed back into the pack | observability and security teams are mentioned only after launch | link the release packet to chapters `14` and `15`, plus the relevant re-review triggers |

## Review Prompts

- Which evaluation pattern best matches the dominant release question: real-system packet, bounded-change regression, scenario-led evidence, calibrated human review, or rollout-linked re-evaluation?
- What changed since the last approved baseline, and where is that change proven safe rather than assumed harmless?
- Which failure mode would most damage trust here: wrong answer confidence, tool misuse, permission leakage, silent routing drift, or degraded human review consistency?
- Which adjacent chapter must re-enter before release: `12`, `14`, `15`, or `16`?

## Re-Review Triggers

- a prompt, model, retrieval source, routing policy, tool binding, or approval rule changed after the last approved packet
- rollout expands to a new audience, geography, language, business process, or action scope
- production telemetry or incident review exposes failure modes the original evaluation pack never measured
- reviewer disagreement stays high, but the team keeps widening rollout by narrowing the sample set instead of improving the system
- rollback depends on artifacts that are not versioned, reproducible, or still available

## Practical Reading Rule

Use these patterns after the release question is known but before approval is treated as routine. If the team cannot show what changed, what evidence matches that change, what would block launch, and how live incidents reopen review, the evaluation design is not finished.

Back to [13.2 Operating Evaluation And QA](13-02-00-operating-evaluation-and-qa.md).
