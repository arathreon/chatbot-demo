# Decisions

This document contains decisions made during development. For examples of major architectural decisions,
see `docs/adr/`.

## No authentication layer

The CLI tool has no authentication. Any user who can run it can access all the documents and tools. Authentication
is unrelated to the patterns this project demonstrates (RAG, tool calling, ingestion). In a production deployment
behind an API, authentication and user authorization for tools and data access would be required.

## Ingestion CLI command vs File watcher

Document ingestion runs as a CLI command, not as a background process watching for file changes. A file watcher is
a valid production pattern but adds complexity while bringing no added value to a small demo application. The ingestion
CLI command is simpler and cleanly demonstrates decoupling from the querying CLI with ChromaDB as the only common point
of contact. In a production, an event-driven architecture (e.g., file watcher, S3 event trigger) is more appropriate.

## Plain functions vs Protocol for document loaders

Each loader (PDF, MD, TXT) is a single function: path in, list of strings out. Wrapping each loader function in a class
is an unnecessary abstraction. A Protocol would make sense if the loader function needed configuration or multiple
methods (e.g., metadata extraction, complex parsing from proprietary formats). Until then, a function with a consistent
signature is enough.

## Chunking strategy

Documents are split into chunks of 500 tokens with a 50-token overlap using `tiktoken` (cl100k_base encoding).
Token-based splitting is used instead of character-based splitting as it is more in line with how the embedding model
actually processes text. The size of 500 tokens is a middle ground for two problems: if the chunks are too small, the
text loses context, if too large, it risks being too broad. Both of these problems result in bad retrieval precision.
The 50-token overlap (10 %) ensures that sentences split by tokenization are not lost. These are reasonable base values.
These should be empirically optimized in production.

## Markdown ingestion

Markdown is ingested as plaintext. The embedding model handles it without issues. In a production, we might want
to make section-based embeddings to enhance context granularity and make references to particular sections possible.
However, this would warrant benchmarking performance against the granularity degree.

## Embedding model

The OpenAI's embedding model `text-embedding-3-small` is used for both, ingestion and query-time embedding. Using
the same model for both is mandatory - mixing different models would result in incompatible vectorization.
The `small` variant was chosen over the `large` variant as a cost-conscious default sufficient for a collection of this
size.

## ChromaDB vs other vector DBs

ChromaDB was chosen mainly for convenience - it can be installed via a single command, it doesn't need any Docker
container, no external service, and no additional account/API key. It stores data to disk. There is no need
for serialization logic. For a production deployment, a managed or self-hosted solution (e.g., Pinecone, Qdrant,
pgvector) would be more appropriate depending on scale and infrastructure constraints.

## Vector DB Protocol

The vector DB is implemented as a concrete ChromaDB class with a narrow public interface (add, query). This is because
different vector DBs have different APIs (e.g., ChromaDB uses embedding function while DBs such as Pinecone or Qdrant
assume already precomputed vectors). An abstraction is premature in this case and could result in being too generic or
too specific to ChromaDB. In case a second vector DB is added, the correct first step is to derive an interface that is
suitable for both DBs.
