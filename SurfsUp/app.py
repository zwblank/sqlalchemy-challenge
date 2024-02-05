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


# reflect an existing database into a new model
engine = create_engine("sqlite:///SurfsUp\Resources\hawaii.sqlite")

# reflect the tables
Base = automap_base()
Base.prepare(engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# Homepage
@app.route("/")
def welcome():
	return(
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end<br/>"
	)

# Precipitation Analysis Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        precipitation = session.query(measurement.date, measurement.prcp).\
		filter(measurement.date >= prev_year).all()
        precip = {date: prcp for date, prcp in precipitation}
        return jsonify(precip)

# Temperature Observations Route
@app.route("/api/v1.0/tobs")
def temp_monthly():
        prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

        results = session.query(measurement.tobs).\
                filter(measurement.station == 'USC00519281').\
                filter(measurement.date >= prev_year).all()

        temps = list(np.ravel(results))
        return jsonify(temps)  

# Min, Max, Avg Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start, end):

        sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

        if not end:
                results = session.query(*sel).\
                        filter(measurement.date >= start).\
                        filter(measurement.date <= end).all()
                temps = list(np.ravel(results))
                return jsonify(temps)
        results = session.query(*sel).\
                        filter(measurement.date >= start).\
                        filter(measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

# Stations Route
@app.route("/api/v1.0/stations")
def stations():
        results = session.query(station).all()
        stations = list(np.ravel(results))
        return jsonify(stations)

if __name__=="__main__":
        app.run(debug=True)