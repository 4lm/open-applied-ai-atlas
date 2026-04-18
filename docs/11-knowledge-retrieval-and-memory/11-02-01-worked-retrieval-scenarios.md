# 11.2.1 Worked Retrieval Scenarios

_Page Type: Worked Example | Maturity: Review-Ready_

Use these scenarios to test whether the team is solving a retrieval problem, a memory problem, or a governance problem wearing a retrieval label. Each scenario is intentionally framed around the dominant decision, the recommended posture, and the evidence outputs that should exist before rollout.

## Internal Policy Assistant

| Field | Decision |
| --- | --- |
| Context | An internal assistant answers HR, security, and operating-policy questions from documents that change regularly and have named owners |
| Dominant question | Should the system rely on live retrieval, persistent memory, or model adaptation for policy answers? |
| Recommended posture | Live retrieval from owned sources, minimal session state, no long-lived memory for policy facts |
| Why | Policy answers go stale quickly, are often permission-sensitive, and must be traceable to a current source rather than remembered from a previous interaction |
| Evidence and control outputs | source inventory, refresh cadence, citation behavior check, stale-content test set, owner escalation path |
| Watch for | Persisting policy answers as convenience memory, indexing unofficial copies, or treating citation text as proof that freshness is handled |
| Adjacent chapters | `06`, `13`, `16` |

## Personalized Support Workspace

| Field | Decision |
| --- | --- |
| Context | A customer-support workflow wants to retain user preferences, account context, and prior interaction summaries to reduce repeated questioning |
| Dominant question | What should be remembered across sessions, and what should still be retrieved from the system of record each time? |
| Recommended posture | Bounded user memory for preferences and approved summaries, live retrieval for entitlements, balances, orders, and policy-bound account data |
| Why | Preferences and workflow continuity may benefit from persistence, but operational facts and permissions change too often to trust memory alone |
| Evidence and control outputs | retention policy, deletion flow, user-memory schema, permission-inheritance check, revalidation rules for account facts |
| Watch for | Storing sensitive facts in free-form memory, failing to separate user preference from regulated account data, or skipping deletion and subject-access handling |
| Adjacent chapters | `06`, `13`, `15`, `16` |

## Relationship-Heavy Engineering Knowledge Layer

| Field | Decision |
| --- | --- |
| Context | An engineering organization needs answers across service ownership, dependency chains, runbooks, and incident history where entity relationships matter more than isolated documents |
| Dominant question | Is semantic search enough, or does the system need structured or graph-backed retrieval to preserve operational relationships? |
| Recommended posture | Hybrid retrieval: semantic search for broad discovery plus structured metadata or graph traversal for ownership, dependency, and escalation paths |
| Why | Pure vector retrieval may surface relevant fragments, but operations questions often depend on explicit relationships, canonical IDs, and source hierarchy |
| Evidence and control outputs | entity model, indexing rules for structured fields, relationship coverage tests, provenance display, fallback path when the graph is incomplete |
| Watch for | Treating every knowledge problem as chunk search, losing source hierarchy during ingestion, or assuming a graph removes the need for source quality controls |
| Adjacent chapters | `03`, `10`, `14`, `19` |

## Permission-Sensitive Research Repository

| Field | Decision |
| --- | --- |
| Context | A research or legal team wants cross-document question answering over mixed public, internal, and restricted material with sharply different access rights |
| Dominant question | Can indexing and retrieval preserve source permissions and revocation behavior well enough for safe self-service use? |
| Recommended posture | Permission-aware retrieval with document- and chunk-level access enforcement, explicit revocation handling, and conservative fallbacks when permission state is uncertain |
| Why | Relevance quality is secondary if the retrieval layer can leak restricted content or continue returning material after access is revoked |
| Evidence and control outputs | access-control mapping, revocation test cases, leakage eval set, re-index trigger rules, incident rollback plan |
| Watch for | Flattening permissions during ingestion, relying on front-end filtering after retrieval, or assuming embeddings are harmless once the source is restricted |
| Adjacent chapters | `06`, `14`, `15`, `18` |

## Reading Rule

If more than one scenario appears to fit, choose the posture that minimizes persistent state first, then justify every additional memory or indexing layer with a named owner, retention rule, and evaluation plan.

Back to [11.2 Operating Retrieval And Memory](11-02-00-operating-retrieval-and-memory.md).
