"""Flask application to handle web requests for GardenStation."""

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/home')
def home_page():
    return render_template('../web/hello.shtml')