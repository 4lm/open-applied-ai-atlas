# 1.3.1 Root Docs And Topic Chapters

_Page Type: Concept Explainer | Maturity: Draft_

The root of the repository is for repository-level guidance. The `docs/` directory is for topic-level knowledge.

This distinction layer matters because the chapter on scope and principles is only useful if readers can separate the recurring categories, responsibilities, or evidence types that would otherwise blur together. The atlas uses distinctions like this to keep comparison rigorous and to stop local shorthand from hiding governance, sourcing, or operational consequences.

## Why These Distinctions Matter

The practical question is not whether the labels are elegant. The practical question is whether the distinctions change how a team designs, reviews, buys, operates, or audits a system. In this chapter, that means checking whether the topic is being reasoned about in the right layer and with the right cross-cutting lenses still visible.

## Repository Layers

| Area | Purpose |
| --- | --- |
| `README.md` | Mission-led one-pager and main entry point |
| `AGENTS.md`, `CONTRIBUTING.md`, `EDITORIAL_RULES.md` | Durable working, contribution, and editorial rules |
| `CHANGELOG.md`, `LICENSE`, `CONTRIBUTORS.md` | Public release history, content licensing, and contributor attribution |
| `docs/` | Numbered chapter content for taxonomy, architecture, governance, sourcing, standards, and implementation |

## Practical Rule

If a piece of text explains how the repository should be maintained, it belongs at root. If it explains a topic in applied organizational AI/ML, it belongs in the numbered chapter system.

## Examples

| Put it at root | Put it in `docs/` |
| --- | --- |
| editorial rules, contribution workflow, changelog guidance | taxonomy, governance, use cases, sourcing, standards, and architecture content |
| durable agent instructions | topic comparisons, worked scenarios, and implementation guidance |

## What Reviewers Should Check

- Are the distinctions here still connected to the chapter's real decision surface rather than being treated as abstract categories?
- Is the proposal using these distinctions to expose trade-offs in control, evidence, ownership, or lock-in?
- Does the chapter language stay consistent with the atlas taxonomy instead of introducing new local categories without need?

## Practical Reading Rule

Use this file to sharpen the chapter, not to replace it. If a proposal still sounds plausible after the distinctions here are applied, it is usually ready to move into heuristics, scenarios, or reference material. If it falls apart, the distinction work has already paid for itself.

Back to [1.3 Repository Contract](01-03-00-repository-contract.md).
