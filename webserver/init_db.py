"""Initialise a new database with generated dummy data"""

from pathlib import Path

from .database import Database

DATABASE_FILENAME = None
#SCHEMA_FILENAME = database.SCHEMA_FILENAME

root_dir = Path(__file__).parents[1]

def insert_moisture_test_data(db, test_data_file):
    """Insert moisture data from a csv file into specified database."""

    with open(test_data_file, 'r') as f:
        lines = f.readlines()

        # skip the header line
        for line in lines[1:]:
            separated = line.strip().split(",")
            #print(separated)

            db.insert_moisture_record(f"{separated[0]}", separated[1], f"{separated[2]}", separated[3])

def setup_script(db_name=None):
    global db_path
    db_path = None
    
    # Set db_path to use
    if db_name != None:
        db_path = root_dir.joinpath("db", db_name)
    


def execute(create_new, moisture_test_data=None):
    print(f"Root directory used: {root_dir}")
    print(f"Database file being used: {db_path}")



    # Initialise a new database
    if db_path != None:
        db = Database(create_new, path=db_path)
    else:
        db = Database(create_new)

    if moisture_test_data != None:
        # Put data into new database
        insert_moisture_test_data(db, moisture_test_data)

    return db    


def run_script(initialise, db_name=None, moisture_data=None):
    setup_script(db_name)
    db = execute(initialise, moisture_data)

    return db

if __name__ == "__main__":
    run_script(True)