# sqlalchemy-challenge

The project involved analyzing and exploring climate data using Python, SQLAlchemy, Pandas, and Matplotlib. The tasks were performed using the provided files: climate_starter.ipynb and hawaii.sqlite.

## Part 1:
In Part 1, the focus was on conducting a climate analysis and data exploration of the climate database. The following steps were followed:

The SQLAlchemy create_engine() function was used to establish a connection to the SQLite database.

The SQLAlchemy automap_base() function was employed to reflect the tables into classes, specifically the station and measurement classes.

A SQLAlchemy session was created to link Python to the database, ensuring the ability to perform queries and retrieve data.

Precipitation analysis was performed by finding the most recent date in the dataset and then querying the previous 12 months of precipitation data. The queries selected only the "date" and "prcp" values, and the results were loaded into a Pandas DataFrame. The DataFrame was sorted by date and plotted using the DataFrame plot method. Summary statistics for the precipitation data were also printed using Pandas.

Station analysis involved designing queries to calculate the total number of stations in the dataset and to identify the most active stations. The most-active station was determined by listing the stations and their observation counts in descending order. Additionally, a query was designed to calculate the lowest, highest, and average temperatures for the most-active station. To further explore the temperature observations (TOBS), a query was created to retrieve the previous 12 months of TOBS data for the most-active station. The TOBS data was then plotted as a histogram with 12 bins.

The SQLAlchemy session was closed to ensure proper resource management.

## Part 2:
In Part 2, the task was to design a Flask API based on the queries and analyses performed in Part 1. The following routes were created:

/: This route represents the homepage and lists all the available routes.

/api/v1.0/precipitation: This route retrieves the query results from the precipitation analysis (last 12 months of data) and converts them into a dictionary, with the date as the key and the precipitation as the value. The route returns the JSON representation of the dictionary.

/api/v1.0/stations: This route returns a JSON list of stations from the dataset.

/api/v1.0/tobs: This route queries the dates and temperature observations of the most-active station for the previous year of data. It returns a JSON list of temperature observations for the previous year.

/api/v1.0/<start> and /api/v1.0/<start>/<end>: These routes calculate the minimum temperature, average temperature, and maximum temperature for a specified start date or start-end range. For a specified start date, the calculations are performed for all dates greater than or equal to the start date. For a specified start and end date, the calculations are done for the dates within the specified range, inclusive. The results are returned as a JSON list.
