# Database
This project uses SQLite as the DBMS and in python can be accessed using the sqlite3 module.

# Database Design

![Basic Database Schema](../resources/soil_moisture_db.svg)

# API
The API allows for inserting new records into the database and retrieving that data. Currently the API only supports retrieving data from the moisture_readings table. 

### Constructor
**Database(initialise=False, path=db_path, schema=schema_path)**

A Database object must be created using this constructor. The arguments specify if a new database file is to be created, what path to use for the database file, and the path for a schema file to use in database construction. There are default values that set the path to "/db/database.db" and the schema path to "/db/schema.sql"


### Methods

**insert_moisture_record(timestamp, reading, location, device_id)**  
Insert a new record into the moisture_readings table with all required fields.

**get_moisture_from_timestamp(device_id, timestamp)**  
Get a single moisture reading at a specific time.

**get_all_moisture_from_device(device_id)**  
Retrieve all moisture readings recorded from a specified device.

**get_moisture_from_device_range(device, start, end)**  
Retrieve a group of moisture readings from a specified datetime range.