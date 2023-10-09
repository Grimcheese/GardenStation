DROP TABLE IF EXISTS moisture;

CREATE TABLE moisture (
    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    moisture REAL NOT NULL,
    location TEXT NOT NULL,
    device_id INT NOT NULL
);