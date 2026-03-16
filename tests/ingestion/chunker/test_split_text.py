import pytest
import tiktoken

from chatbot.ingestion.chunker import split_text


def test_split_text_short():
    result = split_text(
        "Hello world",
        tiktoken.encoding_for_model("text-embedding-3-small"),
        chunk_size=500,
        chunk_overlap=50,
    )
    assert len(result) == 1
    assert result[0] == "Hello world"


def test_split_text_long():
    long_text = "This is a very long text that should be split in at least three parts"
    result = split_text(
        long_text,
        tiktoken.encoding_for_model("text-embedding-3-small"),
        chunk_size=6,
        chunk_overlap=1,
    )
    assert len(result) == 3
    assert result[0] == "This is a very long text"
    assert result[1] == " text that should be split in"
    assert result[2] == " in at least three parts"


def test_split_text_unknown_encoder():
    with pytest.raises(KeyError):
        split_text("Hello world", tiktoken.encoding_for_model("unknown-model"), 500, 50)
