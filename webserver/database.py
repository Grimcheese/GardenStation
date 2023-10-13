"""Provides a library of methods to access the database"""

import sqlite3
import datetime
from pathlib import Path



DATABASE_FILENAME = "database.db"
SCHEMA_FILENAME = "schema.sql"

root_dir = Path(__file__).parents[1]
db_path = root_dir.joinpath("db", DATABASE_FILENAME)
schema_path = root_dir.joinpath("db", SCHEMA_FILENAME)

class Database:

    def __init__(self, path=db_path, schema=schema_path):
        self.database = path

        self._create_from_schema(schema)

    def open_standard_connection(self):
        """Create a new connection to the specified database."""
        
        connection = sqlite3.connect(self.database)
        return connection


    def open_row_connection(self):
        """Open a connection for retrieving data."""

        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row

        return connection


    def _create_from_schema(self, schema=schema_path):
        """Create a new database using the specified schema."""
        
        if db_path.exists():
            db_path.unlink() # Ensure a new database is created
        connection = self.open_standard_connection()

        with open(schema) as f:
            connection.executescript(f.read())
        
        connection.commit()
        connection.close()

    def insert_record(self, table, **column_values):
        connection = self.open_standard_connection()
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

    def insert_moisture_record(self, timestamp, reading, location, device_id):
        """Create a new record in the moisture table.
        
        Args:
            timestamp: String containing the date and time of record collection. 
            reading: The moisture level recorded in the soil.
            location: The name of the location where the reading was taken.
            device_id: ID number of the device that took the reading.
            database: Path to the database file. Default value is set by global
                variable.
        
        """
        connection = self.open_standard_connection()
        
        # TODO VALIDATE variables before using them in query
        
        cur = connection.cursor()
        cur.execute("INSERT INTO moisture_readings (timestamp, moisture, location, device_id) VALUES (?, ?, ?, ?)",
                        (timestamp, reading, location, device_id)
                    )
        
        connection.commit()
        connection.close()

    def get_all_moisture_from_device(self, device_id):
        """Retrieve all moisture records from the specified database."""
        
        connection = self.open_row_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM moisture_readings WHERE device_id = {device_id}")
        
        # Convert rows to dictionary key:value pairs
        results = [dict(row) for row in cursor.fetchall()]
        connection.close()

        return results

    def get_moisture_from_device_range(self, device, start, end):
        """Get all moisture readings from a device within a datetime range."""
        
        connection = self.open_row_connection()
        cursor = connection.cursor()

        query = f"SELECT * FROM moisture WHERE device_id IS {device} \
        AND timestamp >= {start} AND timestamp <= {end}"
        
        cursor.execute(query)

        results = [dict(row) for row in cursor.fetchall()]
        connection.close()
        
        return results

