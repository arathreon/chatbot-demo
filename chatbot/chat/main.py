from chatbot.chat.orchestration import run_agent_loop
from chatbot.tools.database_search import create_search_database_tool
from chatbot.tools.registry import ToolRegistry
from chatbot.tools.vacation import create_vacation_tool
from chatbot.vector_db.chroma import ChromaDB


EXIT_COMMANDS = ("exit", "quit")


def run_chat():
    chroma_db = ChromaDB()

    tool_registry = ToolRegistry()
    tool_registry.register(create_search_database_tool(chroma_db))
    tool_registry.register(create_vacation_tool())

    conversation_history: list[dict] = []

    print("System: Assistant ready. Please ask your questions. Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except EOFError, KeyboardInterrupt:
            print("\n\nSystem: Shutting down.")
            break

        if not user_input or user_input.lower() in EXIT_COMMANDS:
            print("\nSystem: Shutting down.")
            break

        response = run_agent_loop(user_input, tool_registry, conversation_history)

        print(f"\nAssistant: {response}\n")
