"""Generate data for testing the GardenStation database and web app.

Data for soil moisture and weather is required for GardenStation to work,
until the microcontrollers have been set up and are running fake data must
be used to test the web app which will be used to display said data.

Data will be generated for the following tables in csv format:

devices:
    device_id, software_version, microprocessor

locations:
    location_id, latitude, longitude, loc_address

soil_readings:
    reading_id, reading_time, soil_reading, device_id, location_id

device_locations:
    device_id, location_id, date_placed, date_removed

"""

from datetime import datetime
from datetime import timedelta

from pathlib import Path

import random

def next_datetime(dt_obj, d=0, h=0, m=0, s=0):
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

@DeprecationWarning
def soil_data_point(prev_data, id, location, mode='random'):
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
        date = next_datetime(prev_data['date'], 1, 30)

    # Generate moisture data
    num = random.randrange(0, 1000)
    ran_float = num / 1000

    generated_data = {"date":date, "reading":ran_float, "location":location, "id":id}

    return generated_data
    
def create_path(fname, directory, root_dir=Path(__file__).parent):
    """Checks for existence of directory in same location as script file and 
    returns abs Path of file. Creates the directory if it does not exist.
    
    Args:
        fname: File name to append to path
        directory: The directory   
        root_dir: The root directory to create the new directory/file in.
            Default argument is to the same directory as this file.

    Returns: A pathlib Path object with the absolute path of fname in directory.
    """

    new_dir_path = Path.joinpath(root_dir, directory)

    try:
        new_dir_path.mkdir()
    except FileExistsError:
        pass

    return Path.joinpath(new_dir_path, fname)


@DeprecationWarning
def generate_moisture_data(num, fname):
    """Generate a set of moisture data and save to disk.
    
    Args:
        num: Number of entries to generate.
        fname: The name of the file to save the data to.
    """

    # File directory should be /data located same directory as .py file
    abs_fpath = create_path(fname, 'data')

    device_map = {0:"front-window", 1:"front-side", 2:"back-garden", 3:"front-corner"}

    with open(abs_fpath, 'w') as f:
        # Create header
        f.write("timestamp,moisture_reading,location,device_id\n")

        written_data_point = None
        for i in range(0, num):
            dev_id = random.randrange(0, 4)
            dev_location = device_map[dev_id]

            new_data_point = soil_data_point(written_data_point, dev_id, dev_location)
            data_string = f"{new_data_point['date'].isoformat(' ')},{new_data_point['reading']},{new_data_point['location']},{new_data_point['id']}\n"
            
            f.write(data_string)
            
            written_data_point = new_data_point


@DeprecationWarning
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


def create_devices(num):
    """Create devices to be stored in db.
    
    Devices will just be created with default values for software
    version and microprocessor. 

    Args:
        num: Number of devices to create.
        
    """

    default_version = '0.1'
    default_microprocessor = 'Arduino Uno'

    devices = []
    for i in range(num):
        current_device = [i, default_version, default_microprocessor]
        devices.append(current_device)

    return devices


def create_locations(num):
    """ Create locations to be stored in db.
    
    Args:
        num: Number of locations to create.
    """
    # top left -3.446694622420489, 82.5136624361147
    # bottom left -8.228272639512625, 80.00517852398696
    # top right -1.619456846560301, 95.31738240426665
    # bottom right -17.14066880626033, 98.40072721292364
    
    latitude_max = -3.446694622420489
    latitude_min = -17.14066880626033

    longitude_max = 80.00517852398696
    longitude_min = 98.40072721292364

    default_address = '400 Road Street Ave, Place'
    
    
    locations = []
    for i in range(num):
        lat = random.randrange(latitude_max, latitude_min)
        long = random.randrange(longitude_max, longitude_min)

        current_location = [i, lat, long, default_address]
        locations.append(current_location)

    return locations


def create_csv(fname, fields, data):
    """Create a csv file with field and data values.
    
    Args:
        fname: The file name to use for csv file.
        fields: The field names for data on subsequent lines.
        data: List of all data to write to file.
        
    """

    abs_fpath = create_path(fname, 'data')

    with open(abs_fpath, 'x') as f:
        f.write(fields)
        f.writelines(data) # NOTE may need to add new line separators


def create_device_locations(devices, locations):
    """Create device_locations data for db.
    
    Each device must be placed in at least one place. If there are 
    unused locations create a new record at a random time interval
    and update the previous device_locations entry for that device.
    
    Args:
        devices: Devices that have been generated for use in db.
        locations: Locations that have been generated for use in db.
    """

    start_date = datetime(2024,1,1,6)

    device_locations = []

    # Assign all devices an initial location
    loc_index = 0
    for dev in devices:
        current_dev_loc = [dev[0], locations[loc_index][0], start_date]
        device_locations.append(current_dev_loc)
        
        loc_index += 1

    # place device in a new location after a random amount of time
    device_move_index = 0
    while loc_index < len(locations):
        
        move_date = None # May need to catch exception if move_date assignment fails

        # Find and update initial device_location record
        f_index = -1
        for i in range(len(device_locations)):
            if device_locations[i][0] == device_move_index and len(device_locations) == 3:
                f_index = i
                
                days_to_move = random.randint(7,40)
                move_date = next_datetime(device_locations[i][2], days_to_move)
                
                device_locations[i] = [device_move_index, locations[loc_index], device_locations[i][2], move_date]

        # Create new device_locations record
        device_locations.append(device_move_index, locations[loc_index][0], move_date)

        # Update index values assume that a device is moved on each loop
        if device_move_index == len(devices):
            device_move_index = 0
        else:
            device_move_index += 1

        loc_index += 1

    return device_locations


def create_samples(num, devices, start_time):
    """Generate a series of data points for each device.
    
    Args:
        num: The number of samples to create per device.
        devices: The devices to be used for the reading.
        start_time: The datetime for the start of the data set.
    
    """

    samples = []

    for device in devices:
        current_time = start_time
        for i in range(num):
            # generate reading value (random)
            num = random.randrange(0, 1000)
            ran_float = num / 1000
            
            # calculate datetime
            current_time = next_datetime(current_time, 0, 1)

            samples.append(len(samples), current_time, ran_float, device[0])

    return samples
            


def generate_soil_reading_table_data(device_num, location_num, sample_num, fname):
    """Generate data for soil reading tables.
    
    Create data for the devices, locations, soil_readings and 
    device_locations tables in the database and then write to
    file in csv format.
    
    Args:
        device_num: number of devices to create
        location_num: number of locations to create
        sample_num: number of soil reading samples to create
        fname: name of file containing test data
    """

    devices = create_devices(device_num)
    locations = create_locations(location_num)
    device_locations = create_device_locations(devices, locations)
    samples = create_samples(devices, locations, sample_num)

    create_csv(f"devices_{fname}", "device_id,software_version,microprocessor",
               devices)
    create_csv(f"locations_{fname}", "location_id,latitude,longitude,loc_address",
               locations)
    create_csv(f"device_locations_{fname}", "device_id,location_id,date_placed,date_removed",
               device_locations)
    create_csv(f"soil_readings_{fname}", "reading_id,reading_time,soil_reading,device_id,location_id",
               samples)


def main():
    generate_soil_reading_table_data(100, "soil_test.txt")
    #generate_moisture_data(100, "test_moisture.txt")
    #generate_weather_data(100, "test_weather.txt")

if __name__ == "__main__":
    main()