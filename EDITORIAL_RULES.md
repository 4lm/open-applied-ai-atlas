# Editorial Rules

## Core Standard

Open Applied AI Atlas should read like maintained public documentation with a clear numbered outline and an equally clear mission. Each chapter is a navigable sequence of numbered files, but the numbered structure must serve the repository purpose: broad applied organizational AI and ML, practical implementation, and explicit treatment of openness, sovereignty, portability, privacy, compliance, and vendor dependence.

## Structure Rules

- Every chapter folder starts with a chapter front door file named `CC-00-00-<chapter-slug>.md`.
- The chapter front door is a real chapter outline, not the place where most of the chapter substance lives.
- Section overview files use `CC-SS-00-<section-slug>.md`.
- Subchapter files use `CC-SS-TT-<subchapter-slug>.md`.
- The maximum depth is chapter + two subchapter levels.
- Every file starts with a numbered H1 such as `# 2. Taxonomy`, `# 2.1 Classification Foundations`, or `# 2.1.1 Entity Classes And Core Distinctions`.

## Writing Rules

- Use prose for explanation and narrative framing.
- Use bullets for takeaways, heuristics, steps, and anti-patterns.
- Use diagrams & graphs (inline Mermaid format) for structure, flow, and sequence where visuals help.
- Use tables for inventories and comparison surfaces when comparison is truly the point.
- Do not overload chapter index files with content that belongs in numbered subchapter files.
- Chapter front matter must preserve mission, audience, and applied context instead of collapsing into generic documentation boilerplate.

## Mission And Coverage Rules

- The atlas is not LLM-only unless a file is intentionally model-specific.
- The atlas should remain useful across business, engineering, governance, privacy, security, sourcing, and leadership roles.
- Openness, sovereignty, portability, privacy, compliance, and lock-in should be explicit when they materially shape the decision.
- Chapters `2`, `4`, `6`, `17`, `18`, and `20` should make those cross-cutting concerns especially visible.

## Taxonomy And Classification

- Reuse canonical terms from [2. Taxonomy](docs/02-taxonomy/02-00-00-taxonomy.md).
- Distinguish vendors, projects, tools, standards, laws, regulations, patterns, and architectures.
- Apply openness-policy tiers only to solution-bearing entries where they fit.
- Keep visible numbering and chapter titles aligned with filenames and links.
