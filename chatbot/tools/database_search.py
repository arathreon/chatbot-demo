from chatbot.tools.base import Tool
from chatbot.vector_db.chroma import ChromaDB


def search_database(vector_db: ChromaDB, query: str, n_results: int = 5) -> dict:
    documents = vector_db.query(text=query, n_results=n_results)
    return {"results": [{"text": document.text, "metadata": document.metadata} for document in documents]}


def create_search_database_tool(vector_db: ChromaDB) -> Tool:
    """Factory function for creating the search database tool"""

    def handler(query: str, n_results: int = 5) -> dict:
        nonlocal vector_db
        return search_database(vector_db, query, n_results)

    return Tool(
        name="search_database",
        description=(
            "Search the internal knowledge base for information about company documents. "
            "Use this when the user asks about policies, procedures, guidelines, or any other information "
            "that could be found in the company documentation."
        ),
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to find relevant documents.",
                },
                "n_results": {
                    "type": "integer",
                    "description": "Number of document chunks to return (default: 5).",
                },
            },
            "required": [
                "query",
            ],
        },
        handler=handler,
    )
