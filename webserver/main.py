"""Flask application to handle web requests for GardenStation."""

from flask import Flask
from flask import render_template, redirect

from ..webserver import graphs
from ..webserver.database import Database

from pathlib import Path

app = Flask(__name__)

@app.route('/')
def root_redirect():
    return redirect('/home/')


@app.route('/home/')
def home_page():
    return render_template('index.html')


@app.route('/weather/')
def weather_page():
    return render_template('weather.html')


@app.route('/soil/')
def soil_page():
    # Generate default data graphs for each device with recorded data

    
    return render_template('soil.html')


@app.route('/graph')
def graph_page():
    db_path = Path(__file__).parents[1].joinpath("db", "test_database.db")

    db = Database(False, db_path)

    # Just get some data from the database - implement options later
    dataset = db.get_all_moisture_from_device(0)
    graphJSON = graphs.get_line_graph_JSON(dataset,"timestamp", "moisture")    

    return render_template('graph.html', title="Device 0", graphJSON=graphJSON)


if __name__ == "__main__":
    app.run(debug=True)
