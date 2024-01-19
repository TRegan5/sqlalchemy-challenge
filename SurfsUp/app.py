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
    return "Welcome to my 'Precipitation' page!"

# Climate App Design 3
@app.route("/api/v1.0/stations")
def home():
    # Query list of stations
    query = session.query(stations.station).all()
    station_list = list(np.ravel(query))
    print("Server received request for 'Stations' page...")
    return (
        f"Welcome to my 'Stations' page!<br/>"
        jsonify(station_list))

# Climate App Design 4
@app.route("/api/v1.0/tobs")
def home():
    print("Server received request for 'Temperature Observations' page...")
    return "Welcome to my 'Temperature Observations' page!"

# Climate App Design 5 and 6
@app.route("/api/v1.0/<start>")
def home():
    print("Server received request for 'Summary Statistics' page...")
    return "Welcome to my 'Summary Statistics' page!"

@app.route("/api/v1.0/<start>/<end>")
def home():
    print("Server received request for 'Summary Statistics' page...")
    return "Welcome to my 'Summary Statistics' page!"