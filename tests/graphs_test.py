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
        data = database.get_all_moisture_from_device(0)

        return data


    @pytest.fixture
    def test_data(self):
        """Rows returned from a database query."""        

    def test_generate(self, query_database_moisture_data):
        """Generate a graph from a list of data in the database."""

        graphs.generate_moisture_graph(query_database_moisture_data)
