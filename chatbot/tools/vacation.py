from sqlite3 import connect
from pathlib import Path

from chatbot.tools.base import Tool

FILE_DIR = Path(__file__).parent
database_path = (
    FILE_DIR.parent.parent / "data" / "databases" / "database.sqlite"
)  # This could be a connection string in the case of a non-local database loaded from a config


def get_vacation_days(employee_name: str) -> dict:
    """Fetches the total vacation days, used vacation days, and remaining vacation days for a given employee."""
    with connect(database_path) as connection:
        cursor = connection.cursor()
        results = cursor.execute(
            """
SELECT
    employees.total_vacation_days,
    coalesce(sum(julianday(vacation_records.end_date) - julianday(vacation_records.start_date) + 1), 0)
FROM
    employees
LEFT JOIN
    vacation_records
ON
    employees.id = vacation_records.employee_id AND vacation_records.status = 'approved'
WHERE
    employees.name = ?
""",
            [employee_name],
        ).fetchone()

        if not results[0]:
            return {"error": f"Employee '{employee_name}' not found in the database."}

        return {
            "employee": employee_name,
            "total_vacation_days": results[0],
            "used": results[1],
            "remaining": results[0] - results[1],
        }


def create_vacation_tool() -> Tool:
    """Create the tool for querying DB for info about employee vacation days."""
    return Tool(
        name="get_vacation_days",
        description=(
            "Look up total vacation days, used vacation days, and remaining vacation days of an employee "
            "specified by full name. This tool should be used every time the user asks about vacation balance, "
            "personal time off (PTO), time off, personal leave, and similar topics."
        ),
        parameters={
            "type": "object",
            "properties": {
                "employee_name": {
                    "type": "string",
                    "description": "The full name of the employee (e.g., 'John Smith').",
                }
            },
            "required": [
                "employee_name",
            ],
        },
        handler=get_vacation_days,
    )
