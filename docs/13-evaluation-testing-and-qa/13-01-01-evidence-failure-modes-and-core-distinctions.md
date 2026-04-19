# 13.1.1 Evidence, Failure Modes, And Core Distinctions

_Page Type: Concept Explainer | Maturity: Draft_

Use this page to classify what must be proved before release. Evaluation work breaks down when benchmark scores, regression results, scenario tests, abuse probes, human review, and live-operating signals are treated as interchangeable evidence just because they all produce numbers or notes.

## Evidence And Failure-Mode Map

| Evidence type | Main question it answers | Failure modes it is best at catching | Common misuse | Typical re-run trigger |
| --- | --- | --- | --- | --- |
| Baseline or benchmark evidence | Does the model or component have enough raw task capability to justify further work? | obvious capability gaps, language or class imbalance, weak starting-point quality | treating a benchmark win as release approval for a full system | model swap, major tuning change, new capability requirement |
| Regression or replay evidence | Did a change break behavior that previously worked in realistic conditions? | prompt regressions, routing drift, tool-contract breakage, retrieval-quality decay | testing only on clean synthetic samples and calling it regression coverage | prompt, workflow, gateway, retrieval, tool, or policy change |
| Scenario evidence | Can the end-to-end workflow survive the high-consequence tasks users actually care about? | approval-path errors, missing citations, incorrect action ordering, unusable edge-case behavior | proving one isolated model answer and assuming the full workflow is safe | new workflow branch, new user role, new integration, broadened rollout scope |
| Adversarial or abuse evidence | How does the system behave when users, content, or integrations try to push it outside the intended boundary? | prompt injection, privilege escalation, unsafe tool use, policy bypass, content abuse | treating adversarial testing as an optional security add-on instead of release evidence | new external input path, agent capability, tool permission, or provider route |
| Human-review evidence | Do qualified reviewers agree the behavior meets the task, policy, or quality bar? | subtle factual quality issues, policy interpretation errors, UX breakdowns, contested edge cases | collecting reviewer opinions without rubric, disagreement handling, or sampling rules | rubric change, new content domain, reviewer disagreement spike |
| Live-operating evidence | Does the system remain acceptable after release under production traffic and operational change? | drift, silent failure classes, unstable latency, exception growth, degraded business usefulness | pretending observability can replace pre-release proof or vice versa | incident, drift signal, traffic-shape change, model or dependency refresh |

## Core Distinctions

| Distinction | Why it changes the review |
| --- | --- |
| Capability proof vs. release proof | A model can be capable enough to continue development while the system is still unsafe or unready to release. |
| Model-level quality vs. system-level behavior | Good model answers do not prove retrieval quality, tool safety, approval handling, or operational resilience. |
| Representative replay vs. high-consequence scenarios | Broad regression coverage catches drift, but a few business-critical paths still need direct scenario tests. |
| Human judgment vs. reproducible scoring | Expert review can detect nuanced failures, but it must be anchored in rubrics, sampling, and disagreement rules. |
| Pre-release evidence vs. post-release visibility | Monitoring can reveal new failure classes after launch, but it cannot justify skipping scenario, regression, or abuse testing beforehand. |
| Failure discovery vs. risk acceptance | Finding a defect is not the same as deciding whether the remaining risk is acceptable, who approved it, and when re-review is required. |
| Single-metric improvement vs. overall operating quality | Better aggregate scores can still hide worse citation behavior, safety regressions, latency, or reviewer disagreement on critical tasks. |

## What These Distinctions Change In Practice

- Build the evaluation pack around the dominant failure modes, not around whatever metric the vendor, benchmark, or team already has handy.
- Treat prompt, routing, retrieval, policy, tool, and model changes as different sources of failure, even when they surface through the same user-facing task.
- Require every human-review program to define rubric, reviewer role, disagreement path, and sampling logic before its outputs are treated as evidence.
- Keep release decisions tied to evidence artifacts, exception handling, rollback readiness, and re-run triggers rather than to a single score or demo.
- Push observability, oversight, and security handoffs explicitly when the unresolved question is post-release drift, abuse resistance, or approval ownership rather than evaluation design alone.

## Reviewer Checks

- Can the team name which evidence type is supposed to catch each important failure mode?
- Which evidence is proving raw model behavior, and which evidence is proving end-to-end workflow behavior?
- Are high-consequence scenarios tested directly, or only implied by aggregate benchmark or regression results?
- If humans are in the loop, what rubric, sampling method, and disagreement rule keep review from collapsing into anecdote?
- Which changes force re-evaluation, and which owner is responsible for blocking release until that evidence exists?
- If a known failure remains open, where is the acceptance decision, expiry, and rollback condition recorded?

## Reading Rule

Classify the evidence first, then choose the release lane in [13.1.2 Decision Boundaries And Release Heuristics](13-01-02-decision-boundaries-and-release-heuristics.md). If the team still cannot say what must be benchmarked, replayed, scenario-tested, abuse-tested, reviewed by humans, and watched in production, the evaluation plan is not ready for a release gate yet.

Back to [13.1 Evaluation Foundations](13-01-00-evaluation-foundations.md).
