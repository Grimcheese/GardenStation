import pytest
from pathlib import Path

from ..webserver import init_db
from ..webserver import graphs

class TestGraphing():

    @pytest.fixture
    def test_db(self):
        return "test_database.db"


    @pytest.fixture
    def root_dir(self):
        return Path(__file__).parents[1]


    @pytest.fixture
    def test_moisture_data(self, root_dir):
        test_data = root_dir.joinpath("misc", "src", "data", "test_moisture.txt")
        return test_data


    @pytest.fixture
    def setup_dummy_database(self, test_db, test_moisture_data):
        database = init_db.run_script(True, test_db, test_moisture_data)
        return database


    @pytest.fixture
    def query_database_moisture_data(self, setup_dummy_database):
        database = setup_dummy_database
        data = database.get_all_moisture_from_column_id('device_id', 0)

        return data


    @pytest.fixture
    def test_data(self):
        """Rows returned from a database query."""        

    """ Unit Tests """
    
    def test_create_graphs(self, setup_dummy_database):
        """Check that correct number of graphs are created."""

        db = setup_dummy_database

        all_ids = db.get_unique_column_vals("device_id")
        JSONgraphs = graphs.create_graphs(db, "device_id")

        assert len(all_ids) == len(JSONgraphs.keys())

        all_locations = db.get_unique_column_vals("location")
        JSONgraphs = graphs.create_graphs(db, "location")

        assert len(all_locations) == len(JSONgraphs.keys())
