from pathlib import Path

import pymupdf

from chatbot.ingestion.loaders.base import Document


def load_pdf(path: Path):
    with pymupdf.open(path) as pdf_file:
        documents: list[Document] = []
        for i, page in enumerate(pdf_file):
            text = page.extract_text().strip()

            if not text:
                continue

            documents.append(
                Document(
                    text=text,
                    metadata={
                        "source": path.name,
                        "type": "pdf",
                        "page": i + 1,
                        "total_pages": len(pdf_file),
                    },
                )
            )
