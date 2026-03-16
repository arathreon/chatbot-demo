# Chatbot

## Setup

### Installing dependencies

The chatbot uses the uv package manager for managing dependencies.
To install dependencies, use the following command:

```bash
uv sync
```

### Environment variables

An `.env` file is required for the chatbot to run. Please see the `.env.example` file for an example of how to set up
the environment variables.

## Running the chatbot

### Running ingestion pipeline

The chatbot is able to ingest documents from `data/documents/`, chunk them, get embeddings, and store them in the vector
database (in our case ChromaDB). To run the ingestion pipeline, use the following command:

```bash
python -m chatbot ingest
```

## Development information

### Documentation

The documentation for the chatbot is available in the `docs/` directory. It includes architectural decisions and design
documents.

### Running tests

The chatbot uses pytest for testing. To run tests, use the following command:

```bash
pytest
```
