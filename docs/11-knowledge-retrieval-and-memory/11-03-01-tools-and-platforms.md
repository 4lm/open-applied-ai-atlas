# 11.3.1 Tools And Platforms

_Page Type: Comparison Page | Maturity: Review-Ready_

This file compares the main retrieval and memory building blocks, from composition frameworks through vector, search, graph, and memory layers. The goal is not to crown one store, but to make permissioning, provenance, refresh, and exit posture visible beside raw retrieval capability.

## How To Use This File

- Read the tables as comparison surfaces, not as a ranking list.
- Treat retrieval frameworks, stores, and memory services as different roles even when vendors market them together.
- Re-check `06`, `09`, `13`, `14`, and `18` before choosing a retrieval stack on relevance metrics alone.

## Retrieval Frameworks, Ingestion, And Composition Layers

These tools matter when the organization needs pipelines around ingestion, chunking, retrieval, context assembly, and evaluation.

| Resource | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best fit | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [LlamaIndex](https://www.llamaindex.ai/) | Framework / platform | Retrieval and document workflows | Acceptable | Mixed ecosystem | Self-hosted library plus managed companions | Knowledge assistants and document-centric RAG | Best fit is strongest when retrieval is central to the app design | [Docs](https://docs.llamaindex.ai/) |
| [Haystack](https://haystack.deepset.ai/) | Open-source framework | Retrieval pipelines | Preferred | Fully open source | Self-hosted | Controlled RAG systems | Needs internal engineering for production hardening and permissions | [Docs](https://docs.haystack.deepset.ai/) |
| [LangChain](https://python.langchain.com/) | Framework | Retrieval and tool composition | Acceptable | Open source / commercial ecosystem | Self-hosted library plus managed companions | Teams already standardizing on LangChain-style app construction | Rich ecosystem can create indirect coupling to companion managed products | [Docs](https://python.langchain.com/) |
| [Unstructured](https://unstructured.io/) | Document processing platform | Parsing, partitioning, and ingestion | Acceptable | Open source / commercial ecosystem | Self-hosted or managed | Document-heavy ingestion and preprocessing for retrieval systems | It solves ingestion, not permissions, quality gates, or search strategy by itself | [Docs](https://docs.unstructured.io/) |
| [Zep](https://help.getzep.com/overview) | Memory and context platform | Agent memory and temporal knowledge graph layer | Acceptable | Open source / commercial ecosystem | Self-hosted or managed | Systems that need persistent user memory, graph retrieval, and context assembly | Memory quality still depends on retention policy, provenance, and application fit | [Docs](https://help.getzep.com/overview) |

## Vector, Search, And Graph Stores

These stores matter when the organization needs a durable retrieval substrate, but they should be evaluated as part of a broader retrieval architecture rather than as the architecture itself.

| Resource | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best fit | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [pgvector](https://github.com/pgvector/pgvector) | Open-source extension | Vector search inside PostgreSQL | Preferred | Fully open source | Self-hosted | Teams preferring simpler retrieval inside existing Postgres estates | Good default when operational simplicity matters more than specialized vector features | [Repo](https://github.com/pgvector/pgvector) |
| [Qdrant](https://qdrant.tech/) | Vector database | Similarity search and vector retrieval | Preferred | Open source / managed ecosystem | Self-hosted or managed | Portable vector retrieval with self-hosted path | Still needs surrounding permissions, freshness, and quality design | [Docs](https://qdrant.tech/documentation/) |
| [Milvus](https://milvus.io/) | Open-source database | Vector store | Preferred | Fully open source | Self-hosted or managed ecosystem | Self-hosted vector retrieval at scale | Operational profile is heavier than simpler Postgres-based starting points | [Docs](https://milvus.io/docs) |
| [Weaviate](https://weaviate.io/) | Database / platform | Vector-native retrieval | Acceptable | Open core / managed service | Self-hosted or managed | Retrieval and semantic search | Managed use improves speed but increases platform dependence | [Docs](https://docs.weaviate.io/) |
| [Pinecone](https://www.pinecone.io/) | Managed platform | Vector database | Controlled Exception | Proprietary service | Managed | Managed retrieval infrastructure | Strong managed dependence and data-plane concentration | [Pinecone](https://docs.pinecone.io/) |
| [Elastic](https://www.elastic.co/) | Search and analytics platform | Hybrid keyword and vector retrieval | Acceptable | Open core / commercial ecosystem | Self-hosted or managed | Enterprise search and observability estates extending into retrieval | Stronger fit for search-centric organizations than greenfield vector-only designs | [Elastic](https://www.elastic.co/enterprise-search/search-ai-platform) |
| [OpenSearch](https://opensearch.org/) | Open-source search platform | Hybrid search and retrieval infrastructure | Preferred | Open source | Self-hosted or managed service ecosystem | Search-centric organizations preferring open search foundations | Relevance tuning and permissions still need deliberate design | [OpenSearch](https://opensearch.org/) |
| [Redis Query Engine](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/) | Data platform capability | Vector and hybrid retrieval close to application state | Acceptable | Open source / commercial ecosystem | Self-hosted or managed | Low-latency retrieval close to operational data | Best fit depends on existing Redis footprint and workload characteristics | [Docs](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/) |
| [Vespa](https://vespa.ai/) | Search platform | Large-scale hybrid and ranking-heavy retrieval | Preferred | Open source | Self-hosted | Search-heavy systems needing ranking and retrieval control | Heavier operational and ranking-tuning burden than lighter vector-first systems | [Vespa](https://docs.vespa.ai/) |
| [Neo4j](https://neo4j.com/) | Graph platform | Knowledge graph layer | Acceptable | Commercial / open ecosystem | Self-hosted or managed | Graph-centric retrieval and relationship-aware knowledge systems | Graph structure only pays off when the domain actually needs it | [Neo4j](https://neo4j.com/) |
| [Stardog](https://www.stardog.com/) | Knowledge graph platform | Semantic and graph-based retrieval | Controlled Exception | Proprietary platform | Self-hosted or managed | Enterprises needing ontology-heavy retrieval and data integration | Commercial knowledge-graph posture can become a strategic dependency | [Stardog](https://www.stardog.com/) |

## Managed Search And Retrieval Services

These services matter when the organization wants faster deployment and accepts more platform concentration.

| Resource | Entity type | Stack role | Openness-policy tier | Open source posture | Hosting / control posture | Best fit | Main constraints / lock-in notes | Primary source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Azure AI Search](https://learn.microsoft.com/azure/search/) | Managed platform capability | Search and retrieval foundation | Controlled Exception | Proprietary service | Azure-managed | Retrieval-backed applications inside Azure estates | Best fit improves inside broader Azure identity and data assumptions | [Docs](https://learn.microsoft.com/azure/search/) |
| [Vertex AI Search](https://cloud.google.com/generative-ai-app-builder/docs/enterprise-search-introduction) | Managed platform capability | Search and retrieval service in GCP | Controlled Exception | Proprietary service | GCP-managed | Google-cloud search and grounding use cases | Strong cloud-estate coupling remains material | [Docs](https://cloud.google.com/generative-ai-app-builder/docs/enterprise-search-introduction) |
| [Amazon Kendra](https://aws.amazon.com/kendra/) | Managed platform | Enterprise search and retrieval | Controlled Exception | Proprietary service | AWS-managed | AWS-centered enterprise search and knowledge retrieval | Managed dependence and AWS-estate gravity remain strong | [AWS](https://aws.amazon.com/kendra/) |

## Evidence Notes

- The factual rows are anchored in official product, project, or documentation pages linked in the `Primary source` column.
- The portability, lock-in, and fit commentary is atlas synthesis based on deployment posture, surrounding ecosystem coupling, and the surrounding control surfaces described in chapters `06`, `09`, `13`, `14`, and `18`.
- The page does not rank one retrieval stack globally. The intended use is comparative narrowing, not one final winner table.

## Reading Notes

- Re-check the main chapter if the comparison starts to feel more detailed than the underlying decision.
- Prefer adjacent chapter context over treating a single table row as a final answer.

Back to [11.3 Reference Points](11-03-00-reference-points.md).
