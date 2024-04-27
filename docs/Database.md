# Database

A database is used in this project to store the readings taken by devices out in the field. It records the device, the date/time, location and the reading itself. 

Using a database for this application is most likely overkill as the data being stored is quite simple, there are not really any complex relationships between the data and only a limited number of people will be using the data. However, designing, implementing and using a database to solve a problem is a valuable learning experience for me and demonstrates my ability to use a database system in a working application.



This project uses SQLite as the DBMS and in python can be accessed using the sqlite3 module.

# Database Design


### Entity Relationship Diagram 

There are two entities with a single relationship that can be described as "Device takes a reading at a location" and is illustrated in this diagram: 

![Database ERD - deprecated]()

### Database Schema

The entities are represented in the schema as expected by the ERD, the only major addition is the device_locations relation.

To represent the relationship between devices and locations (devices being placed at a specific location for a duration of time) a new relation 'device_locations' has been created. This table can be used to set the location field in each reading taken by checking the current location of the device that has sent the reading. **Accuracy depends on this table being updated whenever a device is moved.** 

The entity relationship diagram has been mapped to a schema as follows:

![Database Schema](../resources/soil_moisture_db_schema.svg)


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