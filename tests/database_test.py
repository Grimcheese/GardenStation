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
    def db_test_data_path(self, root_dir):
        return root_dir.joinpath("misc", "src", "data")


    @pytest.fixture
    def test_soil_readings_data(self, db_test_data_path):
        return db_test_data_path.joinpath("soil_readings_soil_test_data.txt")


    @pytest.fixture
    def test_locations_data(self, db_test_data_path):
        return db_test_data_path.joinpath("locations_soil_test_data.txt")


    @pytest.fixture
    def test_devices_data(self, db_test_data_path):
        return db_test_data_path.joinpath("devices_soil_test_data.txt")


    @pytest.fixture
    def test_device_locations_data(self, db_test_data_path):
        return db_test_data_path.joinpath("device_locations_soil_test_data.txt")


    @pytest.fixture
    def test_soil_moisture_data(self, db_test_data_path):

        data_files = {}
        
        data_files["devices"] = db_test_data_path.joinpath("devices_soil_test_data.txt")
        data_files["locations"] = db_test_data_path.joinpath("locations_soil_test_data.txt")
        data_files["soil_readings"] = db_test_data_path.joinpath("soil_readings_soil_test_data.txt")
        data_files["device_locations"] = db_test_data_path.joinpath("device_locations_soil_test_data.txt")

        #test_data = root_dir.joinpath("misc", "src", "data", "test_moisture.txt")
        return data_files
    

    @pytest.fixture
    def num_of_devices(self):
        return 4
    

    @pytest.fixture
    def get_test_data(self, test_soil_moisture_data):
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
    def setup_empty_database(self, db_path):
        print("\nSetting up empty database...")
    
        # Create new empty database
        database = init_db.run_script(True, db_path)
        return database

    @pytest.fixture
    def setup_dummy_database(self, db_path, test_soil_moisture_data):
        print("\nSetting up database with generated moisture data...")

        database = init_db.run_script(True, db_path, test_soil_moisture_data)
        return database


    @pytest.fixture
    def get_latest_date(self, get_test_data):
        max_date = datetime.datetime(year=1990,month=1,day=1)
        for reading in get_test_data["soil_readings"]:
            split_col = reading.split(",")
            timestamp = split_col[1]

            dt_timestamp = datetime.datetime.fromisoformat(timestamp)
            if max_date < dt_timestamp:
                max_date = dt_timestamp

        return max_date



    """Unit tests"""

    def test_add_device(self, setup_empty_database, get_test_data):
        """Add devices to the database"""

        print("Check insertion of records to the devices table")

        database = setup_empty_database
        test_devices = get_test_data["devices"]

        for i in range(len(test_devices)):
            line = test_devices[i].strip().split(",")

            software_version = line[1]
            microprocessor = line[2]

            database.add_device(software_version, microprocessor)

            devices = database.execute_query("SELECT * FROM devices;")

            # Check that data from csv can be added to db without errors
            assert len(devices) == i + 1

            # Check that 


    def test_add_locations(self, setup_empty_database, get_test_data):
        """Add locations to the database"""

        print("Check insertion of records to the locations table")

        database = setup_empty_database
        test_locations = get_test_data["locations"]
        for i in range(len(test_locations)):
            line = test_locations[i].strip().split(",")

            latitude = line[1]
            longitude = line[2]
            address = line[3]

            database.add_location(latitude, longitude, address)
            
            locations = database.execute_query("SELECT * FROM locations;")

            assert len(locations) == i + 1


    def test_add_soil_readings(self, setup_empty_database, get_test_data):
        """Add soil readings to the database"""

        print("Check insertion of records to the soil readings table")


    def test_add_device_locations(self, setup_empty_database, get_test_data):
        """Add device locations to the database"""
    
        print("Check insertion of records to the device_locations table")


    def test_retrieve_date_range(self, get_latest_date, setup_dummy_database, num_of_devices, get_test_data):
        print("\nCheck retrieval based on date range...")
        
        database = setup_dummy_database
        raw_data = get_test_data
        
        #Test data starts from 1/1/2023 6AM ends at 7/1/2023 10:30AM for 100 records
        min_date = datetime.datetime(year=3000,month=1,day=1)
        for reading in raw_data["soil_readings"]:
            tmp_date_string = reading.split(",")[1]
            tmp_date_obj = datetime.datetime.fromisoformat(tmp_date_string)

            if tmp_date_obj < min_date:
                min_date = tmp_date_obj

        max_date = get_latest_date #Gets latest date from raw data
        
        # Get records from all devices for entire date range
        db_query_results = database.get_moisture_from_timestamp_range(min_date, max_date)
        
        assert len(db_query_results) == len(raw_data["soil_readings"])
        
        # Get records from outside date range (before first)
        lower_bound = min_date- datetime.timedelta(days=5)
        upper_bound = min_date - datetime.timedelta(hours=1)            
        db_query_results = database.get_moisture_from_timestamp_range(lower_bound, upper_bound)

        assert len(db_query_results) == 0
        
        # Get records from outside date range (after last)

        lower_bound = max_date + datetime.timedelta(hours=1)
        upper_bound = max_date + datetime.timedelta(days=365)
        db_query_results = database.get_moisture_from_timestamp_range(lower_bound, upper_bound)
            
        assert len(db_query_results) == 0
    

    def test_get_unique_column_vals(self, setup_dummy_database, get_test_data):
        
        # Test getting all devices
        print("Getting all device id values...")
        
        database = setup_dummy_database

        ids = database.get_unique_column_vals("device_id")

        for element in ids:
            print(element)

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

        # Test getting all locations
        print("Getting values based on seleted column...")

        print("\tChecking locations...")
        db = setup_dummy_database
        locations = db.get_unique_column_vals("location")

        locations_from_file = []
        for line in get_test_data:
            line = line.strip().split(",")
            if line[2] not in locations_from_file:
                locations_from_file.append(line[2])

        locations_from_file.sort()
        
        print(f"Locations from the data: {locations_from_file}")
        print(f"Locations from the database: {locations}")

        assert set(locations_from_file).intersection(locations)