import pytest
from pathlib import Path

from ..webserver import init_db

@pytest.fixture
def root_dir():
    return Path(__file__).parents[1]


@pytest.fixture
def db_path():
    return "test_database.db"


@pytest.fixture
def db_test_data_path(root_dir):
    return root_dir.joinpath("misc", "src", "data")


@pytest.fixture
def test_soil_readings_data(db_test_data_path):
    return db_test_data_path.joinpath("soil_readings_soil_test_data.txt")


@pytest.fixture
def test_locations_data(db_test_data_path):
    return db_test_data_path.joinpath("locations_soil_test_data.txt")


@pytest.fixture
def test_devices_data(db_test_data_path):
    return db_test_data_path.joinpath("devices_soil_test_data.txt")


@pytest.fixture
def test_device_locations_data(db_test_data_path):
    return db_test_data_path.joinpath("device_locations_soil_test_data.txt")


@pytest.fixture
def test_soil_moisture_data(db_test_data_path):

    data_files = {}
    
    data_files["devices"] = db_test_data_path.joinpath("devices_soil_test_data.txt")
    data_files["locations"] = db_test_data_path.joinpath("locations_soil_test_data.txt")
    data_files["soil_readings"] = db_test_data_path.joinpath("soil_readings_soil_test_data.txt")
    data_files["device_locations"] = db_test_data_path.joinpath("device_locations_soil_test_data.txt")

    #test_data = root_dir.joinpath("misc", "src", "data", "test_moisture.txt")
    return data_files

@pytest.fixture
def get_test_data(test_soil_moisture_data):
    print("\nGet raw test data...")
    
    test_data = {}

    for table_name in test_soil_moisture_data.keys():
        with open(test_soil_moisture_data[table_name], 'r') as f:
            lines = []
            f.readline()
            for line in f.readlines():
                lines.append(line)
            
            test_data[table_name] = lines

    #with open(test_moisture_data, 'r') as f:
        #   f.readline()
        #  for line in f.readlines():
        #     lines.append(line)
            
    return test_data


@pytest.fixture
def setup_empty_database(db_path):
    print("\nSetting up empty database...")

    # Create new empty database
    database = init_db.run_script(True, db_path)
    return database

@pytest.fixture
def setup_dummy_database(db_path, test_soil_moisture_data):
    print("\nSetting up database with generated moisture data...")

    database = init_db.run_script(True, db_path, test_soil_moisture_data)
    return database