import argparse

from dotenv import load_dotenv

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
        "ingest",
        "chat",
    ],
)

args = parser.parse_args()

if __name__ == "__main__":
    match args.command:
        case "hello":
            print("Hello! How can I assist you today?")
        case "ingest":
            from chatbot.ingestion.main import run_ingestion

            run_ingestion()
        case _:
            print(f"Unknown command: {args.command}. Type 'help' for available commands.")
