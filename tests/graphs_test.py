import pytest
from pathlib import Path

from ..webserver import init_db
from ..webserver import graphs

class TestGraphing():

    @pytest.fixture
    def query_database_moisture_data(self, setup_dummy_database):
        database = setup_dummy_database
        data = database.get_all_moisture_from_column_id('device_id', 0)

        return data

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
