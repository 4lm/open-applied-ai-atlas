---
NEVER CHANGE THIS FILE.
---

# Open Applied AI Atlas

## Mission

Create an open knowledge-base repository named **Open Applied AI Atlas**.

Build it as a practical, taxonomy-driven, comparison-oriented, implementation-focused knowledge base for applying AI and ML in business, enterprise, public, nonprofit, and other organizational contexts of all sizes.

Do not limit scope to LLMs.

Treat AI systems as organizational systems, not isolated model demos.

Keep these concerns visible across the full stack:

- openness
- open source
- sovereignty
- portability
- privacy
- compliance
- lock-in
- buy-vs-build

## Instruction precedence

This file is the task-specific execution brief for the current run.

Follow it closely, but treat `AGENTS.md` as the durable source of truth for repository mission, structure, evidence, quality, and cleanup rules. If this file overlaps or conflicts with `AGENTS.md`, the newer `AGENTS.md` guidance wins.

Keep this file focused on the current delivery mission. Do not expand it into a parallel copy of repository-wide guidance unless that duplication is intentionally useful.

## Working order

1. read `AGENTS.md` first
2. read `README.md` and other root-level guidance before editing
3. read this local execution brief before planning or editing
4. understand repository structure, conventions, and adjacent-document context before making changes
5. prefer improving existing content and structure over adding parallel duplicates
6. reconcile links, numbering, titles, and neighboring documents before finishing
7. remove temporary artifacts, duplication, and stale scaffolding at the end

## Audience

Serve cross-functional implementers, reviewers, and decision-makers, including:

- product, project, business, and domain roles
- architecture and engineering roles
- ML, data, and platform roles
- QA, test, security, privacy, and GRC roles
- operations, sourcing, procurement, leadership, and organizational decision-makers

Representative roles include:

- product managers
- project managers
- business analysts
- domain experts
- enterprise architects
- AI architects
- software architects
- developers
- ML engineers
- data engineers
- platform engineers
- QA and test engineers
- security professionals
- privacy professionals
- governance, risk, and compliance professionals
- IT operations
- platform operations
- procurement and sourcing
- technical leadership
- organizational decision-makers

## Scope

Cover applied organizational AI and ML broadly, including:

- chat systems
- copilots
- coding assistants
- coding agents
- workflow agents
- document intelligence
- retrieval systems
- memory systems
- forecasting
- recommender systems
- anomaly detection
- optimization systems
- computer vision
- speech systems
- classical ML
- deep learning
- generative AI
- hybrid systems
- fine-tuning
- training systems

## Recurring priorities

Keep these visible throughout:

- open knowledge
- open source
- open governance
- open tooling
- open standards
- open research
- practical implementation guidance
- shared taxonomy
- prose for explanation and narrative framing.
- selected comparison tables
- selected diagrams & graphs (inline Mermaid format)
- selected bullet lists
- explicit trade-off framing
- sovereignty
- portability
- privacy
- vendor lock-in
- buy-vs-build
- compliance-aware implementation

Treat these frameworks as especially relevant where applicable:

- EU AI Act
- EU Data Act
- GDPR
- ISO/IEC 42001
- ISO/IEC 23894
- NIST AI RMF

## Navigation model

Make the atlas usable this way:

- start from mission and decision spine
- move sideways into layers matching role and problem

Reflect this in `README.md` and the `docs/` structure.

## Goals

Must:

1. create a serious, scalable knowledge repository
2. make taxonomy first-class
3. keep layers clearly separated
4. cover worker-level and organization-level AI use cases
5. make openness, sovereignty, compliance, portability, lock-in, and enterprise readiness explicit comparison dimensions
6. keep `README.md` navigational and push depth into `docs/`
7. support orientation, comparison, and decision-making
8. support high-quality future contributions by humans and coding agents

## Non-goals

Do not create:

- a generic link dump
- an “awesome list”
- hype or marketing copy
- an LLM-only repository
- mixed categories without taxonomy
- long prose essays with weak comparison structure
- duplicate topic files across root and `docs/`
- temporary scaffolding or internal planning artifacts in the final public repo unless intentionally retained

## Operating principles

Must:

1. prefer structure over verbosity
2. prefer reusable tables where comparison matters
3. use neutral, primary-source-oriented wording
4. keep categories distinct
5. optimize for comparability over raw completeness
6. stay readable across leadership and implementation roles
7. treat openness and open source as first-class evaluation dimensions
8. define shared taxonomies once and reuse them
9. keep intros short
10. mark unknowns explicitly
11. use the format that best serves the content
12. make each substantive page's primary purpose obvious from its structure
13. prefer fewer strong pages over many weak pages
14. reduce repetition and generic boilerplate
15. increase information density where pages are thin
16. preserve consistency with adjacent documents
17. do not create filler content just to preserve symmetry

## Repository structure

Create at least these root files:

- `README.md`
- `LICENSE`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `EDITORIAL_RULES.md`

Create:

- `docs/` with one Markdown file per major topic

Rules:

- keep repository-level process, editorial, licensing, and implementation-control files in root
- keep topic content in `docs/`
- do not duplicate topic files between root and `docs/`
- keep the canonical taxonomy file in `docs/02...`
- make the final repo feel like a coherent public knowledge product, not a scratch workspace
- follow existing repository naming, numbering, and placement conventions
- preserve ordered chapter and section models where they already exist
- keep headings, filenames, and internal references aligned
- update affected references and backlinks when files move or rename
- do not copy root guidance into topical documents unless that duplication is intentionally useful

## License

Use a **Creative Commons** content license.

Default to:

- **CC BY 4.0**

The `LICENSE` file must reflect a Creative Commons content license, not a software-only license.

## README contract

`README.md` must serve as:

- landing page
- navigation surface
- conceptual overview
- editorial promise
- decision spine

Do not turn `README.md` into the main content dump.

## Topic file contract

Each major file in `docs/` must, where relevant, contain:

1. title
2. short intro
3. why this chapter exists
4. included / excluded scope
5. classification / taxonomy tables
6. landscape / comparison tables
7. decision-support tables
8. cross-links to adjacent docs
9. open questions / future extensions

Rules:

- use Markdown
- optimize for scanability via headings and tables
- do not leave thin placeholders
- choose the format that best serves the page purpose
- use prose for explanation and narrative framing
- use bullets for distinctions, heuristics, and concise guidance
- use tables for real comparison work, not decoration
- use checklists, scorecards, decision trees, diagrams, worked examples, and reference structures when they improve practical usefulness

A topic file is acceptable only if it has:

- real scope
- at least one taxonomy table where relevant
- at least one comparison or landscape table
- at least one decision-support table
- adjacency cross-links
- relevant cross-cutting treatment of open source, sovereignty, lock-in, privacy, compliance, and operational maturity where applicable
- a clear primary purpose such as navigation, explainer, comparison, decision guide, worked example, operational artifact, reference sheet, or glossary

## Global taxonomy

Define one reusable global taxonomy.

Reuse it consistently across the repository.

At minimum include these taxonomy families:

1. openness
2. open source posture
3. sovereignty
4. compliance and assurance
5. enterprise readiness
6. AI method type
7. use-case mode
8. risk sensitivity
9. human oversight level
10. hosting control
11. lock-in / portability
12. data sensitivity
13. organizational entity type

Relevant dimensions may include:

- license openness
- open source status
- weights openness
- training pipeline openness
- hosting freedom
- deployment control
- data residency control
- auditability
- traceability
- policy enforcement support
- operational maturity
- business criticality
- autonomy level
- risk level
- portability
- dependency concentration
- vendor lock-in mode

Do not redefine taxonomy independently per file.

## Use-case coverage

Cover both organizational and worker-level AI use cases.

At minimum include these families:

1. knowledge work assistance
2. software and IT engineering
3. business process automation
4. decision support
5. customer-facing AI
6. operations and back office
7. domain-specific intelligence
8. agentic task execution
9. retrieval, memory, and organizational knowledge systems
10. AI production systems such as evaluation, training, fine-tuning, routing, and policy enforcement

Representative examples must include:

- enterprise chat assistants
- internal knowledge assistants
- coding assistants
- coding agents
- workflow agents
- document processing
- forecasting
- recommendation systems
- anomaly detection
- computer vision inspection
- compliance assistants
- QA/test generation
- enterprise search
- RAG systems
- model evaluation pipelines
- observability / monitoring systems

## Section ordering

Model AI implementation top-to-bottom in roughly this order:

1. governance, GRC, AIMS, policy, legal, accountability
2. organizational goals and use cases
3. data, privacy, sovereignty, and information boundaries
4. AI method choices
5. model ecosystem
6. hosting and inference
7. gateways and access control
8. agentic orchestration and workflow execution
9. knowledge, retrieval, memory, and state
10. adaptation: prompting, RAG, fine-tuning, training
11. QA, evaluation, testing, monitoring, and observability
12. human oversight, operating model, sourcing, and operations
13. vendors, organizations, standards, and ecosystem context

Make this ordering visible in `README.md` and `docs/`.

## Cleanup loop

Use this loop during implementation:

1. produce a first pass
2. inspect for duplication, weak framing, structure drift, broken links, and unnecessary artifacts
3. repair factual, structural, and navigation issues
4. simplify wording and formatting where possible
5. verify consistency with adjacent documents
6. remove leftovers that no longer belong

This loop is mandatory.

## Editorial rules

Must:

1. use neutral wording
2. prefer structure over prose
3. prefer reusable table schemas over ad hoc formats
4. separate facts, classifications, and judgments
5. avoid marketing language
6. avoid mixing tools, vendors, models, frameworks, standards, and use cases without classification
7. ensure cross-links across related docs
8. preserve distinctions between governance, architecture, tooling, ecosystem actors, sourcing, and operations
9. treat open source as a first-class evaluation aspect where relevant
10. distinguish evidence-backed claims, descriptive mapping, normative guidance, and editorial judgment
11. prefer primary or official sources where practical
12. strengthen citation coverage where trust matters most
13. if a claim is uncertain, verify it, qualify it, or remove it
14. do not present unsupported claims as settled fact

When improving the repository:

1. diagnose before rewriting broadly
2. identify weak, repetitive, outdated, or duplicative areas
3. strengthen, merge, defer, or remove weak standalone pages
4. improve the highest-leverage areas first
5. review the result for coherence and maintainability

## Acceptance criteria

The implementation succeeds only if:

1. the required repository structure exists
2. `README.md` works as a front door and decision spine
3. each `docs/` file has clear purpose and usable structure
4. one reusable global taxonomy exists
5. use cases cover worker-facing and org/system-facing AI applications
6. the stack is represented from governance to runtime and assurance
7. openness, sovereignty, privacy, compliance, lock-in, and buy-vs-build remain visible across the design
8. the delivery harness was created first
9. the Cleanup loop was used
10. temporary scaffolding was removed unless intentionally retained
11. no unnecessary duplicate topic files exist between root and `docs/`
12. the repository uses a Creative Commons license suitable for open knowledge
13. topic files are not thin placeholders
14. cross-links and taxonomy reuse are consistent across the repository

## Done means

Work is done only when:

- the result is materially clearer or stronger than before
- duplication has not increased
- structure still makes sense
- links and references are coherent
- the repository remains maintainable
- the changes fit the mission and conventions of the repository
