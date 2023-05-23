# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route('/')
def welcome():
    '''List all available routes'''
    return(
        f"Web Page Home<br/>"
        f"Available Routes:<br/>"
        f"- /api/v1.0/precipitation : Dictionary containing most recent 12 months of precipitation data in the database (key format YYYY-MM-DD<br/>"
        f"- /api/v1.0/stations : List of stations involved in data collection<br/>"
        f"- /api/v1.0/tobs : List of temperatures at the most active station over the most recent year of data<br/>"
        f"- /api/v1.0/<start> : Given a start date in format YYYY-MM-DD, returns list of min, avg, and max temperatures from the start to the most recent date in the database<br/>"
        )

@app.route('/api/v1.0/precipitation')
def prcp_analysis():
    #finding most recent date in measurement class:
    date_max = session.query(func.max(Measurement.date)).all()
    #converting date into datetime timedelta input format using split
    input_latest = date_max[0][0].split("-")
    input_latest = [int(x) for x in input_latest]
    #getting date one year back from most recent date in measurements
    one_year_back = dt.date(*input_latest) - dt.timedelta(days=365)
    one_year_str = one_year_back.strftime("%Y-%m-%d")
    # query from climate_starter ipynb for last 12 months of prcp
    year_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > one_year_str)\
    .order_by(Measurement.date.desc()).all()
    #convert tuples into a dict
    year_rain_list = dict(year_precip)
    #jsonify
    return jsonify(year_rain_list)

@app.route('/api/v1.0/stations')
def stations():
    #querying the stations
    stations_raw = session.query(Station.station).all()
    #getting into list format
    station_list = [station[0] for station in stations_raw]
    #jsonify
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    #getting most active station:
    active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    most_active = active_station[0]
    #now getting the year back from the most recent date in measurements
    #finding most recent date in measurement class:
    date_max = session.query(func.max(Measurement.date)).all()
    #converting date into datetime timedelta input format using split
    input_latest = date_max[0][0].split("-")
    input_latest = [int(x) for x in input_latest]
    #getting date one year back from most recent date in measurements
    one_year_back = dt.date(*input_latest) - dt.timedelta(days=365)
    one_year_str = one_year_back.strftime("%Y-%m-%d")
    # now can query for the most recent year of data at the most active station
    year_temp_most_active = session.query(Measurement.tobs)\
        .filter(Measurement.station == most_active).filter(Measurement.date > one_year_str).all()
    tobs_data = year_temp_most_active
    # flattening tuples into list and jsonifying
    return jsonify(list(np.ravel(tobs_data))) 

@app.route('/api/v1.0/<start>')
def start(start):
    #query based on start, returning min, avg, and max in json list
    query_post_start = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date > str(start)).all()
    return jsonify(list(np.ravel(query_post_start)))

@app.route('/api/v1.0/<start>/<end>')
def start_end(start,end):
    #query based on start, returning min, avg, and max in json list
    query_start_end = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date > str(start))\
        .filter(Measurement.date < str(end)).all()
    return jsonify(list(np.ravel(query_start_end)))

session.close()

if __name__ == '__main__':
    app.run(debug=True)