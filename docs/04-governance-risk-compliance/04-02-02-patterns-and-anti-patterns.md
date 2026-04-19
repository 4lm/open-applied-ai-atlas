# 4.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use these patterns to stress-test whether governance is operating as a real management system or only as reassuring language.

## Reusable Patterns

| Pattern | What good looks like |
| --- | --- |
| Named ownership with reusable review lanes | Each system has a clear owner, and reviewers know when they are advisory versus approving |
| Policy translated into controls | Stated rules map to runtime, process, and evidence controls that can actually be inspected |
| Release evidence before launch | Approval depends on a reviewable package of tests, exceptions, and ownership records |
| Re-review triggered by change | Material model, data, supplier, or workflow changes reopen the right lane automatically |

## Governance Anti-Patterns

| Anti-pattern | Why it fails |
| --- | --- |
| Approval theater | A forum exists, but nobody can say what evidence is required or who owns the decision after launch |
| Policy without enforcement | The organization writes red lines that are not mapped to controls, tooling, or approval criteria |
| Permanent temporary exception | A short-term accommodation becomes the default pattern without expiry, compensating control, or exit plan |
| Incident isolation | The team patches the failure but never asks whether the approval model, thresholds, or ownership were wrong |

## Review Prompt

| Ask during review... | Why it matters |
| --- | --- |
| Which role owns this system after release? | Governance fails quickly when ownership ends at approval |
| Which artifact would an auditor or incident reviewer inspect first? | Forces the team to name real evidence, not only confidence |
| What change would trigger re-review? | Prevents stale approvals from silently covering new systems |
| Which risk is being accepted rather than controlled? | Exceptions should be explicit, not hidden inside vague language |

## Drift Signals

- nobody can distinguish policy, control, and evidence
- the review group signs off without a standard evidence package
- supplier or data-boundary changes happen outside governance visibility
- teams describe governance as "just paperwork" because it never changes delivery decisions

Back to [4.2 Operating The Governance Model](04-02-00-operating-the-governance-model.md).
