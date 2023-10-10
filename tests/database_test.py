import pytest
from pathlib import Path

from ..webserver import init_db


class TestDatabase():

    @pytest.fixture
    def root_dir(self):
        return Path(__file__.parent[1])


    @pytest.fixture
    def test_moisture_data(self, root_dir):
        test_data = root_dir.joinpath("misc", "src", "data", "test_moisture")
        return test_data
    

    @pytest.fixture
    def setup_database(self):
        print("\nSetting up database...")
    
        # Create new empty database
        init_db.run_script("test_database.db")
        

    def test_insert(self, setup_database):
        print("Testing")
        pass

