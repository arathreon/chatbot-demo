import pytest

from chatbot.ingestion.chunker import chunk_documents
from chatbot.ingestion.loaders.base import Document


def test_chunk_documents():
    test_data = [
        Document(
            text="hello world",
            metadata={"source": "test"},
        ),
        Document(
            text="This is a very long text that should be split in at least three parts",
            metadata={"source": "test"},
        ),
    ]

    results = chunk_documents(test_data, chunk_size=6, chunk_overlap=1)
    assert len(results) == 4
    assert results == [
        Document(
            text="hello world",
            metadata={"source": "test", "chunk_id": 0, "total_chunks": 1},
        ),
        Document(
            text="This is a very long text",
            metadata={"source": "test", "chunk_id": 0, "total_chunks": 3},
        ),
        Document(
            text=" text that should be split in",
            metadata={"source": "test", "chunk_id": 1, "total_chunks": 3},
        ),
        Document(
            text=" in at least three parts",
            metadata={"source": "test", "chunk_id": 2, "total_chunks": 3},
        ),
    ]


def test_chunk_documents_empty():
    assert chunk_documents([], chunk_size=6, chunk_overlap=1) == []


def test_chunk_documents_wrong_encoder():
    with pytest.raises(KeyError):
        chunk_documents(
            [
                Document(
                    text="Hello world",
                    metadata={"source": "test"},
                )
            ],
            chunk_size=6,
            chunk_overlap=1,
            model="unknown-model",
        )
