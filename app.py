# FLASK
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
#################################################
# check names!!!
################################################
Measurement = Base.classes.measurement
Stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#find date range to query
last = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
last_date, = last
year,month,day = last_date.split('-')
query_date = dt.date(int(year),int(month),int(day)) - dt.timedelta(days=365)
print("Last Date Measured: ",last_date)
print("Query Date: ",query_date)

@app.route("/")
def welcome():
    # List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # get a list of precipitation values for the past year
    results_precipitation = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>query_date).all()

    all_precipitation = []
    for measurement in results_precipitation:
        precipitation_dict = {}
        precipitation_dict["date"] = measurement.date
        precipitation_dict["precipitation"] = measurement.prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # query to find the weather stations
    #################################################
    # check names!!!
    ################################################
    results_stations = session.query(Stations.station).all()
    # Convert list of tuples into normal list
    station_list = list(np.ravel(results_stations))
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def temperature():
    # get a list of temperature values for the past year
    results_temperature = session.query(Measurement.date,Measurement.station,Measurement.tobs)\
                              .filter(Measurement.date>query_date).all()

    all_temperatures = []
    for measurement in results_temperature:
        temperature_dict = {}
        temperature_dict["date"] = measurement.date
        temperature_dict["temperature"] = measurement.tobs
        all_temperatures.append(temperature_dict)

    return jsonify(all_temperatures)


if __name__ == '__main__':
    app.run(debug=False)
