# 15.2.2 Patterns And Anti-Patterns

_Page Type: Reference Sheet | Maturity: Draft_

Use this page during rollout review, abuse-response design, and control-model changes to recognize healthy security operating shapes before teams mistake a red-team exercise, a prompt filter, or a vendor safety claim for real containment.

## Reusable Security Patterns

| Pattern | What good looks like | Fit signal | Review warning |
| --- | --- | --- | --- |
| Deny-by-default tool and action posture | The service exposes only the smallest approved action set, every action path has explicit preconditions, approvals are logged, and dangerous capabilities can be disabled without full redeploy | the system can create records, send messages, call APIs, or trigger workflows with real side effects | reviewers can see which tools exist, but cannot show which actions are blocked, who approves the rest, or how emergency disablement works |
| Typed memory with security and retention boundaries | Persistent state is deliberately minimal, field-typed, role-scoped, and linked to deletion plus review rules so memory does not become an ungoverned authority store | assistants or agents keep cross-session preferences, workflow state, or user-authored notes | memory is described as "helpful context," but nobody can list which fields are allowed, how long they persist, or which writes are rejected |
| Abuse testing tied to the live control surface | Prompt abuse, retrieval attacks, tool misuse, privilege drift, and provider egress cases are tested against the real production shape rather than a simplified demo path | the service depends on gateways, tools, external content, or multiple approval layers | security testing exists, but it covers only prompt wording while real route, identity, or side-effect boundaries stay untested |
| Containment-first incident path with linked evidence | Investigators can reconstruct the request, policy path, tool attempt, approval outcome, provider route, and containment action from one incident packet | the system spans application logs, gateway controls, provider APIs, and human approvals | the team has alerts and screenshots, but cannot prove what happened quickly enough to disable the risky path |
| Shared-control review with explicit vendor-boundary ownership | Local teams know which protections live in the application, gateway, model host, and provider layers, and can export evidence or degrade safely if one layer changes | managed gateways, hosted models, SaaS safety features, or external plugins mediate critical control points | the design depends on vendor-only rules or consoles, but nobody owns export tests, fallback posture, or residual lock-in risk |

## Security Anti-Patterns

| Anti-pattern | Why it fails | Early signal | Review action |
| --- | --- | --- | --- |
| Prompt-filter theater | filtering prompts or outputs helps, but it does not contain broad permissions, weak identity boundaries, or unsafe tools | security discussion keeps returning to prompt rules while tool grants, routes, or approvals remain vague | reopen foundations in `15.1`, then require explicit action, identity, and rollback controls before rollout expands |
| Broad service credentials hidden behind agent polish | a well-behaved demo does not make a high-authority runtime safe when the underlying credentials can perform too much | the agent "can do many useful things," but the permission manifest is missing or largely unrestricted | freeze new tool rollout, narrow credentials, and require deny-by-default manifests plus disablement drills |
| Memory and logging sprawl justified as investigation support | indiscriminate retention increases secret exposure, privacy risk, and long-lived authority while still failing to create usable incident proof | the team asks to keep more prompts, retrieved passages, or user state because the structured evidence path is too thin | redesign memory and telemetry with chapter handoffs to `06`, `11`, and `14` before granting broader retention |
| Red-team theater with no release consequence | isolated attack exercises create little security value if unresolved failures do not block launch or reopen adjacent review | a red-team slide deck exists, but there is no owner, fix plan, or acceptance record for open findings | convert the exercise into a reusable abuse-test pack with named blockers, owners, and retest criteria |
| Vendor-opaque containment | incident response fails when key policy decisions, abuse signals, or route outcomes live only in one provider console or managed service | support, security, and platform teams each have partial logs, but nobody can produce one portable incident timeline | document the shared-control dependence, add export drills, and reopen chapters `09`, `14`, and `18` if portability remains weak |

## Review Prompts

- Which operating pattern carries the most security weight here: deny-by-default actions, typed memory, live-surface abuse testing, linked containment evidence, or shared-control review?
- Which artifact proves the service can be contained quickly: tool manifest, kill-switch drill, memory schema, route-policy export, or provider exception register?
- Where would an investigator look first to explain a harmful output or side effect, and would that evidence still exist if one vendor console were unavailable?
- Which adjacent chapter must re-enter before rollout widens: `06`, `09`, `10`, `11`, `14`, `16`, or `18`?

## Re-Review Triggers

- a new tool, permission, background workflow, or external integration is added without retesting abuse paths and disablement steps
- memory begins storing new role-sensitive, customer, or policy-governing state that changes retention or deletion risk
- provider routing, gateway policy, or managed safety controls change in ways that alter which layer owns enforcement or evidence
- incident response depends on wider access to prompts, retrieved content, or raw payloads because the structured review packet no longer answers routine questions
- unresolved abuse findings are accepted temporarily, but rollout scope, audience, geography, or action authority keeps expanding anyway

## Practical Reading Rule

Use these patterns after the trust boundary is understood but before the operating model is treated as safe. If the team cannot show how risky actions stay narrow, how memory stays governable, how abuse tests match the real service shape, and how incidents can be contained across vendor boundaries, the security design is not finished.

Back to [15.2 Operating Security And Abuse Resistance](15-02-00-operating-security-and-abuse-resistance.md).
