import hashlib
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from chatbot.ingestion.loaders.base import Document

LOCAL_VDB_PATH = Path() / "chroma_db"  # Will be created in the current working directory


class ChromaDB:
    def __init__(
        self,
        collection_name: str = "documents",
        persist_directory: Path = LOCAL_VDB_PATH,
        embedding_model=None,
    ):
        self._client = chromadb.PersistentClient(persist_directory)
        self._embedding_fn = embedding_model or OpenAIEmbeddingFunction(
            model_name="text-embedding-3-small",
            # reads OPENAI_API_KEY from env automatically
        )
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            embedding_function=self._embedding_fn,
            # Note: The default is L2. For OpenAI embedding models returning unit vectors, that would be fine.
            # Cosine is for correctness.
            metadata={"hnsw:space": "cosine"},
        )

    def add(self, documents: list[Document]):
        if not documents:
            return

        self._collection.add(
            ids=[self._get_id(document) for document in documents],
            documents=[document.text for document in documents],
            metadatas=[document.metadata for document in documents],
        )

    def query(self, text: str, n_results: int = 5) -> list[Document]:
        results = self._collection.query(query_texts=[text], n_results=n_results)

        return [
            Document(text=doc, metadata=dict(meta))
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]

    def _get_id(self, document: Document):
        raw_document = document.text + str(sorted(document.metadata.items()))
        return hashlib.sha256(raw_document.encode()).hexdigest()
