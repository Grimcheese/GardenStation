import pytest
from pathlib import Path
import datetime

from ..webserver import init_db
from ..webserver.database import Database


class TestDatabase():

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


    def test_retrieve_date_range(self, get_latest_date, setup_dummy_database, get_test_data):
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
    