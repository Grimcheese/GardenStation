# Garden Station
Garden station is a web application that tracks data from my garden and displays it on a web page.  
The following data will be tracked:
- Moisture levels of the soil
- Temperature
- Wind speed and direction
- Air pressure

There should also be a live feed of the garden from the front.

# Tech
## Web Server
The web server will be run using Apache 2.4. Currently using it on a Winodws installation however later the intent is to run it on a linux box vm.
## Database
To be decided.
## Data Collection
The data collection will be done using microcontrollers that are fit for the job. The general idea is to have devices out in the garden colllecting the data and sending it back to a central device using wireless communication. This central device will then pass the data to the database on the server.