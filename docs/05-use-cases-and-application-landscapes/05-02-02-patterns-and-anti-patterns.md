# 5.2.2 Patterns And Anti-Patterns

This subsection captures reusable good shapes and recurring failure shapes so the chapter remains useful during design review as well as implementation.

## Better Patterns

- classify the use case before naming the preferred tool
- keep worker assistance separate from action-taking automation
- treat retrieval, evaluation, and observability as first-class design concerns where needed
- scale human-oversight intensity with consequence and autonomy
- let sourcing and portability posture vary by use-case family instead of forcing one default estate-wide answer

## Anti-Patterns

- calling every workflow “agentic” because it contains several steps
- treating all AI adoption as a chatbot program
- selecting tools before the use-case family and constraints are understood
- assuming predictive, retrieval, and generative systems can share the same evidence model without adjustment
- assuming internal enablement systems such as routing, evaluation, or monitoring do not count as use cases
- copying customer-facing patterns into internal systems, or internal patterns into customer-facing systems, without adjusting the control model

## Decision Reminder

| Smell | Safer correction |
| --- | --- |
| The proposal starts with a vendor or model name | Restate the dominant work pattern and failure consequence first |
| The initiative mixes search, automation, and decision support in one label | Split the use-case family and assign separate owners or review steps |
| The team wants one approval model for all AI systems | Match approval strength to autonomy, consequence, and boundary sensitivity |
| The platform plan ignores exit or portability | Make dependency concentration explicit before rollout |

Back to [5.2 Applying Use-Case Portfolios](05-02-00-applying-use-case-portfolios.md).
