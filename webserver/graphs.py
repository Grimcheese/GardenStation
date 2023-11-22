"""Create plotly graphs using data from the database"""

from ..webserver.database import Database
from pathlib import Path

from ..webserver import init_db

import pandas as pd
import json
import plotly
import plotly.graph_objects as go
import plotly.express as px

def get_default_data(db, device, start, end):
    data = db.get_moisture_from_device_range(device, start, end)

    return data

def get_line_graph_JSON(data, xVal, yVal):
    fig = px.line(data, x=xVal, y=yVal)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def generate_all_default_graphs(db):
    # Get all device ids stored in database

    # For each unique id get the complete dataset

    # return dict of each graph in JSON encoded format
    pass

def generate_moisture_graph(data):
    print("Data retrieved:")
    for element in data:
        print(element)

    extractedData = tuple([(element["timestamp"], element["moisture"]) for element in data])

    for t in extractedData:
        print(t)

    fig = px.line(data, x="timestamp", y="moisture")
    fig.show()

if __name__ == '__main__':
    db_path = Path(__file__).parents[1].joinpath("db","test_database.db")
    
    db = init_db.run_script(True, "test_database.db", Path(__file__).parents[1].joinpath("misc", "src", "test_moisture.txt"))
    
    #db = Database(db_path)

    data = db.get_all_moisture_from_device(0)
    generate_moisture_graph(data)

    data = db.get_all_moisture_from_device(1)
    generate_moisture_graph(data)