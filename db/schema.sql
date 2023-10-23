DROP TABLE IF EXISTS moisture_readings;
DROP TABLE IF EXISTS sensors;

CREATE TABLE moisture_readings (
    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP NOT NULL,
    moisture REAL NOT NULL,
    location TEXT NOT NULL,
    device_id INT NOT NULL
);

CREATE TABLE sensors (
    device_id INTEGER PRIMARY KEY,
    software_version TEXT
);
