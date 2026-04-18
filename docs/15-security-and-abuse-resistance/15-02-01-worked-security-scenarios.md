# 15.2.1 Worked Security Scenarios

This subsection turns the chapter into concrete organizational situations so the abstractions can be checked against real delivery contexts.

These examples turn the chapter into concrete organizational situations. They are deliberately short and comparative so the reader can see where the chapter changes a real decision.

## Prompt-injection-resistant assistant

A team limits context scope and treats retrieval results as untrusted input.

- What this example makes visible: covers AI-specific threat surfaces, misuse patterns, and defensive controls across prompts, retrieval, tools, memory, gateways, and operating environments.
- What to watch for: The failure mode is assuming the prompt boundary is enough protection.

## Tool-using workflow hardening

A workflow is given narrow tools and explicit approvals before it is allowed to affect external systems.

- What this example makes visible: covers AI-specific threat surfaces, misuse patterns, and defensive controls across prompts, retrieval, tools, memory, gateways, and operating environments.
- What to watch for: The failure mode is broad capability grants for convenience.

## Memory retention risk review

A team rethinks persistent memory because it becomes a source of sensitive state and permission drift.

- What this example makes visible: covers AI-specific threat surfaces, misuse patterns, and defensive controls across prompts, retrieval, tools, memory, gateways, and operating environments.
- What to watch for: The failure mode is treating memory as harmless personalization.

## Gateway-centered abuse investigation

Abuse review uses gateway, route, and policy traces together rather than only application logs.

- What this example makes visible: covers AI-specific threat surfaces, misuse patterns, and defensive controls across prompts, retrieval, tools, memory, gateways, and operating environments.
- What to watch for: The failure mode is splitting the security story across tools that do not line up.

Back to [15.2 Operating Security And Abuse Resistance](15-02-00-operating-security-and-abuse-resistance.md).
