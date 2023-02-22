"""Generate data for testing the GardenStation database and web app.

Data for soil moisture and weather is required for GardenStation to work,
until the microcontrollers have been set up and are running fake data must
be used to test the web app which will be used to display said data.

The following data will be generated in the specified format.

Soil Moisture:
    DateTime,MoistureLevel,MonitorId

Weather Data:
    DateTime,Temperature,WindDirection

"""

from datetime import datetime
from datetime import timedelta

from pathlib import Path

import random

def soil_data_point(prev_data, id, mode='random'):
    """Take a previous soil data point and generate the next one.
    
    Data is generated according to mode specified. 

    Modes:
        Random - A random float between 0 and 1 to 3 decimal places is 
            generated.

    Args:
        prev_data: The previous data point generated. If None then use
            inital datetime value.
        id: The id number of the "device" generating data. 
    """
    # Get datetime object
    if prev_data == None:
        date = datetime(2023, 1, 1, 6)
    else:
        old_date = prev_data[0]
        delta = timedelta(hours=1)
        date = old_date + delta

    # Generate moisture data
    num = random.randrange(0, 1000)
    ran_float = num / 1000

    generated_data = [date, id, ran_float]

    return generated_data
    

def generate_moisture_data(num, fname):
    """Generate a set of moisture data and save to disk.
    
    Args:
        num: Number of entries to generate.
        fname: The name of the file to save the data to.
    """

    # File directory should be /data located same directory as .py file
    abs_fpath = Path.joinpath(Path(__file__).parent, "data", fname)

    with open(abs_fpath, 'w') as f:
        written_data_point = None
        for i in range(0, num):
            new_data_point = soil_data_point(written_data_point, 1)
            data_string = f"{new_data_point[0].isoformat()},{new_data_point[1]},{new_data_point[2]}\n"
            
            f.write(data_string)
            
            written_data_point = new_data_point

def generate_weather_data():
    """Generate a set of weather data and save to disk.
    
    Args:
        num: Number of entries to generate.
        fname: The name of the file to save the data to.
    """

if __name__ == "__main__":
    generate_moisture_data(100, "test_moisture.txt")
    #generate_weather_data()

    #soil_data_point(None, 1)