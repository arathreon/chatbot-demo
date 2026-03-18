from pathlib import Path

from chatbot.ingestion.loaders.pdf_loader import load_pdf

TEST_PDF = Path(__file__).parent / "test_pdf.pdf"


def test_load_pdf():
    documents = load_pdf(TEST_PDF)

    assert len(documents) == 2

    assert documents[0].text.strip() == "Test text on page 1"
    assert documents[0].metadata == {
        "source": "test_pdf.pdf",
        "type": "pdf",
        "page": 1,
        "total_pages": 2,
    }

    assert documents[1].text.strip() == "Test text on page 2"
    assert documents[1].metadata == {
        "source": "test_pdf.pdf",
        "type": "pdf",
        "page": 2,
        "total_pages": 2,
    }
