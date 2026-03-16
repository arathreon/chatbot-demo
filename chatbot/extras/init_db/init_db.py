import sqlite3
from pathlib import Path

FILE_DIR = Path(__file__).parent
database_path = (
    FILE_DIR.parent.parent.parent / "data" / "databases" / "database.sqlite"
)  # This could be a connection string in the case of a non-local database

database_path.parent.mkdir(parents=True, exist_ok=True)


def init_db():
    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        with open(FILE_DIR / "init_db.sql", "r") as file:
            sql_script = file.read()
        sql_commands = sql_script.split(";")
        for sql_command in sql_commands:
            cursor.execute(sql_command)
