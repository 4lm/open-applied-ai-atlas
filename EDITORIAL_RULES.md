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

## Structural Triage Rules

Use these tests before creating, keeping, merging, or splitting numbered pages. Structural change should improve reader value and chapter fit, not preserve outline symmetry.

### Reader-Job Test For Keeping A Standalone Page

A page deserves to stand alone only if all of these are true:

- it serves a distinct reader question, task, or decision that adjacent pages do not already cover well
- it can explain why that job belongs in this chapter and why a subsection or cross-reference would not be enough
- it has enough substance to be more than a thin preface, symmetry placeholder, or local note
- readers would lose clarity if the material were folded into the stronger neighboring page

If those conditions are not met, merge the material into the stronger adjacent page or keep it as a subsection instead of a standalone file.

### Overlap Test For When Two Pages Should Merge

Merge neighboring pages when any of these are true:

- they answer the same reader job with mostly the same distinctions, framing, or examples
- one page mainly restates the other with lighter detail or chapter-local synonyms
- the pair depends on constant cross-reference because neither page works well on its own
- one of the pages exists mainly to preserve outline symmetry rather than durable reader value

Keep pages separate only when the split makes navigation, comparison, or reader-role differences materially clearer.

### Overload Test For When One Page Should Split

Split a page when any of these are true:

- one file is trying to serve two or more distinct reader jobs or decision surfaces
- the page mixes unlike entity classes, evidence postures, or page types that need different framing
- readers must scan through long unrelated sections before finding the part they actually need
- one retained page can become a clearer anchor while the new page takes on a distinct, durable job

Do not split only to create symmetry, shorten a file mechanically, or preserve repeated stock intros. Both resulting pages must have distinct scope and enough substance to stand on their own.

## Writing Rules

- Use prose for explanation and narrative framing.
- Use bullets for takeaways, heuristics, steps, and anti-patterns.
- Use diagrams & graphs (inline Mermaid format) for structure, flow, and sequence where visuals help.
- Use tables for inventories and comparison surfaces when comparison is truly the point.
- Do not overload chapter index files with content that belongs in numbered subchapter files.
- Chapter front matter must preserve mission, audience, and applied context instead of collapsing into generic documentation boilerplate.
- Keep chapter and section overview pages concise; repeated stock framing should be removed rather than customized lightly.
- Every page in `docs/` should place a visible metadata line directly under the numbered H1 in this form: `_Page Type: … | Maturity: …_`.

## Page-Type System

- `Chapter Index`: chapter or section navigation with concise framing, not the main substance.
- `Concept Explainer`: definitions, distinctions, and conceptual framing.
- `Comparison Page`: tools, vendors, standards, projects, or options compared on reusable criteria.
- `Decision Guide`: heuristics, decision trees, selection rules, or boundary-setting guidance.
- `Worked Example`: scenario-based application of the chapter to a real organizational context.
- `Operational Artifact`: checklists, templates, matrices, review prompts, control artifacts, or reusable operating aids.
- `Reference Sheet`: compact reusable schema, rules, or comparison logic.
- `Glossary`: fast-reference terminology anchor.

## Maturity System

- `Outline`: structure exists, but content depth or trust coverage is still limited.
- `Draft`: useful material exists, but the page is incomplete, uneven, or lightly sourced.
- `Review-Ready`: coherent, substantial material ready for editorial review.
- `Curated Reference`: high-confidence, denser reference material with strong primary-source anchoring.

Assign maturity honestly. Do not use `Curated Reference` as a stylistic compliment.

## Comparison And Evidence Rules

- Comparison-heavy pages should reuse the canonical schema in [2.2.3 Comparison Schema](docs/02-taxonomy/02-02-03-comparison-schema.md).
- At minimum, comparison pages should make entity type, purpose, control posture, openness posture, lock-in note, and primary source visible.
- Add `## Evidence Notes` when a comparison page or standards-heavy page mixes direct facts with atlas synthesis or editorial judgment.
- Prefer primary sources for laws, regulations, standards, vendors, organizations, projects, and product claims.

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
