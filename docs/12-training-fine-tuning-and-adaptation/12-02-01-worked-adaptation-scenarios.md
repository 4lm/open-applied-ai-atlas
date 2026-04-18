# 12.2.1 Worked Adaptation Scenarios

This subsection turns the chapter into concrete organizational situations so the abstractions can be checked against real delivery contexts.

These examples turn the chapter into concrete organizational situations. They are deliberately short and comparative so the reader can see where the chapter changes a real decision.

## Prompt-first stabilization

A team fixes task behavior with prompt structure and workflow constraints before considering fine-tuning.

- What this example makes visible: compares how AI systems are adapted over time, from prompting and retrieval to fine-tuning and classical retraining, with emphasis on cost, governance, and QA burden.
- What to watch for: The failure mode is assuming stronger adaptation is always better.

## Retrieval before training

A knowledge-heavy system improves freshness by fixing retrieval instead of retraining weights.

- What this example makes visible: compares how AI systems are adapted over time, from prompting and retrieval to fine-tuning and classical retraining, with emphasis on cost, governance, and QA burden.
- What to watch for: The failure mode is solving a data freshness problem with model changes.

## Fine-tuning for repeatable specialization

A team fine-tunes only after repeated evidence shows retrieval and prompting are not enough.

- What this example makes visible: compares how AI systems are adapted over time, from prompting and retrieval to fine-tuning and classical retraining, with emphasis on cost, governance, and QA burden.
- What to watch for: The failure mode is skipping the evidence threshold.

## Predictive retraining loop

A classical model is retrained because data distribution shifted, with change control and QA updated accordingly.

- What this example makes visible: compares how AI systems are adapted over time, from prompting and retrieval to fine-tuning and classical retraining, with emphasis on cost, governance, and QA burden.
- What to watch for: The failure mode is treating ML retraining as separate from the broader adaptation governance story.

Back to [12.2 Operating Adaptation Work](12-02-00-operating-adaptation-work.md).
