# 6.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use these patterns to check whether a data-boundary design still holds once memory, telemetry, support, and exit posture are included.

## Reusable Patterns

| Pattern | What good looks like |
| --- | --- |
| Full-surface boundary mapping | Reviews include prompts, outputs, logs, memory, eval traces, and support artifacts |
| Residency plus control review | Region selection is paired with support, telemetry, subcontractor, and key-control analysis |
| Verifiable deletion and export | Lifecycle claims are supported by product capability or tested operating procedure |
| Boundary review triggered by feature change | New memory, retrieval, telemetry, or supplier features reopen the assessment automatically |

## Boundary Anti-Patterns

| Anti-pattern | Why it fails |
| --- | --- |
| Region equals sovereignty | Geography alone does not answer operational control or override rights |
| Training-only framing | A provider can avoid training reuse and still keep broad retention or support access |
| Invisible persistence | Logs, traces, memory, and eval datasets accumulate without owner or retention policy |
| Contract-only comfort | Legal terms are treated as a substitute for technical evidence and operating checks |

## Review Prompt

| Ask during review... | Why it matters |
| --- | --- |
| Which data states persist after the interaction ends? | Persistence often creates the real control burden |
| Which access paths are technical versus contractual? | Helps separate enforceable controls from assurances |
| Could the team export and delete this state today? | Tests portability and lifecycle reality early |
| What change would force boundary re-review? | Prevents stale approvals from covering a wider system later |

## Drift Signals

- the team cannot describe where traces, memory, or support snapshots live
- portability is discussed only at renewal time
- supplier docs and contracts describe different data handling behavior
- the architecture adds observability or memory features without reopening the boundary assessment

Back to [6.2 Operating Data Boundaries](06-02-00-operating-data-boundaries.md).
