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

def soil_data_point(prev_data, mode='random'):
    """Take a previous soil data point and generate the next one.
    
    Data is generated according to mode specified. 

    Modes:
        Random - A random float between 0 and 1 to 3 decimal places is 
            generated.

    Args:
        prev_data: The previous data point generated. If None then use
            inital datetime value.
    """

    if prev_data == None:
        date = datetime(2023, 1, 1)
    else:
        date = prev_data.strip(",")[0]
    print(date)
    

def generate_moisture_data(num, fname):
    """Generate a set of moisture data and save to disk.
    
    Args:
        num: Number of entries to generate.
        fname: The name of the file to save the data to.
    """

    with open(fname, 'w') as f:
        current_data_point = None
        for i in range(0, num):
            new_data_point = soil_data_point(current_data_point)
            f.write(new_data_point)

            current_data_point = new_data_point


def generate_weather_data():
    """Generate a set of weather data and save to disk.
    
    Args:
        num: Number of entries to generate.
        fname: The name of the file to save the data to.
    """

if __name__ == "__main__":
    generate_moisture_data(100, "/data/test_moisture.txt")
    generate_weather_data()