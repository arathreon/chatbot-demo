from pathlib import Path

from chatbot.ingestion.loaders.txt_loader import load_txt


def test_load_txt(tmp_path: Path):
    file = tmp_path / "notes.txt"
    file.write_text("Hello, world!", encoding="utf-8")

    documents = load_txt(file)

    assert len(documents) == 1

    doc = documents[0]
    assert doc.text == "Hello, world!"
    assert doc.metadata == {"source": "notes.txt", "format": "txt"}
