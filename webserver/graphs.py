"""Create plotly graphs using data from the database"""

from ..webserver.database import Database
from pathlib import Path

from ..webserver import init_db

import plotly.graph_objects as go

def get_default_data(db, device, start, end):
    data = db.get_moisture_from_device_range(device, start, end)

    return data

def generate_moisture_graph(data):
    print("Data retrieved:")
    for element in data:
        print(element)

    extractedData = tuple([(element["timestamp"], element["moisture"]) for element in data])

    for t in extractedData:
        print(t)
    fig = go.Figure([go.Bar(x=extractedData[1], y=extractedData[0])])
    fig.show()

if __name__ == '__main__':
    db_path = Path(__file__).parents[1].joinpath("db","test_database.db")
    
    db = init_db.run_script(True, "test_database.db", Path(__file__).parents[1].joinpath("misc", "src", "test_moisture.txt"))
    
    #db = Database(db_path)

    data = db.get_all_moisture_from_device(0)
    generate_moisture_graph(data)