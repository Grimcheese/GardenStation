"""Flask application to handle web requests for GardenStation."""

from flask import Flask
from flask import render_template, redirect

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
    # Generate default data graphs
    return render_template('soil.html')

if __name__ == "__main__":
    app.run(debug=True)
