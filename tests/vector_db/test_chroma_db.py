import pytest
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from chatbot.ingestion.loaders.base import Document
from chatbot.vector_db.chroma import ChromaDB


@pytest.fixture
def chroma_db(tmp_path):
    """
    Isolated ChromaDB instance backed by a temporary directory, using
    ChromaDB's bundled ONNX embedding model — no external service calls.

    The PersistentClient is explicitly closed on teardown so that the file
    lock on chroma.sqlite3 is released before pytest attempts to delete
    tmp_path (critical on Windows).
    """
    db = ChromaDB(
        collection_name="test_collection",
        persist_directory=tmp_path,
        embedding_model=DefaultEmbeddingFunction(),
    )
    yield db
    db._client.close()


def test_query_returns_most_relevant_document(chroma_db):
    documents = [
        Document(
            text="Employees are entitled to 20 paid vacation days per calendar year.",
            metadata={"source": "vacation_policy"},
        ),
        Document(
            text="All personnel must wear safety helmets on the construction site.",
            metadata={"source": "safety_directive"},
        ),
        Document(
            text="Python is a high-level, dynamically typed programming language.",
            metadata={"source": "coding_practices"},
        ),
    ]
    chroma_db.add(documents)

    results = chroma_db.query("How many days off am I entitled to?", n_results=1)

    assert len(results) == 1
    assert results[0].text == documents[0].text
    assert results[0].metadata["source"] == "vacation_policy"


def test_query_respects_n_results(chroma_db):
    documents = [
        Document(text="Vacation policy: 20 days per year.", metadata={"source": "a"}),
        Document(text="Safety directive: wear helmets at all times.", metadata={"source": "b"}),
        Document(text="Code review must be completed before merging.", metadata={"source": "c"}),
    ]
    chroma_db.add(documents)

    results = chroma_db.query("workplace rules", n_results=2)

    assert len(results) == 2
    # All returned items must be Document instances with populated fields.
    for result in results:
        assert isinstance(result, Document)
        assert result.text
        assert result.metadata


def test_add_empty_document_list(chroma_db):
    chroma_db.add([])  # must not raise

    results = chroma_db.query("anything", n_results=1)

    assert results == []
