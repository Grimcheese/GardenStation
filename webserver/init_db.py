"""Initialise a new database with generated dummy data"""

from pathlib import Path

from .database import Database

DATABASE_FILENAME = None
#SCHEMA_FILENAME = database.SCHEMA_FILENAME

root_dir = Path(__file__).parents[1]

def insert_moisture_test_data(db, data_files):
    """Insert moisture data from csv files into specified database.
    
    This function expects data for four tables in csv format.
    
    Args:
        db: The Database object referring to the database.
        data_files: A dictionary containing table names as keys, 
            and file paths as values.
    """

    for table_name in data_files.keys():
        with open(data_files[table_name], 'r') as f:
            lines = f.readlines()

            # skip the header line
            for line in lines[1:]:
                separated = line.strip().split(",")
                print(separated)
                #print(separated)

                #db.insert_moisture_record(f"{separated[0]}", separated[1], f"{separated[2]}", separated[3])
                
                # Insert using Database interface methods
                if table_name == "devices":
                    db.add_device(separated[1], separated[2])
                elif table_name == "locations":
                    db.add_location(separated[1], separated[2], separated[3])
                elif table_name == "soil_readings":
                    db.add_reading(separated[1], separated[2], separated [3])
                elif table_name == "device_locations":
                    try:
                        db.add_device_location(separated[0], separated[2], separated[3], separated[1])
                    except IndexError as e:
                        separated.append(None)

def setup_script(db_name=None):
    global db_path
    db_path = None
    
    # Set db_path to use
    if db_name != None:
        db_path = root_dir.joinpath("db", db_name)
    


def execute(create_new, table_data=None):
    """Run the main functionality of the script
    
    Create a new database and if provided, insert data into it.

    Args:
        create_new: Boolean value determining if a new database is to
            be created or not when creating the Database object.
        table_data: Dictionary containing table name as keys and
            file path for the associated data as values.
    """


    print(f"Root directory used: {root_dir}")
    print(f"Database file being used: {db_path}")



    # Initialise a new database
    if db_path != None:
        db = Database(create_new, path=db_path)
    else:
        db = Database(create_new)

    if table_data != None:
        # Put data into new database
        insert_moisture_test_data(db, table_data)

    return db    


def run_script(initialise, db_name=None, moisture_data=None):
    setup_script(db_name)
    db = execute(initialise, moisture_data)

    return db

if __name__ == "__main__":
    run_script(True)