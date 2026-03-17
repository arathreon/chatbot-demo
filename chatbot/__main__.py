import argparse

from dotenv import load_dotenv

import chatbot.log_config  # noqa: F401


load_dotenv()

parser = argparse.ArgumentParser(
    prog="chatbot",
    description="A basic chatbot with simple tools",
)

parser.add_argument(
    "command",
    help="the command to execute",
    choices=[
        "hello",
        "init_db",
        "ingest",
        "chat",
    ],
)

args = parser.parse_args()

if __name__ == "__main__":
    match args.command:
        case "hello":
            print("Hello! How can I assist you today?")
        case "init_db":
            from chatbot.extras.init_db.init_db import init_db

            init_db()

        case "ingest":
            from chatbot.ingestion.main import run_ingestion

            run_ingestion()

        case "chat":
            from chatbot.chat.main import run_chat

            run_chat()
        case _:
            print(f"Unknown command: {args.command}. Type 'help' for available commands.")
