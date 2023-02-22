"""Generate data for testing the GardenStation database and web app.

Data for soil moisture and weather is required for GardenStation to work,
until the microcontrollers have been set up and are running fake data must
be used to test the web app which will be used to display said data.

The following data will be generated in the specified format.

Soil Moisture:
    DateTime,MoistureLevel,MonitorId

Weather Data:
    DateTime,Temperature

"""

from datetime import datetime
from datetime import timedelta

from pathlib import Path

import random

def next_datetime(dt_obj, h, m=0, s=0):
    """Create a new datetime object with specified time added to it.
    
    Args:
        dt_obj: The original datetime object to add time to.
        h, m, s: The amount of time to add (hours, minutes, seconds). 
            Only hours is required, minutes and seconds are optional 
            arguments.
    
    Returns: A datetime object with the specified delta from the original.
    """

    delta = timedelta(hours=h, minutes=m, seconds=s)
    new_datetime = dt_obj + delta

    return new_datetime


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
        date = next_datetime(prev_data[0], 1, 30)

    # Generate moisture data
    num = random.randrange(0, 1000)
    ran_float = num / 1000

    generated_data = [date, id, ran_float]

    return generated_data
    
def create_path(fname, directory):
    """Checks for existence of directory in same location as script file and 
    returns abs Path of file. Creates the directory if it does not exist.
    
    Args:
        fname: File name to append to path
        directory: The directory   

    Returns: A pathlib Path object with the absolute path of fname in directory.
    """
    py_file_path = Path(__file__).parent
    new_dir_path = Path.joinpath(py_file_path, directory)

    try:
        new_dir_path.mkdir()
    except FileExistsError:
        pass

    return Path.joinpath(new_dir_path, fname)

def generate_moisture_data(num, fname):
    """Generate a set of moisture data and save to disk.
    
    Args:
        num: Number of entries to generate.
        fname: The name of the file to save the data to.
    """

    # File directory should be /data located same directory as .py file
    abs_fpath = create_path(fname, 'data')

    with open(abs_fpath, 'w') as f:
        written_data_point = None
        for i in range(0, num):
            new_data_point = soil_data_point(written_data_point, 1)
            data_string = f"{new_data_point[0].isoformat()},{new_data_point[1]},{new_data_point[2]}\n"
            
            f.write(data_string)
            
            written_data_point = new_data_point

def generate_weather_data(num, fname):
    """Generate a set of weather data and save to disk.
    
    Args:
        num: Number of entries to generate.
        fname: The name of the file to save the data to.
    """

    abs_fpath = create_path(fname, 'data')

    with open(abs_fpath, 'w') as f:
        prev_date = datetime(2023, 1, 1, 4, 30)
        for i in range(num):
            # make date
            test_date = next_datetime(prev_date, 1, 30)
            # make temp
            test_temperature = random.randrange(20, 40)

            data_string = f"{test_date.isoformat()},{test_temperature}\n"
            f.write(data_string)

            prev_date = test_date


if __name__ == "__main__":
    generate_moisture_data(100, "test_moisture.txt")
    generate_weather_data(100, "test_weather.txt")

    #soil_data_point(None, 1)