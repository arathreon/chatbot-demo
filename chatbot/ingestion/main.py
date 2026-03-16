from pathlib import Path

from chatbot.ingestion.ingestion import ingest
from chatbot.vector_db.chroma import ChromaDB

DEFAULT_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "documents"


def run_ingestion():
    vector_db = ChromaDB()
    ingest(
        paths=list(DEFAULT_DATA_PATH.iterdir()),
        vector_db=vector_db,
    )
