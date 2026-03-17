from pathlib import Path

from chatbot.ingestion.loaders.base import Document


def load_markdown(path: Path) -> list[Document]:
    return [
        Document(
            text=path.read_text(encoding="utf-8"),
            metadata={"source": path.name, "format": "markdown"},
        )
    ]
