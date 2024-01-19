# Import the dependencies.
import numpy as np
import pandas as pd
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
stations = Base.classes.station
measurements = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Find the most recent date in the data set.
last_date = session.query(measurements.date).order_by(measurements.date.desc()).first()#[0]
print(last_date)

# Calculate the date one year from the last date in data set.
last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
print(last_year)

# Design a query to find the most active stations (i.e. which stations have the most rows?)
# List the stations and their counts in descending order.
station_activity = session.query(measurements.station, func.count(measurements.station)).\
    group_by(measurements.station).\
    order_by(func.count(measurements.date).desc()).all()
most_active = station_activity[0][0] # get id of most active station

# calculate the lowest, highest, and average temperature
most_active_stats = session.query(func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).\
    filter(measurements.station == most_active).all()

# Climate App Design 1
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to my Climate App 'Home' page!<br/>"
        f"Here, you may follow links to precipitation information, station information, or various forms of observed temperatures.<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        )

# Climate App Design 2
@app.route("/api/v1.0/precipitation")
def home():
    print("Server received request for 'Precipitation' page...")
    last_yr_prcp = session.query(measurements.date, measurements.prcp).\
        filter(measurements.date >= last_year).\
            filter(measurements.prcp != None).\
            order_by(measurements.date).all()
    return jsonify(last_yr_prcp)

# Climate App Design 3
@app.route("/api/v1.0/stations")
def home():
    print("Server received request for 'Stations' page...")
    # Query list of stations
    query = session.query(stations.station).all()
    station_list = list(np.ravel(query))
    return jsonify(station_list)

# Climate App Design 4
@app.route("/api/v1.0/tobs")
def home():
    print("Server received request for 'Temperature Observations' page...")
    last_yr_tobs = session.query(measurements.date, measurements.tobs).\
        filter(measurements.date >= last_year).\
        filter(measurements.tobs != None).\
        filter(measurements.station == most_active).\
        order_by(measurements.date).all()
    return jsonify(last_yr_tobs)

# Climate App Design 5 and 6
@app.route("/api/v1.0/<start>")
def home():
    print("Server received request for 'Summary Statistics' page...")
    return "Welcome to my 'Summary Statistics' page!"

@app.route("/api/v1.0/<start>/<end>")
def home():
    print("Server received request for 'Summary Statistics' page...")
    return "Welcome to my 'Summary Statistics' page!"