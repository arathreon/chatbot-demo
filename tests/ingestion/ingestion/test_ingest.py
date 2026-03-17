from unittest.mock import MagicMock

from chatbot.ingestion.ingestion import ingest
from chatbot.ingestion.loaders.base import Document


def test_ingest_txt_file(tmp_path):
    """
    Real .txt file → loader registry → chunker → mock vector DB.
    Short text stays as a single chunk; metadata carries source, format,
    chunk_id, and total_chunks.
    """
    txt_file = tmp_path / "policy.txt"
    txt_file.write_text("Employees are entitled to 20 vacation days per year.", encoding="utf-8")

    mock_vector_db = MagicMock()

    ingest([txt_file], mock_vector_db)

    mock_vector_db.add.assert_called_once()
    chunks = mock_vector_db.add.call_args[0][0]

    assert len(chunks) == 1
    assert isinstance(chunks[0], Document)
    assert chunks[0].text == "Employees are entitled to 20 vacation days per year."
    assert chunks[0].metadata["source"] == "policy.txt"
    assert chunks[0].metadata["format"] == "txt"
    assert chunks[0].metadata["chunk_id"] == 0
    assert chunks[0].metadata["total_chunks"] == 1
