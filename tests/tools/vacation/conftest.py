import sqlite3
from pathlib import Path
from unittest.mock import patch

import pytest


PARENT_DIR = Path(__file__).parent
INIT_DB_SCRIPT_PATH = PARENT_DIR / "init_test_db.sql"


@pytest.fixture(scope="module", autouse=True)
def create_table():
    with sqlite3.connect(":memory:", autocommit=False) as connection:
        cursor = connection.cursor()
        with INIT_DB_SCRIPT_PATH.open() as sql_file:
            for command in sql_file.read().strip().split(";"):
                cursor.execute(command)
        connection.commit()

        with patch("chatbot.tools.vacation.connect") as connection_mock:
            connection_mock.return_value.__enter__.return_value = connection
            yield connection_mock
