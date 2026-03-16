# ADR 001: Framework vs LLM provider SDK

## Status

Accepted

## Context

The orchestration layer requires an agent loop that accepts user prompts, sends them to the LLM along with tool options,
calls tools locally, feeds results back, and returns the final answer to the user.

The ingestion layer requires document parsing, text chunking, and embedding via an embedding model.

Frameworks like LangChain provide abstraction for both. The alternative is to use a specific LLM provider's SDK
directly and implement the orchestration and ingestion layers ourselves.

## Options considered

1. Use existing framework like LangChain

- pros:
    - Provides agent loop, document loaders, text splitters, and vector store integrations out of the box.
    - Uses a single interface for multiple LLM providers.
- cons:
    - Large dependency.
    - Abstracts the agent loop, obscuring the implementation details.

2. Use a specific LLM provider's SDK with a custom agent loop

- pros:
    - Smaller dependency.
    - Explicit control over the agent loop.
- cons:
    - Locks us into a specific LLM provider's SDK.
    - Requires us to implement the agent loop, document loaders, and text splitters ourselves
      (but these should be simple to implement for our scope).

## Decision

Use the OpenAI SDK with a custom agent loop.

In the current scope, a framework adds abstraction without any value added. The custom implementation
keeps every decision transparent and modifiable.

## Consequences

- The agent loop and ingestion pipeline are explicit and debuggable.
- Switching LLM providers requires adapting a few files, not a framework migration.
- Built-in LangChain utilities (document loaders, text splitters) must be replaced with custom implementations.
