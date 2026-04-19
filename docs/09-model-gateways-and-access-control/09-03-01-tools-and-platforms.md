# 9.3.1 Tools And Platforms

_Page Type: Comparison Page | Maturity: Draft_

This file compares the control-plane tools that sit between applications, models, identities, and policies. It includes AI-native gateways, general API gateways adapted to AI traffic, and adjacent access-control layers because gateway value depends on the policy and identity systems around it.

## How To Use This File

- Read the tables as comparison surfaces, not as universal rankings.
- Separate routing convenience from governance quality; a gateway without identity, policy, and evidence design is just another proxy.
- Check `06`, `14`, `15`, and `18` before treating a gateway as a simple provider-switching feature.

## AI-Native Gateways And Control Planes

These entries matter when organizations need model routing, spend control, prompt and response policy hooks, or centralized AI usage visibility.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [LiteLLM](https://docs.litellm.ai/) | Open-source project | Model gateway and abstraction layer | Preferred | Fully open source | Self-hosted or managed | Multi-provider developer and platform use | Needs internal policy design and operational hardening | [Docs](https://docs.litellm.ai/) |
| [Envoy AI Gateway](https://aigateway.envoyproxy.io/) | Open-source project | AI-aware API gateway | Preferred | Open source | Self-hosted | Organizations standardizing on Envoy-style gateway patterns | Requires internal engineering and policy design maturity | [Docs](https://aigateway.envoyproxy.io/) |
| [Kong AI Gateway](https://developer.konghq.com/ai-gateway/) | Gateway capability | Policy and routing layer | Acceptable | Open core / commercial ecosystem | Self-managed or enterprise-managed | Enterprises already using Kong for API control | Policy logic can become tied to Kong ecosystem choices | [Docs](https://developer.konghq.com/ai-gateway/) |
| [Portkey](https://portkey.ai/) | Product | AI gateway and observability | Controlled Exception | Proprietary service | Managed | Central routing, governance, and usage analysis | Shared control plane becomes a strategic dependency | [Portkey](https://portkey.ai/) |
| [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/) | Managed capability | AI request gateway | Controlled Exception | Proprietary service | Managed edge platform | Edge-centric governance, caching, and logging | Strong dependence on Cloudflare edge estate | [Docs](https://developers.cloudflare.com/ai-gateway/) |
| [Helicone](https://docs.helicone.ai/) | Product / project | Gateway plus usage telemetry | Acceptable | Open source / commercial ecosystem | Self-hosted or managed | Teams needing request-level visibility and controls | Governance quality depends on deployment and policy maturity | [Docs](https://docs.helicone.ai/) |
| [Tyk AI Studio](https://tyk.io/) | Gateway platform capability | Open-core AI control plane | Acceptable | Open core / commercial ecosystem | Self-hosted, hybrid, or managed | Organizations wanting stronger deployment control than pure SaaS AI gateways | Product breadth can pull teams into wider Tyk platform choices | [Tyk](https://tyk.io/) |

## Enterprise API Gateways Extended To AI Traffic

These entries matter when the organization already has a general API governance layer and wants to extend it to model access rather than introducing a separate AI-specific proxy immediately.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Azure API Management](https://learn.microsoft.com/azure/api-management/) | Managed gateway platform | Enterprise API control layer adaptable to AI traffic | Controlled Exception | Proprietary service | Managed | Existing Azure estates extending shared policy control | Not AI-native by itself; more assembly required | [Docs](https://learn.microsoft.com/azure/api-management/) |
| [Apigee](https://cloud.google.com/apigee) | Managed API platform | Enterprise API policy and mediation | Controlled Exception | Proprietary service | Managed | GCP-centered organizations extending existing API governance to AI endpoints | Strong fit assumes broader Google Cloud API estate | [Apigee](https://cloud.google.com/apigee) |
| [Amazon API Gateway](https://aws.amazon.com/api-gateway/) | Managed API platform | Shared API control plane adaptable to AI traffic | Controlled Exception | Proprietary service | Managed | AWS estates centralizing auth, throttling, and exposure policies | Requires additional AI-specific controls and observability design | [AWS](https://aws.amazon.com/api-gateway/) |
| [Tyk Gateway](https://docs.tyk.technology/tyk-oss-gateway) | Open-source gateway | General API gateway reusable for AI traffic | Preferred | Open source / commercial ecosystem | Self-hosted or managed companion platform | Teams that want self-hosted gateway control with broader API needs | AI-specific semantics still need added policy and telemetry layers | [Docs](https://docs.tyk.technology/tyk-oss-gateway) |
| [Gravitee API Gateway](https://www.gravitee.io/platform/api-gateway) | API gateway platform | Policy and mediation layer adaptable to AI traffic | Acceptable | Open core / commercial ecosystem | Self-hosted or managed | Enterprises already running Gravitee for API governance | AI-native features are weaker than dedicated AI gateway products | [Gravitee](https://www.gravitee.io/platform/api-gateway) |

## Identity, Policy, And Access Enforcement Layers

These systems matter because the gateway is only as strong as the identity and policy material it can enforce.

| Name | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best-fit use cases | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Open Policy Agent](https://www.openpolicyagent.org/) | Open-source project | Policy-as-code enforcement | Preferred | Open source | Self-hosted | Shared authorization and policy enforcement around AI systems | Not AI-native; requires explicit integration | [OPA](https://www.openpolicyagent.org/) |
| [Keycloak](https://www.keycloak.org/) | Open-source identity platform | Identity, SSO, and access federation | Preferred | Open source | Self-hosted | Self-managed identity and access control around gateways and internal AI apps | Identity control alone does not solve model policy, logging, or routing needs | [Keycloak](https://www.keycloak.org/) |
| [Okta](https://www.okta.com/) | Identity platform | Enterprise identity and access management | Controlled Exception | Proprietary platform | Managed | Centralized identity for managed AI and application estates | Managed identity concentration can become structural | [Okta](https://www.okta.com/) |
| [Auth0](https://auth0.com/) | Identity platform | Application identity and authorization | Controlled Exception | Proprietary platform | Managed | Application-facing access control for external and internal AI products | Managed control-plane dependence remains material | [Auth0](https://auth0.com/) |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [9.3 Reference Points](09-03-00-reference-points.md).
