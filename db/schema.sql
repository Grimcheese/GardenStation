-- SQLite Schema script to create a new database according to
-- schema diagram in Database documentation

DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS soil_readings;
DROP TABLE IF EXISTS device_locations;


CREATE TABLE devices (
    device_id           INTEGER PRIMARY KEY,
    software_version    VARCHAR(10) NOT NULL,
    microprocessor      VARCHAR(20) NOT NULL
);

CREATE TABLE locations (
    location_id         INTEGER AUTOINCREMENT,
    latitude            REAL NOT NULL,
    longitude           REAL NOT NULL,
    loc_address         VARCHAR(50)             
);

CREATE TABLE soil_readings (
    reading_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    reading_time        DATETIME NOT NULL,
    soil_reading        REAL NOT NULL,
    device_id           REFERENCES devices (device_id) NOT NULL,
    --location_id         REFERENCES locations (location_id) NOT NULL
);

CREATE TABLE device_locations (
    device_id           REFERENCES devices (device_id),
    location_id         REFERENCES locations (location_id),
    date_placed         DATE NOT NULL, 
    PRIMARY KEY (device_id, date_placed),
    date_removed        DATE
);