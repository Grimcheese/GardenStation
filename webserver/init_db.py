"""Initialise a new database with generated dummy data"""

from pathlib import Path

from . import database

DATABASE_FILENAME = None
SCHEMA_FILENAME = database.SCHEMA_FILENAME

root_dir = Path(__file__).parents[1]

def insert_moisture_test_data(test_data_file, db=None):
    """Insert moisture data from a csv file into specified database."""

    test_moisture_path = Path.joinpath(root_dir, "misc", "src", "data", "test_moisture.txt")
    with open(test_data_file, 'r') as f:
        lines = f.readlines()

        # skip the header line
        for line in lines[1:]:
            separated = line.strip().split(",")
            print(separated)

            if db != None:
                database.insert_moisture_record(f"{separated[0]}", separated[1], f"{separated[2]}", separated[3], db)
            else:
                database.insert_moisture_record(f"{separated[0]}", separated[1], f"{separated[2]}", separated[3])


def setup_script(db_name=None):
    global db_path
    db_path = None
    
    # Set db_path to use
    if db_name != None:
        db_path = root_dir.joinpath("db", db_name)
    


def execute(moisture_test_data=None):
    print(f"Root directory used: {root_dir}")
    print(f"Database file being used: {db_path}")

    # Initialise a new database
    if db_path != None:
        database.create_from_schema(database=db_path)
    else:
        database.create_from_schema()

    if moisture_test_data != None:
        # Put data into new database
        if db_path != None:
            insert_moisture_test_data(moisture_test_data, db_path)
        else:
            insert_moisture_test_data(moisture_test_data)


def run_script(db_name=None, moisture_data=None):
    setup_script(db_name)
    execute(moisture_data)

if __name__ == "__main__":
    run_script()