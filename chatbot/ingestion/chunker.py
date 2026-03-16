import tiktoken

from chatbot.ingestion.loaders.base import Document


def split_text(
    text: str,
    encoder: tiktoken.Encoding,
    chunk_size: int,
    chunk_overlap: int,
) -> list[str]:
    """Text splitting based on tokens; chunks respect the model's tokenization."""
    tokens = encoder.encode(text)

    if len(tokens) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    step = chunk_size - chunk_overlap

    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))  # Ensure we don't go out of bounds
        chunk_tokens = tokens[start:end]
        chunks.append(encoder.decode(chunk_tokens))
        start += step

    return chunks


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    model: str = "text-embedding-3-small",
) -> list[Document]:
    """Create document chunks from provided documents. Add metadata about chunks."""
    encoder = tiktoken.encoding_for_model(model)
    chunks: list[Document] = []

    for document in documents:
        document_chunks = split_text(document.text, encoder, chunk_size, chunk_overlap)

        for i, chunk_text in enumerate(document_chunks):
            chunks.append(
                Document(
                    text=chunk_text,
                    metadata={
                        **document.metadata,
                        "chunk_id": i,
                        "total_chunks": len(document_chunks),
                    },
                )
            )

    return chunks
