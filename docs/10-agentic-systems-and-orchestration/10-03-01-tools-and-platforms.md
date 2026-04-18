# 10.3.1 Tools And Platforms

_Page Type: Comparison Page | Maturity: Review-Ready_

This file compares the frameworks and runtimes used to build agentic systems, but it keeps the chapter's core bias intact: explicit workflows, constrained tool use, and durable state usually matter more than novelty.

## How To Use This File

- Read the tables as comparison surfaces, not as a ranking list.
- Prefer bounded orchestration and durable execution before free-form multi-agent architectures.
- Re-check `09`, `13`, `14`, and `15` before choosing an orchestration framework as if it were only a developer-experience decision.

## Agent Frameworks And State Management Layers

These frameworks matter when the organization needs to coordinate tools, memory, handoffs, or graph-shaped reasoning under application control.

| Resource | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best fit | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Framework | Stateful agent workflows | Acceptable | Open source / commercial ecosystem | Self-hosted library plus managed companions | Agent orchestration and durable state | Rich ecosystem can pull teams toward broader LangChain coupling | [Docs](https://langchain-ai.github.io/langgraph/) |
| [OpenAI Agents SDK](https://platform.openai.com/docs/guides/agents-sdk) | Framework / SDK | Model-native agent orchestration | Controlled Exception | Open source SDK around proprietary model platform | Code-controlled with vendor model dependence | Teams standardizing on OpenAI-native agents and tracing | Stronger dependence on vendor models and managed platform evolution | [Docs](https://platform.openai.com/docs/guides/agents-sdk) |
| [Google Agent Development Kit](https://docs.cloud.google.com/agent-builder/agent-development-kit/overview) | Framework | Model-agnostic agent development framework with managed deployment path | Acceptable | Open source / Google-led ecosystem | Self-hosted library plus managed companions | Teams that want software-style agent development with Google Cloud deployment options | Best fit strengthens when the broader Google estate is already in scope | [Docs](https://docs.cloud.google.com/agent-builder/agent-development-kit/overview) |
| [PydanticAI](https://ai.pydantic.dev/) | Framework | Python-first agent and tool orchestration | Preferred | Open source | Self-hosted library | Python-heavy systems that need typed outputs and explicit control | Still requires separate choices for state, telemetry, and gateway control | [Docs](https://ai.pydantic.dev/) |
| [Mastra](https://mastra.ai/) | Framework | TypeScript-first agent and workflow framework | Acceptable | Open source / commercial ecosystem | Self-hosted library plus platform options | Web and TypeScript teams building agents close to application code | Ecosystem is newer than some Python-centric alternatives | [Docs](https://mastra.ai/en/reference/agents/agent) |
| [LlamaIndex Workflows](https://docs.llamaindex.ai/) | Framework | Agent and retrieval workflows | Acceptable | Mixed product and open-source ecosystem | Self-hosted library plus managed companions | Document-centric agent flows and retrieval-heavy systems | Best fit usually assumes retrieval is central to the application | [Docs](https://docs.llamaindex.ai/) |
| [Haystack Agents](https://haystack.deepset.ai/) | Open-source framework | Retrieval-aware agents and pipelines | Preferred | Fully open source | Self-hosted | RAG and controlled orchestration | Stronger fit for retrieval-centric systems than generic autonomous tooling | [Docs](https://docs.haystack.deepset.ai/) |
| [Semantic Kernel](https://learn.microsoft.com/semantic-kernel/overview/) | Framework | Agent and tool-use orchestration | Acceptable | Open source / Microsoft-led ecosystem | Self-hosted library with managed ecosystem ties | .NET and enterprise application integration | Best fit improves inside Microsoft-centered engineering estates | [Docs](https://learn.microsoft.com/semantic-kernel/overview/) |
| [AutoGen](https://microsoft.github.io/autogen/) | Framework | Multi-agent composition and experimentation | Acceptable | Open source | Self-hosted library | Research-heavy and multi-agent design work | Easy to overuse where a simpler workflow would be safer | [Docs](https://microsoft.github.io/autogen/) |
| [CrewAI](https://docs.crewai.com/) | Framework | Role-based agent orchestration | Acceptable | Open source / commercial ecosystem | Self-hosted or managed layers | Faster multi-agent assembly with explicit roles | Higher risk of theater-driven designs without clear failure handling | [Docs](https://docs.crewai.com/) |
| [DSPy](https://dspy.ai/) | Framework | Programmatic prompt and workflow optimization | Preferred | Open source | Self-hosted library | Structured agent and pipeline optimization | Optimization value still depends on strong eval and release discipline | [DSPy](https://dspy.ai/) |

## Durable Execution, BPM, And Operational Orchestration

These platforms matter when agentic work must coexist with retries, approvals, SLAs, and operational ownership.

| Resource | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best fit | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Temporal](https://temporal.io/) | Workflow platform | Durable execution | Acceptable | Open core / commercial ecosystem | Self-managed or managed cloud | High-reliability workflow orchestration | Better for explicit workflows than unconstrained autonomous behavior | [Docs](https://docs.temporal.io/) |
| [Camunda](https://camunda.com/) | Workflow platform | BPM and process orchestration | Acceptable | Open core / commercial ecosystem | Self-managed or managed | Human approvals and process-governed automation | Strongest when the process model itself is part of governance | [Docs](https://docs.camunda.io/) |
| [Prefect](https://www.prefect.io/) | Workflow platform | Data and service orchestration | Acceptable | Open source / managed ecosystem | Self-hosted or managed | Pipeline-centric orchestration with operational visibility | Better for engineering-owned services than business-facing agent governance | [Docs](https://docs.prefect.io/) |
| [Apache Airflow](https://airflow.apache.org/) | Open-source project | Batch and pipeline orchestration | Preferred | Open source | Self-hosted | Scheduled and pipeline-heavy systems that need explicit DAGs | Not an agent framework; best used when deterministic DAGs are enough | [Airflow](https://airflow.apache.org/) |
| [Dagster](https://dagster.io/) | Orchestration platform | Asset-aware workflow orchestration | Acceptable | Open source / commercial ecosystem | Self-hosted or managed | Data and ML-heavy orchestrations with stronger software-engineering ergonomics | Still better for explicit pipelines than open-ended action-taking agents | [Docs](https://docs.dagster.io/) |
| [n8n](https://n8n.io/) | Workflow platform | Low-code automation | Acceptable | Source-available / commercial ecosystem | Self-hosted or managed | Business workflow automation and lightweight AI orchestration | Low-code speed can hide weak control boundaries | [Docs](https://docs.n8n.io/) |

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [10.3 Reference Points](10-03-00-reference-points.md).
