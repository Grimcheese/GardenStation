# Decisions
Throughout the development of this project certain decisions had to be made each with their own trade-offs and reasonings. Here some of the ones I noticed are written down to be used later for further writing or self analysis.

# Abstracting Line Graph Creation 

# Introduction
For the default graph display on requests to /soil the web app retrieves the data recorded for each location stored in the database. This was initially done through a method call in graphs.py that would get all the ids, get the data for each id, then create a line graph for each id.

A further revision involved grouping each graph by location, rather than device id. 
I prefer to abstract methods down as much as possible