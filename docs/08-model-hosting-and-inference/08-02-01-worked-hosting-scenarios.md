# 8.2.1 Worked Hosting Scenarios

_Page Type: Worked Example | Maturity: Outline_

This subsection turns the chapter into concrete organizational situations so the abstractions can be checked against real delivery contexts.

## Public API experimentation

A low-risk team begins with managed vendor inference for speed while keeping the boundary explicit.

- What this example makes visible: compares where models run, how inference is operated, and what trade-offs emerge across sovereignty, support burden, cost, and performance.
- What to watch for: The mistake is allowing early convenience to silently define the long-term architecture.

## Dedicated managed service rollout

A platform team accepts managed hosting with stronger tenancy control while keeping observability and export needs explicit.

- What this example makes visible: compares where models run, how inference is operated, and what trade-offs emerge across sovereignty, support burden, cost, and performance.
- What to watch for: The mistake is assuming dedicated managed equals full private control.

## Open-weight self-hosting

A team self-hosts for portability and private processing, then discovers the need for stronger monitoring and release discipline.

- What this example makes visible: compares where models run, how inference is operated, and what trade-offs emerge across sovereignty, support burden, cost, and performance.
- What to watch for: The mistake is underestimating the operator burden.

## Air-gapped deployment review

A regulated environment tests whether offline operations are viable without losing required functionality.

- What this example makes visible: compares where models run, how inference is operated, and what trade-offs emerge across sovereignty, support burden, cost, and performance.
- What to watch for: The mistake is choosing air-gap language without validating the real operational workflow.

Back to [8.2 Operating Hosting And Inference](08-02-00-operating-hosting-and-inference.md).
