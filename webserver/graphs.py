"""Create plotly graphs using data from the database"""

from ..webserver.database import Database
from pathlib import Path

from ..webserver import init_db

import pandas as pd
import json
import plotly
import plotly.graph_objects as go
import plotly.express as px


def create_line_graph_JSON(data, xVal, yVal):
    """Get the JSON representation of a plotly line graph.
    
    Args:
        data: The data retrieved from the database to display in the graph.
        xVal: Dictionary key to use for data displayed on the x-axis.
        yVal: Dictionary key to use for data displayed on the y-axis.
        
    Return: A plotly graph encoded as a JSON object.
    """
    
    fig = px.line(data, x=xVal, y=yVal)
    
    fig.update_xaxes(title_text="Time/Date")
    fig.update_yaxes(title_text="Moisture Level")
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def create_graphs(db, graph_identity):
    """"""
    
    # Get all unique values of a column
    loaded_identifiers = db.get_unique_column_vals(graph_identity)

    # For each identifier get all records and create JSON graph
    JSONgraphs = {}
    for id in loaded_identifiers:
        data = db.get_all_moisture_from_column_id(graph_identity, id)
        JSONgraphs[id] = create_line_graph_JSON(data, "timestamp", "moisture")

    return JSONgraphs

def get_all_default_device_graphs(db):
    """Get the default JSON representation of the graphs for each device in the database.
    
    Args:
        db: Database object that contains soil moisture data to be displayed.
        
    Return: Dictionary of plotly graphs encoded into JSON objects. The key value
        is the device_id for the device the data has been recorded from.
    """
    # Get all device ids stored in database
    ids = db.get_all_ids()
    
    # For each unique id get the complete dataset and create JSON graph
    JSONgraphs = {}
    for id in ids:
        device_data = db.get_all_moisture_from_device(id)
        JSONgraphs[id] = create_line_graph_JSON(data, "timestamp", "moisture")
    
    return JSONgraphs


def get_all_default_location_graphs(db):
    """Get the default graphs for each location in JSON format"""

    locations = db.get_all_locations()

    JSONgraphs = {}




def generate_moisture_graph(data):
    """Create a plotly graph using data passed in as an argument.
    
    Args:
        data: List of records retrieved from the SQLite database to be displayed. 
            Each record must have a timestamp and moisture column to be accessed.
    """
    
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