# 13.3.2 Controls And Artifacts

_Page Type: Operational Artifact | Maturity: Review-Ready_

This page turns the chapter into a reusable evidence packet. Use it when the team needs reviewable artifacts rather than a general statement that “we tested it.”

## Core QA Artifacts

| Artifact | What it should contain |
| --- | --- |
| Gold set | Stable reference cases, expected behavior, and version owner |
| Replay set | Realistic historical or production-like cases used for regression |
| Scenario pack | High-consequence workflows, edge cases, and abuse cases |
| Review rubric | Human-evaluation criteria, scoring rules, and escalation thresholds |
| Exception log | Known failures, approval status, owner, and expiry date |

## Core QA Controls

| Control | Why it exists | Owner |
| --- | --- | --- |
| Release gate | Prevents untested changes from shipping | Release owner |
| Regression suite | Protects against behavior drift across changes | QA or engineering owner |
| Adversarial testing | Finds abuse, safety, and boundary failures | QA plus security owner |
| Re-run trigger policy | Defines when evals must be re-run after model, prompt, data, or policy changes | Product or QA owner |

## Minimal Review Packet

- release scope and change summary
- links to gold set, replay set, and scenario-pack results
- named approvers and blocked issues
- open exceptions with expiry or mitigation plan
- rollback and monitoring links

## Approval Prompt

If the team cannot show which artifact would be inspected for a failed release decision, the evaluation program is still too informal.

Back to [13.3 Reference Points](13-03-00-reference-points.md).
