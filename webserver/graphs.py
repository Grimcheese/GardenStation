"""Create plotly graphs using data from the database"""

from ..webserver.database import Database
from pathlib import Path

from ..webserver import init_db

import pandas as pd
import json
import plotly
import plotly.graph_objects as go
import plotly.express as px

def create_line_graph(data, xVal, yVal):
    """Create a plotly line graph from a dataset.
    
    Args:
        xVal: The dictionary key used to access the data on the x-axis.
        yVal: The dictionary key used to access the data on the y-axis
    
    Returns: A plotly graph.
    """

    fig = px.line(data, x=xVal, y=yVal)
    
    fig.update_xaxes(title_text="Time/Date")
    fig.update_yaxes(title_text="Moisture Level")

    return fig


def create_line_graph_JSON(data, xVal, yVal):
    """Get the JSON representation of a plotly line graph.
    
    Args:
        data: The data retrieved from the database to display in the graph.
        xVal: Dictionary key to use for data displayed on the x-axis.
        yVal: Dictionary key to use for data displayed on the y-axis.
        
    Return: A plotly graph encoded as a JSON object.
    """
    
    line_graph = create_line_graph(data, xVal, yVal)
    
    graphJSON = json.dumps(line_graph, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_graphs(db, graph_identity):
    """Create a series of graphs for use in default /soil page.
    
    Args:
        graph_identity: Name of the table column in the database to select
            and sort tables by. E.g: graph_identity of device_id creates a 
            new graph for each device_id found in the moisture_reading 
            database.
    
    Returns: A dictionary of plotly graphs encoded in JSON format. The graphs
        are each mapped to an identifier linked to the data used for the graph.
    """
    
    # Get all unique values of a column
    loaded_identifiers = db.get_unique_column_vals(graph_identity)

    # For each identifier get all records and create JSON graph
    JSONgraphs = {}
    for id in loaded_identifiers:
        data = db.get_all_moisture_from_column_id(graph_identity, id)
        JSONgraphs[id] = create_line_graph_JSON(data, "timestamp", "moisture")

    return JSONgraphs


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