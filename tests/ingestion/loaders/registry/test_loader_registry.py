from pathlib import Path

import pytest

from chatbot.ingestion.loaders.base import Document
from chatbot.ingestion.loaders.markdown_loader import load_markdown
from chatbot.ingestion.loaders.pdf_loader import load_pdf
from chatbot.ingestion.loaders.registry import LoaderRegistry, create_default_registry
from chatbot.ingestion.loaders.txt_loader import load_txt

TEST_DOCUMENT = Document(text="test_text", metadata={"source": "test"})
TEST_PATH = Path("./test/path/file.pdf")


def dummy_pdf_loader(path: Path) -> list[Document]:
    assert path == TEST_PATH
    return [TEST_DOCUMENT]


def test_loader_registry_registers_correctly():
    registry = LoaderRegistry()

    assert registry._loaders == {}

    registry.register(".pdf", dummy_pdf_loader)

    assert len(registry._loaders) == 1
    assert registry._loaders[".pdf"] == dummy_pdf_loader


def test_loader_registry_not_registering_for_same_format_twice():
    registry = LoaderRegistry()
    registry.register(".pdf", dummy_pdf_loader)
    assert len(registry._loaders) == 1
    assert registry._loaders[".pdf"] == dummy_pdf_loader

    with pytest.raises(ValueError):
        registry.register(".pdf", lambda x: [])


def test_loader_registry_uses_correct_loader():
    registry = LoaderRegistry()
    registry.register(".pdf", dummy_pdf_loader)

    assert len(registry._loaders) == 1
    assert registry._loaders[".pdf"] == dummy_pdf_loader

    results = registry.load(TEST_PATH)
    assert results == [TEST_DOCUMENT]


def test_loader_registry_raises_error_when_no_loader_for_extension():
    registry = LoaderRegistry()

    assert registry._loaders == {}

    with pytest.raises(ValueError, match="No loader registered for file extension: .pdf"):
        registry.load(TEST_PATH)


def test_creating_default_loader_registry():
    result = create_default_registry()
    assert len(result._loaders) == 3
    assert ".pdf" in result._loaders
    assert result._loaders[".pdf"] == load_pdf
    assert ".txt" in result._loaders
    assert result._loaders[".txt"] == load_txt
    assert ".md" in result._loaders
    assert result._loaders[".md"] == load_markdown
