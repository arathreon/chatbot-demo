import sqlite3
from pathlib import Path

FILE_DIR = Path(__file__).parent
database_path = (
    FILE_DIR.parent.parent / "databases" / "database.sqlite"
)  # This could be a connection string in the case of a non-local database


def get_vacation_days(employee_name: str) -> dict:
    """Fetches the total vacation days, used vacation days, and remaining vacation days for a given employee."""
    with sqlite3.connect(database_path) as connection:
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
    employees.id = vacation_records.employee_id
WHERE
    employees.name = ?
AND
    vacation_records.status = 'approved';
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
