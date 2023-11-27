import pytest
from pathlib import Path
import datetime

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
    def test_moisture_data(self, root_dir):
        test_data = root_dir.joinpath("misc", "src", "data", "test_moisture.txt")
        return test_data
    
    
    @pytest.fixture
    def num_of_devices(self):
        return 4
    

    @pytest.fixture
    def get_test_data(self, test_moisture_data):
        print("\nGet raw test data...")
        
        lines = []
        with open(test_moisture_data, 'r') as f:
            f.readline()
            for line in f.readlines():
                lines.append(line)
                
        return lines
    

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


    """Unit tests"""

    def test_insert(self, get_test_data, setup_empty_database):
        """Insert moisture table records."""
        
        print("\nCheck insertion of single record into database")
        
        database = setup_empty_database
        test_data = get_test_data
        # Test insertion of each record
        for i in range(len(test_data)):
            line = test_data[i].strip().split(",")
            
            timestamp = line[0]
            reading = line[1]
            location = line[2]
            device_id = line[3]
            
            database._insert_record("moisture_readings", timestamp=timestamp, moisture=reading, location=location, device_id=device_id)

            check_record = database.get_moisture_from_timestamp(device_id, timestamp)
            assert len(check_record) == 1
            
            assert check_record[0]['timestamp'] == timestamp
            assert f"{check_record[0]['moisture']}" == reading
            assert check_record[0]['location'] == location
            assert f"{check_record[0]['device_id']}" == device_id


    def test_moisture_insert(self, get_test_data, setup_empty_database):
        pass


    def test_retrieve_all_records(self, test_moisture_data, setup_dummy_database, get_test_data):
        print("\nCheck retrieval of all records from specified device...\n")
        
        database = setup_dummy_database
        """
        # Get each line from the test data file
        with open(test_moisture_data, 'r') as f:
            for line in f.readlines():
                if line.strip().split(',')[3] == '0':
                    lines.append(line)
           """ 
        lines = get_test_data
        
        # Compare number of records in data file to records retrieved from db for each device
        for device_id in range(0, 4):
            device_lines = []
            for line in lines:
                if line.strip().split(',')[3] == f'{device_id}':
                    device_lines.append(line)
            
            records = database.get_all_moisture_from_device(device_id)
            assert len(device_lines) == len(records)

    
    def test_retrieve_date_range(self, setup_dummy_database, num_of_devices, get_test_data):
        print("\nCheck retrieval based on date range...")
        
        database = setup_dummy_database
        raw_data = get_test_data
        
        
        #Test data starts from 1/1/2023 6AM ends at 7/1/2023 10:30AM for 100 records
        minDate = raw_data[0].split(",")[0]
        maxDate = raw_data[-1].split(",")[0]
        
        # Get records from all devices for entire date range
        records = []
        for i in range(num_of_devices):
            print(f"Arguments: \n\tDevice: {i}\n\tStart: {minDate}   End: {maxDate}")
            device_records = database.get_moisture_from_device_range(i, minDate, maxDate)
            print(f"Device: {i}\n\tRecords: {device_records}")
            records.extend(device_records)

        assert len(records) == len(raw_data)
        
        # Get records from outside date range (before first)
        records = []
        for i in range(num_of_devices):
            lower_bound = datetime.datetime.fromisoformat(minDate) - datetime.timedelta(days=5)
            upper_bound = datetime.datetime.fromisoformat(minDate) - datetime.timedelta(hours=1)
            device_records = database.get_moisture_from_device_range(i, lower_bound, upper_bound)
            records.extend(device_records)

        assert len(records) == 0
        
        # Get records from outside date range (after last)
        records = []
        for i in range(num_of_devices):
            lower_bound = datetime.datetime.fromisoformat(maxDate) + datetime.timedelta(hours=1)
            upper_bound = datetime.datetime.fromisoformat(maxDate) + datetime.timedelta(days=365)
            device_records = database.get_moisture_from_device_range(i, lower_bound, upper_bound)
            records.extend(device_records)
            
        assert len(records) == 0
        
        # Get first record
        records = []
        for i in range(num_of_devices):
            lower_bound = datetime.datetime.fromisoformat(minDate)
            upper_bound = datetime.datetime.fromisoformat(minDate) + datetime.timedelta(minutes=10)
            device_records = database.get_moisture_from_device_range(i, lower_bound, upper_bound)
            records.extend(device_records)
            
        assert len(records) == 1


    def test_get_all_ids(self, setup_dummy_database, get_test_data):
        print("Getting all device id values...")
        
        database = setup_dummy_database

        ids = database.get_all_ids()

        for element in ids:
            print(element)

        # Assert that the returned id values is the same set as in the test data file
        ids_from_file = []
        for i in get_test_data:
            line = i.strip().split(",")
            if line[3] not in ids_from_file:
                ids_from_file.append(line[3])
        
        ids_from_file = [int(num) for num in ids_from_file]
        ids_from_file.sort()

        print(f"Device ids from the data: {ids_from_file}")
        print(f"Device ids from the database: {ids}")

        assert set(ids_from_file).intersection(ids)
              
    def test_get_all_locations(self, setup_dummy_database, get_test_data):
        print("Getting all locations...")
        
        db = setup_dummy_database
        locations = db.get_all_locations()
        
        locations_from_file = []
        for line in get_test_data:
            line = line.strip().split(",")
            if line[2] not in locations_from_file:
                locations_from_file.append(line[2])
        
        print(locations)
