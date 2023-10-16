import pytest
from pathlib import Path

from ..webserver import init_db
from ..webserver.database import Database


class TestDatabase():

    @pytest.fixture
    def root_dir(self):
        return Path(__file__).parents[1]

    @pytest.fixture
    def db_path(self):
        return "test_database.db"

    @pytest.fixture
    def test_db_path(self, root_dir, db_path):
        return root_dir.joinpath("db", db_path)

    @pytest.fixture
    def test_moisture_data(self, root_dir):
        test_data = root_dir.joinpath("misc", "src", "data", "test_moisture.txt")
        return test_data
    

    @pytest.fixture
    def setup_empty_database(self, db_path):
        print("\nSetting up empty database...")
    
        # Create new empty database
        database = init_db.run_script(True, db_path)
        return database

    @pytest.fixture
    def setup_dummy_database(self, db_path, root_dir, test_moisture_data):
        print("\nSetting up database with generated moisture data...")

        database = init_db.run_script(True, db_path, test_moisture_data)
        return database

    def test_(self, test_db_path):
        """Create a new database using a schema file."""
        pass


    def test_retrieve_all_records(self, test_moisture_data, test_db_path, setup_dummy_database):
        database = setup_dummy_database
        records = database.get_all_moisture_from_device(0)

        for record in records:
            print(record)
        
        lines = []
        # Get each line from the test data file
        with open(test_moisture_data, 'r') as f:
            for line in f.readlines():
                print(line.strip().split(','))
                if line.strip().split(',')[3] == '0':
                    lines.append(line)

        # Get correct number of rows based on device id
        assert len(lines) == len(records)

    
    def test_retrieve_single_records(self):
        pass

    def test_insert(self):
        """Insert moisture table records."""
        pass
