"""Flask application to handle web requests for GardenStation."""

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.shtml')

@app.route('/weather')
def weather_page():
    return render_template('weather.html')

@app.route('/soil')
def soil_page():
    return render_template('soil.html')