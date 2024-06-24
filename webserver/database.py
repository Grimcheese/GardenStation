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


    def _open_standard_connection(self):
        """Get a new connection to the database."""
        
        connection = sqlite3.connect(self.database)
        return connection


    def _open_row_connection(self):
        """Get a new connection to be used for retrieving rows from the database."""

        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row

        return connection


    def _create_from_schema(self, schema=schema_path):
        """Create a new database using the schema file.
        
        WARNING: THIS WILL DELETE ALL DATA STORED IN DB!"""
        
        if self.database.exists():
            self.database.unlink() # Ensure a new database is created
        connection = sqlite3.connect(self.database)

        with open(schema) as f:
            connection.executescript(f.read())
        
        connection.commit()
        connection.close()


    def _insert_record(self, table, **column_values):
        """Insert a single new record into the database.
        
        This method can take an arbitrary number of column:value key pairs to 
        allow new rows to be inserted without specifying a value for each column.
        
        Args:
            table: The table to insert the new record into.
            column_values: Key:Value pair representing the column name and desired
                value to insert into the database.
        """
        
        connection = self._open_standard_connection()
        cursor = connection.cursor()

        # Get column names from table
        values = []
        for key in column_values.keys():
            values.append("?")
        
        query = f"INSERT INTO {table} ({', '.join(column_values.keys())}) VALUES ({', '.join(values)});"
        data = tuple(column_values.values())

        cursor.execute(query, data)
        connection.commit()
        connection.close()


    def execute_query(self, query, parameters=None):
        connection = self._open_row_connection()
        cursor = connection.cursor()

        if parameters is None:
            cursor.execute(query)
        else:
            cursor.execute(query, parameters)
        
        results = [dict(row) for row in cursor.fetchall()]
        connection.close()

        return results


    @DeprecationWarning
    def insert_moisture_record(self, timestamp, reading, location, device_id):
        """Create a new record in the moisture table.
        
        Args:
            timestamp: String containing the date and time of record collection. 
            reading: The moisture level recorded in the soil.
            location: The name of the location where the reading was taken.
            device_id: ID number of the device that took the reading.
        """
        
        self._insert_record("moisture_readings", timestamp=timestamp, moisture=reading, location=location, device_id=device_id)
    
    
    def get_moisture_from_timestamp(self, device_id, timestamp):
        """Retrieve a single record based on device_id and timestamp.
        
        Args:
            device_id: The ID number of the device to retrieve records from.
            timestamp: The timestamp to use to search the database with.
        """

        connection = self._open_row_connection()
        cursor = connection.cursor()
        
        query = "SELECT * FROM moisture_readings WHERE device_id = (?) \
            AND timestamp = (?);"
        cursor.execute(query, (device_id, timestamp))
        results = [dict(row) for row in cursor.fetchall()]
        connection.close()
        
        return results
        

    def get_all_moisture_from_column_id(self, column_name, column_id):

        connection = self._open_row_connection()
        cursor = connection.cursor()

        query = f"SELECT * FROM moisture_readings WHERE {column_name} = (?);"
        cursor.execute(query, (column_id,))

        results = [dict(row) for row in cursor.fetchall()]
        connection.close()

        return results


    def get_moisture_from_timestamp_range(self, start, end):
        """Get all moisture readings from a device within a datetime range.
        
        Note, start and end times are inclusive.

        Args:
            device: The ID number of the device to query results from.
            start: Starting datetime for the range being searched. As a String in
                iso date time format.
            end: Ending datetime for the range being searched. As a String in
                iso date time format.
        """
        
        connection = self._open_row_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM soil_readings WHERE reading_time >= (?) AND reading_time <= (?);"
        
        cursor.execute(query, (start, end))

        results = [dict(row) for row in cursor.fetchall()]
        connection.close()
        
        return results


    def get_devices(self):
        """Get all devices stored in database"""

        query = "SELECT * FROM devices;"
        results = self.execute_query(query)

        return results


    @DeprecationWarning
    def get_unique_column_vals(self, column_name):
        """Get a sorted list of all unique values for a columm."""

        # Valid list of values for column_name
        valid_names = ["device_id", "location"]

        if column_name not in valid_names:
            raise ValueError

        connection = self._open_row_connection()
        cursor = connection.cursor()

        query = f"SELECT DISTINCT {column_name} FROM moisture_readings;"
        cursor.execute(query)

        raw_results = [dict(row) for row in cursor.fetchall()]
        connection.close()

        results = [row[f'{column_name}'] for row in raw_results]
        results.sort()

        return results
    

    def add_device(self, in_software_version, in_microprocessor):
        """Add a new device to the devices table."""

        # TODO validate input values

        self._insert_record("devices", 
                            software_version=in_software_version, 
                            microprocessor=in_microprocessor)

        """
        connection = self._open_standard_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO devices (device_id, software_version, microprocessor) VALUES (?, ?, ?)", 
                       (device_id, software_version, microprocessor))
        
        connection.commit()
        connection.close()
        """
    
    def add_location(self, in_latitude, in_longitude, in_address):
        """Add a new location to the locations table."""

        # TODO validate input values

        self._insert_record("locations",
                            latitude=in_latitude,
                            longitude=in_longitude,
                            loc_address=in_address)
        


    def add_reading(self, timestamp, in_soil_reading, in_device_id):
        """Add a new soil reading to soil_readings table."""

        # TODO validate input values

        self._insert_record("soil_readings", 
                            reading_time=timestamp,
                            soil_reading=in_soil_reading,
                            device_id=in_device_id)


    def add_device_location(self, in_device_id, in_date_placed, in_date_removed, in_location):
        # TODO validate input values

        if in_date_removed == None:
            in_date_removed = "NULL"
        
        self._insert_record("device_location",
                            device_id=in_device_id,
                            date_placed=in_date_placed,
                            date_removed=in_date_removed,
                            location=in_location)


    def move_device_location(self, in_device_id, date_placed, new_location_id, move_time):
        """Move a device from existing location to a new location."""

        # TODO validate input values

        self.remove_device_from_location(in_device_id, date_placed, move_time)
        self.new_device_location(in_device_id, new_location_id, move_time)


    def new_device_location(self, in_device_id, in_location_id, timestamp):
        """Move a device to a new location."""

        # TODO validate input values

        self._insert_record("device_locations",
                            device_id=in_device_id,
                            date_placed=timestamp,
                            location_id=in_location_id)


    def remove_device_from_location(self, device_id, date_placed, date_removed):
        """Remove a device from a location."""

        # TODO validate input values

        connection = self._open_standard_connection()
        cursor = connection.cursor()

        query = "UPDATE device_locations SET date_removed = (?) WHERE device_id = (?) AND date_placed = (?)"
        params = tuple(date_removed, device_id, date_placed)
        cursor.execute(query, params)