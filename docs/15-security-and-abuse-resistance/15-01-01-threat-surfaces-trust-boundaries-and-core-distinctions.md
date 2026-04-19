# 15.1.1 Threat Surfaces, Trust Boundaries, And Core Distinctions

_Page Type: Concept Explainer | Maturity: Draft_

Use this page to separate the threat surfaces that are usually collapsed into one vague "AI security" bucket. Security review gets weaker fast when prompt abuse, retrieval poisoning, tool misuse, memory leakage, provider dependence, and software supply-chain risk are treated as one interchangeable problem just because a model sits in the middle.

## Threat-Surface Map

| Threat surface | Primary boundary crossing | What fails when it is misclassified | First control question |
| --- | --- | --- | --- |
| User input and prompt handling | untrusted instructions or content crossing into model or workflow context | teams optimize for content filtering alone and miss privilege, action, or evidence failures | what can untrusted input influence directly: generation only, routing, tool calls, approvals, or stored state? |
| Retrieval and external content intake | documents, search results, or third-party records entering the decision path | retrieved text is treated as trusted policy or authority instead of as untrusted evidence | how is retrieved content separated from system instructions, and who can trace which source changed the answer or action? |
| Tool and action execution | model or workflow output crossing into systems with real side effects | harmless-looking assistant logic becomes an automation channel for ticket, message, payment, or data changes | which actions are allowed, what preconditions exist, and what remains reversible if the model is wrong or manipulated? |
| Memory and persistent state | transient interaction becoming durable cross-session state | sensitive facts, stale permissions, or risky user instructions quietly become long-lived operating context | what may be stored, for how long, by whose authority, and how is deletion or correction proved? |
| Identity, secrets, and provider routing | credentials, tokens, routes, or tenant boundaries deciding what the system may access | teams rely on prompt rules while the real risk sits in broad API keys, weak impersonation controls, or opaque provider routing | which identity actually performs the action, and can the organization prove or revoke that authority quickly? |
| Model, platform, and artifact supply chain | external models, plugins, packages, containers, or serialized artifacts entering runtime | the system inherits malicious code, unsafe defaults, or unverifiable provenance through dependencies rather than prompts | what is being trusted from outside the team, and what signing, scanning, or provenance evidence exists before release? |

## Core Distinctions

| Distinction | Why it changes the control design |
| --- | --- |
| Prompt abuse vs. authorization failure | A filtered prompt can still cause damage if the system identity, tool grants, or approval path are too broad. |
| Content risk vs. action risk | Wrong text is serious, but a wrong state change, outbound message, or system update usually needs stricter gating and rollback. |
| Model safety behavior vs. surrounding application security | Provider-side safety features do not replace local controls over retrieval, tools, secrets, tenancy, and audit evidence. |
| Untrusted retrieved content vs. trusted internal policy | Internal documents and search hits may be authentic records while still being unsafe to treat as executable instruction. |
| Ephemeral context vs. durable state | A risky answer in one session is different from storing the same content as memory, profile data, or workflow state that persists. |
| Prevention controls vs. containment and recovery | Detection and guardrails matter, but teams also need disablement paths, rollback, and incident reconstruction when prevention fails. |
| Vendor attestations vs. portable security evidence | Managed-platform assurances help, but release and audit review still need exportable logs, ownership clarity, and exit-safe control records. |

## What These Distinctions Change In Practice

- Threat-model the real crossings in the workflow: user input, retrieved content, model output, tool invocation, approval, stored state, and provider egress should appear as separate review lanes.
- Make tool permissions and system identities narrow by default. If a model can trigger irreversible or high-authority actions, the security question is no longer "is the prompt safe?" but "is the authority bounded and reviewable?"
- Treat retrieval results, memory recalls, and prior conversation content as untrusted inputs unless a separate control proves they are safe to elevate into policy or action context.
- Require containment plans alongside preventive controls: emergency disablement, route shutdown, key rotation, rollback, and evidence preservation should exist before rollout expands.
- Test exportability and reconstruction early when managed providers or security platforms mediate the traffic, because incident response fails when only the vendor can explain what happened.
- Keep privacy, sovereignty, and lock-in visible: the safest-looking security layer may still be unacceptable if it centralizes sensitive traces, blocks deletion handling, or makes provider exit unrealistic.

## Reviewer Checks

- Which boundary crossing carries the highest authority: answer generation, retrieval choice, tool execution, stored state, provider routing, or operator override?
- Where is the team relying on one broad guardrail story instead of naming separate controls for prompts, retrieval, tools, memory, and supply chain?
- Can the organization reconstruct an abuse incident across gateway, application, provider, and human approval layers without unrestricted raw-content access?
- Which secrets, identities, or delegated permissions would remain dangerous even if the prompt-defense stack worked exactly as designed?
- If the current provider, plugin, or model artifact had to be removed tomorrow, what evidence would still prove the system boundary and recent incidents?

## Practical Reading Rule

Classify the boundary first, then choose the default hardening lane in [15.1.2 Decision Boundaries And Hardening Heuristics](15-01-02-decision-boundaries-and-hardening-heuristics.md). If the team still cannot say which crossings are read-only, which are action-capable, which create durable state, and which depend on vendor-only controls, the security design is not ready for release review yet.

Back to [15.1 Security Foundations](15-01-00-security-foundations.md).
