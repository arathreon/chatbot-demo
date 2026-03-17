from unittest.mock import MagicMock

from chatbot.ingestion.loaders.base import Document
from chatbot.tools.database_search import search_database


def test_search_database_returns_results():
    mock_db = MagicMock()
    mock_db.query.return_value = [
        Document(text="some policy text", metadata={"source": "policy.pdf", "page": 1}),
        Document(text="another doc", metadata={"source": "guide.md"}),
    ]

    result = search_database(mock_db, query="vacation policy", n_results=2)

    mock_db.query.assert_called_once_with(text="vacation policy", n_results=2)
    assert result == {
        "results": [
            {"text": "some policy text", "metadata": {"source": "policy.pdf", "page": 1}},
            {"text": "another doc", "metadata": {"source": "guide.md"}},
        ]
    }


def test_search_database_empty_results():
    mock_db = MagicMock()
    mock_db.query.return_value = []

    result = search_database(mock_db, query="nonexistent topic")

    assert result == {"results": []}
