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
INSERT INTO employees (id, name, total_vacation_days)
VALUES ("1", "John Smith", 20);
INSERT INTO employees (id, name, total_vacation_days)
VALUES ("2", "Amy Potter", 25);
INSERT INTO employees (id, name, total_vacation_days)
VALUES ("3", "Peter Doe", 20);
INSERT INTO employees (id, name, total_vacation_days)
VALUES ("4", "Patrick Green", 25);
INSERT INTO vacation_records (employee_id, start_date, end_date, description)
VALUES ("1", "2024-07-01", "2024-07-10", "Family vacation");
INSERT INTO vacation_records (employee_id, start_date, end_date, description)
VALUES ("1", "2024-08-01", "2024-08-05", "Family vacation");
INSERT INTO vacation_records (employee_id, start_date, end_date, description)
VALUES ("2", "2024-07-01", "2024-07-10", "Family vacation");
INSERT INTO vacation_records (employee_id, start_date, end_date, description)
VALUES ("4", "2024-06-05", "2024-06-06", "Family vacation");
INSERT INTO vacation_records (employee_id, start_date, end_date, description, status)
VALUES ("1", "2024-07-01", "2024-07-10", "Family vacation", "rejected");
