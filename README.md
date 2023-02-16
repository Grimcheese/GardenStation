# NOTE: WORK IN PROGRESS
This project and this document are a work in progress. Everything outlined here is written to describe the current state of the project, future goals and as such will be updated to correctly reflect when something is actually implemented.
Eg: Using the word "is" rather than "will" to describe a technology (it *will* be this rather than it *is* this).

# Garden Station
Garden station is a web application that tracks data from my garden and displays it on a web page. It is designed using the LAMP stack framework.

The following data will be tracked:
- Moisture levels of the soil
- Temperature
- Wind speed and direction
- Air pressure

There should also be a live feed of the garden from the front.

Initially the web page should only be accessible to local traffic so the data can be accessed from home or devices connected via VPN. 

# Tech
## Web Server
The web server will be run using Apache 2.4. Currently using it on a Winodws installation however later the intent is to run it on a linux box vm.

## Database
DBMS: MySQL database with the following tables:   
- Weather records
- Soil Moisture

#### Weather Records
Primary Key: weather_id - TIMESTAMP
temperature - SMALLINT
air_pressure - INT
wind_direction - CHAR

#### Soil Moisture
Primary Key: soil_moisture_id - TIMESTAMP
moisture_level - FLOAT
location - CHAR


#### Soil Moisture

## Data Collection
The data collection will be done using microcontrollers that are fit for the job. The general idea is to have devices out in the garden colllecting the data and sending it back to a central device using wireless communication. This central device will then pass the data to the database on the server.