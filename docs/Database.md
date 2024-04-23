# Database

A database is used in this project to store the readings taken by devices out in the field. It records the device, the date/time, location and the reading itself. 

Using a database for this application is most likely overkill as the data being stored is quite simple, there are not really any complex relationships between the data and only a limited number of people will be using the data. However, designing, implementing and using a database to solve a problem is a valuable learning experience for me and demonstrates my ability to use a database system in a working application.



This project uses SQLite as the DBMS and in python can be accessed using the sqlite3 module.

# Database Design


### Entity Relationship Diagram 

There are two entities with a single relationship that can be described as "Device takes a reading at a location" and is illustrated in this diagram: 
![Database ERD](../resources/soil_moisture_erd.svg)

### Mapping ERD

As this is a 1:1 relationship it could be merged into a single relation however I decided to create an extra relation as it provides flexibility if the database needs to be modified in the future.

The schema describing the database illustrated here:



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