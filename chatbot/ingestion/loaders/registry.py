import logging
from pathlib import Path

from chatbot.ingestion.loaders.base import Document, DocumentLoader
from chatbot.ingestion.loaders.markdown_loader import load_markdown
from chatbot.ingestion.loaders.pdf_loader import load_pdf
from chatbot.ingestion.loaders.txt_loader import load_txt


logger = logging.getLogger(__name__)


class LoaderRegistry:
    def __init__(self):
        self._loaders = {}

    def register(self, file_extension: str, loader_function: DocumentLoader):
        """
        Register a document loading function for a given file extension.

        :param file_extension: File extension for which the loader function should be registered (".txt", ".pdf", etc.)
        :param loader_function: Function for retrieving documents from a file
        """
        file_extension = file_extension.lower()

        if file_extension in self._loaders:
            message = f"A loader function is already registered for file extension '{file_extension}'"
            logger.error(message)
            raise ValueError(message)

        self._loaders[file_extension] = loader_function

    def load(self, file_path: Path) -> list[Document]:
        file_extension = file_path.suffix.lower()
        loader_function = self._loaders.get(file_extension)
        if not loader_function:
            message = f"No loader registered for file extension: {file_extension}"
            logger.error(message)
            raise ValueError(message)
        return loader_function(file_path)


loader_registry = None


def create_default_registry() -> LoaderRegistry:
    default_registry = LoaderRegistry()
    default_registry.register(".pdf", load_pdf)
    default_registry.register(".txt", load_txt)
    default_registry.register(".md", load_markdown)
    return default_registry


def get_registry() -> LoaderRegistry:
    global loader_registry
    if not loader_registry:
        loader_registry = create_default_registry()
    return loader_registry
