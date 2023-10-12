"""Provides a library of methods to access the database"""

import sqlite3
import datetime
from pathlib import Path

DATABASE_FILENAME = "database.db"
SCHEMA_FILENAME = "schema.sql"

root_dir = Path(__file__).parents[1]
db_path = root_dir.joinpath("db", DATABASE_FILENAME)
schema_path = root_dir.joinpath("db", SCHEMA_FILENAME)

def open_standard_connection(database=db_path):
    """Create a new connection to the specified database."""
    
    connection = sqlite3.connect(database)
    return connection


def open_row_connection(database=db_path):
    """Open a connection for retrieving data."""

    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row

    return connection


def create_from_schema(database=db_path, sc_path=schema_path):
    """Create a new database using the specified schema."""
    
    connection = open_standard_connection(database)

    with open(sc_path) as f:
        connection.executescript(f.read())
    
    connection.commit()
    connection.close()

def insert_record(table, database=db_path, **column_values):
    connection = open_standard_connection(database)
    cursor = connection.cursor()

    # Get column names from table
    """
    cursor.execute("SELECT * FROM {table}")
    columns = [description[0] for description in cursor.description]
    
    """
    values = []
    for key in column_values.keys():
        values.append("?")
    
    # TODO Sanitise values in column_values
    query = f"INSERT INTO {table} ({', '.join(column_values.keys())}) VALUES ({', '.join(values)})"
    data = tuple(column_values.values())

    cursor.execute(query, data)
    connection.commit()
    connection.close()

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
    connection = open_standard_connection(database)
    
    # TODO VALIDATE variables before using them in query
    
    cur = connection.cursor()
    cur.execute("INSERT INTO moisture_readings (timestamp, moisture, location, device_id) VALUES (?, ?, ?, ?)",
                    (timestamp, reading, location, device_id)
                )
    
    connection.commit()
    connection.close()

def get_all_moisture_from_device(device_id, database=db_path):
    """Retrieve all moisture records from the specified database."""
    
    connection = open_row_connection()
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM moisture WHERE device_id = {device_id}")
    
    # Convert rows to dictionary key:value pairs
    results = [dict(row) for row in cursor.fetchall()]
    connection.close()

    return results

def get_moisture_from_device_range(device, start, end, database=db_path):
    """Get all moisture readings from a device within a datetime range."""
    
    connection = open_row_connection()
    cursor = connection.cursor()

    query = f"SELECT * FROM moisture WHERE device_id IS {device} \
    AND timestamp >= start AND timestamp <= end"
    
    cursor.execute(query)

    results = [dict(row) for row in cursor.fetchall()]
    connection.close()
    
    return results

