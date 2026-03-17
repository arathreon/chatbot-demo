CREATE TABLE employees
(
    id                  TEXT PRIMARY KEY,
    name                TEXT    NOT NULL,
    total_vacation_days INTEGER NOT NULL
);
CREATE TABLE vacation_records
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT NOT NULL REFERENCES employees (id),
    start_date  DATE NOT NULL,
    end_date    DATE NOT NULL,
    description TEXT,
    status      TEXT DEFAULT 'approved' -- approved, pending, rejected
);
-- Data for happy path
INSERT INTO employees (id, name, total_vacation_days)
VALUES ("1", "John Doe", 25);
INSERT INTO vacation_records (employee_id, start_date, end_date, description, status)
VALUES ("1", "2024-01-05", "2024-01-10", "family vacation", "approved");

-- Employee exists, no vacation records exist
INSERT INTO employees (id, name, total_vacation_days)
VALUES ("2", "Jane Doe", 30);

-- Employee has more vacation records
INSERT INTO employees (id, name, total_vacation_days)
VALUES ("3", "Emma Smith", 25);
INSERT INTO vacation_records (employee_id, start_date, end_date, description, status)
VALUES ("3", "2024-01-05", "2024-01-10", "family vacation", "approved");
INSERT INTO vacation_records (employee_id, start_date, end_date, description, status)
VALUES ("3", "2024-02-05", "2024-02-10", "family vacation", "approved");
INSERT INTO vacation_records (employee_id, start_date, end_date, description, status)
VALUES ("3", "2024-03-05", "2024-03-10", "family vacation", "rejected");
