from chatbot.tools.vacation import get_vacation_days


def test_get_vacation_days_happy_path():
    results = get_vacation_days("John Doe")
    assert results == {
        "employee": "John Doe",
        "remaining": 19,
        "used": 6,
        "total_vacation_days": 25,
    }


def test_get_vacation_days_user_does_not_exist():
    results = get_vacation_days("Annie Doe")
    assert results == {"error": "Employee 'Annie Doe' not found in the database."}


def test_get_vacation_days_employee_exists_no_records():
    results = get_vacation_days("Jane Doe")
    assert results == {
        "employee": "Jane Doe",
        "remaining": 30,
        "used": 0,
        "total_vacation_days": 30,
    }


def test_get_vacation_days_employee_exists_multiple_records():
    results = get_vacation_days("Emma Smith")
    assert results == {
        "employee": "Emma Smith",
        "remaining": 13,
        "used": 12,
        "total_vacation_days": 25,
    }
