"""Provides a library of methods to access the database"""

import sqlite3
from pathlib import Path

DATABASE_FILENAME = "database.db"
SCHEMA_FILENAME = "schema.sql"

root_dir = Path(__file__).parents[1]
db_path = root_dir.joinpath("db", DATABASE_FILENAME)
schema_path = root_dir.joinpath("db", SCHEMA_FILENAME)

def open_row_connection(database=db_path):
    """Open a connection for retrieving data."""

    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row

    return connection

def insert_moisture_record(timestamp, reading, location, device_id, database=db_path):
    """Create a new record in the moisture table.
    
    Args:
        timestamp: String containing the date and time of record collection. 
        reading: The moisture level recorded in the soil.
        location: The name of the location where the reading was taken.
        device_id: ID number of the device that took the reading.
        database: Path to the database file. Default value is set by global
            variable.
    
    """
    connection = sqlite3.connect(database)
    
    # TODO VALIDATE variables before using them in query
    
    cur = connection.cursor()
    cur.execute("INSERT INTO moisture (timestamp, moisture, location, device_id) VALUES (?, ?, ?, ?)",
                    (timestamp, reading, location, device_id)
                )
    
    connection.commit()
    connection.close()

def get_all_moisture(database=db_path):
    """Retrieve all moisture records from the specified database."""
    
    connection = open_row_connection()

    records = connection.execute("SELECT * FROM moisture").fetchall()
    connection.close()

    return records

def retrieve_moisture_timestamp_range(start, end, database=db_path):
    """Retrieve moisture records from a specified date/time range.
    
    Args:
        start: The starting timestamp for the range.
        end: The ending timestamp for the range (inclusive).

    Returns: List of all records from the database that match the range. 
    """

    connection = open_row_connection()


if __name__ == "__main__":
