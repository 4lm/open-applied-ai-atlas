# 14.2.1 Worked Monitoring Scenarios

_Page Type: Worked Example | Maturity: Outline_

This subsection turns the chapter into concrete organizational situations so the abstractions can be checked against real delivery contexts.

## Internal assistant trace design

A team captures prompt, route, and citation metadata but redacts sensitive content and limits access.

- What this example makes visible: covers the runtime visibility needed to reconstruct what happened in AI systems while balancing privacy, retention, cost, and investigative usefulness.
- What to watch for: The failure mode is either logging too little to investigate or too much to govern safely.

## Agent execution incident review

Step traces and approval events make a multi-step failure understandable after the fact.

- What this example makes visible: covers the runtime visibility needed to reconstruct what happened in AI systems while balancing privacy, retention, cost, and investigative usefulness.
- What to watch for: The failure mode is having only final output logs.

## Observability export review

A platform team tests whether logs and traces can leave a vendor silo before adopting it broadly.

- What this example makes visible: covers the runtime visibility needed to reconstruct what happened in AI systems while balancing privacy, retention, cost, and investigative usefulness.
- What to watch for: The failure mode is accepting visibility today at the cost of portability tomorrow.

## Replay-safe support workflow

A team designs structured traces so incidents can be replayed or inspected without exposing raw sensitive data broadly.

- What this example makes visible: covers the runtime visibility needed to reconstruct what happened in AI systems while balancing privacy, retention, cost, and investigative usefulness.
- What to watch for: The failure mode is making investigation depend on unrestricted access to raw requests.

Back to [14.2 Operating Observability](14-02-00-operating-observability.md).
