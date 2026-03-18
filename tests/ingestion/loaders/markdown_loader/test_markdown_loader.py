from pathlib import Path

from chatbot.ingestion.loaders.markdown_loader import load_markdown


def test_load_markdown(tmp_path: Path):
    file = tmp_path / "guide.md"
    file.write_text("# Welcome\n\nSome content.", encoding="utf-8")

    documents = load_markdown(file)

    assert len(documents) == 1

    doc = documents[0]
    assert doc.text == "# Welcome\n\nSome content."
    assert doc.metadata == {"source": "guide.md", "format": "markdown"}
