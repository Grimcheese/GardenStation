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
    """References and interacts with an SQLite database."""

    def __init__(self, initialise=False, path=db_path, schema=schema_path):
        """Initialise the Database with the path to use for the database and schema.
        
        By default no new database will be created, instead using a database file
        in the db directory called database.db.
        
        Args:
            initialise: Set to False by default. Specifies if a new database should
                be created using the schema file on creation of Database object.
            path: The Path of the database file this Database will interact with.
            schema: Path of the schema file to use when initialising a new database.
        """
        
        self.database = path

        if initialise:
            self._create_from_schema(schema)

    def open_standard_connection(self):
        """Get a new connection to the database."""
        
        connection = sqlite3.connect(self.database)
        return connection


    def open_row_connection(self):
        """Get a new connection to be used for retrieving rows from the database."""

        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row

        return connection


    def _create_from_schema(self, schema=schema_path):
        """Create a new database using the schema file."""
        
        if self.database.exists():
            self.database.unlink() # Ensure a new database is created
        connection = sqlite3.connect(self.database)

        with open(schema) as f:
            connection.executescript(f.read())
        
        connection.commit()
        connection.close()

    def insert_record(self, table, **column_values):
        """Insert a single new record into the database.
        
        This method can take an arbitrary number of column:value key pairs to 
        allow new rows to be inserted without specifying a value for each column.
        
        Args:
            table: The table to insert the new record into.
            column_values: Key:Value pair representing the column name and desired
                value to insert into the database.
        """
        
        connection = self.open_standard_connection()
        cursor = connection.cursor()

        # Get column names from table
        values = []
        for key in column_values.keys():
            values.append("?")
        
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
        """
        connection = self.open_standard_connection()
                
        cur = connection.cursor()
        cur.execute("INSERT INTO moisture_readings (timestamp, moisture, location, device_id) VALUES (?, ?, ?, ?)",
                        (timestamp, reading, location, device_id)
                    )
        
        connection.commit()
        connection.close()
        
    def get_moisture_from_timestamp(self, device_id, timestamp):
        """Retrieve a single record based on device_id and timestamp.
        
        Args:
            device_id: The ID number of the device to retrieve records from.
            timestamp: The timestamp to use to search the database with.
        """

        connection = self.open_row_connection()
        cursor = connection.cursor()
        
        query = "SELECT * FROM moisture_readings WHERE device_id = (?) \
            AND timestamp = (?)"
        cursor.execute(query, (device_id, timestamp))
        results = [dict(row) for row in cursor.fetchall()]
        connection.close()
        
        return results


    def get_all_moisture_from_device(self, device_id):
        """Retrieve all moisture records from the specified database.
        
        Args:
            device_id: The ID number of the device which records are to be
                retrieved.
        """
        
        connection = self.open_row_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM moisture_readings WHERE device_id = (?)", (device_id,))
        
        # Convert rows to dictionary key:value pairs
        results = [dict(row) for row in cursor.fetchall()]
        connection.close()

        return results

    def get_moisture_from_device_range(self, device, start, end):
        """Get all moisture readings from a device within a datetime range.
        
        Args:
            device: The ID number of the device to query results from.
            start: Starting datetime for the range being searched. As a String in
                iso date time format.
            end: Ending datetime for the range being searched. As a String in
                iso date time format.
        """
        
        connection = self.open_row_connection()
        cursor = connection.cursor()

        query = f"SELECT * FROM moisture_readings WHERE device_id IS (?) \
        AND timestamp >= (?) AND timestamp <= (?)"
        
        cursor.execute(query, (device, start, end))

        results = [dict(row) for row in cursor.fetchall()]
        connection.close()
        
        return results

