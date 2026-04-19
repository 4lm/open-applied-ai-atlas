# 2.1.3 Terminology Ledger

_Page Type: Glossary | Maturity: Draft_

This ledger complements the taxonomy chapter by giving contributors and readers one fast reference for the terms that drift most easily across architecture, governance, sourcing, and delivery conversations.

## How To Use This Ledger

- Use these definitions as the atlas default unless a page states a narrower, chapter-specific meaning.
- Reuse these terms before inventing local synonyms.
- When a tool vendor uses the same word differently, keep the atlas term stable and note the vendor usage separately.

## Core System Terms

| Term | Atlas meaning | What it is not |
| --- | --- | --- |
| AI system | An organizational system that uses AI methods inside a broader product, workflow, or operating model | A standalone model endpoint treated as the whole solution |
| ML system | A system whose behavior depends materially on trained statistical or learning components | A rule-only application with no learned component |
| Model | A trained artifact or service used for prediction, generation, ranking, classification, or transformation | The entire application, workflow, or governance stack |
| Foundation model | A broadly reusable model family adapted into many downstream tasks | A synonym for every model used in practice |
| Frontier model | A high-capability, fast-moving model family typically concentrated among a small set of actors | A formal regulatory class with one fixed threshold |

## Runtime And Interaction Terms

| Term | Atlas meaning | What it is not |
| --- | --- | --- |
| Assistant | A bounded interaction pattern focused on helping a user interpret, draft, search, or summarize | A system that should automatically execute multi-step operations by default |
| Agent | A system that can plan, choose actions, and use tools with some bounded autonomy | Any chatbot with a prompt loop |
| Workflow | A durable, explicit sequence of steps, state, approvals, and integrations | A loose synonym for agent behavior |
| Orchestration | The coordination layer that determines sequencing, tool use, routing, memory, and control flow | A synonym for “uses an LLM somewhere” |
| Tool use | Structured invocation of an external capability such as search, APIs, code execution, or a business action | General reasoning without side effects |

## Knowledge And Data Terms

| Term | Atlas meaning | What it is not |
| --- | --- | --- |
| Retrieval | Looking up relevant external information at run time | Long-lived memory by another name |
| Grounding | Constraining or supporting outputs with external sources, context, or system state | A guarantee of truth |
| Memory | Persisted state retained across turns, sessions, or workflows | Every prompt context window |
| Provenance | Evidence about where content, decisions, or artifacts came from and how they changed | A vague claim that “the system looked something up” |
| Self-hosted | Operated under the organization’s direct infrastructure control or a closely governed dedicated environment | Any vendor product with enterprise settings |

## Governance And Assurance Terms

| Term | Atlas meaning | What it is not |
| --- | --- | --- |
| Evaluation | Deliberate evidence generation about system quality, failure modes, and release readiness | A one-off demo or benchmark screenshot |
| Governance | The decision rights, policy structure, accountability, and review system around AI work | A document folder with no operating effect |
| Assurance | The evidence, controls, and review discipline used to justify trust in a system | Marketing language about responsibility |
| Oversight | Human review, escalation, approval, or intervention rights inside the operating model | A claim that humans are “somewhere in the loop” |
| Safety | Measures that reduce harmful, abusive, or uncontrolled outcomes | A single model policy feature |

## Sourcing And Control Terms

| Term | Atlas meaning | What it is not |
| --- | --- | --- |
| Portability | How easily interfaces, data, controls, and operations can move to another stack or provider | A promise that export exists in theory |
| Sovereignty | Where effective operational control, support dependence, auditability, and jurisdictional exposure really sit | A synonym for privacy |
| Lock-in | Dependence created by APIs, data gravity, workflow coupling, control planes, expertise concentration, or contracts | Only an SDK integration issue |
| Open source | Software with an open-source license and inspectable source code | A synonym for every “open” claim |
| Open weights | Model weights that are made available for use, subject to their actual license and restrictions | Full openness across training data, governance, tooling, and deployment |

## Reader Rule

When a page uses one of these terms in a way that would change a decision materially, link back here or to the canonical taxonomy subsection rather than silently redefining it.

Back to [2.1 Classification Foundations](02-01-00-classification-foundations.md).
