import logging
from pathlib import Path

from chatbot.ingestion.chunker import chunk_documents
from chatbot.ingestion.loaders.registry import get_registry
from chatbot.vector_db.chroma import ChromaDB

logger = logging.getLogger(__name__)


def ingest(paths: list[Path], vector_db: ChromaDB):
    """Process a list of paths and add the documents to the vector database."""
    registry = get_registry()

    for path in paths:
        logger.info("Processing file: %s", path)
        try:
            documents = registry.load(path)
            chunks = chunk_documents(documents)
            vector_db.add(chunks)
        except Exception:
            logger.exception("Couldn't process file: %s", path)
