# 20.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use this page during design and renewal review to tell the difference between a real standards operating model and standards theater.

## Reusable Standards Patterns

| Pattern | What good looks like | Fit signal | Review warning |
| --- | --- | --- | --- |
| Law first, then standards crosswalk | The team names the governing obligations first and only then adds standards that help operationalize them | regulation or rights exposure is clearly part of the decision | standards are chosen before anyone can explain the legal question |
| Management system plus local evidence pack | A governance standard is mapped to approval lanes, control owners, and reusable evidence artifacts | the organization needs durable oversight across more than one system | the standard is cited, but no release evidence or control map exists |
| Public framework for accessibility, local controls for rigor | A public framework accelerates shared vocabulary, while local controls, templates, and review criteria do the real work | the team needs broad adoption across mixed technical maturity | the public framework is treated as the finished operating model |
| Technical practice anchored to named owner | Security, provenance, or telemetry guidance is tied to a concrete service owner and operating process | the system depends on runtime, workflow, or data-plane controls that must actually be run | the technical guide is admired but nobody owns implementation or drift review |
| Standards tracking separated from compliance claims | Bodies, committees, and programs inform horizon-scanning without being presented as conformance proof | the landscape is evolving quickly or EU harmonization matters | tracking participation is described as evidence that controls already exist |

## Standards Anti-Patterns

| Anti-pattern | Why it fails | Early signal | Review action |
| --- | --- | --- | --- |
| Certification theater | The team borrows confidence from standard names without showing what changed locally | slides mention conformance before any control pack or evidence bundle exists | require concrete outputs: owner, control map, evidence set, re-review trigger |
| One-framework-for-everything thinking | No single artifact settles law, governance, security, privacy, portability, and oversight together | the same named framework appears in every answer regardless of context | force the team to name the dominant question and missing chapter handoffs |
| Committee or principle citation as implementation proof | Bodies and principle sets help orientation, but they do not implement controls | a coordination body is listed where a control standard or local procedure should be | replace the citation with the actual normative or operational anchor |
| Standards shopping without control mapping | The team collects impressive references but none change review depth or delivery behavior | long reference list, no mapped controls, no owner, no lifecycle trigger | reduce to a starting set and require explicit outputs |
| Portability or privacy by implication | The team assumes a standards label settles exit posture, data boundary, or supplier dependence | portability is discussed only in principle language, not in evidence, formats, or contracts | pull in chapters `06`, `18`, and the relevant operational artifacts |

## Review Prompts

| Ask during review... | Why it matters |
| --- | --- |
| Which standard or framework changed a concrete control decision here? | Distinguishes implementation from citation |
| What local artifact would prove this standards set is operating? | Forces the team to name evidence, not only intent |
| Which chapter still needs to be pulled in before this standards set is credible? | Prevents chapter `20` from swallowing security, privacy, or sourcing issues |
| What change would trigger a fresh standards crosswalk? | Keeps the standards set alive as the system changes |

## Drift Signals

- standards language appears in approval material, but not in release artifacts
- the team can name committees and frameworks but not owners and evidence
- portability, privacy, or oversight claims remain abstract after the standards review
- the standards set grows each quarter, but delivery review gets no clearer

Back to [20.2 Applying Standards And Frameworks](20-02-00-applying-standards-and-frameworks.md).
